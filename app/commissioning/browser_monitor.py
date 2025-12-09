"""
Browser Commissioning & Monitoring System
==========================================

Monitors and validates all browser interactions:
- Console messages (errors, warnings, logs)
- Network requests (API calls, resources)
- Page navigation
- Click events
- Form submissions
- Performance metrics
"""

import asyncio
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class MessageType(Enum):
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"
    LOG = "log"


class RequestType(Enum):
    XHR = "xhr"
    FETCH = "fetch"
    SCRIPT = "script"
    STYLESHEET = "stylesheet"
    IMAGE = "image"
    FONT = "font"
    WEBSOCKET = "webSocket"
    MAIN_FRAME = "mainFrame"
    OTHER = "other"


@dataclass
class ConsoleMessage:
    """Browser console message"""
    type: MessageType
    message: str
    timestamp: int
    source: Optional[str] = None
    line: Optional[int] = None
    column: Optional[int] = None


@dataclass
class NetworkRequest:
    """Network request details"""
    url: str
    method: str
    timestamp: int
    resource_type: RequestType
    status_code: Optional[int] = None
    response_time: Optional[float] = None
    size: Optional[int] = None
    error: Optional[str] = None


@dataclass
class PageInteraction:
    """User interaction on page"""
    action: str  # click, type, hover, scroll, etc.
    element: str
    timestamp: int
    details: Dict = field(default_factory=dict)


@dataclass
class BrowserSession:
    """Complete browser session data"""
    session_id: str
    start_time: datetime
    pages_visited: List[str] = field(default_factory=list)
    console_messages: List[ConsoleMessage] = field(default_factory=list)
    network_requests: List[NetworkRequest] = field(default_factory=list)
    interactions: List[PageInteraction] = field(default_factory=list)
    errors: List[Dict] = field(default_factory=list)
    warnings: List[Dict] = field(default_factory=list)


