import os
import base64
import logging
from typing import Dict, List, Optional

import httpx
from superagentx.handler.base import BaseHandler
from superagentx.handler.decorators import tool

logger = logging.getLogger(__name__)


class SonarQubeHandler(BaseHandler):

    def __init__(self):
        self.sonar_host = os.getenv("SONAR_HOST_URL", "https://sonarcloud.io")
        self.sonar_token = os.getenv("SONAR_TOKEN", None)

        if not self.sonar_token:
            raise ValueError("SONAR_TOKEN environment variable is missing")

        # Basic Auth header
        token_bytes = f"{self.sonar_token}:".encode("utf-8")
        auth_token = base64.b64encode(token_bytes).decode("utf-8")
        self.headers = {"Authorization": f"Basic {auth_token}"}

    async def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        url = f"{self.sonar_host}{endpoint}"
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            return response.json()

    # ---------------- BUG DETAILS ----------------
    @tool
    async def get_bug_details(self, project_key: str) -> Dict:
        data = await self._get(
            "/api/issues/search",
            params={
                "componentKeys": project_key,
                "types": "BUG",
                "ps": 100
            }
        )

        bugs: List[Dict] = []
        for issue in data.get("issues", []):
            bugs.append({
                "issue_key": issue["key"],
                "rule": issue["rule"],
                "severity": issue["severity"],
                "message": issue["message"],
                "file_path": issue["component"],
                "line": issue.get("line"),
                "status": issue["status"]
            })

        return {
            "project_key": project_key,
            "bug_count": len(bugs),
            "bugs": bugs
        }

    # ---------------- VULNERABILITY DETAILS ----------------
    @tool
    async def get_vulnerability_details(self, project_key: str) -> Dict:
        vulnerabilities: List[Dict] = []

        # 1️⃣ Get real vulnerabilities
        vuln_data = await self._get(
            "/api/issues/search",
            params={
                "componentKeys": project_key,
                "types": "VULNERABILITY",
                "ps": 100
            }
        )

        for issue in vuln_data.get("issues", []):
            vulnerabilities.append({
                "issue_key": issue["key"],
                "type": issue["type"],
                "rule": issue["rule"],
                "severity": issue["severity"],
                "message": issue["message"],
                "file_path": issue["component"],
                "line": issue.get("line"),
                "status": issue["status"]
            })

        # 2️⃣ Get security hotspots (separate API)
        hotspot_data = await self._get(
            "/api/hotspots/search",
            params={
                "projectKey": project_key,
                "ps": 100
            }
        )

        for hotspot in hotspot_data.get("hotspots", []):
            vulnerabilities.append({
                "issue_key": hotspot["key"],
                "type": "SECURITY_HOTSPOT",
                "rule": hotspot["ruleKey"],
                "severity": hotspot["vulnerabilityProbability"],
                "message": hotspot["message"],
                "file_path": hotspot["component"],
                "line": hotspot.get("line"),
                "status": hotspot["status"]
            })

        return {
            "project_key": project_key,
            "vulnerability_count": len(vulnerabilities),
            "vulnerabilities": vulnerabilities
        }

    # ---------------- QUALITY GATE ----------------
    @tool
    async def get_quality_gate_status(self, project_key: str) -> Dict:
        data = await self._get(
            "/api/qualitygates/project_status",
            params={"projectKey": project_key}
        )
        return {
            "project_key": project_key,
            "quality_gate_status": data["projectStatus"]["status"]
        }


# ---------------- Example Usage ----------------
if __name__ == "__main__":
    import asyncio

    async def main():
        project = "your_project_key_here"
        handler = SonarQubeHandler()

        bugs = await handler.get_bug_details(project)
        print("Bugs:", bugs)

        vulns = await handler.get_vulnerability_details(project)
        print("Vulnerabilities + Hotspots:", vulns)

        qg = await handler.get_quality_gate_status(project)
        print("Quality Gate Status:", qg)

    asyncio.run(main())
