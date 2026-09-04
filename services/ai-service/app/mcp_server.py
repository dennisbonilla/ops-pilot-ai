from mcp.server.fastmcp import FastMCP

mcp = FastMCP("OpsPilot Tools")


@mcp.tool()
def get_service_health(service: str) -> dict:
    """Return simulated read-only health for an allow-listed service."""
    allowed = {"api", "database", "web"}
    if service not in allowed:
        return {"status": "unknown", "reason": "service_not_allowed"}
    return {"service": service, "status": "healthy", "source": "demo-monitor"}


@mcp.tool()
def create_incident(title: str, severity: str) -> dict:
    """Create an incident. The host must obtain human approval before calling."""
    return {"status": "created", "title": title, "severity": severity}


if __name__ == "__main__":
    mcp.run(transport="stdio")