class BrowserMonitor:
    """
    Browser Commissioning & Monitoring System

    Capabilities:
    1. Console message tracking
    2. Network request monitoring
    3. Error detection & reporting
    4. Performance analysis
    5. Interaction logging
    6. Page validation
    7. API endpoint verification
    8. Resource loading analysis
    9. WebSocket monitoring
    10. Commission report generation
    """

    def __init__(self):
        self.sessions: Dict[str, BrowserSession] = {}
        self.current_session: Optional[str] = None

    def start_session(self, session_id: str = None) -> str:
        """Start a new monitoring session"""
        session_id = session_id or f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.sessions[session_id] = BrowserSession(
            session_id=session_id,
            start_time=datetime.now(),
        )
        self.current_session = session_id
        return session_id

    def parse_console_messages(self, messages: List[Dict]) -> List[ConsoleMessage]:
        """Parse raw console messages from browser"""
        parsed = []
        for msg in messages:
            try:
                msg_type = MessageType(msg.get("type", "log"))
            except ValueError:
                msg_type = MessageType.LOG

            parsed.append(ConsoleMessage(
                type=msg_type,
                message=msg.get("message", ""),
                timestamp=msg.get("timestamp", 0),
                source=msg.get("source"),
                line=msg.get("line"),
                column=msg.get("column"),
            ))
        return parsed

    def parse_network_requests(self, requests: List[Dict]) -> List[NetworkRequest]:
        """Parse raw network requests from browser"""
        parsed = []
        for req in requests:
            try:
                resource_type = RequestType(req.get("resourceType", "other"))
            except ValueError:
                resource_type = RequestType.OTHER

            parsed.append(NetworkRequest(
                url=req.get("url", ""),
                method=req.get("method", "GET"),
                timestamp=req.get("timestamp", 0),
                resource_type=resource_type,
                status_code=req.get("statusCode"),
                response_time=req.get("responseTime"),
                size=req.get("size"),
                error=req.get("error"),
            ))
        return parsed

    def add_console_messages(self, messages: List[Dict], session_id: str = None):
        """Add console messages to session"""
        session_id = session_id or self.current_session
        if session_id not in self.sessions:
            self.start_session(session_id)

        parsed = self.parse_console_messages(messages)
        self.sessions[session_id].console_messages.extend(parsed)

        # Track errors and warnings separately
        for msg in parsed:
            if msg.type == MessageType.ERROR:
                self.sessions[session_id].errors.append({
                    "message": msg.message,
                    "timestamp": msg.timestamp,
                    "source": msg.source,
                })
            elif msg.type == MessageType.WARNING:
                self.sessions[session_id].warnings.append({
                    "message": msg.message,
                    "timestamp": msg.timestamp,
                    "source": msg.source,
                })

    def add_network_requests(self, requests: List[Dict], session_id: str = None):
        """Add network requests to session"""
        session_id = session_id or self.current_session
        if session_id not in self.sessions:
            self.start_session(session_id)

        parsed = self.parse_network_requests(requests)
        self.sessions[session_id].network_requests.extend(parsed)

    def add_page_visit(self, url: str, session_id: str = None):
        """Record page visit"""
        session_id = session_id or self.current_session
        if session_id and session_id in self.sessions:
            self.sessions[session_id].pages_visited.append(url)

    def add_interaction(
        self,
        action: str,
        element: str,
        details: Dict = None,
        session_id: str = None,
    ):
        """Record user interaction"""
        session_id = session_id or self.current_session
        if session_id and session_id in self.sessions:
            self.sessions[session_id].interactions.append(PageInteraction(
                action=action,
                element=element,
                timestamp=int(datetime.now().timestamp() * 1000),
                details=details or {},
            ))

    def analyze_session(self, session_id: str = None) -> Dict:
        """Analyze session for issues and metrics"""
        session_id = session_id or self.current_session
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]

        # Analyze console messages
        error_count = len([m for m in session.console_messages if m.type == MessageType.ERROR])
        warning_count = len([m for m in session.console_messages if m.type == MessageType.WARNING])

        # Analyze network requests
        failed_requests = [r for r in session.network_requests if r.status_code and r.status_code >= 400]
        api_requests = [r for r in session.network_requests if r.resource_type == RequestType.XHR]

        # Calculate metrics
        total_requests = len(session.network_requests)
        success_rate = ((total_requests - len(failed_requests)) / total_requests * 100) if total_requests > 0 else 100

        return {
            "session_id": session_id,
            "duration": (datetime.now() - session.start_time).total_seconds(),
            "pages_visited": len(session.pages_visited),
            "interactions": len(session.interactions),
            "console": {
                "total_messages": len(session.console_messages),
                "errors": error_count,
                "warnings": warning_count,
            },
            "network": {
                "total_requests": total_requests,
                "failed_requests": len(failed_requests),
                "api_requests": len(api_requests),
                "success_rate": f"{success_rate:.1f}%",
            },
            "health": "HEALTHY" if error_count == 0 and len(failed_requests) == 0 else "ISSUES_DETECTED",
        }

    def get_errors(self, session_id: str = None) -> List[Dict]:
        """Get all errors from session"""
        session_id = session_id or self.current_session
        if session_id in self.sessions:
            return self.sessions[session_id].errors
        return []

    def get_failed_requests(self, session_id: str = None) -> List[Dict]:
        """Get failed network requests"""
        session_id = session_id or self.current_session
        if session_id not in self.sessions:
            return []

        return [
            {
                "url": r.url,
                "method": r.method,
                "status": r.status_code,
                "error": r.error,
            }
            for r in self.sessions[session_id].network_requests
            if r.status_code and r.status_code >= 400
        ]

    def generate_commission_report(self, session_id: str = None) -> Dict:
        """Generate comprehensive commission report"""
        session_id = session_id or self.current_session
        if session_id not in self.sessions:
            return {"error": "Session not found"}

        session = self.sessions[session_id]
        analysis = self.analyze_session(session_id)

        # Categorize issues
        critical_issues = []
        warnings = []
        info = []

        # Check for JavaScript errors
        js_errors = [m for m in session.console_messages if m.type == MessageType.ERROR]
        for error in js_errors:
            if "TypeError" in error.message or "ReferenceError" in error.message:
                critical_issues.append({
                    "type": "JavaScript Error",
                    "message": error.message[:200],
                    "severity": "CRITICAL",
                })
            else:
                warnings.append({
                    "type": "Console Error",
                    "message": error.message[:200],
                    "severity": "WARNING",
                })

        # Check for hydration mismatches (React SSR issues)
        hydration_warnings = [
            m for m in session.console_messages
            if "did not match" in m.message.lower() or "hydration" in m.message.lower()
        ]
        for warn in hydration_warnings:
            info.append({
                "type": "Hydration Mismatch",
                "message": "Server/Client render mismatch detected (common in dev mode)",
                "severity": "INFO",
            })

        # Check for failed API calls
        failed_apis = [
            r for r in session.network_requests
            if r.resource_type == RequestType.XHR and r.status_code and r.status_code >= 400
        ]
        for api in failed_apis:
            critical_issues.append({
                "type": "API Failure",
                "message": f"{api.method} {api.url} returned {api.status_code}",
                "severity": "CRITICAL",
            })

        # Check for missing resources
        missing_resources = [
            r for r in session.network_requests
            if r.status_code == 404
        ]
        for res in missing_resources:
            warnings.append({
                "type": "Missing Resource",
                "message": f"404 Not Found: {res.url}",
                "severity": "WARNING",
            })

        # Generate recommendations
        recommendations = []
        if critical_issues:
            recommendations.append("Fix critical JavaScript errors before deployment")
        if hydration_warnings:
            recommendations.append("Hydration mismatches are normal in dev mode but should be fixed for production")
        if missing_resources:
            recommendations.append("Ensure all resources (images, fonts, scripts) are available")
        if not recommendations:
            recommendations.append("No critical issues found - system is ready for deployment")

        return {
            "session_id": session_id,
            "generated_at": datetime.now().isoformat(),
            "summary": analysis,
            "status": "PASS" if not critical_issues else "FAIL",
            "issues": {
                "critical": critical_issues,
                "warnings": warnings,
                "info": info,
            },
            "counts": {
                "critical": len(critical_issues),
                "warnings": len(warnings),
                "info": len(info),
            },
            "pages_tested": session.pages_visited,
            "interactions_recorded": len(session.interactions),
            "recommendations": recommendations,
        }


