"""Dora plugin module.

This module defines the Dora plugin interface and related functionality.
"""

from abc import ABC, abstractmethod
from typing import Iterator
from pkgutil import iter_modules

from pydantic import BaseModel, Field

class Plugin(BaseModel, ABC):
    """Dora Plugin Interface.

    Attributes:
        name (str): Configuration name.
    """
    name: str = Field(description="Configuration name", exclude=True)

    @property
    def type(self) -> str:
        """Get the plugin name.

        Returns:
            str: The plugin name.
        """
        return self.__class__.__module__

    @abstractmethod
    def render(self, *args, **kwargs) -> int:
        """Implement the render method.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Returns:
            int: The result of the render method.
        """

class Volume(Plugin, ABC):
    """Dora Volume Plugin Interface."""

class Topic(Plugin, ABC):
    """Dora Topic Plugin Interface."""

class Sensor(Plugin, ABC):
    """Dora Sensor Plugin Interface."""

class Engine(Plugin, ABC):
    """Dora Sensor Plugin Interface."""


class PluginManager:
    """Plugin manager class."""

    PLUGIN_MODULE_PREFIX = "dora_"

    @classmethod
    def get_prefixed_modules(cls) -> Iterator[str]:
        """Get the prefixed module names.

        Yields:
            Iterator[str]: An iterator of module names that start with the prefix.
        """
        for _, name, _ in iter_modules():
            if name.startswith(cls.PLUGIN_MODULE_PREFIX):
                yield name
