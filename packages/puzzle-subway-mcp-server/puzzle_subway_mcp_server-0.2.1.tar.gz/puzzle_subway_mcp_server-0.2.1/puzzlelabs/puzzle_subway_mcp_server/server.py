from typing import Any, Optional
import httpx
import os
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP server
mcp = FastMCP("subway")

# Get appKey from environment variable
APP_KEY = os.getenv("APP_KEY")
if not APP_KEY:
    raise ValueError("APP_KEY environment variable is not set")

@mcp.tool()
def get_subway_congestion(station_name: str) -> str:
    """
    Get the current congestion level of a subway station using the Puzzle Subway API.
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

@mcp.tool()
def get_available_subway_stations(
    offset: int = 0,
    limit: int = 100
) -> str:
    """
    Get a list of available subway stations that provide congestion data.

    Args:
        offset (int): Starting point for the list (default: 0)
        limit (int): Maximum number of stations to return (default: 100, max: 1000)
    """
    base_url = "https://apis.openapi.sk.com/puzzle/subway/meta/stations"
    params = {
        "offset": offset,
        "limit": limit
    }
    
    try:
        response = httpx.get(
            base_url,
            params=params,
            headers={
                "accept": "application/json",
                "appKey": APP_KEY
            }
        )
        response.raise_for_status()
        return f"Available subway stations: {response.text}"
    except httpx.HTTPError as e:
        return f"Error fetching available stations: {str(e)}"

def main():
    """Main function to run the MCP server"""
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()
