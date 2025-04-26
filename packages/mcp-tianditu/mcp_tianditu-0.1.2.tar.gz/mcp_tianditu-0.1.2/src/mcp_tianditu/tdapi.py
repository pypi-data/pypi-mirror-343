import os
from typing import Callable
import httpx
import json
import copy # 添加 copy 模块导入
from .util import xml_to_dict

'''

获取环境变量中的API密钥, 用于调用天地图API
环境变量名为: TIANDITU_API_KEY, 在客户端侧通过配置文件进行设置传入
获取方式请参考: https://console.tianditu.gov.cn/api/key

'''

_api_key = os.getenv('TIANDITU_API_KEY')
_api_url = "http://api.tianditu.gov.cn"

async def api_addr_to_geocode( address: str) -> dict:
    """
    Name:
        地理编码服务
        
    Description:
        将地址解析为对应的位置坐标。地址结构越完整，地址内容越准确，解析的坐标精度越高。
        
    Args:
        address: 待解析的地址，如北京市海淀区上地十街十号【推荐，地址结构越完整，解析精度越高】
    
    """
    return await _tdapi_invoke("/geocoder", dict(ds=json.dumps(dict(keyWord=address), ensure_ascii=False)))

async def api_geocode_to_addr( latitude: float, longitude: float) -> dict:
    """
    Name:
        逆地理编码服务
        
    Description:
        根据纬经度坐标, 获取对应位置的地址描述, 所在行政区划, 道路以及相关POI等信息
        
    Args:
        latitude: 纬度 (gcj02ll)
        longitude: 经度 (gcj02ll)
        
    """
    return await _tdapi_invoke("/geocoder", dict(postStr=json.dumps(dict(lon=longitude, lat=latitude), ensure_ascii=False), type='geocode'))

async def api_search(query_type: int, **search_params) -> dict:
    """
    Name:
        地点检索服务 (Search API V2.0)

    Description:
        根据关键字、周边、范围、行政区划等条件检索POI信息。
        详细参数请参考: http://lbs.tianditu.gov.cn/server/search2.html

    Args:
        search_params: 检索参数字典，包含以下可能的键:
            keyWord (str): 搜索关键字，如"银行"。
            queryType (int): 查询类型 (1: 普通查询, 2: 视野内查询, 3: 周边搜索, 7: 地名搜索, 10: 多边形搜索, 12: 行政区划查询, 13: 分类搜索)。
            dataTypes (str): 分类名或分类编码列表，元素间用","隔开（英文逗号）。
            specify(str): 指定行政区的国标码（行政区划编码表）严格按照行政区划编码表中的（名称，gb码）;9位国标码，如：北京：156110000。
            mapBound (str): 视野范围，格式为"minx,miny,naxx,maxy"，如"116.35,39.9,116.45,40.0"。
            level (int): 搜索级别，1-18级。
            queryRadius (str): 查询半径，单位为米。
            pointLonlat (str): 中心点坐标，格式为"lon,lat"，如"116.404,39.915"。
            polygon (str): 多边形范围数据(经纬度坐标对)"lon1,lat1,lon2,lat2,lon3,lat3;..."，如"116.35,39.9,116.45,39.9,116.45,40.0,116.35,40.0"。
            start (int): 起始记录数，默认为0。
            count (int): 返回记录数量，默认为10，最大为100。
            show (int): 是否返回POI详细信息，1: 返回基本信息, 1: 返回详细信息。
    """
    # Search API 需要将参数封装在 postStr 或 getStr 中
    # 这里我们统一使用 postStr (虽然是 GET 请求，但文档示例如此)
    # 确保 keyWord 使用 UTF-8 编码
    return await _tdapi_invoke("/v2/search", dict(postStr=json.dumps(dict(queryType=query_type, **search_params), ensure_ascii=False), type='query'),
        resp_checker=lambda resp: resp.get("status", dict()).get('infocode') == 1000)

