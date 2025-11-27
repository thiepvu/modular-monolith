"""
Dynamic module loader for bounded contexts.
Discovers and loads modules automatically.
"""

from typing import List, Optional, Tuple, Any
from importlib import import_module
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ModuleLoader:
    """Dynamic module loader for bounded contexts"""
    
    def __init__(self, modules_path: str = "src.modules"):
        """
        Initialize module loader.
        
        Args:
            modules_path: Python path to modules directory
        """
        self.modules_path = modules_path
        self._loaded_modules: List[str] = []
        self._failed_modules: List[Tuple[str, str]] = []
    
    def discover_modules(self) -> List[str]:
        """
        Discover all modules in the modules directory.
        
        Returns:
            List of module names
        """
        modules_dir = Path("src/modules")
        if not modules_dir.exists():
            logger.warning(f"Modules directory not found: {modules_dir}")
            return []
        
        modules = []
        for item in modules_dir.iterdir():
            if item.is_dir() and not item.name.startswith("_"):
                # Check if it's a valid module (has __init__.py)
                if (item / "__init__.py").exists():
                    modules.append(item.name)
        
        logger.info(f"Discovered {len(modules)} modules: {', '.join(modules)}")
        return modules
    
    def load_module_routes(
        self,
        module_name: str,
        api_version: str = "v1"
    ) -> Optional[Any]:
        """
        Load routes from a specific module.
        
        Args:
            module_name: Name of the module to load
            api_version: API version (v1, v2, etc.)
            
        Returns:
            Router object if found, None otherwise
        """
        try:
            # Try to import the routes module
            routes_module_path = (
                f"{self.modules_path}.{module_name}."
                f"presentation.api.{api_version}.routes"
            )
            
            logger.debug(f"Loading routes from: {routes_module_path}")
            routes_module = import_module(routes_module_path)
            
            # Get the router object
            router = getattr(routes_module, "router", None)
            
            if router is None:
                logger.warning(
                    f"Module {module_name} has no 'router' export in routes.py"
                )
                self._failed_modules.append(
                    (module_name, "No router found in routes.py")
                )
                return None
            
            self._loaded_modules.append(module_name)
            logger.info(f"✓ Successfully loaded module: {module_name}")
            
            return router
            
        except ImportError as e:
            logger.warning(
                f"Could not load routes for module {module_name} ({api_version}): {e}"
            )
            self._failed_modules.append((module_name, str(e)))
            return None
        except Exception as e:
            logger.error(
                f"Error loading module {module_name}: {e}",
                exc_info=True
            )
            self._failed_modules.append((module_name, str(e)))
            return None
    
    def load_all_routes(
        self,
        api_version: str = "v1"
    ) -> List[Tuple[str, Any]]:
        """
        Load routes from all discovered modules.
        
        Args:
            api_version: API version to load
            
        Returns:
            List of tuples (module_name, router)
        """
        modules = self.discover_modules()
        routers = []
        
        logger.info(f"Loading routes for API version: {api_version}")
        
        for module_name in modules:
            router = self.load_module_routes(module_name, api_version)
            if router:
                routers.append((module_name, router))
        
        logger.info(
            f"Loaded {len(routers)} modules successfully, "
            f"{len(self._failed_modules)} failed"
        )
        
        if self._failed_modules:
            logger.warning(f"Failed modules: {self._failed_modules}")
        
        return routers
    
    @property
    def loaded_modules(self) -> List[str]:
        """
        Get list of successfully loaded modules.
        
        Returns:
            List of module names
        """
        return self._loaded_modules.copy()
    
    @property
    def failed_modules(self) -> List[Tuple[str, str]]:
        """
        Get list of failed modules with error messages.
        
        Returns:
            List of tuples (module_name, error_message)
        """
        return self._failed_modules.copy()