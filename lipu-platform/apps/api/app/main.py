"""
FastAPI Application Entry Point

This module initializes the FastAPI application with all necessary
middleware, routes, and error handlers.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

# Import routes
# from app.api.v1 import products, orders, quotes, customers, inventory, ai, analytics, auth, health

app = FastAPI(
    title="LIPU API",
    description="AI-powered UPVC Windows & Doors E-commerce Platform",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure from environment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"],  # TODO: Configure from environment
)

# Routes will be registered here
# app.include_router(products.router, prefix="/api/v1", tags=["products"])
# app.include_router(orders.router, prefix="/api/v1", tags=["orders"])
# etc.


@app.get("/health")
async def health_check():
    """Health check endpoint for readiness probes"""
    return {"status": "healthy", "version": "0.1.0"}


@app.get("/healthz")
async def liveness_check():
    """Liveness probe endpoint"""
    return {"status": "alive"}


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    print("LIPU API starting up...")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("LIPU API shutting down...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
