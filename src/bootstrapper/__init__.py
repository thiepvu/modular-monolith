"""
Bootstrapper module for application initialization.
Handles IoC container, module loading, and application factory.
"""

from .container import Container, get_container
from .app_factory import create_app
from .module_loader import ModuleLoader

__all__ = ["Container", "get_container", "create_app", "ModuleLoader"]