class PageValidator:
    """
    Validates specific pages for completeness and functionality
    """

    REQUIRED_ELEMENTS = {
        "/": [
            "Dashboard",
            "Create Video",
            "AI Agents",
            "System Online",
        ],
        "/landing": [
            "Create Viral Videos",
            "10 specialist AI agents",
            "Start Creating",
            "Pricing",
        ],
        "/create": [
            "Video prompt",
            "Target Platforms",
            "Workflow Mode",
            "Generate Video",
        ],
        "/studio": [
            "Timeline",
            "Assets",
            "Effects",
            "Export",
        ],
        "/agents": [
            "Content Analysis",
            "Video Generation",
            "Music Generation",
            "Image Generation",
        ],
        "/social": [
            "Connected Platforms",
            "TikTok",
            "Instagram",
            "YouTube",
            "Twitter",
        ],
        "/analytics": [
            "Total Views",
            "Engagement",
            "Platform Performance",
        ],
        "/commissioning": [
            "Commission",
            "Run",
            "Agents",
        ],
    }

    def validate_page(self, page_url: str, page_snapshot: str) -> Dict:
        """Validate page contains required elements"""
        # Extract path from URL
        path = "/" if page_url.endswith("/") or "localhost:3000" in page_url and "/" not in page_url.split("3000")[1] else "/" + page_url.split("localhost:3000/")[1].split("?")[0] if "localhost:3000/" in page_url else "/"

        required = self.REQUIRED_ELEMENTS.get(path, [])

        found = []
        missing = []

        for element in required:
            if element.lower() in page_snapshot.lower():
                found.append(element)
            else:
                missing.append(element)

        return {
            "page": path,
            "status": "PASS" if not missing else "FAIL",
            "required_elements": len(required),
            "found": found,
            "missing": missing,
            "completeness": f"{len(found) / len(required) * 100:.0f}%" if required else "100%",
        }


# Global instance
browser_monitor = BrowserMonitor()
page_validator = PageValidator()


def analyze_browser_data(console_messages: List[Dict], network_requests: List[Dict]) -> Dict:
    """Quick analysis of browser data"""
    monitor = BrowserMonitor()
    session_id = monitor.start_session()
    monitor.add_console_messages(console_messages)
    monitor.add_network_requests(network_requests)
    return monitor.generate_commission_report(session_id)




