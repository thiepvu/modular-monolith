"""
IoC (Inversion of Control) Container for Dependency Injection.
Simple implementation of dependency injection pattern.
"""

from typing import Callable, Dict, Any, Type, TypeVar, Optional
from functools import lru_cache
import inspect

T = TypeVar("T")


class Container:
    """Simple IoC container for dependency injection"""
    
    def __init__(self):
        self._services: Dict[Type, Callable] = {}
        self._singletons: Dict[Type, Any] = {}
        self._factories: Dict[Type, Callable] = {}
    
    def register_transient(
        self,
        service_type: Type[T],
        implementation: Callable[..., T]
    ) -> None:
        """
        Register a transient service (new instance each time).
        
        Args:
            service_type: The type to register
            implementation: Factory function that creates instances
        """
        self._services[service_type] = implementation
    
    def register_singleton(
        self,
        service_type: Type[T],
        implementation: Optional[Callable[..., T]] = None,
        instance: Optional[T] = None
    ) -> None:
        """
        Register a singleton service (single instance).
        
        Args:
            service_type: The type to register
            implementation: Factory function (if instance not provided)
            instance: Pre-created instance (if implementation not provided)
        """
        if instance is not None:
            self._singletons[service_type] = instance
        elif implementation is not None:
            if service_type not in self._singletons:
                self._singletons[service_type] = implementation()
        else:
            raise ValueError("Either implementation or instance must be provided")
    
    def register_factory(
        self,
        service_type: Type[T],
        factory: Callable[..., T]
    ) -> None:
        """
        Register a factory function.
        
        Args:
            service_type: The type to register
            factory: Factory function
        """
        self._factories[service_type] = factory
    
    def register_instance(self, service_type: Type[T], instance: T) -> None:
        """
        Register an existing instance as singleton.
        
        Args:
            service_type: The type to register
            instance: The instance to register
        """
        self._singletons[service_type] = instance
    
    def resolve(self, service_type: Type[T]) -> T:
        """
        Resolve a service from the container.
        
        Args:
            service_type: The type to resolve
            
        Returns:
            Instance of the requested type
            
        Raises:
            ValueError: If service is not registered
        """
        # Check if it's a singleton
        if service_type in self._singletons:
            return self._singletons[service_type]
        
        # Check if it's a factory
        if service_type in self._factories:
            return self._factories[service_type]()
        
        # Check if it's registered as transient
        if service_type in self._services:
            factory = self._services[service_type]
            
            # Auto-inject dependencies
            sig = inspect.signature(factory)
            kwargs = {}
            for param_name, param in sig.parameters.items():
                if param.annotation != inspect.Parameter.empty:
                    try:
                        kwargs[param_name] = self.resolve(param.annotation)
                    except ValueError:
                        # If dependency not found, skip it
                        pass
            
            return factory(**kwargs)
        
        raise ValueError(f"Service {service_type.__name__} not registered in container")
    
    def is_registered(self, service_type: Type[T]) -> bool:
        """
        Check if a service is registered.
        
        Args:
            service_type: The type to check
            
        Returns:
            True if registered, False otherwise
        """
        return (
            service_type in self._singletons or
            service_type in self._services or
            service_type in self._factories
        )
    
    def clear(self) -> None:
        """Clear all registrations"""
        self._services.clear()
        self._singletons.clear()
        self._factories.clear()


# Global container instance
_container: Optional[Container] = None


@lru_cache()
def get_container() -> Container:
    """
    Get global container instance.
    Creates container on first call and caches it.
    
    Returns:
        Global container instance
    """
    global _container
    if _container is None:
        _container = Container()
    return _container


def reset_container() -> None:
    """Reset global container (useful for testing)"""
    global _container
    _container = None
    get_container.cache_clear()