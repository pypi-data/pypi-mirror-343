import json
import os

import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel,Field
from typing import Dict, Any, Optional

#给服务器一个基本的名字
mcp = FastMCP("WeatherServer")
# server.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

"""
这只是一个简单的百度天气查询api，并未封装成mcp服务器的形式
所以未处理封装的话，无法运行

==处理如下==
1、显示封装input_schema
    --class类封装
2、返回结构从原始数据变为：封装状态码+数据+元数据
3、对于客户端请求的交互，由直接调用URL，变为通过MCP协议发现和调用工具
    --@mcp.tool()装饰器
"""
BAIDU_API_KEY = os.getenv("BAIDU_API_KEY")
BAIDU_API_URL = "http://api.map.baidu.com"

#自定义输入参数模型（自动生成input_schema）

@mcp.tool(
    name="make_baidu_get_weather_request",
    description="根据行政区划编码，获取指定行政区划的实时天气和预报信息",

)
async def make_baidu_get_weather_request(district_id :str)-> Dict[str, Any]:
    #注意下面三引号包括的部分，那是docstring，一种文档说明字符串
    #在mcp开发中，mcp.tool()装饰器会根据方法的参数定义自动生成input_schema
    #以及docstring中的description，作为tool的描述
    #所以在开发mcp_server的过程中，docstring要仔细写
    """查天气，向百度天气api发送请求,并返回原始数据

    Name:天气查询服务

    Description:用户可通过区县的行政区划编码或者经纬度（经度在前纬度在后，逗号分隔）来查询实时天气和预报信息

    Args:
        district_id (str): 区县的行政区划编码，6位（例如：222405）
    """
    print("==服务端== 实际接收到的参数:", district_id)
    print("==服务端== 参数类型:", type(district_id))
    #assert isinstance(params, dict), "参数必须是字典类型"

    #设置请求参数
    #更多参数信息请参考https://lbsyun.baidu.com/faq/api?title=webapi/weather/base
    params = {
        "district_id": district_id,
        "data_type": "all",
        "ak": BAIDU_API_KEY,
    }
    url = f"{BAIDU_API_URL}/weather/v1/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                url,params=params)

            response.raise_for_status()
            result = response.json()


            if result.get("status")!=0:
                error_msg = result.get("message", "unkown error")
                raise Exception(f"==Server== API response error: {error_msg}")

            return {
                "status": response.status_code,
                "data": response.json(),  #MCP规范建议封装原始数据
                "metadata":{"source":"baidu"}
            }
        except httpx.HTTPStatusError as e:
            raise ValueError(f"=Server= HTTP请求失败，状态码：{e.response.status_code}") from e
        except Exception as e:
            raise ValueError(f"=Server= 请求失败，错误信息：{e}") from e


@mcp.tool(
    name="map_geocode",
    description="将地址解析为对应的位置坐标。地址结构越完整，地址内容越准确，解析的坐标精度越高。"
)
async def map_geocode(
        address: str,
) -> dict:
    """
    Name:
        地理编码服务

    Description:
        将地址解析为对应的位置坐标。地址结构越完整，地址内容越准确，解析的坐标精度越高。

    Args:
        address: 待解析的地址。最多支持84个字节。可以输入两种样式的值，分别是：
        1、标准的结构化地址信息，如北京市海淀区上地十街十号【推荐，地址结构越完整，解析精度越高】
        2、支持“*路与*路交叉口”描述方式，如北一环路和阜阳路的交叉路口
        第二种方式并不总是有返回结果，只有当地址库中存在该地址描述时才有返回。

    """

    # 设置请求参数
    # 更多参数信息请参考:https://lbsyun.baidu.com/faq/api?title=webapi/guide/webservice-geocoding
    params = {
        "ak": BAIDU_API_KEY,
        "output": "json",
        "address": f"{address}",
        "from": "py_mcp"
    }
    url = f"{BAIDU_API_URL}/geocoding/v3/"

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params)
            response.raise_for_status()
            result = response.json()

            if result.get("status") != 0:
                error_msg = result.get("message", "unkown error")
                raise Exception(f"API response error: {error_msg}")

            return {
                "status": response.status_code,
                "data": response.json(),  # MCP规范建议封装原始数据
                "metadata": {"source": "baidu"}
            }
        except httpx.HTTPStatusError as e:
            raise ValueError(f"=Server= HTTP请求失败，状态码：{e.response.status_code}") from e
        except Exception as e:
            raise ValueError(f"=Server= 请求失败，错误信息：{e}") from e



"""
当我们指定transport=stdio来运行mcp服务器时，客户端必须要在启动时，
同时启动当前服务器脚本，否则无法顺利通信

因为stdio是一种本地进程间通信方式，需要服务器作为子进程运行，并通过标准输入输出
"""

import sys
def run_server():
    try:
        print("MCP服务器正在启动...")
        #以标准io方式运行mcp服务器
        #对应的，我们需要一个能够进行stdio的客户端才能顺利完成通信
        mcp.run(transport='stdio')
        print("MCP服务器已关闭")
    except KeyboardInterrupt:
        print("\n服务器正常终止")
        sys.exit(0)
    except Exception as e:
        print(f"服务器启动失败: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    import asyncio
    run_server()

if __name__ == "__main__":
    main()