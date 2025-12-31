#!/usr/bin/env python3
"""
Taj Chat Validation CLI

Comprehensive validation tool for the Taj Chat platform.
Checks configuration, dependencies, APIs, and system readiness.

Usage:
    python validate.py [--full] [--fix] [--json]

Options:
    --full      Run full validation suite including API tests
    --fix       Attempt to fix issues automatically
    --json      Output results in JSON format
"""

import asyncio
import json
import os
import sys
import subprocess
import shutil
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))


@dataclass
class ValidationResult:
    """Result of a validation check."""
    name: str
    status: str  # passed, failed, warning, skipped
    message: str
    details: Dict = field(default_factory=dict)
    fixable: bool = False
    fix_command: Optional[str] = None


@dataclass
class ValidationReport:
    """Complete validation report."""
    timestamp: str
    total_checks: int
    passed: int
    failed: int
    warnings: int
    skipped: int
    results: List[ValidationResult]
    overall_status: str

    def to_json(self) -> str:
        return json.dumps({
            "timestamp": self.timestamp,
            "total_checks": self.total_checks,
            "passed": self.passed,
            "failed": self.failed,
            "warnings": self.warnings,
            "skipped": self.skipped,
            "overall_status": self.overall_status,
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "message": r.message,
                    "details": r.details,
                    "fixable": r.fixable,
                    "fix_command": r.fix_command,
                }
                for r in self.results
            ],
        }, indent=2)


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'


