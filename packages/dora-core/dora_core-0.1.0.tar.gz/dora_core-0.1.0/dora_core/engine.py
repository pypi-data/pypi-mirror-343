"""Dora engine SQL module.

This module provides functionality to handle SQL operations for the Dora engine.
"""

# pylint: disable=no-member
# pylint: disable=line-too-long
from typing import Iterator, Callable, List, Tuple, Optional, Any
from enum import Enum
from hashlib import md5
from os import path

from sqlglot import transpile, Expression, exp
from pydantic import BaseModel, Field, model_validator
from pydantic_core import PydanticCustomError
from pyiceberg.catalog import Catalog, NoSuchTableError, Table as IcebergTable
from pyiceberg.table.snapshots import Snapshot
from pyarrow import Table as ArrowTable
from numpy import full

from .utils import logger
from .parser import TableType, CheckType, constraint_type
from .asset import Job, Table, META_COLUMN_EXEC, META_COLUMN_DATE

META_COLUMN_UNMAPPED = "Unmapped"
INPUT_DATE_COLUMN = "__InputDate__"
INPUT_FILE_COLUMN = "__InputFile__"
# Max number of upserts using pyiceberg
MAXUPSERT = 30000

log = logger(__name__)

class EngineType(Enum):
    """Enumeration of supported SQL execution engines."""
    ATHENA = "athena"
    TRINO = "trino"
    DUCKDB = "duckdb"
    SPARK = "spark2"