async def api_drive_plan(origin: str, destination: str, **route_params) -> dict:
    """
    Name:
        驾车路线规划服务

    Description:
        根据起点、终点坐标规划驾车出行路线。
        详细参数请参考: http://lbs.tianditu.gov.cn/server/drive.html

    Args:
        origin (str): 起点坐标，格式为"经度,纬度"，如"116.307901,40.057044"。
        destination (str): 终点坐标，格式为"经度,纬度"，如"116.407401,39.904211"。
        route_params: 其他可选的路线规划参数字典，包含以下可能的键:
            type (str): 路线类型 (0: 最快路线, 1: 最短路线, 2: 避开高速, 3: 不行)。默认为0。
            midpoints (str): 途经点坐标，格式为"经度,纬度;经度,纬度;..."，最多支持10个途经点。
    """
    # 驾车规划 API 需要将参数封装在 postStr 中
    midpoints = route_params.get("midpoints")
    style = route_params.get("type")
    params = dict(orig=origin, dest=destination)
    if midpoints:
        params["mid"] = midpoints
    if style:
        params["style"] = style
    return await _tdapi_invoke("/drive", dict(postStr=json.dumps(params, ensure_ascii=False), type='search'))

async def api_trans_plan(origin: str, destination: str, line_type='1') -> dict:
    """
    Name:
        公交路线规划服务
    Description:
        根据起点、终点坐标规划公交出行路线。
        详细参数请参考: http://lbs.tianditu.gov.cn/server/bus.html
    """
    params = dict(startposition=origin, endposition=destination, linetype=line_type)
    return await _tdapi_invoke("/transit", dict(postStr=json.dumps(params, ensure_ascii=False), type='busline'),
        resp_checker=lambda resp: resp.get("resultCode") == 0)

def config_api_key(ak: str) -> None:
    """
    Name:
        设置API密钥
    Description:
        设置API密钥，用于调用地图API
    Args:
        ak: API密钥
    """
    global _api_key
    _api_key = ak

async def _tdapi_invoke(api_uri: str, params: dict, resp_checker: Callable[dict, bool] = None) -> dict:
    """
    Name:
        地图API调用

    Description:
        调用地图API接口，获取返回结果

    Args:
        api_uri: API接口地址
        params: API接口参数
    """
    try:
        # 获取API密钥
        if not _api_key:
            raise Exception("Can not found API key.")
                    # 调用百度API
        url = f"{_api_url}{api_uri}"
        
        params = dict(**(params or dict()), tk=_api_key)
        
        async with httpx.AsyncClient() as client:
            response = await client.get(url, params=params)
            response.raise_for_status()
            try:
                result = response.json()
            except json.JSONDecodeError:
                # 如果不是JSON格式，尝试解析为文本
                result = response.text
                if result and result.strip().startswith('<'):
                    return xml_to_dict(result)
                else:
                    raise Exception(f"Failed to parse reponse: {result}")
 
        resp_checker = resp_checker or _default_resp_checker
        if not resp_checker(result):
            error_msg = result.get("message", result)
            raise Exception(f"API response error: {error_msg}")
 
        return result
 
    except httpx.HTTPError as e:
        raise Exception(f"HTTP request failed: {str(e)}") from e
    except KeyError as e:
        raise Exception(f"Failed to parse reponse: {str(e)}") from e

def _default_resp_checker(resp: dict) -> bool:
    return resp.get("status") == "0"

#========================================================================
def _filter_result(data) -> dict:
    '''
    过滤路径规划结果，用于剔除冗余字段信息，保证输出给模型的数据更简洁，避免长距离路径规划场景下chat中断
    '''
    
    # 创建输入数据的深拷贝以避免修改原始数据
    processed_data = copy.deepcopy(data)
    
    # 检查是否存在'result'键
    if 'result' in processed_data:
        result = processed_data['result']
        
        # 检查'result'中是否存在'routes'键
        if 'routes' in result:
            for route in result['routes']:
                # 检查每个'route'中是否存在'steps'键
                if 'steps' in route:
                    new_steps = []
                    for step in route['steps']:
                        # 提取'instruction'字段，若不存在则设为空字符串
                        new_step = {
                            'distance': step.get('distance', ''),
                            'duration': step.get('duration', ''),
                            'instruction': step.get('instruction', '')
                        }
                        new_steps.append(new_step)
                    # 替换原steps为仅含instruction的新列表
                    route['steps'] = new_steps
    
    return processed_data