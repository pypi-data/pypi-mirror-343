import os
from typing import Dict, Any
import requests
from mcp.server.fastmcp import FastMCP


def get_api_key() -> str:
    """从环境变量获取高德API Key"""
    api_key = os.getenv("AMAP_MAPS_API_KEY")
    if not api_key:
        raise ValueError("请设置AMAP_MAPS_API_KEY环境变量")
    return api_key


# 初始化MCP服务
mcp = FastMCP("amap-weather")


@mcp.tool()
def maps_weather(city: str) -> Dict[str, Any]:
    """
    查询指定城市天气
    参数: city - 城市名称或adcode
    """
    try:
        response = requests.get(
            "https://restapi.amap.com/v3/weather/weatherInfo",
            params={
                "key": get_api_key(),
                "city": city,
                "extensions": "base"  # 基础预报
            }
        )
        response.raise_for_status()
        data = response.json()

        if data["status"] != "1":
            return {"error": f"查询失败: {data.get('info', '未知错误')}"}

        return {
            "city": data["lives"][0]["city"],
            "weather": data["lives"][0]["weather"],
            "temperature": data["lives"][0]["temperature"],
            "humidity": data["lives"][0]["humidity"]
        }
    except Exception as e:
        return {"error": f"API请求异常: {str(e)}"}


def main():
    mcp.run(transport='stdio')


if __name__ == "__main__":
    main()