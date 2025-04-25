from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("subway")

@mcp.tool()
def get_subway_congestion(station_name: str) -> str:
    """
    Get the current congestion level of a subway station using the Seoul Metro API.

    Args:
        station_name (str): The name of the subway station in Korean (e.g., '을지로입구').

    Returns:
        str: A string containing the congestion information for the station.

    Example:
        >>> get_subway_congestion('을지로입구')
        'Congestion data for 을지로입구 station: ...'
    """
    base_url = "http://alb-diaas-pzl-dev-1196007480.ap-northeast-2.elb.amazonaws.com:3000"
    endpoint = f"/subway-qa/congestion-car-rltm/{station_name}"
    
    try:
        response = httpx.get(
            f"{base_url}{endpoint}",
            headers={"accept": "application/json"}
        )
        response.raise_for_status()
        return f"Congestion data for {station_name} station: {response.text}"
    except httpx.HTTPError as e:
        return f"Error fetching congestion data: {str(e)}"

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
