"""
Application factory for creating FastAPI application instances.
Handles all application initialization and configuration.
"""

from contextlib import asynccontextmanager
from typing import AsyncGenerator, Any
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError

from config.settings import get_settings
from config.logging_config import setup_logging
from infrastructure.database.connection import db
from shared.api.error_handler import (
    app_exception_handler,
    validation_exception_handler,
    database_exception_handler,
    generic_exception_handler
)
from core.exceptions.base_exceptions import BaseException as AppBaseException
from .module_loader import ModuleLoader

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    """
    Application lifespan events.
    Handles startup and shutdown tasks.
    
    Args:
        app: FastAPI application instance
    """
    # Startup
    settings = get_settings()
    
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize database
    db.initialize()
    logger.info("✓ Database initialized")
    
    # Log loaded modules
    if hasattr(app.state, "loaded_modules"):
        logger.info(f"✓ Loaded modules: {', '.join(app.state.loaded_modules)}")
    
    logger.info(f"✅ {settings.APP_NAME} started successfully")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")
    
    # Close database connections
    await db.close()
    logger.info("✓ Database connections closed")
    
    logger.info("👋 Application shutdown complete")


def create_app() -> FastAPI:
    """
    Application factory function.
    Creates and configures a FastAPI application instance.
    
    Returns:
        Configured FastAPI application
    """
    settings = get_settings()
    
    # Setup logging
    setup_logging(
        level=settings.LOG_LEVEL,
        format_type=settings.LOG_FORMAT
    )
    
    # Create FastAPI app
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Modular Monolith with Clean Architecture",
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
        debug=settings.DEBUG
    )
    
    # Add middlewares
    _add_middlewares(app, settings)
    
    # Add exception handlers
    _add_exception_handlers(app)
    
    # Load modules and routes
    _load_modules(app, settings)
    
    # Add health check endpoint
    _add_health_check(app, settings)
    
    return app


def _add_middlewares(app: FastAPI, settings) -> None:
    """Add middleware to the application"""
    
    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_CREDENTIALS,
        allow_methods=settings.CORS_METHODS,
        allow_headers=settings.CORS_HEADERS,
    )
    logger.info("✓ CORS middleware added")
    
    # GZip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)
    logger.info("✓ GZip middleware added")


def _add_exception_handlers(app: FastAPI) -> None:
    """Add exception handlers to the application"""
    
    app.add_exception_handler(AppBaseException, app_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(SQLAlchemyError, database_exception_handler)
    app.add_exception_handler(Exception, generic_exception_handler)
    
    logger.info("✓ Exception handlers registered")


def _load_modules(app: FastAPI, settings) -> None:
    """Load modules and their routes"""
    
    module_loader = ModuleLoader()
    
    # Load v1 routes
    v1_routers = module_loader.load_all_routes("v1")
    for module_name, router in v1_routers:
        app.include_router(router, prefix=settings.API_V1_PREFIX)
        logger.debug(f"✓ Included {module_name} v1 routes")
    
    # Load v2 routes (if any)
    # v2_routers = module_loader.load_all_routes("v2")
    # for module_name, router in v2_routers:
    #     app.include_router(router, prefix=settings.API_V2_PREFIX)
    #     logger.debug(f"✓ Included {module_name} v2 routes")
    
    # Store loaded modules in app state
    app.state.loaded_modules = module_loader.loaded_modules
    app.state.failed_modules = module_loader.failed_modules


def _add_health_check(app: FastAPI, settings) -> None:
    """Add health check endpoint"""
    
    @app.get("/health", tags=["Health"], summary="Health check endpoint")
    async def health_check():
        """
        Health check endpoint.
        Returns application status and version.
        """
        return {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "environment": settings.ENVIRONMENT,
            "modules": {
                "loaded": app.state.loaded_modules,
                "failed": app.state.failed_modules
            }
        }
    
    @app.get("/", tags=["Root"], include_in_schema=False)
    async def root():
        """Root endpoint redirecting to docs"""
        return {
            "message": f"Welcome to {settings.APP_NAME}",
            "version": settings.APP_VERSION,
            "docs": "/api/docs"
        }
    
    logger.info("✓ Health check endpoint added")