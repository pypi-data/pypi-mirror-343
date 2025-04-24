"""Dora Parser module.

This module provides functionality to parse and analyze SQL statements.
"""

# pylint: disable=no-member
from typing import Iterator, List
from enum import Enum
from os import environ

from pydantic import BaseModel, Field, ConfigDict
from sqlglot.dialects.duckdb import DuckDB
from sqlglot import (
    Expression,
    parse,
    expressions,
    transpile)
from pyiceberg.types import (
    PrimitiveType,
    BooleanType,
    IntegerType,
    LongType,
    StringType,
    FloatType,
    TimeType,
    TimestampType,
    TimestamptzType,
    UUIDType,
    DoubleType,
    DateType,
    DecimalType)
from pyiceberg.transforms import (
    Transform,
    YearTransform,
    MonthTransform,
    DayTransform,
    HourTransform,
    BucketTransform,
    TruncateTransform,
    IdentityTransform)

from .utils import logger

log = logger(__name__)

DEFAULT_CONSTRAINT_VIOLATION = environ.get("DEFAULT_CONSTRAINT_VIOLATION","DROP")

class CheckType(Enum):
    """Enumeration for check constraint types."""
    FAIL = "FAIL"
    DROP = "DROP"

class TableType(Enum):
    """Enumeration for table types."""
    APPENDING = "APPENDING"
    MERGING = "MERGING"
    OVERWRITING = "OVERWRITING"
    STREAMING = "STREAMING"
    UPSERTING = "UPSERTING"

class AppendingTableProperty(expressions.Property):
    """Represents an appending table property in SQL."""
    arg_types = {}

class MergingTableProperty(expressions.Property):
    """Represents a merging table property in SQL."""
    arg_types = {}

class OverwritingTableProperty(expressions.Property):
    """Represents a overwriting table property in SQL."""
    arg_types = {}

class StreamingTableProperty(expressions.Property):
    """Represents a streaming table property in SQL."""
    arg_types = {}

class UpsertingTableProperty(expressions.Property):
    """Represents an upserting table property in SQL."""	
    arg_types = {}

class DoraDialect(DuckDB):
    """Custom SQL dialect for Dora."""

    class Generator(DuckDB.Generator):
        """SQL generator for the Dora dialect."""
        TRANSFORMS = {
            **DuckDB.Generator.TRANSFORMS,
            AppendingTableProperty: lambda *_: "APPENDING",
            MergingTableProperty: lambda *_: "MERGING",
            OverwritingTableProperty: lambda *_: "OVERWRITING",
            StreamingTableProperty: lambda *_: "STREAMING",
            UpsertingTableProperty: lambda *_: "UPSERTING",
        }

    class Parser(DuckDB.Parser):
        """SQL parser for the Dora dialect."""
        PROPERTY_PARSERS = {
            **DuckDB.Parser.PROPERTY_PARSERS,
             "APPENDING": lambda self: self.expression(AppendingTableProperty),
             "MERGING": lambda self: self.expression(MergingTableProperty),
             "OVERWRITING": lambda self: self.expression(OverwritingTableProperty),
             "STREAMING": lambda self: self.expression(StreamingTableProperty),
             "UPSERTING": lambda self: self.expression(UpsertingTableProperty),
        }
        CONSTRAINT_PARSERS = {
            **DuckDB.Parser.CONSTRAINT_PARSERS,
            "FAIL": lambda self: self.expression(
                expressions.OnProperty,
                this=expressions.Identifier(this="FAIL")),
            "DROP": lambda self: self.expression(
                expressions.OnProperty,
                this=expressions.Identifier(this="DROP")),
        }

def constraint_type(constraint:Expression) -> CheckType:
    """Extracts the constraint type from a constraint expression.

    Args:
        constraint (Expression): The constraint expression.

    Returns:
        CheckType: The constraint type.
    """
    for _type in constraint.find_all(expressions.OnProperty):
        if _type.this.this == CheckType.FAIL.value:
            return CheckType.FAIL
        if _type.this.this == CheckType.DROP.value:
            return CheckType.DROP

