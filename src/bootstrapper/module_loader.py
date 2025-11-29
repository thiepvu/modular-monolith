"""
Dynamic module loader for bounded contexts.
Discovers and loads modules automatically with Swagger/OpenAPI support.
"""

from typing import List, Optional, Tuple, Any, Dict
from importlib import import_module
from pathlib import Path
import logging
from fastapi import APIRouter

logger = logging.getLogger(__name__)


class ModuleLoader:
    """Dynamic module loader for bounded contexts with Swagger support"""
    
    def __init__(self, modules_path: str = "modules"):
        """
        Initialize module loader.
        
        Args:
            modules_path: Python path to modules directory
        """
        self.modules_path = modules_path
        self._loaded_modules: List[str] = []
        self._failed_modules: List[Tuple[str, str]] = []
        self._routers: Dict[str, APIRouter] = {}
    
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
    
    def _validate_router(self, router: Any, module_name: str) -> bool:
        """
        Validate that the router is a proper FastAPI APIRouter.
        
        Args:
            router: Router object to validate
            module_name: Name of the module (for logging)
            
        Returns:
            True if valid, False otherwise
        """
        if not isinstance(router, APIRouter):
            logger.error(
                f"Module {module_name}: 'router' is not an APIRouter instance. "
                f"Found type: {type(router)}"
            )
            return False
        
        if not router.routes:
            logger.warning(
                f"Module {module_name}: Router has no routes defined"
            )
            return False
        
        logger.debug(
            f"Module {module_name}: Router validated with {len(router.routes)} routes"
        )
        return True
    
    def load_module_routes(
        self,
        module_name: str,
        api_version: str = "v1",
        prefix: Optional[str] = None,
        tags: Optional[List[str]] = None
    ) -> Optional[APIRouter]:
        """
        Load routes from a specific module.
        
        Args:
            module_name: Name of the module to load
            api_version: API version (v1, v2, etc.)
            prefix: URL prefix for the module (e.g., "/users")
            tags: OpenAPI tags for documentation
            
        Returns:
            Router object if found, None otherwise
        """
        try:
            # Try to import the routes module
            routes_module_path = (
                f"{self.modules_path}.{module_name}."
                f"presentation.api.{api_version}.routes"
            )
            
            logger.debug(f"Attempting to load: {routes_module_path}")
            routes_module = import_module(routes_module_path)
            
            # Get the router object
            router = getattr(routes_module, "router", None)
            
            if router is None:
                error_msg = "No 'router' export found in routes.py"
                logger.warning(f"Module {module_name}: {error_msg}")
                self._failed_modules.append((module_name, error_msg))
                return None
            
            # Validate the router
            if not self._validate_router(router, module_name):
                error_msg = "Router validation failed"
                self._failed_modules.append((module_name, error_msg))
                return None
            
            # Apply prefix and tags if provided
            if prefix and not router.prefix:
                logger.debug(f"Setting prefix '{prefix}' for module {module_name}")
                router.prefix = prefix
            
            if tags and not router.tags:
                logger.debug(f"Setting tags {tags} for module {module_name}")
                router.tags = tags
            
            # Store the router
            self._routers[module_name] = router
            self._loaded_modules.append(module_name)
            
            # Log route details
            route_paths = [route.path for route in router.routes]
            logger.info(
                f"✓ Successfully loaded module: {module_name}\n"
                f"  - Routes: {len(router.routes)}\n"
                f"  - Paths: {route_paths}\n"
                f"  - Prefix: {router.prefix or 'None'}\n"
                f"  - Tags: {router.tags or 'None'}"
            )
            
            return router
            
        except ImportError as e:
            error_msg = f"Import failed: {str(e)}"
            logger.warning(
                f"Could not load routes for module {module_name} ({api_version}): {error_msg}"
            )
            self._failed_modules.append((module_name, error_msg))
            return None
            
        except Exception as e:
            error_msg = f"Unexpected error: {str(e)}"
            logger.error(
                f"Error loading module {module_name}: {error_msg}",
                exc_info=True
            )
            self._failed_modules.append((module_name, error_msg))
            return None
    
    def load_all_routes(
        self,
        api_version: str = "v1",
        auto_prefix: bool = True,
        auto_tags: bool = True
    ) -> List[Tuple[str, APIRouter]]:
        """
        Load routes from all discovered modules.
        
        Args:
            api_version: API version to load
            auto_prefix: Automatically set URL prefix based on module name
            auto_tags: Automatically set OpenAPI tags based on module name
            
        Returns:
            List of tuples (module_name, router)
        """
        modules = self.discover_modules()
        routers = []
        
        logger.info(f"\n{'='*60}")
        logger.info(f"Loading routes for API version: {api_version}")
        logger.info(f"{'='*60}\n")
        
        for module_name in modules:
            # Generate prefix and tags
            prefix = f"/{module_name.replace('_', '-')}" if auto_prefix else None
            tags = [module_name.replace("_", " ").title()] if auto_tags else None
            
            router = self.load_module_routes(
                module_name,
                api_version,
                prefix=prefix,
                tags=tags
            )
            
            if router:
                routers.append((module_name, router))
        
        logger.info(f"\n{'='*60}")
        logger.info(
            f"✓ Loaded {len(routers)} modules successfully\n"
            f"✗ {len(self._failed_modules)} modules failed"
        )
        logger.info(f"{'='*60}\n")
        
        if self._failed_modules:
            logger.warning("Failed modules:")
            for module_name, error in self._failed_modules:
                logger.warning(f"  - {module_name}: {error}")
        
        return routers
    
    def get_router(self, module_name: str) -> Optional[APIRouter]:
        """
        Get a specific loaded router by module name.
        
        Args:
            module_name: Name of the module
            
        Returns:
            Router if found, None otherwise
        """
        return self._routers.get(module_name)
    
    def get_all_routers(self) -> Dict[str, APIRouter]:
        """
        Get all loaded routers.
        
        Returns:
            Dictionary mapping module names to routers
        """
        return self._routers.copy()
    
    def print_routes_summary(self) -> None:
        """Print a summary of all loaded routes for debugging."""
        logger.info("\n" + "="*60)
        logger.info("ROUTES SUMMARY")
        logger.info("="*60 + "\n")
        
        for module_name, router in self._routers.items():
            logger.info(f"Module: {module_name}")
            logger.info(f"  Prefix: {router.prefix or '/'}")
            logger.info(f"  Tags: {router.tags or 'None'}")
            logger.info(f"  Routes:")
            
            for route in router.routes:
                methods = ",".join(route.methods) if hasattr(route, 'methods') else "N/A"
                logger.info(f"    [{methods}] {route.path}")
            
            logger.info("")
    
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
    
    @property
    def stats(self) -> Dict[str, int]:
        """
        Get loading statistics.
        
        Returns:
            Dictionary with loading stats
        """
        total_routes = sum(len(router.routes) for router in self._routers.values())
        
        return {
            "total_modules": len(self._loaded_modules) + len(self._failed_modules),
            "loaded_modules": len(self._loaded_modules),
            "failed_modules": len(self._failed_modules),
            "total_routes": total_routes
        }