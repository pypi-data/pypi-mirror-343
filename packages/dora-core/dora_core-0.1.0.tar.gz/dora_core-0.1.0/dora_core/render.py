"""SQL Render module.

This module provides functionality to render SQL templates using Jinja2.
"""
from jinja2 import Environment, FileSystemLoader

from .conf import Profile

class Sources:
    """Render the SQL sources.

    Args:
        profile (Profile): The configuration profile.
    """
    def __init__(self, profile: Profile):
        # Configures the Jinja2 environment with the file system loader.
        self.sources = Environment(loader=FileSystemLoader(profile.sources))
        # Gets the rendering context from the profile.
        self.context = profile.conf(render=True)[profile.target]

    def volume(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Render the volume in the template based on the profile values.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            str: The rendered volume.
        """
        _type, _name = args
        return f"'{self.context['volumes'][_type][_name]}'"

    def topic(self, *args, **kwargs):  # pylint: disable=unused-argument
        """Render the topic in the template based on the profile values.

        Args:
            *args: Positional arguments.
            **kwargs: Keyword arguments.

        Returns:
            str: The rendered topic.
        """
        _type, _name = args
        return f"'{self.context['topics'][_type][_name]}'"

    def render(self, template: str):
        """Render the template.

        Args:
            template (str): The path to the template to be rendered.

        Returns:
            str: The rendered template.
        """
        _template = self.sources.get_template(template)  # Gets the Jinja2 template.
        # Renders the template with the volume and topic methods.
        return _template.render(volume=self.volume, topic=self.topic)
