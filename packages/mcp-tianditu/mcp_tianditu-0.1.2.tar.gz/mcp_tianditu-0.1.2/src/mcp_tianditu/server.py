from mcp.server.fastmcp import FastMCP, Context
from typing import Any
from .tdapi import api_addr_to_geocode, api_geocode_to_addr, api_search
 
# 创建MCP服务器实例
mcp = FastMCP("mcp-server-tianditu")


@mcp.tool('addr_to_geocode')
async def addr_to_geocode(
    address: str,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        地理编码服务
        
    Description:
        将地址数据（如：北京市海淀区莲花池西路28号）转换为对应坐标点（经纬度）；地址解析仅限于国内。
        
    Args:
        address: 待解析的地址（如：北京市海淀区莲花池西路28号）地址结构越完整，解析精度越高。
        
    Returns:
        地址经纬度信息数据字典，包含如下键：
            lon (float): 经度 (gcj02ll)
            lat (float): 纬度 (gcj02ll)
            score (int): 置信度评分, 分值范围0-100, 分值越大精度越高
            keyWord (str): 输入的地址内容
    """
    geocode_data = await api_addr_to_geocode(address)
    return geocode_data['location'] if geocode_data else None

 
@mcp.tool('geocode_to_addr')
async def geocode_to_addr(
    latitude: float,
    longitude: float,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        逆地理编码服务
        
    Description:
        根据纬经度坐标, 获取对应位置的地址描述, 所在行政区划, 道路以及相关POI等信息
        
    Args:
        latitude: 纬度 (gcj02ll)
        longitude: 经度 (gcj02ll)
        
    Returns:
        地址经纬度信息数据字典，包含如下键：
            formatted_address (str): 格式化地址信息
            addressComponent (dict): 地址信息
                nation (str): 国家
                province (str): 省
                city (str): 市
                county (str): 区
                town (str): 镇/县
                road (str): 道路
            location (dict): 输入的经纬度信息
                lon (float): 经度 (gcj02ll)
                lat (float): 纬度 (gcj02ll)
    """
    addr_data = await api_geocode_to_addr(latitude, longitude)
    return addr_data['result'] if addr_data else None
 

@mcp.tool('search_by_redius')
async def search_by_redius(
    query: str,
    latitude: float,
    longitude: float,
    radius: int,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        周边检索服务
    
    Description:
        设置圆心和半径，检索圆形区域内的地点信息（常用于周边检索场景）。
    
    Args:
        query: 检索关键字, 可直接使用名称或类型, 如'query=天安门'
        latitude: 纬度 (gcj02ll)
        longitude: 经度 (gcj02ll)
        radius: 半径 (米)
        
    Returns:
        周边查询结果数据字典，包含如下键：
            keyWord (str): 输入的检索关键字
            count (int): 检索结果总数
            pois(list[dict]): POI结果元素列表，每个元素包含如下键：
                name (str): Poi点名称
                address (str): Poi点地址
                lonlat (str): 经纬度 (gcj02ll)，格式为：经度,纬度
                phone (str): 联系电话
                distance (str): 距离（单位 m,km），1千米以下单位为米（m），1千米以上单位为千米（km）

    """
    return await api_search(3, keyWord=query, pointLonlat=f"{longitude},{latitude}", queryRadius=radius)
 
@mcp.resource('tdt://admin-code', name='行政区划编码表')
async def admin_code() -> str:
    """
    Name:
        行政区划编码表

    Description:
        中国行政区划编码，包括省市区。

    """
    with open('resources/AdminCode.txt', 'r', encoding='utf-8') as f:
        return f.read()

@mcp.resource('tdt://data-type', name='数据分类编码表')
async def data_type() -> str:
    """
    Name:
        数据分类编码表

    Description:
        数据分类编码表

    """
    with open('resources/Type.txt', 'r', encoding='utf-8') as f:
        return f.read()
 
if __name__ == "__main__":
    mcp.run()