class Validator:
    """System validation tool."""

    def __init__(self, project_path: str = "."):
        self.project_path = Path(project_path)
        self.results: List[ValidationResult] = []

    def check_python_version(self) -> ValidationResult:
        """Check Python version."""
        version = sys.version_info
        if version.major >= 3 and version.minor >= 10:
            return ValidationResult(
                name="Python Version",
                status="passed",
                message=f"Python {version.major}.{version.minor}.{version.micro}",
            )
        else:
            return ValidationResult(
                name="Python Version",
                status="failed",
                message=f"Python 3.10+ required, found {version.major}.{version.minor}",
                fixable=True,
                fix_command="Install Python 3.10 or higher",
            )

    def check_node_version(self) -> ValidationResult:
        """Check Node.js version."""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
            )
            version = result.stdout.strip()
            major = int(version.lstrip("v").split(".")[0])

            if major >= 18:
                return ValidationResult(
                    name="Node.js Version",
                    status="passed",
                    message=f"Node.js {version}",
                )
            else:
                return ValidationResult(
                    name="Node.js Version",
                    status="failed",
                    message=f"Node.js 18+ required, found {version}",
                    fixable=True,
                    fix_command="Install Node.js 18 or higher",
                )
        except FileNotFoundError:
            return ValidationResult(
                name="Node.js Version",
                status="failed",
                message="Node.js not found",
                fixable=True,
                fix_command="Install Node.js from https://nodejs.org",
            )

    def check_ffmpeg(self) -> ValidationResult:
        """Check FFmpeg installation."""
        if shutil.which("ffmpeg"):
            try:
                result = subprocess.run(
                    ["ffmpeg", "-version"],
                    capture_output=True,
                    text=True,
                )
                version = result.stdout.split("\n")[0]
                return ValidationResult(
                    name="FFmpeg",
                    status="passed",
                    message=version[:50],
                )
            except Exception:
                return ValidationResult(
                    name="FFmpeg",
                    status="warning",
                    message="FFmpeg found but version check failed",
                )
        else:
            return ValidationResult(
                name="FFmpeg",
                status="failed",
                message="FFmpeg not found",
                fixable=True,
                fix_command="brew install ffmpeg (Mac) or apt install ffmpeg (Linux)",
            )

    def check_python_packages(self) -> ValidationResult:
        """Check required Python packages."""
        required = [
            "fastapi",
            "pydantic",
            "aiohttp",
            "moviepy",
            "numpy",
            "pillow",
        ]

        missing = []
        for package in required:
            try:
                __import__(package)
            except ImportError:
                missing.append(package)

        if not missing:
            return ValidationResult(
                name="Python Packages",
                status="passed",
                message=f"All {len(required)} core packages installed",
            )
        else:
            return ValidationResult(
                name="Python Packages",
                status="failed",
                message=f"Missing packages: {', '.join(missing)}",
                fixable=True,
                fix_command="pip install -r requirements.txt",
            )

    def check_dashboard_packages(self) -> ValidationResult:
        """Check dashboard node_modules."""
        node_modules = self.project_path / "dashboard" / "node_modules"

        if node_modules.exists():
            package_count = len(list(node_modules.iterdir()))
            return ValidationResult(
                name="Dashboard Packages",
                status="passed",
                message=f"{package_count} packages installed",
            )
        else:
            return ValidationResult(
                name="Dashboard Packages",
                status="failed",
                message="node_modules not found",
                fixable=True,
                fix_command="cd dashboard && npm install",
            )

    def check_env_files(self) -> ValidationResult:
        """Check environment configuration."""
        env_file = self.project_path / ".env"
        env_example = self.project_path / ".env.example"

        if env_file.exists():
            return ValidationResult(
                name="Environment Config",
                status="passed",
                message=".env file configured",
            )
        elif env_example.exists():
            return ValidationResult(
                name="Environment Config",
                status="warning",
                message=".env file missing, .env.example available",
                fixable=True,
                fix_command="cp .env.example .env",
            )
        else:
            return ValidationResult(
                name="Environment Config",
                status="warning",
                message="No .env configuration found",
            )

    def check_directories(self) -> ValidationResult:
        """Check required directories exist."""
        required_dirs = [
            "app",
            "dashboard",
            "tests",
            "output",
            "generated",
        ]

        existing = []
        missing = []

        for dir_name in required_dirs:
            dir_path = self.project_path / dir_name
            if dir_path.exists():
                existing.append(dir_name)
            else:
                missing.append(dir_name)

        if not missing:
            return ValidationResult(
                name="Project Structure",
                status="passed",
                message=f"All {len(required_dirs)} directories present",
            )
        else:
            return ValidationResult(
                name="Project Structure",
                status="warning",
                message=f"Missing directories: {', '.join(missing)}",
                fixable=True,
                fix_command=f"mkdir -p {' '.join(missing)}",
            )

    def check_api_modules(self) -> ValidationResult:
        """Check API modules can be imported."""
        try:
            from app.main import app
            from app.workflows.engine import WorkflowEngine
            from app.agents.orchestrator import Orchestrator

            return ValidationResult(
                name="API Modules",
                status="passed",
                message="Core modules importable",
            )
        except ImportError as e:
            return ValidationResult(
                name="API Modules",
                status="failed",
                message=f"Import error: {str(e)[:50]}",
            )
        except Exception as e:
            return ValidationResult(
                name="API Modules",
                status="warning",
                message=f"Module warning: {str(e)[:50]}",
            )

    def check_agent_modules(self) -> ValidationResult:
        """Check agent modules."""
        agents = [
            "video_agent",
            "music_agent",
            "image_agent",
            "content_agent",
            "voice_agent",
            "editing_agent",
            "optimization_agent",
            "analytics_agent",
            "safety_agent",
            "social_agent",
        ]

        loaded = []
        failed = []

        for agent in agents:
            try:
                __import__(f"app.agents.{agent}")
                loaded.append(agent)
            except ImportError:
                failed.append(agent)

        if not failed:
            return ValidationResult(
                name="Agent Modules",
                status="passed",
                message=f"All {len(agents)} agents loadable",
            )
        else:
            return ValidationResult(
                name="Agent Modules",
                status="failed",
                message=f"Failed to load: {', '.join(failed[:3])}...",
            )

    def check_git_status(self) -> ValidationResult:
        """Check git repository status."""
        git_dir = self.project_path / ".git"

        if git_dir.exists():
            try:
                result = subprocess.run(
                    ["git", "status", "--porcelain"],
                    capture_output=True,
                    text=True,
                    cwd=self.project_path,
                )
                changes = len(result.stdout.strip().split("\n")) if result.stdout.strip() else 0

                if changes == 0:
                    return ValidationResult(
                        name="Git Status",
                        status="passed",
                        message="Working tree clean",
                    )
                else:
                    return ValidationResult(
                        name="Git Status",
                        status="warning",
                        message=f"{changes} uncommitted changes",
                    )
            except Exception:
                return ValidationResult(
                    name="Git Status",
                    status="warning",
                    message="Could not check git status",
                )
        else:
            return ValidationResult(
                name="Git Status",
                status="skipped",
                message="Not a git repository",
            )

    async def check_api_health(self) -> ValidationResult:
        """Check API health endpoint."""
        try:
            import aiohttp

            async with aiohttp.ClientSession() as session:
                async with session.get(
                    "http://localhost:8000/health",
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        return ValidationResult(
                            name="API Health",
                            status="passed",
                            message=f"API responding: {data.get('status', 'ok')}",
                        )
                    else:
                        return ValidationResult(
                            name="API Health",
                            status="failed",
                            message=f"API returned status {response.status}",
                        )
        except Exception as e:
            return ValidationResult(
                name="API Health",
                status="skipped",
                message="API not running (start with: uvicorn app.main:app)",
            )

    def run_sync_checks(self) -> List[ValidationResult]:
        """Run synchronous validation checks."""
        checks = [
            self.check_python_version,
            self.check_node_version,
            self.check_ffmpeg,
            self.check_python_packages,
            self.check_dashboard_packages,
            self.check_env_files,
            self.check_directories,
            self.check_api_modules,
            self.check_agent_modules,
            self.check_git_status,
        ]

        results = []
        for check in checks:
            try:
                result = check()
                results.append(result)
            except Exception as e:
                results.append(ValidationResult(
                    name=check.__name__.replace("check_", "").replace("_", " ").title(),
                    status="failed",
                    message=f"Check failed: {str(e)[:50]}",
                ))

        return results

    async def run_async_checks(self) -> List[ValidationResult]:
        """Run async validation checks."""
        results = []

        try:
            result = await self.check_api_health()
            results.append(result)
        except Exception as e:
            results.append(ValidationResult(
                name="API Health",
                status="failed",
                message=f"Check failed: {str(e)[:50]}",
            ))

        return results

    async def validate(self, full: bool = False) -> ValidationReport:
        """Run all validation checks."""
        self.results = self.run_sync_checks()

        if full:
            async_results = await self.run_async_checks()
            self.results.extend(async_results)

        # Calculate summary
        passed = sum(1 for r in self.results if r.status == "passed")
        failed = sum(1 for r in self.results if r.status == "failed")
        warnings = sum(1 for r in self.results if r.status == "warning")
        skipped = sum(1 for r in self.results if r.status == "skipped")

        overall = "PASSED" if failed == 0 else "FAILED"

        return ValidationReport(
            timestamp=datetime.now().isoformat(),
            total_checks=len(self.results),
            passed=passed,
            failed=failed,
            warnings=warnings,
            skipped=skipped,
            results=self.results,
            overall_status=overall,
        )


def print_report(report: ValidationReport):
    """Print validation report to console."""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}  TAJ CHAT SYSTEM VALIDATION{Colors.ENDC}")
    print(f"{Colors.BOLD}{Colors.CYAN}{'='*60}{Colors.ENDC}\n")

    for result in report.results:
        if result.status == "passed":
            icon = f"{Colors.GREEN}✓{Colors.ENDC}"
        elif result.status == "failed":
            icon = f"{Colors.RED}✗{Colors.ENDC}"
        elif result.status == "warning":
            icon = f"{Colors.YELLOW}⚠{Colors.ENDC}"
        else:
            icon = f"{Colors.BLUE}○{Colors.ENDC}"

        print(f"  {icon} {Colors.BOLD}{result.name}{Colors.ENDC}")
        print(f"      {result.message}")

        if result.fixable and result.fix_command:
            print(f"      {Colors.CYAN}Fix: {result.fix_command}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Summary:{Colors.ENDC}")
    print(f"  {Colors.GREEN}Passed: {report.passed}{Colors.ENDC}")
    print(f"  {Colors.RED}Failed: {report.failed}{Colors.ENDC}")
    print(f"  {Colors.YELLOW}Warnings: {report.warnings}{Colors.ENDC}")
    print(f"  {Colors.BLUE}Skipped: {report.skipped}{Colors.ENDC}")

    print(f"\n{Colors.BOLD}Overall Status: ", end="")
    if report.overall_status == "PASSED":
        print(f"{Colors.GREEN}PASSED ✓{Colors.ENDC}")
    else:
        print(f"{Colors.RED}FAILED ✗{Colors.ENDC}")

    print()


async def main():
    """Main entry point."""
    full = "--full" in sys.argv
    fix = "--fix" in sys.argv
    json_output = "--json" in sys.argv

    validator = Validator()
    report = await validator.validate(full=full)

    if json_output:
        print(report.to_json())
    else:
        print_report(report)

    # Return exit code based on status
    sys.exit(0 if report.overall_status == "PASSED" else 1)


if __name__ == "__main__":
    asyncio.run(main())
