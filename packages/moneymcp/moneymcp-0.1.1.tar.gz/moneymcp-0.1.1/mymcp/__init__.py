"""
MYMCP - Financial Analysis MCP Server
A comprehensive financial analysis tool that provides APIs for market data
"""

__version__ = "0.1.1"

# 导出重要的类型
from mymcp.types import Sector, TopType, SearchType

# 导出 MCP 对象供开发者使用
from mymcp.server import mcp 
