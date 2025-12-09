#!/usr/bin/env python
"""
Taj Chat - Quick Start Script

Run the application with various modes.
"""

import argparse
import asyncio
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def run_api(host: str = "0.0.0.0", port: int = 8000):
    """Run FastAPI server."""
    import uvicorn
    logger.info(f"Starting API server at http://{host}:{port}")
    uvicorn.run("app.main:app", host=host, port=port, reload=True)


def run_ui(port: int = 7860, share: bool = False):
    """Run Gradio UI."""
    from app.workflows.engine import WorkflowEngine
    from app.ui.gradio_interface import launch_ui

    logger.info(f"Starting Gradio UI at http://localhost:{port}")
    engine = WorkflowEngine()
    launch_ui(workflow_engine=engine, port=port, share=share)


async def run_demo():
    """Run a demo video generation."""
    from app.workflows.engine import WorkflowEngine, WorkflowMode

    logger.info("Running demo video generation...")

    engine = WorkflowEngine()

    result = await engine.create_video(
        prompt="Create a 30-second motivational video about achieving your goals with energetic music",
        mode=WorkflowMode.HYBRID,
        platforms=["tiktok"],
    )

    print("\n" + "="*60)
    print("DEMO COMPLETE")
    print("="*60)
    print(f"Workflow ID: {result.workflow_id}")
    print(f"Status: {result.status}")
    print(f"Mode: {result.mode.value}")
    print(f"Execution Time: {result.total_execution_time_ms:.0f}ms")
    print(f"\nOutput Files:")
    for f in result.output_files:
        print(f"  - {f}")
    print(f"\nAgent Results:")
    for agent, res in result.agent_results.items():
        print(f"  - {agent}: {res.status}")
    if result.errors:
        print(f"\nErrors:")
        for e in result.errors:
            print(f"  - {e}")
    print("="*60)


def main():
    parser = argparse.ArgumentParser(
        description="Taj Chat - Ultimate AI Video Creation Platform"
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # API command
    api_parser = subparsers.add_parser("api", help="Run FastAPI server")
    api_parser.add_argument("--host", default="0.0.0.0", help="Host to bind")
    api_parser.add_argument("--port", type=int, default=8000, help="Port to bind")

    # UI command
    ui_parser = subparsers.add_parser("ui", help="Run Gradio UI")
    ui_parser.add_argument("--port", type=int, default=7860, help="Port to bind")
    ui_parser.add_argument("--share", action="store_true", help="Create public link")

    # Demo command
    subparsers.add_parser("demo", help="Run demo video generation")

    # Status command
    subparsers.add_parser("status", help="Check system status")

    args = parser.parse_args()

    if args.command == "api":
        run_api(host=args.host, port=args.port)
    elif args.command == "ui":
        run_ui(port=args.port, share=args.share)
    elif args.command == "demo":
        asyncio.run(run_demo())
    elif args.command == "status":
        from app.config import get_config
        config = get_config()
        status = config.validate()
        print("\nTaj Chat - System Status")
        print("="*40)
        print("\nAI Providers:")
        for provider, available in status["ai_providers"].items():
            print(f"  {provider}: {'✅' if available else '❌'}")
        print("\nSocial Media:")
        for platform, available in status["social_media"].items():
            print(f"  {platform}: {'✅' if available else '❌'}")
        print("\nDatabase:")
        for db, available in status["database"].items():
            print(f"  {db}: {'✅' if available else '❌'}")
        print("="*40)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
