"""
Taj Chat - Main Application

FastAPI application for AI video creation.
"""

import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Optional

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .config import get_config
from .workflows.engine import WorkflowEngine, WorkflowMode
from .monitoring.metrics import metrics
from .monitoring.performance import performance_monitor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Global workflow engine
workflow_engine: Optional[WorkflowEngine] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    global workflow_engine

    logger.info("Starting Taj Chat...")

    # Initialize workflow engine
    workflow_engine = WorkflowEngine()

    # Validate configuration
    config = get_config()
    status = config.validate()
    logger.info(f"Configuration status: {status}")

    yield

    logger.info("Shutting down Taj Chat...")


# Create FastAPI app
app = FastAPI(
    title="Taj Chat",
    description="Ultimate AI Video Creation Platform with 10x Specialist Agents",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class VideoRequest(BaseModel):
    """Request to create a video."""
    prompt: str = Field(..., min_length=1, description="Description of the video to create")
    mode: str = Field("hybrid", description="Workflow mode: sequential, parallel, hybrid")
    platforms: list[str] = Field(
        default=["tiktok"],
        description="Target platforms: tiktok, instagram_reels, youtube_shorts, twitter"
    )
    parameters: dict = Field(default_factory=dict, description="Additional parameters")


class VideoResponse(BaseModel):
    """Response from video creation."""
    workflow_id: str
    status: str
    mode: str
    platforms: list[str]
    execution_time_ms: float
    output_files: list[str]
    errors: list[str]


class StatusResponse(BaseModel):
    """System status response."""
    app_name: str
    version: str
    agents_registered: list[str]
    ai_providers: dict
    social_media: dict


# API Routes
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "app": "Taj Chat",
        "version": "1.0.0",
        "description": "Ultimate AI Video Creation Platform",
        "docs": "/docs",
    }


@app.get("/status", response_model=StatusResponse)
async def get_status():
    """Get system status."""
    config = get_config()
    status = config.validate()

    agents = workflow_engine.get_agent_status() if workflow_engine else {}

    return StatusResponse(
        app_name=config.app.app_name,
        version=config.app.version,
        agents_registered=list(agents.keys()),
        ai_providers=status.get("ai_providers", {}),
        social_media=status.get("social_media", {}),
    )


@app.post("/create", response_model=VideoResponse)
async def create_video(request: VideoRequest, background_tasks: BackgroundTasks):
    """Create a video using the 10x agent system."""

    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")

    # Map mode string to enum
    mode_map = {
        "sequential": WorkflowMode.SEQUENTIAL,
        "parallel": WorkflowMode.PARALLEL,
        "hybrid": WorkflowMode.HYBRID,
    }
    mode = mode_map.get(request.mode.lower(), WorkflowMode.HYBRID)

    logger.info(f"Creating video: {request.prompt[:50]}...")

    # Run workflow
    result = await workflow_engine.create_video(
        prompt=request.prompt,
        mode=mode,
        platforms=request.platforms,
        parameters=request.parameters,
    )

    return VideoResponse(
        workflow_id=result.workflow_id,
        status=result.status,
        mode=result.mode.value,
        platforms=request.platforms,
        execution_time_ms=result.total_execution_time_ms,
        output_files=[str(f) for f in result.output_files],
        errors=result.errors,
    )


@app.get("/workflow/{workflow_id}")
async def get_workflow(workflow_id: str):
    """Get workflow status."""

    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")

    status = workflow_engine.get_workflow_status(workflow_id)

    if not status:
        raise HTTPException(status_code=404, detail="Workflow not found")

    return status


@app.get("/agents")
async def get_agents():
    """Get status of all agents."""

    if not workflow_engine:
        raise HTTPException(status_code=503, detail="Workflow engine not initialized")

    return workflow_engine.get_agent_status()


@app.get("/config")
async def get_configuration():
    """Get configuration status (without sensitive data)."""
    config = get_config()
    return config.validate()


# Health check
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "engine": workflow_engine is not None}


# Monitoring endpoints
@app.get("/metrics")
async def get_metrics():
    """Get all metrics."""
    return metrics.get_all_metrics()


@app.get("/metrics/prometheus")
async def get_prometheus_metrics():
    """Get metrics in Prometheus format."""
    from fastapi.responses import PlainTextResponse
    return PlainTextResponse(
        content=metrics.get_prometheus_metrics(),
        media_type="text/plain",
    )


@app.get("/performance")
async def get_performance():
    """Get performance report."""
    return performance_monitor.get_report()


@app.get("/performance/slow")
async def get_slow_operations(threshold_ms: float = 1000):
    """Get slow operations."""
    slow_ops = performance_monitor.get_slow_operations(threshold_ms)
    return {
        "threshold_ms": threshold_ms,
        "count": len(slow_ops),
        "operations": [
            {
                "name": op.name,
                "duration_ms": op.duration_ms,
                "timestamp": op.start_time.isoformat(),
                "success": op.success,
            }
            for op in slow_ops[-100:]  # Last 100
        ],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
