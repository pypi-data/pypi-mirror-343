from typing import Literal
from pydantic import Field
from mcp.server.fastmcp import FastMCP, Context

mcp = FastMCP("sample_mcp", port=3002)

# 必填：如果设置了 default 属性，则不是required
# 默认值建议同时写一份到tool说明里，因为它不会展示给用户。


# 用户输入问题：为客人张三预定酒店，要标间


@mcp.tool()
async def book_hotel(
        context: Context,
        guest_name: str = Field(description="客人姓名"),
        room_type: Literal["标间", "商务套房", "大床"] = Field(description="房间类型"),
        guests: int = Field(default=1, description="入住人数，默认1人"),
        num1: int = Field(default=12345, description="整数参数测试。默认12345"),
        str1: str = Field(default='', description="字符串参数测试"),
) -> str:
    """预定房间、预定酒店、住宿的工具（mock模拟）"""

    return f"你好 {guest_name} 你预定的是 {room_type} 一共 {guests} 位客人"

def run():
    mcp.run(transport="sse")


if __name__ == "__main__":
    mcp.run(transport='sse')