class Engine(BaseModel):
    """Abstract base class for Dora query engines.

    This class defines the interface and common functionality for different types of SQL engines
    used in the Dora platform.

    Attributes:
        job (Job): Dora Job object.
        table (Table): Dora Table object.
        engine (EngineType): Execution SQL engine type.
        raw_columns (Optional[List[str]]): List of column names found in the original source.
        cast_columns (Optional[List[str]]): List of column names in the normalized table.
    """
    job: Job = Field(description="Dora Job object")
    table: Table = Field(description="Dora Table object")
    engine: EngineType = Field(description="Execution SQL engine", default=EngineType.DUCKDB)
    raw_columns: Optional[List[str]] = Field(
        description="List of column names in found in the original source", default=None, init=False)
    cast_columns: Optional[List[str]] = Field(
        description="List of column names in the normalized table", default=None, init=False)

    def model_post_init(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Post-initialization method to set default values for raw_columns and cast_columns."""
        self.raw_columns = list()
        self.cast_columns = list()

    @model_validator(mode='after')
    def validate_table_type(self):
        """Validate the table type to ensure compatibility with the engine.

        Raises:
            PydanticCustomError: If the table type is not compatible with the engine.
        """
        if not self.check_table_type():
            log.error("This table is not able to be used in this engine: %s", self.table.table_type.value)
            raise PydanticCustomError("table", f"Table type error:{self.table.table_type}")
        return self

    def check_table_type(self) -> bool:
        """Check if the table type is correct for the engine.

        Returns:
            bool: True if the table type is correct, False otherwise.
        """
        return True

    @property
    def raw_view(self) -> exp.Identifier:
        """Get the temporary raw view name.

        Returns:
            exp.Identifier: The raw view identifier.
        """
        raise NotImplementedError("raw_view property must be implemented")

    @property
    def raw_table(self) -> exp.Identifier:
        """Get the temporary raw table name.

        Returns:
            exp.Identifier: The raw table identifier.
        """
        return exp.Identifier(this="__raw_data__", quote=False)

    @property
    def cast_table(self) -> exp.Identifier:
        """Get the cast table name.

        Returns:
            exp.Identifier: The cast table identifier.
        """
        return exp.Identifier(this=f"{self.table.name}_tmp", quote=False)

    @property
    def test_table(self) -> exp.Identifier:
        """Get the test table name.

        Returns:
            exp.Identifier: The test table identifier.
        """
        return exp.Identifier(this=f"{self.table.name}_test", quote=False)

    def set_raw_columns(self, raw_columns: List[str]) -> None:
        """Set the raw columns.

        Args:
            raw_columns (List[str]): List of raw column names.
        """
        self.raw_columns = list()
        for _col in raw_columns:
            self.raw_columns.append(exp.Identifier(this=_col))

    def set_cast_columns(self, cast_columns: List[str]) -> None:
        """Set the cast columns.

        Args:
            cast_columns (List[str]): List of cast column names.
        """
        self.cast_columns = list()
        for _col in cast_columns:
            self.cast_columns.append(exp.Identifier(this=_col))

    def _query_with_placeholders(self) -> Expression:
        """Add placeholders to the table query.

        Returns:
            Expression: The query with placeholders.
        """
        _query = self.table.ast.ddl.expression
        for _source in self.table.ast.get_source():
            for tbl in _query.find_all(exp.Table):
                for __f in tbl.find_all(exp.Literal):
                    if __f.this == _source.this:
                        tbl.replace(exp.Placeholder())
        return _query

    def _cast_columns(self) -> Iterator[Expression]:
        """Cast columns to the correct data type.

        Yields:
            Iterator[Expression]: An iterator of cast expressions.
        """
        if exp.Identifier(this=META_COLUMN_EXEC) not in self.raw_columns:
            yield exp.Alias(
                this=exp.Placeholder(this="dag"),
                alias=exp.Identifier(this=META_COLUMN_EXEC),
            )
        if exp.Identifier(this=INPUT_FILE_COLUMN) not in self.raw_columns:
            yield exp.Alias(
                this=exp.Placeholder(this="input_file"),
                alias=exp.Identifier(this=INPUT_FILE_COLUMN),
            )
        if exp.Identifier(this=META_COLUMN_DATE) not in self.raw_columns:
            yield exp.Alias(
                this=exp.Cast(
                    this=exp.Placeholder(this="input_date"),
                    to=exp.DataType(this=exp.DataType.Type.TIMESTAMP),
                ),
                alias=exp.Identifier(this=META_COLUMN_DATE),
            )
        col_identifiers = list()
        for _col in self.table.ast.get_columns():
            _col_identifier = _col.find(exp.Identifier)
            col_identifiers.append(_col_identifier)
            yield exp.Alias(
                alias=_col_identifier,
                this=exp.Cast(this=_col_identifier, to=_col.find(exp.DataType)))
        if len(col_identifiers) > 0:
            for raw_column in self.raw_columns:
                if raw_column not in col_identifiers:
                    yield exp.Identifier(this=raw_column)
        else:
            yield exp.Star()

    def _foreign_keys(self, source_name: str, target_name: str):
        """Generate foreign key expressions.

        Args:
            source_name (str): The source table name.
            target_name (str): The target table name.

        Yields:
            exp.EQ: The foreign key expression.
        """
        for _pk in self.table.primary_keys:
            yield exp.EQ(
                this=exp.Column(this=_pk,
                                table=exp.Identifier(this=target_name)),
                expression=exp.Column(
                    this=_pk,
                    table=exp.Identifier(this=source_name)),
            )

    def _merge_on(self, source_name: str, target_name: str):
        """Generate the merge ON clause.

        Args:
            source_name (str): The source table name.
            target_name (str): The target table name.

        Returns:
            exp.Paren: The merge ON clause.
        """
        _fks = list(self._foreign_keys(source_name, target_name))
        if len(_fks) > 1:
            return exp.Paren(
                this=exp.And(this=exp.EQ(
                    this=exp.Literal(this="1", is_string=False),
                    expression=exp.Literal(this="1", is_string=False),
                ),
                expressions=_fks))
        elif len(_fks) == 1:
            return exp.Paren(this=_fks[0])
        else:
            raise ValueError("No foreign keys found")

    def _merge_insert(self, columns: list, source_name: str):
        """Generate the merge INSERT clause.

        Args:
            columns (list): List of column names.
            source_name (str): The source table name.

        Returns:
            exp.Insert: The merge INSERT clause.
        """
        return exp.Insert(
            this=exp.Tuple(
                expressions=[exp.Column(this=exp.Identifier(this=col)) for col in columns]
            ),
            expression=exp.Tuple(
                expressions=[
                    exp.Column(
                        this=exp.Identifier(this=col, quoted=True),
                        table=exp.Identifier(this=source_name),
                    )
                    for col in columns
                ]
            ),
        )


    def _merge_update(self, columns: list, source_name: str, target_name: str):
        """Generate the merge UPDATE clause.

        Args:
            columns (list): List of column names.
            source_name (str): The source table name.
            target_name (str): The target table name.

        Returns:
            exp.Update: The merge UPDATE clause.
        """
        return exp.Update(
            expressions=[
                exp.EQ(
                    this=exp.Column(
                        this=exp.Identifier(this=col, quoted=True),
                        table=exp.Identifier(this=target_name),
                    ),
                    expression=exp.Column(
                        this=exp.Identifier(this=col, quoted=True),
                        table=exp.Identifier(this=source_name),
                    ),
                )
            for col in columns],
        )

    def merge(self, columns_names: list, target_engine: EngineType, pretty: bool = False):
        """Generate the merge query.

        Args:
            columns_names (list): List of column names.
            target_engine (EngineType): The target execution engine type.
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _source_alias = "source"
        _target_alias = "target"
        _sql = exp.Merge(
            this=exp.Alias(
                alias=exp.Identifier(this=_target_alias),
                this=exp.Table(this=self.table.table, db=self.table.database)
                ),
            using=exp.Alias(
                alias=exp.Identifier(this=_source_alias),
                this=self.stage_table
            ),
            on=self._merge_on(_source_alias, _target_alias),
            whens=exp.Whens(
                expressions=[
                    exp.When(
                        matched=False,
                        then=self._merge_insert(
                            columns=columns_names,
                            source_name=_source_alias)
                    ),
                    exp.When(
                        matched=True,
                        then=self._merge_update(
                            columns=columns_names,
                            source_name=_source_alias,
                            target_name=_target_alias),
                        condition=exp.GT(
                            this=exp.Column(
                                this=exp.Identifier(this=META_COLUMN_DATE),
                                table=exp.Identifier(this=_source_alias)
                            ),
                            expression=exp.Column(
                                this=exp.Identifier(this=META_COLUMN_DATE),
                                table=exp.Identifier(this=_target_alias)
                            )
                        ),
                    )
                ]
            )
        )
        # Transpile the query to the engine dialect
        for _query in transpile(sql=_sql.sql(), write=target_engine.value, pretty=pretty):
            return _query

    def read_desc(self, pretty: bool = False) -> str:
        """Describe the raw table.

        Args:
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _sql = exp.Describe(
            this=self.raw_table
        )
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def cast_desc(self, pretty: bool = False) -> str:
        """Describe the cast table.

        Args:
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _sql = exp.Describe(
            this=self.cast_table
        )
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def cast(self, dag: str, input_file: str = None, input_date: str = None, pretty: bool = False) -> str:
        """Generate the cast query.

        Args:
            dag (str): The execution unique identifier.
            input_file (str, optional): The input file path. Defaults to None.
            input_date (str, optional): The input date. Defaults to None.
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _sql = exp.Create(
            this=self.cast_table,
            kind="TABLE",
            exists=True,
            expression=exp.Subquery(
                this=exp.Select(
                    expressions=list(self._cast_columns()),
                ).from_(self.raw_table)
            ),
            properties=exp.Properties(expressions=[exp.TemporaryProperty()]),
        )
        _sql = exp.replace_placeholders(_sql,
               dag=dag if dag is not None else exp.Null(),
               input_file=input_file if input_file is not None else exp.Null(),
               input_date=input_date if input_date is not None else exp.Null())

        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def unmapped(self, pretty: bool = False) -> str:
        """Generate the unmapped query.

        Args:
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _meta_columns = [META_COLUMN_EXEC, META_COLUMN_DATE]
        _unmapped = [col for col in self.raw_columns if col not in self._column_identifiers()]
        if len(_unmapped)>0:
            _sql = exp.Describe(
                this=exp.Subquery(
                    this=exp.Select(
                    expressions=[col for col in _unmapped if col not in _meta_columns],
                    sample=exp.TableSample(
                        size=exp.Literal(this=100, is_string=False)
                    )).from_(self.raw_table)))
            for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
                return _query

    def _column_identifiers(self) -> Iterator[exp.Identifier]:
        """Get column identifiers.

        Yields:
            Iterator[exp.Identifier]: An iterator of column identifiers.
        """
        for _col in self.table.ast.get_columns():
            yield _col.find(exp.Identifier)

    def test_column_names(self) -> Iterator[str]:
        """Get the test column names.

        Yields:
            Iterator[str]: An iterator of test column names.
        """
        for _ , _test in self._test_checks():
            yield _test.find(exp.Identifier).name
        for _ , _test in self._test_uniques():
            yield _test.find(exp.Identifier).name
        for _ , _test in self._test_nulls():
            yield _test.find(exp.Identifier).name

    @staticmethod
    def _test_results_column_prop(col: exp.ColumnDef, check_type: CheckType) -> str:
        """Get the test name and type from a column.

        Args:
            col (exp.ColumnDef): The column definition.
            check_type (CheckType): The check type.

        Returns:
            str: The test name and type.
        """
        return col.name.removeprefix(check_type.name+'_')

    def _test_results(self, test_generator: Callable, input_file: str = None) -> Iterator[Tuple[CheckType, str, Expression]]:
        """Generate test results.

        Args:
            test_generator (Callable): The test generator function.
            input_file (str, optional): The input file path. Defaults to None.

        Yields:
            Iterator[Tuple[CheckType, str, Expression]]: An iterator of test result expressions.
        """
        lit0 = exp.Literal(this='0', is_string=False)
        lit1 = exp.Literal(this='1', is_string=False)
        for _type, _test in test_generator():
            _col = _test.find(exp.Identifier)
            _col_name = self._test_results_column_prop(_col, _type)
            # Check if the column is a file column
            if input_file:
                _fil = exp.Literal(this=input_file, is_string=True)
            else:
                _fil = exp.Literal(this='', is_string=True)
            # Check the violation type
            if _type == CheckType.DROP:
                _should_warn = exp.GT(this=exp.Count(this=lit1),expression=lit0)
                _should_fail = exp.false()
            if _type == CheckType.FAIL:
                _should_warn = exp.false()
                _should_fail = exp.GT(this=exp.Count(this=lit1),expression=lit0)
            else: # dafult is warning
                _should_warn = exp.GT(this=exp.Count(this=lit1),expression=lit0)
                _should_fail = exp.false()

            yield (_type,
                   _col_name,
                   exp.Select(
                expressions=[
                    exp.Alias(
                        alias=exp.Identifier(this="name"),
                        this=exp.Literal(this=_col_name, is_string=True)
                    ),
                    exp.Alias(
                        alias=exp.Identifier(this="failures"),
                        this=exp.Count(this=lit1)
                    ),
                    exp.Alias(
                        this=_should_warn,
                        alias=exp.Identifier(this="warn"),
                    ),
                    exp.Alias(
                        this=_should_fail,
                        alias=exp.Identifier(this="fail"),
                    ),
                    exp.Alias(
                        alias=exp.Identifier(this=INPUT_FILE_COLUMN),
                        this=_fil,
                    ),
                ],
                where=exp.Where(
                    this=exp.Not(this=_col)
                ),
            ).from_(self.test_table))

    def test_results(self, input_file: str = None, pretty: bool = False) -> Iterator[Tuple[CheckType, str, str]]:
        """Generate test query results.

        Args:
            input_file (str, optional): The input file path. Defaults to None.
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Yields:
            Iterator[Tuple[CheckType, str, str]]: An iterator of transpiled SQL queries.
        """
        for check in [self._test_checks, self._test_nulls, self._test_uniques]:
            for _type, _name, _test in self._test_results(check, input_file):
                for _query in transpile(sql=_test.sql(), write=self.engine.value, pretty=pretty):
                    yield (_type, _name, _query)

    def test(self, pretty: bool = False) -> str:
        """Generate the test query.

        Args:
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        _tests = [exp.Star()]
        for _ , _test in self._test_checks():
            _tests.append(_test)
        for _ , _test in self._test_nulls():
            _tests.append(_test)
        for _ , _test in self._test_uniques():
            _tests.append(_test)
        _sql = exp.Create(
            this=self.test_table,
            kind="TABLE",
            exists=True,
            expression=exp.Subquery(
                this=exp.Select(expressions=_tests
                ).from_(
                    exp.Alias(
                    alias=exp.Identifier(this="t0"),
                    this=self.cast_table)
                )
            ),
            properties=exp.Properties(expressions=[exp.TemporaryProperty()]))
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def _test_checks(self) -> Iterator[Tuple[CheckType, Expression]]:
        """Generate test checks.

        Yields:
            Iterator[Tuple[CheckType, Expression]]: An iterator of check expressions.
        """
        for _check in self.table.ast.get_checks():
            _check_name = _check.find(exp.Identifier).this
            _check_type = constraint_type(_check)
            yield (_check_type, exp.Alias(
                alias=exp.Identifier(this=f"{_check_type.name}_{_check_name}"),
                this=exp.Coalesce(
                    this=exp.Paren(this=_check.find(exp.CheckColumnConstraint).this),
                    expressions=[exp.Boolean(this=True)],
                ),
            ))

    def _test_nulls(self) -> Iterator[Tuple[CheckType, Expression]]:
        """Generate null tests.

        Yields:
            Iterator[Tuple[CheckType, Expression]]: An iterator of null test expressions.
        """
        for _check in self.table.ast.get_required():
            _col = _check.find(exp.Identifier)
            _type = constraint_type(_check)
            yield (_type, exp.Alias(
                alias=exp.Identifier(this=f"{_type.name}_{_col.this}_not_null", quote=True),
                this=exp.Paren(
                    this=exp.Not(this=exp.Is(this=_col, expression=exp.Null()))
                ),
            ))

    def _test_uniques(self) -> Iterator[Tuple[CheckType, Expression]]:
        """Generate unique constraint tests.

        Yields:
            Iterator[Tuple[CheckType, Expression]]: An iterator of unique constraint test expressions.
        """
        for idx, _check in enumerate(self.table.ast.get_unique(), start=1):
            _col = _check.find(exp.Identifier)
            _type = constraint_type(_check)
            _tbl_id = exp.Identifier(this=f"t{idx}")
            yield (_type, exp.Alias(
                alias=exp.Identifier(this=f"{_type.name}_{_col.this}_unique", quote=True),
                this=exp.Paren(
                this=exp.Select(
                expressions=[
                    exp.Paren(this=exp.Not(
                        this=exp.GT(
                        this=exp.Count(this=exp.Star()),
                        expression=exp.Literal(this="1", is_string=False)
                        ))),
                ],
                where=exp.Where(
                this=exp.EQ(
                    this=exp.Column(this=_col, table=_tbl_id),
                    expression=exp.Column(
                        this=_col,
                        table=exp.Identifier(this="t0")),
                    )
            )
            ).from_(exp.Alias(
                alias=_tbl_id,
                this=self.cast_table)
            ))))

    def _resultset_ctes(self, test: Callable) -> Iterator[Tuple[str, exp.CTE]]:
        """Create CTEs to filter tests with fail conditions.

        Args:
            test (Callable): The test function.

        Yields:
            Iterator[Tuple[str, exp.CTE]]: An iterator of CTE expressions and their aliases.
        """
        for _type, _test in test():
            if _type == CheckType.FAIL:
                _alias = f"t_{md5(_test.find(exp.Identifier).this.encode()).hexdigest()}"
                yield (_alias, exp.CTE(
                    this=exp.Select(
                        expressions=[
                            exp.Alias(this=exp.Count(
                                this=exp.Literal(this="1", is_string=False)),
                            alias=exp.Identifier(this="failures"))
                            ])
                        .from_(self.test_table)
                        .where(exp.Not(this=_test.find(exp.Identifier))),
                    alias=exp.TableAlias(
                        this=exp.Identifier(this=_alias))
                ))

    def _resultset_lists(self, test: Callable) -> Tuple[List[Expression], List[Expression], List[Expression]]:
        """Create lists of CTEs, joins, and tests.

        Args:
            test (Callable): The test function.

        Returns:
            Tuple[List[Expression], List[Expression], List[Expression]]: Lists of CTEs, joins, and tests.
        """
        _cte_list = list()
        _join_list = list()
        _test_list = list()
        for _alias, _cte in self._resultset_ctes(test):
            _cte_list.append(_cte)
            _join_list.append(exp.Join(this=exp.Table(this=exp.Identifier(this=_alias))))
            _test_list.append(
                exp.EQ(
                    this=exp.Column(
                        this=exp.Identifier(this="failures"),
                        table=exp.Identifier(this=_alias)),
                    expression=exp.Literal(this="0", is_string=False)))
        return (_cte_list,_join_list,_test_list)

    def resultset(self, pretty: bool = False) -> str:
        """Generate the results query.

        Args:
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        # Default where clause
        # Return all lines if there are no data quality tests
        _where = exp.Where(
            this=exp.EQ(
                this=exp.Literal(this="1", is_string=False),
                expression=exp.Literal(this="1", is_string=False)))
        # Select all test columns
        _test_list = list(self._filter_cols(self._test_checks, True)) + \
                     list(self._filter_cols(self._test_uniques, True)) + \
                     list(self._filter_cols(self._test_nulls, True))
        # Create CTE for fail tests
        _ctes_c, _joins_c, _tests_c = self._resultset_lists(self._test_checks)
        _ctes_u, _joins_u, _tests_u = self._resultset_lists(self._test_uniques)
        _ctes_n, _joins_n, _tests_n = self._resultset_lists(self._test_nulls)
        # If there are test columns, modify the where clause
        if len(_test_list) > 0:
            _where = self._filter(tests=_test_list + _tests_c + _tests_u + _tests_n, check=True)
        # Create the select statement
        _selection = [col for col in self.cast_columns if col.find(exp.Identifier).this not in [INPUT_DATE_COLUMN, INPUT_FILE_COLUMN]]
        _sql = exp.Select(
            expressions=_selection,
            from_=self.cast_table,
            where=_where).from_(self.test_table)
        # Add all the ctes and joins then to the query
        if len(_ctes_c +_ctes_u +_ctes_n) > 0:
            _sql.args.update({'with':exp.With(expressions=_ctes_c + _ctes_u + _ctes_n)})
        if len(_joins_c +_joins_u +_joins_n) > 0:
            _sql.args.update({'joins':_joins_c +_joins_u +_joins_n})
        # Transpile the query to the engine dialect
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def droped(self, check_type: CheckType, check_name: str, pretty: bool = False) -> str:
        """Generate the dropped results query.

        Args:
            check_type (CheckType): The type of check.
            check_name (str): The check name.
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        # Default where clause
        # Do not return any lines if there are no data quality tests
        _where = exp.Where(
            this=exp.NEQ(
                this=exp.Identifier(this=f"{check_type.name}_{check_name}"),
                expression=exp.true()))
        # Select raw columns
        _raw_columns = list()
        for _col in self.raw_columns:
            _raw_columns.append(exp.Alias(
                alias=exp.Identifier(this=_col),
                this=exp.Cast(
                    this=_col,
                    to=exp.DataType(this=exp.DataType.Type.TEXT))))
        # If there are test columns, modify the where clause
        # Create the select statement
        _sql = exp.Select(
            expressions=_raw_columns,
            from_=self.cast_table,
            where=_where).from_(self.test_table)
        # Transpile the query to the engine dialect
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def _filter_cols(self, test_function: Callable, check: bool = True) -> Iterator[exp.Column]:
        """Select all test columns.

        Args:
            test_function (Callable): The test function.
            check (bool, optional): Whether to check the columns. Defaults to True.

        Yields:
            Iterator[exp.Column]: An iterator of test columns.
        """
        for _, _test in test_function():
            if check:
                yield exp.Column(this=_test.find(exp.Identifier))
            else:
                yield exp.Not(this=exp.Column(this=_test.find(exp.Identifier)))

    def _filter(self, tests: List[exp.Column], ast: Expression = None, check: bool = True) -> Expression:
        """Create filters for the where clause.

        Args:
            tests (List[exp.Column]): The list of test columns.
            ast (Expression, optional): The abstract syntax tree. Defaults to None.
            check (bool, optional): Whether to check the columns. Defaults to True.

        Returns:
            Expression: The where clause expression.
        """
        try:
            _test = tests.pop()
            if ast is None:
                return self._filter(tests, ast=_test, check=check)
            else:
                if check:
                    return self._filter(tests, ast=exp.And(this=_test, expression=ast), check=check)
                else:
                    return self._filter(tests, ast=exp.Or(this=_test, expression=ast), check=check)
        except IndexError:
            return exp.Where(this=ast)

    def _dag_filter(self, alias: list, value: str, ast: Expression = None) -> Expression:
        """Create filters for the DAG.

        Args:
            alias (list): List of aliases.
            value (str): The value to filter by.
            ast (Expression, optional): The abstract syntax tree. Defaults to None.

        Returns:
            Expression: The DAG filter expression.
        """
        try:
            _alias = alias.pop()
            _filter = exp.EQ(
                    this=exp.Column(
                        this=exp.Identifier(this=META_COLUMN_EXEC),
                        table=exp.Identifier(this=str(_alias))),
                    expression=exp.Literal(this=value, is_string=True))
            if ast is None:
                return self._dag_filter(alias, value, ast=_filter)
            else:
                return self._dag_filter(alias, value, ast=exp.And(this=_filter, expression=ast))
        except IndexError:
            return exp.Where(this=ast)

    @staticmethod
    def fill_columns(dataset: ArrowTable, table: IcebergTable) -> ArrowTable:
        """Fill unmapped columns in the table schema with None values.
        
        Args:
            dataset (ArrowTable): The dataset to be processed.
            table (IcebergTable): The Iceberg table schema.
        
        Returns:
            ArrowTable: The dataset with filled columns.
        """
        _series = dict()
        _schema = table.schema().as_arrow()
        for _column in _schema:
            if dataset.schema.field(_column.name):
                _series[_column.name] = dataset[_column.name]
            else:
                _series[_column.name] = full(shape=dataset.num_rows, fill_value=None)
        return ArrowTable.from_pydict(_series, schema=_schema)


    def save(self, catalog:Catalog, dataset:ArrowTable, **kwargs) -> Snapshot:
        """Save the table to the catalog."""
        raise NotImplementedError("save method must be implemented")

class Append(Engine):
    """Dora query engine class for appending tables.

    This class handles the logic for appending data to existing tables.
    """

    def check_table_type(self) -> bool:
        """Check if the table is an APPENDING table.

        Returns:
            bool: True if the table is an APPENDING table, False otherwise.
        """
        return self.table.table_type == TableType.APPENDING

    @property
    def raw_view(self) -> exp.Identifier:
        """Get the temporary raw view name.

        Returns:
            exp.Identifier: The raw view identifier.
        """
        return exp.Identifier(this="__storage__", quote=False)

    @property
    def stage_table(self) -> exp.Identifier:
        """Get the stage table name.

        Returns:
            exp.Identifier: The stage table identifier.
        """
        return exp.Table(this=f"temp_{self.table.table}_stg_", db=self.table.database)

    def read(self, input_file: str = None, event_dag: str = None, alias: list = None, pretty: bool = False) -> str:
        """Generate the read query.

        Args:
            input_file (str, optional): The input file path. Defaults to None.
            event_dag (str, optional): The event DAG identifier. Defaults to None.
            alias (list, optional): List of aliases. Defaults to None.
            pretty (bool, optional): Whether to format the query prettily. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        if len(alias) > 0:
            _query = self._query_with_placeholders()
            _query.this.args['where'] = self._dag_filter(alias, event_dag)
        else:
            _query = self._query_with_placeholders()
        _sql = exp.Create(
            this=self.raw_table,
            kind="TABLE",
            exists=True,
            expression=_query,
            properties=exp.Properties(expressions=[exp.TemporaryProperty()]),
        )
        if input_file:
            _sql = exp.replace_placeholders(_sql, input_file)
        for _query in transpile(sql=_sql.sql(), write=self.engine.value, pretty=pretty):
            return _query

    def save(self, catalog:Catalog, dataset:ArrowTable, **kwargs) -> Snapshot:
        """Save the table to the catalog."""
        _n_rows, _ = dataset.shape
        if _n_rows == 0:
            return None
        _table = self.table.update(catalog=catalog, schema=dataset.schema)
        _table.append(df=self.fill_columns(dataset, _table).cast(_table.schema().as_arrow()))
        return _table.current_snapshot()

class Upsert(Append):
    """Dora query engine class for UPSERTING tables.

    This class handles the logic for upserting data into existing tables.
    """

    def check_table_type(self) -> bool:
        """Check if the table is an UPSERTING table.

        Returns:
            bool: True if the table is an UPSERTING table, False otherwise.
        """
        return self.table.table_type == TableType.UPSERTING

    @property
    def stage_location(self) -> str:
        """Get the stage location."""
        return path.join(self.table.location, '.stage')

    @staticmethod
    def predicate(dataset: ArrowTable, keys:list):
        """Create the predicate for the dataset overwrite.
        
        Args:
            dataset (ArrowTable): The dataset to be processed.
            keys (list): The list of primary keys.
        
        Yields:
            str: The predicate for the dataset overwrite.
        """
        if len(keys) != 1:
            raise ValueError("Only one primary key is supported on the overwrite tables")
        for col in dataset[keys[0]]:
            _val = col.as_py()
            if isinstance(_val, str):
                yield f"'{_val}'"
            else:
                yield str(_val)

    def save(self, catalog:Catalog, dataset:ArrowTable, **kwargs) -> Any:
        """Save the table to the catalog."""
        _n_rows, _ = dataset.shape
        if _n_rows == 0:
            return None
        _pks = [str(pk) for pk in self.table.primary_keys]
        if len(_pks)==0:
            log.error("Upsert tables must have at least one primary key")
            raise ValueError("No primary key defined for the table")
        _table = self.table.update(catalog=catalog, schema=dataset.schema)
        # For performance issues, we use external engine for large datasets
        if _n_rows <= MAXUPSERT and len(_pks) == 1:
            # Create filter predicates. The reason for using only one primary key is to avoid issues
            # with more than 300 and clausules in the predicate (max recurrency in PyIceberg)
            _filter = f"{_pks[0]} in ({','.join(list(self.predicate(dataset=dataset,keys=_pks)))})"
            with _table.transaction() as trx:
                trx.overwrite(overwrite_filter=_filter,
                              df=self.fill_columns(dataset, _table).cast(_table.schema().as_arrow()))
            return _table.current_snapshot()
        # Use external engine for large datasets
        stage_identifier = self.stage_table.sql()
        try:
            catalog.purge_table(stage_identifier)
            log.debug("Table '%s' purged", stage_identifier)
        except NoSuchTableError:
            log.debug("Table '%s' not found", stage_identifier)
        # Create the stage table
        log.debug("Creating stage '%s'", stage_identifier)
        stage_table = catalog.create_table(
            identifier=stage_identifier,
            schema=dataset.schema,
            location=self.stage_location)
        stage_table.append(df=dataset)
        return self.merge(
            columns_names=dataset.column_names,
            target_engine=kwargs['engine'])

class Overwrite(Append):
    """Dora query engine class for OVERWRITING tables.

    This class handles the logic for overwriting data in existing tables.
    """

    def check_table_type(self) -> bool:
        """Check if the table is an OVERWRITING table.

        Returns:
            bool: True if the table is an OVERWRITING table, False otherwise.
        """
        return self.table.table_type == TableType.OVERWRITING

    def save(self, catalog:Catalog, dataset:ArrowTable, **kwargs) -> Snapshot:
        """Save the table to the catalog."""
        _n_rows, _ = dataset.shape
        if _n_rows == 0:
            return None
        _table = self.table.update(catalog=catalog, schema=dataset.schema)
        with _table.transaction() as trx:
            trx.delete(delete_filter=f"{META_COLUMN_EXEC} == '{kwargs['dag']}'")
            trx.append(df=self.fill_columns(dataset, _table).cast(_table.schema().as_arrow()))
        return _table.current_snapshot()
