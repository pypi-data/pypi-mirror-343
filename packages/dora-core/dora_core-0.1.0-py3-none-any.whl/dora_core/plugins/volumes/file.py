"""File System Volume Plugin"""
from os import path
from pydantic import Field

from dora_core.plugins import Volume

class Profile(Volume):
    """File System Volume Implementation"""
    dir: str = Field(description="Directory")
    format: str = Field(description="File format")
    wildcard: str = Field(description="Wildcard", default="*")

    def render(self, *args, **kwargs):
        """Implement the volume method."""
        _file = f"{self.wildcard}.{self.format}"
        if str(self.format).strip().lower() == 'iceberg':
            _file = ""
        _path = path.join(self.bucket,self.prefix,_file)
        return f"{_path}"