class SQLParser(BaseModel):
    """SQL Parser class for parsing and analyzing SQL statements.

    Attributes:
        ddl (Expression): The Data Definition Language (DDL) expression.
        dcl (List[Expression]): The Data Control Language (DCL) expressions.
    """
    ddl: Expression = Field(description="DDL expression", exclude=True)
    dcl: List[Expression] = Field(description="DCL expression", default=None, exclude=True)

    model_config = ConfigDict(arbitrary_types_allowed=True)

    def _validate(self):
        """Validates the SQL statement to ensure it is a valid CREATE TABLE statement.

        Raises:
            ValueError: If the SQL statement is not a valid CREATE TABLE statement.
        """
        if self.ddl.find(expressions.Create) is None:
            raise ValueError(f"Not a CREATE TABLE statement: {self.ddl.sql()}")
        if self.ddl.find(expressions.Table) is None:
            raise ValueError(f"Not a CREATE TABLE statement: {self.ddl.sql()}")
        if self.ddl.find(expressions.Subquery | expressions.Query).find(expressions.Select) is None:
            raise ValueError(f"Cant find a SELECT statement in: {self.ddl.sql()}")

    def get_foreign_key(self) -> Iterator[expressions.Table]:
        """Extracts foreign key expressions from the SQL statement.

        Yields:
            Iterator[expressions.Table]: An iterator of foreign key expressions.
        """
        for _fk in self.ddl.find_all(expressions.ForeignKey):
            yield _fk.find(expressions.Table)

    def get_query(self, dialect: str, pretty:bool=False) -> str:
        """Transpiles the SQL statement to the specified dialect.

        Args:
            dialect (str): The target SQL dialect.
            pretty (bool, optional): Whether to format the SQL query for readability. Defaults to False.

        Returns:
            str: The transpiled SQL query.
        """
        return transpile(
            sql=self.ddl.expression.sql(),
            read=DoraDialect,
            write=dialect,
            pretty=pretty)

    def get_table_type(self) -> TableType:
        """Determines the table type from the SQL statement.

        Returns:
            TableType: The type of the table.
        """
        if self.ddl.find(AppendingTableProperty):
            return TableType.APPENDING
        if self.ddl.find(OverwritingTableProperty):
            return TableType.OVERWRITING
        if self.ddl.find(UpsertingTableProperty):
            return TableType.UPSERTING
        if self.ddl.find(MergingTableProperty):
            return TableType.MERGING
        if self.ddl.find(StreamingTableProperty):
            return TableType.STREAMING
        return None

    def get_columns(self) -> Iterator[expressions.ColumnDef]:
        """Extracts column definitions from the SQL statement.

        Yields:
            Iterator[expressions.ColumnDef]: An iterator of column definitions.
        """
        _schema_expression = self.ddl.find(expressions.Schema)
        if _schema_expression is not None:
            for _schema in _schema_expression:
                if isinstance(_schema, expressions.ColumnDef):
                    yield _schema

    def get_partitions(self) -> Iterator[expressions.Anonymous]:
        """Extracts partition definitions from the SQL statement.

        Yields:
            Iterator[expressions.Anonymous]: An iterator of partition definitions.
        """
        _properties = self.ddl.find(expressions.Properties)
        for _partitions in _properties.expressions:
            if isinstance(_partitions, expressions.PartitionedByProperty):
                for __partition in _partitions.this.expressions:
                    yield __partition

    def get_location(self) -> Iterator[expressions.LocationProperty]:
        """Extracts the location property from the SQL statement.

        Yields:
            Iterator[expressions.LocationProperty]: An iterator of location properties.
        """
        _properties = self.ddl.find(expressions.Properties)
        _location = _properties.find(expressions.LocationProperty)
        if isinstance(_location, expressions.LocationProperty):
            yield _location.find(expressions.Literal)

    def get_table(self) -> str:
        """Extracts the table name from the SQL statement.

        Returns:
            str: The table name.
        """
        return self.ddl.find(expressions.Table)

    def get_properties(self) -> Iterator[expressions.Property]:
        """Extracts properties from the SQL statement.

        Yields:
            Iterator[expressions.Property]: An iterator of properties.
        """
        _properties = self.ddl.find(expressions.Properties)
        for _property in _properties.find_all(expressions.Property):
            if _property.__class__ == expressions.Property:
                yield _property

    def get_description(self) -> Iterator[expressions.SchemaCommentProperty]:
        """Extracts the description property from the SQL statement.

        Yields:
            Iterator[expressions.SchemaCommentProperty]: An iterator of schema comment properties.
        """
        _properties = self.ddl.find(expressions.Properties)
        _comment = _properties.find(expressions.SchemaCommentProperty)
        if isinstance(_comment, expressions.SchemaCommentProperty):
            yield _comment.find(expressions.Literal)

    def get_upstream(self) -> Iterator[expressions.Table]:
        """Extracts upstream tables from the SQL statement.

        Yields:
            Iterator[expressions.Table]: An iterator of upstream tables.
        """
        for ref in self.ddl.expression.find_all(expressions.Table):
            if ref.db != str() and ref.name != str():
                yield ref

    def get_constraints(self) -> Iterator[expressions.Constraint]:
        """Extracts constraint expressions from the SQL statement.

        Yields:
            Iterator[expressions.Constraint]: An iterator of constraints.
        """
        for unique in self.get_unique():
            yield unique
        for required in self.get_required():
            yield required
        for check in self.get_checks():
            yield check

    def get_unique(self) -> Iterator[expressions.UniqueColumnConstraint]:
        """Extracts unique constraints from the SQL statement.

        Yields:
            Iterator[expressions.UniqueColumnConstraint]: An iterator of unique constraints.
        """
        for _column in self.ddl.find_all(expressions.ColumnDef):
            if _column.find(expressions.UniqueColumnConstraint):
                _column.constraints.extend(self._add_default_contraint_properties(_column))
                yield _column

    def get_required(self) -> Iterator[expressions.NotNullColumnConstraint]:
        """Extracts nullable constraints from the SQL statement.

        Yields:
            Iterator[expressions.NotNullColumnConstraint]: An iterator of unique constraints.
        """
        for _column in self.ddl.find_all(expressions.ColumnDef):
            if _column.find(expressions.NotNullColumnConstraint):
                _column.constraints.extend(self._add_default_contraint_properties(_column))
                yield _column

    def get_checks(self) -> Iterator[expressions.Constraint]:
        """Extracts check constraints from the SQL statement.

        Yields:
            Iterator[expressions.Constraint]: An iterator of check constraints.
        """
        for _constraint in self.ddl.find_all(expressions.Constraint):
            for _check in _constraint.expressions:
                if isinstance(_check, expressions.CheckColumnConstraint):
                    _defaults = list()
                    for _default in self._add_default_contraint_properties(_constraint):
                        _defaults.append(expressions.ColumnConstraint(this=_default))
                    _constraint.expressions.extend(_defaults)
                    yield _constraint

    @staticmethod
    def _add_default_contraint_properties(constraint: Expression) -> List[expressions.OnProperty]:
        """Adds default constraint properties to a constraint.

        Args:
            constraint (Expression): The constraint expression.

        Returns:
            List[expressions.OnProperty]: A list of default constraint properties.
        """
        _defaults = list()
        props = [str(p.find(expressions.Identifier)).strip().upper() for p in constraint.find_all(expressions.OnProperty)]
        if 'VIOLATION' not in props:
            _defaults.append(
                expressions.OnProperty(this=expressions.Identifier(this="VIOLATION")))
        # If no check type is specified, default to DROP
        if len([v.value for v in CheckType.__members__.values() if v.value in props]) == 0:
            _defaults.append(
                expressions.OnProperty(this=expressions.Identifier(this=DEFAULT_CONSTRAINT_VIOLATION)))
        return _defaults

    @staticmethod
    def _check_protocol(value:str) -> bool:
        """Checks if the given value has a supported protocol.

        Args:
            value (str): The value to check.

        Returns:
            bool: True if the protocol is supported, False otherwise.

        Raises:
            NotImplementedError: If the protocol is not supported.
        """
        protocols = ['s3', 'az', 'abfss', 'gs'] # supported protocols
        if value.startswith(tuple(f"{_protocol}://" for _protocol in protocols)):
            return True
        if "://" in value:
            raise NotImplementedError(f"Invalid path: {value}. Supported protocols: {protocols}")
        return False


    def _get_sources(self, sql:expressions.Expression) -> Iterator[expressions.Anonymous]:
        """Extracts source expressions from the SQL statement.

        Args:
            sql (expressions.Expression): The SQL expression.

        Yields:
            Iterator[expressions.Anonymous]: An iterator of source expressions.
        """
        for _table in sql.find_all(expressions.Table):
            _name = _table.find(expressions.Identifier)
            if _name is not None:
                if self._check_protocol(_name.this):
                    if _name.this.endswith(
                        tuple(_fmt for _fmt in ['.csv', '.csv.gz', '.csv.zip'])):
                        yield expressions.Anonymous(
                            this='read_csv',
                            expressions=[
                                expressions.Literal(this=_name.this),
                                expressions.EQ(
                                    this=expressions.Identifier(this='header'),
                                    expression=expressions.Boolean(this=True))])
                    if _name.this.endswith(
                        tuple(_fmt for _fmt in ['.json', '.json.gz', '.json.zip'])):
                        yield expressions.Anonymous(
                            this='read_json',
                            expressions=[expressions.Literal(this=_name.this)])
                    if _name.this.endswith(
                        tuple(_fmt for _fmt in ['.avro'])):
                        yield expressions.Anonymous(
                            this='read_avro',
                            expressions=[expressions.Literal(this=_name.this)])
                    if _name.this.endswith(
                        tuple(_fmt for _fmt in ['.parquet', '.snappy.parquet'])):
                        yield expressions.Anonymous(
                            this='read_parquet',
                            expressions=[expressions.Literal(this=_name.this)])
            if isinstance(_table.this, expressions.ReadCSV):
                yield expressions.Anonymous(
                    this='read_csv',
                    expressions=[_table.this.find(expressions.Literal)] + _table.this.expressions
                )
            if isinstance(_table.this, expressions.Anonymous):
                if _table.this.this in ['read_csv', 'read_json', 'read_parquet', 'read_avro']:
                    yield _table.this

    def get_source(self) -> Iterator[expressions.Literal]:
        """Extracts source literals from the SQL statement.

        Yields:
            Iterator[expressions.Literal]: An iterator of source literals.
        """
        for _from in self.ddl.find(expressions.Subquery | expressions.Query).find_all(expressions.From):
            for _source in self._get_sources(_from):
                yield _source.find(expressions.Literal)

    def _ddl_statements(self, sql: str) -> Expression:
        """Parses a SQL string into a CREATE TABLE expression.

        Args:
            sql (str): The SQL string to parse.

        Returns:
            Expression: The CREATE TABLE expression.

        Raises:
            NotImplementedError: If the SQL string is not a CREATE TABLE statement.
        """
        for _p_exp in parse(sql, dialect=DoraDialect):
            if isinstance(_p_exp, expressions.Create):
                if _p_exp.kind == 'TABLE':
                    return _p_exp
                else:
                    raise NotImplementedError(f'Unsupported CREATE type: {_p_exp.kind}')

    def _dcl_statements(self, sql: str) -> Iterator[Expression]:
        """Parses a SQL string into a list of GRANT expressions.

        Args:
            sql (str): The SQL string to parse.

        Yields:
            Iterator[Expression]: An iterator of GRANT expressions.

        Raises:
            NotImplementedError: If the SQL string contains unsupported GRANT types.
            ValueError: If the GRANT TABLE does not match the CREATE TABLE.
        """
        for _p_exp in parse(sql, dialect=DoraDialect):
            if isinstance(_p_exp, expressions.Grant):
                if _p_exp.args['kind'] != 'TABLE':
                    log.error('Only GRANT TABLE is supported. Found: %s', _p_exp.args["kind"])
                    raise NotImplementedError(f'Unsupported GRANT type: {_p_exp.args["kind"]}')
                _grant_tbl = _p_exp.find(expressions.Table)
                if _grant_tbl != self.get_table():
                    _msg = 'grant table "%s" is different from "%s"'
                    log.error(_msg, _grant_tbl, self.get_table())
                    _err = f'GRANT TABLE does not match CREATE TABLE: {_grant_tbl}'
                    raise ValueError(_err)
                yield _p_exp

    @staticmethod
    def column_required(col: Expression) -> bool:
        """Checks if a column is required (NOT NULL or PRIMARY KEY).

        Args:
            col (Expression): The column expression.

        Returns:
            bool: True if the column is required, False otherwise.
        """
        if col.find(expressions.NotNullColumnConstraint):
            return True
        if col.find(expressions.PrimaryKeyColumnConstraint):
            return True
        return False

    def get_primary_keys(self) -> Iterator[expressions.Identifier]:
        """Extracts primary key columns from the SQL statement.

        Yields:
            Iterator[expressions.Identifier]: An iterator of primary key columns.
        """
        for _col in self.ddl.find_all(expressions.ColumnDef):
            if _col.find(expressions.PrimaryKeyColumnConstraint):
                yield _col.find(expressions.Identifier)

    @staticmethod
    def column_comment(col: Expression) -> str:
        """Extracts the comment from a column.

        Args:
            col (Expression): The column expression.

        Returns:
            str: The column comment.
        """
        if isinstance(col.constraints, list):
            for constraint in col.constraints:
                if isinstance(constraint, expressions.ColumnConstraint):
                    if isinstance(constraint.kind, expressions.CommentColumnConstraint):
                        return constraint.kind.this.this
        return str()

    @staticmethod
    def column_type(column: expressions.ColumnDef) -> PrimitiveType:
        """Maps SQL types to Iceberg PrimitiveType.

        Args:
            column (expressions.ColumnDef): The column definition.

        Returns:
            PrimitiveType: The corresponding Iceberg PrimitiveType.

        Raises:
            NotImplementedError: If the SQL type is not supported.
        """
        # Boolean Type
        if column.kind.sql() == "BOOLEAN":
            return BooleanType()
        if column.kind.sql() == "BOOL":
            return BooleanType()
        # Integer Types
        if column.kind.sql() == "INTEGER":
            return IntegerType()
        if column.kind.sql() == "INT":
            return IntegerType()
        if column.kind.sql() == "BIGINT":
            return LongType()
        if column.kind.sql() == "LONG":
            return LongType()
        # Floating-Point Types
        if column.kind.sql() == "FLOAT":
            return FloatType()
        if column.kind.sql() == "REAL":
            return DoubleType()
        if column.kind.sql() == "DOUBLE":
            return DoubleType()
        # Fixed-Point Decimals (Precision, Scale)
        if column.kind.sql().startswith("DECIMAL"):
            return DecimalType(*[int(exp.this.this) for exp in column.kind.expressions])
        if column.kind.sql().startswith("NUMERIC"):
            return DecimalType(*[int(exp.this.this) for exp in column.kind.expressions])
        # Text Types
        if column.kind.sql() == "STRING":
            return StringType()
        if column.kind.sql() == "VARCHAR":
            return StringType()
        if column.kind.sql() == "TEXT":
            return StringType()
        # Time Types
        if column.kind.sql() == "TIME":
            return TimeType()
        # Timestamp Types
        if column.kind.sql() == "TIMESTAMPTZ":
            return TimestamptzType()
        if column.kind.sql() == "TIMESTAMP":
            return TimestampType()
        if column.kind.sql() == "DATETIME":
            return TimestampType()
        # Date Types
        if column.kind.sql() == "DATE":
            return DateType()
        # Universally Unique Identifiers
        if column.kind.sql() == "UUID":
            return UUIDType()
        if column.kind.sql() == "STRUCT":
            return StringType()
        raise NotImplementedError(column.kind)

    @staticmethod
    def partition_transform(exp: expressions.Anonymous) -> Transform:
        """Extracts the partition transform from a SQL expression.

        Args:
            exp (expressions.Anonymous): The partition expression.

        Returns:
            Transform: The corresponding partition transform.
        """
        # partition by year
        if str(exp.this).lower() == "years":
            return YearTransform()
        if isinstance(exp, expressions.Year):
            return YearTransform()
        # partition by month
        if str(exp.this).lower() == "months":
            return MonthTransform()
        if isinstance(exp, expressions.Month):
            return MonthTransform()
        # equivalent to dateint partitioning
        if str(exp.this).lower() == "days":
            return DayTransform()
        if isinstance(exp, expressions.Day):
            return DayTransform()
        # equivalent to dateint and hour partitioning
        if str(exp.this).lower() == "hour":
            return HourTransform()
        if str(exp.this).lower() == "hours":
            return HourTransform()
        if str(exp.this).lower() == "date_hour":
            return HourTransform()
        # partition by hashed value mod N buckets
        if str(exp.this).lower() == "bucket":
            _buckets = int(exp.find(expressions.Literal).this)
            return BucketTransform(num_buckets=_buckets)
        # partition by hashed value mod N buckets
        if str(exp.this).lower() == "truncate":
            _width = int(exp.find(expressions.Literal).this)
            return TruncateTransform(width=_width)
        if isinstance(exp, expressions.Identifier):
            return IdentityTransform()
