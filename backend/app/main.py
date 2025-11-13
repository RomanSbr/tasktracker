from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.api import api_router
from app.db.session import engine
from app.services.bootstrap import ensure_default_admin


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan events"""
    # Startup
    print("🚀 Starting Task Tracker API...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(lambda _: None)
        print("✅ Database connection established")
        await ensure_default_admin()
        print("👑 Default admin ensured")
    except Exception as exc:
        print("❌ Failed to connect to database:", exc)
        raise
    yield
    # Shutdown
    print("🛑 Shutting down...")
    await engine.dispose()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION
        }
    )


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


# Custom exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "detail": str(exc)
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
