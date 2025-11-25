"""
Application entry point.
"""

import uvicorn
from src.bootstrapper.app_factory import create_app

# Create application instance
app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )