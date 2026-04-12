#!/usr/bin/env python3
"""
CLI entry point for the TTP manager module

Usage:
    python -m ttp_manager import-fhir --source synthea_florida
    python -m ttp_manager import-fhir --source synthea_texas --limit 100
"""

# from fluvius.manager import fluvius_manager
# from .entrypoint import ecom_manager

# fluvius_manager.add_command(ecom_manager)
# fluvius_manager()


import uvicorn
from . import app

# Export the app for ASGI servers
__all__ = ["app"]

if __name__ == "__main__":
    uvicorn.run(
        "ecom_manager.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 