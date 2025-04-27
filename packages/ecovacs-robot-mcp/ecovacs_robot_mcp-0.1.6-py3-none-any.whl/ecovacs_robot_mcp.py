import os
import sys
import httpx
from pydantic import Field

from mcp.server.fastmcp import FastMCP

# 创建MCP服务器实例
mcp = FastMCP("RobotControl")

# API配置
API_KEY = os.getenv('ECO_API_KEY')  
API_URL = os.getenv('ECO_API_URL')



ENDPOINT_ROBOT_CTL = "robot/ctl"
ENDPOINT_ROBOT_DEVICE_LIST = "robot/deviceList"
REQUEST_TIMEOUT = 10.0  # 设置请求超时时间(秒)

async def call_api(endpoint: str, params: dict, method: str = 'post') -> dict:
    """
    通用API调用函数
    
    Args:
        endpoint: API端点
        params: 请求参数
        method: 请求方法，'get'或'post'
    
    Returns:
        Dict: API响应结果，格式为 {"msg": "OK", "code": 0, "data": [...]}
    """
    # 构建完整URL
    url = f"{API_URL}/{endpoint}"
    
    # 确保所有参数都是字符串
    params = {k: str(v) for k, v in params.items()}
    
    # 添加API密钥
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
        # 发生错误时返回统一的错误格式
        return {"msg": f"请求失败: {str(e)}", "code": -1, "data": []}

@mcp.tool()
async def set_cleaning(
    nickname: str = Field(description="机器人的昵称，支持模糊匹配", default=""),
    act: str = Field(description="清扫行为, s-开始清扫, r-恢复清扫, p-暂停清扫, h-停止清扫", default="s")
) -> dict:
    """
    启动扫地机器人清扫
    
    Args:
        nickname: 机器人昵称，用于查找设备
        act: 清扫行为 s-开始清扫, r-恢复清扫, p-暂停清扫, h-停止清扫
    Returns:
        Dict: 包含执行结果的字典
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Clean", "act": act})

@mcp.tool()
async def set_charging(
    nickname: str = Field(description="机器人的昵称，用于查找设备"),
    act: str = Field(description="机器行为, go-start 开始回充, stopGo 结束回充", default="go-start")
) -> dict:
    """
    让机器人回充
    
    Args:
        nickname: 机器人昵称，用于查找设备
        act: 机器行为, go-start 开始回充, stopGo 结束回充
    
    Returns:
        Dict: 包含执行结果的字典
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "Charge", "act": act})

@mcp.tool()
async def get_work_state(
    nickname: str = Field(description="机器人的昵称，用于查找设备")
) -> dict:
    """
    查询机器工作状态
    
    Args:
        nickname: 机器人昵称，用于查找设备
    
    Returns:
        Dict: 包含机器人工作状态的字典
    """
    return await call_api(ENDPOINT_ROBOT_CTL, {"nickName": nickname, "cmd": "GetWorkState", "act": ""})

@mcp.tool()
async def get_device_list() -> dict:
    """
    查询机器列表

    Returns:
        Dict: 包含机器人昵称列表的字典
    """
    return await call_api(ENDPOINT_ROBOT_DEVICE_LIST, {}, method='get')

def main():
    """
    主函数，使用stdio模式运行MCP服务器
    """
    # 打印启动信息
    print("\n===== 启动MCP机器人控制服务器（stdio模式） =====", file=sys.stderr)
    # 使用stdio模式运行MCP服务器
    mcp.run(transport='stdio')

if __name__ == "__main__":
    main()