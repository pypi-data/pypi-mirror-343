"""Constants and Configs for Dora."""

from importlib import import_module
from enum import Enum, auto
from typing import Dict, Optional, List
from re import fullmatch, error
from os import path, getcwd, environ
from yaml import dump, load, CDumper, CLoader
from pydantic import BaseModel, Field, ConfigDict

from .exceptions import ProfileNotFound
from .plugins import Plugin, PluginManager

# Environment variables for configuration files
CONFIG_FILE =  environ.get('DORA_PROJECT_CONF','dora_project.yml')
PROFILE_FILE = environ.get('DORA_PROFILE_FILE','dora_profile.yml')
DEFAULT_NAME = environ.get('DORA_PROJECT_NAME','dora')

# Regex pattern for valid names
NAME_PATTERN = r"^[a-zA-Z0-9_]*$"

class SaveOption(Enum):
    """Save option for project configurations."""
    JSON = auto()
    YAML = auto()

class Profile(BaseModel):
    """Profile configurations."""
    model_config = ConfigDict(strict=False, str_strip_whitespace=True, extra="allow")

    sources: str = Field(description="SQL Source directory.")
    ouputs: Optional[Dict[str,List[Plugin]]] = Field(
        description="Output configurations.", default=None)
    target: Optional[str] = Field(
        description="Target name.", default=None)
    name: Optional[str] = Field(
        description="Project name.",
        default=DEFAULT_NAME,
        pattern=NAME_PATTERN)

    def model_post_init(self, *args, **kwargs): # pylint: disable=unused-argument
        """Post init method to configure the profile."""
        self.conf()

    def conf(self, render:bool=False) -> dict:
        """Generate the profile configuration dictionary.
        
        Args:
            render (bool): Whether to render the output or not.
        
        Returns:
            dict: The profile configuration.
        """
        _conf = dict()
        _target = None
        # Iterate over outputs and build the configuration dictionary
        for _target, outputs in self.ouputs.items(): #pylint: disable=E1101
            _conf[_target] = dict()
            for output in outputs:
                _, _, _type, _plugin = output.type.split(".")
                if _type not in _conf[_target]:
                    _conf[_target][_type] = dict()
                if _plugin not in _conf[_target][_type]:
                    _conf[_target][_type][_plugin] = dict()
                if render:
                    _conf[_target][_type][_plugin][output.name] = output.render()
                else:
                    _conf[_target][_type][_plugin][output.name] = output.model_dump()
        if _target: # Update default target
            self.target = _target
        _conf['sources']=self.sources
        _conf['target']=self.target
        _conf.update(self.model_extra)
        return _conf

    @classmethod
    def profile_location(cls):
        """Get the profile file location.
        
        Returns:
            str: The profile file path.
        """
        return path.join(getcwd(), PROFILE_FILE)

    @staticmethod
    def validate_name(string: str, pattern: str) -> bool:
        """Validate if a string matches a given regex pattern.
        
        Args:
            string (str): The string to validate.
            pattern (str): The regex pattern to match.
        
        Returns:
            bool: True if the string matches the pattern, False otherwise.
        """
        try:
            return bool(fullmatch(pattern, string))
        except error:
            return False

    @classmethod
    def _load_plugins(cls, profiles: dict) -> dict:
        """Parse and load plugins from the profiles.
        
        Args:
            profiles (dict): The profiles dictionary.
        
        Returns:
            dict: The loaded plugins.
        
        Raises:
            ImportError: If a plugin cannot be imported.
        """
        _loaded = dict()
        for _target, _outputs in profiles.items():
            if _target != profiles['target']:
                continue
            _loaded[_target] = list()
            for _type, plugin in _outputs.items():
                for _name, _configs in plugin.items():
                    for _key, _config in _configs.items():
                        _config.update({'name': _key})
                        import_success = False
                        for dora_module in PluginManager.get_prefixed_modules():
                            _module = f"{dora_module}.plugins.{_type}.{_name}"
                            try:
                                plug = import_module(_module, package=".")
                                _loaded[_target].append(plug.Profile.model_validate(_config))
                                import_success = True
                            except ImportError: #pylint: disable=W0702
                                continue
                        if not import_success:
                            raise ImportError(f"Plugin not found: {_type}.{_name}")
        return _loaded

    @classmethod
    def load(cls, name:str=DEFAULT_NAME) -> 'Profile':
        """Load the profile configurations from YAML.
        
        Args:
            name (str): The profile name to load.
        
        Returns:
            Profile: The loaded profile.
        
        Raises:
            ProfileNotFound: If the profile is not found.
        """
        if name is None:
            name = DEFAULT_NAME
        try:
            with open(file=cls.profile_location(), mode='r', encoding='utf-8') as file:
                _profiles = load(file, Loader=CLoader)[name]
                _plugins = cls._load_plugins(_profiles)
                for _plugin in _plugins:
                    del _profiles[_plugin]
                _profiles.update({'ouputs': _plugins})
                return cls.model_validate(_profiles)
        except FileNotFoundError as err:
            raise ProfileNotFound(f'Profile not found: {name}') from err
        except KeyError as err:
            raise ProfileNotFound(f'Profile not found: {name}') from err

    def save(self, name:str=None, option: SaveOption = SaveOption.YAML):
        """Save the profile configurations to a file.
        
        Args:
            name (str): The profile name to save.
            option (SaveOption): The save option (JSON or YAML).
        
        Raises:
            NotImplementedError: If an unknown save option is provided.
        """
        if name is not None:
            self.name = name
        _profile = {self.name:self.conf()}
        with open(file=Profile.profile_location(), mode='w', encoding='utf-8') as file:
            if option == SaveOption.JSON:
                file.write(_profile)
            elif option == SaveOption.YAML:
                file.write(dump(data=_profile, Dumper=CDumper, sort_keys=False))
            else:
                raise NotImplementedError(f'Unknown save option: {option}')

class Project(BaseModel):
    """Project configurations."""
    version: int = Field(
        default=1,
        description="Project configurations version.")
    name: str = Field(
        pattern=NAME_PATTERN,
        description="Project name and identifier.",
        min_length=3,
        max_length=50)
    profile: str = Field(
        description="Profile name.")
    sqls: str = Field(
        description="SQL files directory.",
    )

    @classmethod
    def project_location(cls):
        """Get the project configuration file location.
        
        Returns:
            str: The project configuration file path.
        """
        return path.join(getcwd(), CONFIG_FILE)

    @classmethod
    def load(cls) -> 'Project':
        """Load the project configurations from YAML.
        
        Returns:
            Project: The loaded project.
        """
        with open(file=cls.project_location(), mode='r', encoding='utf-8') as file:
            return cls.model_validate(load(file, Loader=CLoader))

    def yaml(self) -> str:
        """Get the project configurations as YAML.
        
        Returns:
            str: The project configurations in YAML format.
        """
        return dump(data=self.model_dump(), Dumper=CDumper, sort_keys=False)

    def save(self, option: SaveOption = SaveOption.YAML):
        """Save the project configurations to a file.
        
        Args:
            option (SaveOption): The save option (JSON or YAML).
        
        Raises:
            NotImplementedError: If an unknown save option is provided.
        """
        with open(file=Project.project_location(), mode='w', encoding='utf-8') as file:
            if option == SaveOption.JSON:
                file.write(self.model_dump_json())
            elif option == SaveOption.YAML:
                file.write(self.yaml())
            else:
                raise NotImplementedError(f'Unknown save option: {option}')
