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

@mcp.tool()
def get_available_subway_stations(
    type: str = "congestionRltm",
    offset: int = 0,
    limit: int = 100
) -> str:
    """
    Get a list of available subway stations that provide congestion data.

    Args:
        type (str): Type of congestion data to check availability for.
            - congestionTrain: 통계성 열차 혼잡도 제공 가능 역사
            - congestionCar: 통계성 칸 혼잡도 제공 가능 역사
            - congestionRltm: 실시간 열차/칸 혼잡도 제공 가능 역사
            - exit: 지하철역 출구별 통행자 수 제공 가능 역사
        offset (int): Starting point for the list (default: 0)
        limit (int): Maximum number of stations to return (default: 100, max: 1000)

    Returns:
        str: A string containing the list of available subway stations with their details.

    Example:
        >>> get_available_subway_stations(type="congestionRltm", offset=0, limit=100)
        'Available subway stations: ...'
    """
    base_url = "https://apis.openapi.sk.com/puzzle/subway/meta/stations"
    params = {
        "type": type,
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
