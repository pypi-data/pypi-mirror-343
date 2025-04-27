import os
import sys
import httpx
from pydantic import Field

from mcp.server.fastmcp import FastMCP

# Create MCP server instance
mcp = FastMCP("RobotControl")

# API Configuration
API_KEY = os.getenv('ECO_API_KEY')  
API_URL = os.getenv('ECO_API_URL')



ENDPOINT_ROBOT_CTL = "robot/ctl"
ENDPOINT_ROBOT_DEVICE_LIST = "robot/deviceList"
REQUEST_TIMEOUT = 10.0  # Set request timeout in seconds

async def call_api(endpoint: str, params: dict, method: str = 'post') -> dict:
    """
    Generic API call function
    
    Args:
        endpoint: API endpoint
        params: Request parameters
        method: Request method, 'get' or 'post'
    
    Returns:
        Dict: API response result, format: {"msg": "OK", "code": 0, "data": [...]}
    """
    # Build complete URL
    url = f"{API_URL}/{endpoint}"
    
    # Ensure all parameters are strings
    params = {k: str(v) for k, v in params.items()}
    
    # Add API key
    if API_KEY:
        params.update({"ak": API_KEY})
    
    try:
        async with httpx.AsyncClient() as client:
            headers = {"Content-Type": "application/json"}
            if method.lower() == 'get':
                response = await client.get(url, params=params, timeout=REQUEST_TIMEOUT)
            else:
                response = await client.post(url, json=params, headers=headers, timeout=REQUEST_TIMEOUT)
            
            response.raise_for_status()
            return response.json()
    
    except Exception as e:
        # Return unified error format when error occurs
        return {"msg": f"Request failed: {str(e)}", "code": -1, "data": []}

@mcp.tool()
async def set_cleaning(
    nickname: str = Field(description="Robot nickname, supports fuzzy matching", default=""),
    act: str = Field(description="Cleaning action, s-start cleaning, r-resume cleaning, p-pause cleaning, h-stop cleaning", default="s")
) -> dict:
    """
    Start cleaning the robot
    
    Args:
        nickname: Robot nickname, for device lookup
        act: Cleaning action s-start cleaning, r-resume cleaning, p-pause cleaning, h-stop cleaning
    Returns:
        Dict: Dictionary containing execution result
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Clean", "act": act})

@mcp.tool()
async def set_charging(
    nickname: str = Field(description="Robot nickname, for device lookup"),
    act: str = Field(description="Machine behavior, go-start start charging, stopGo end charging", default="go-start")
) -> dict:
    """
    Make the robot charge
    
    Args:
        nickname: Robot nickname, for device lookup
        act: Machine behavior, go-start start charging, stopGo end charging
    
    Returns:
        Dict: Dictionary containing execution result
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Charge", "act": act})

@mcp.tool()
async def get_work_state(
    nickname: str = Field(description="Robot nickname, for device lookup")
) -> dict:
    """
    Query robot work state
    
    Args:
        nickname: Robot nickname, for device lookup
    
    Returns:
        Dict: Dictionary containing robot work state
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "GetWorkState", "act": ""})

@mcp.tool()
async def get_device_list() -> dict:
    """
    Query robot list

    Returns:
        Dict: Dictionary containing robot nickname list
    """
    return await call_api(ENDPOINT_ROBOT_DEVICE_LIST, {}, method='get')

def main():
    """
    Main function, run MCP server in stdio mode
    """
    # Print startup information
    print("\n===== Start MCP robot control server (stdio mode) =====", file=sys.stderr)
    # Run MCP server in stdio mode
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()