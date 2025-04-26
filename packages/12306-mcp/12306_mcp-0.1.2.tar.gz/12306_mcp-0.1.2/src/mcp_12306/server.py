import json
from enum import Enum

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, ImageContent, EmbeddedResource
from mcp.shared.exceptions import McpError
from pydantic import BaseModel
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Sequence

class TrainTools(str, Enum):
    SEARCH_TICKETS = "search_tickets"  # 火车票搜索工具

class TicketSearchInput(BaseModel):
    date: str  # 日期，格式为 YYYY-MM-DD
    from_city: str  # 出发城市
    to_city: str  # 到达城市

class TicketSearchResult(BaseModel):
    content: List[Dict]  # 搜索结果列表

class TrainTicketServer:
    def search_tickets(self, date_str: str, from_city: str, to_city: str) -> List[Dict]:
        # 保持原有 ChinaRailway 的搜索逻辑
        try:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            now = datetime.now().date()
            if now > date_obj or (now + timedelta(days=15)) < date_obj:
                raise McpError('日期需为0~15天内')
            from_cities = self.find_cities(from_city)  # 假设已加载数据
            if not from_cities:
                raise McpError(f'没有找到出发城市: {from_city}')
            to_cities = self.find_cities(to_city)
            if not to_cities:
                raise McpError(f'没有找到到达城市: {to_city}')
            from_city_code = from_cities[0]
            to_city_code = to_cities[0]
            session = requests.Session()
            session.get('https://kyfw.12306.cn/')
            cookies = '; '.join([f"{cookie.name}={cookie.value}" for cookie in session.cookies])
            api_url = (
                f'https://kyfw.12306.cn/otn/leftTicket/queryG?'
                f'leftTicketDTO.train_date={date_obj.strftime("%Y-%m-%d")}'
                f'&leftTicketDTO.from_station={from_city_code}'
                f'&leftTicketDTO.to_station={to_city_code}'
                f'&purpose_codes=ADULT'
            )
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
                'Cookie': cookies
            }
            response = session.get(api_url, headers=headers)
            response.raise_for_status()
            data = response.json()
            if not data or not data.get('status'):
                raise McpError('获取余票数据失败')
            result = data.get('data', {}).get('result', [])
            map_data = data.get('data', {}).get('map', {})
            return self.parse_train_info(result, map_data)  # 返回解析后的数据
        except Exception as e:
            raise McpError(str(e))

    # 其他 ChinaRailway 方法保持不变，例如 get_station_data, find_cities, parse_train_info 等
    # 这里简化了，假设这些方法已定义在 TrainTicketServer 中

async def serve() -> None:
    server = Server("mcp-train-ticket")  # 创建服务器实例
    train_server = TrainTicketServer()  # 实例化火车票服务器

    print("----init---")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        """列出可用火车票工具。"""
        return [
            Tool(
                name=TrainTools.SEARCH_TICKETS.value,
                description="搜索火车票信息",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "date": {"type": "string", "description": "日期，格式为 YYYY-MM-DD"},
                        "from_city": {"type": "string", "description": "出发城市"},
                        "to_city": {"type": "string", "description": "到达城市"},
                    },
                    "required": ["date", "from_city", "to_city"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict) -> Sequence[TextContent | ImageContent | EmbeddedResource]:
        """处理火车票工具调用。"""
        try:
            match name:
                case TrainTools.SEARCH_TICKETS.value:
                    if not all(k in arguments for k in ["date", "from_city", "to_city"]):
                        raise ValueError("缺少必要参数：date, from_city, to_city")
                    result = train_server.search_tickets(
                        arguments["date"],
                        arguments["from_city"],
                        arguments["to_city"],
                    )
                    return [
                        TextContent(type="text", text=json.dumps(result, indent=2))  # 返回 JSON 格式的结果
                    ]
                case _:
                    raise ValueError(f"未知工具: {name}")
        except Exception as e:
            raise McpError(f"处理火车票查询错误: {str(e)}")

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options)

# 运行服务器
if __name__ == "__main__":
    import asyncio
    asyncio.run(serve())  # 异步运行服务器