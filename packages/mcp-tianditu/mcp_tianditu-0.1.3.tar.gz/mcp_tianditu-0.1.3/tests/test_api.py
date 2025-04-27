import asyncio
import tdapi
import json

#tdapi.config_api_key(YOUR_API_KEY)

if __name__ == '__main__':
    # 获取地址经纬度
    result = asyncio.run(tdapi.api_addr_to_geocode('北京天安门广场'))

    # 获取经纬度对应地址
    result = asyncio.run(tdapi.api_geocode_to_addr(30.301765, 120.094235))

    # 行政规划区域搜索示例
    result = asyncio.run(tdapi.api_search(12, keyWord='商厦', specify="156110108", start=0, count=5))
    # 视野内搜索示例
    result = asyncio.run(tdapi.api_search(2, keyWord='医院', level=12, mapBound='116.02524,39.83833,116.65592,39.99185', show=2, start=0, count=10))
    # 周边搜索示例
    result = asyncio.run(tdapi.api_search(3, keyWord='商场', level=12, queryRadius=5000, pointLonlat='120.094235,30.301765', start=0, count=10))
    # 多边形搜索示例
    result = asyncio.run(tdapi.api_search(10, keyWord='学校', polygon="118.93232636500011,27.423305726000024,118.93146426300007,27.30976105800005,118.80356153600007,27.311829507000027,118.80469010700006,27.311829508000073,118.8046900920001,27.32381604300008,118.77984777400002,27.32381601800006,118.77984779100007,27.312213007000025,118.76792266100006,27.31240586100006,118.76680145600005,27.429347074000077,118.93232636500011,27.423305726000024", start=0, count=10))
    # 数据分类搜索示例
    result = asyncio.run(tdapi.api_search(13, specify="156110000", start=0, count=5, dataTypes='法院,公园'))
    # 普通搜索示例
    result = asyncio.run(tdapi.api_search(1, keyWord='北京大学', level=12, mapBound='116.02524,39.83833,116.65592,39.99185', start=0, count=10))
    # 统计搜索示例: 测试不通过
    result = asyncio.run(tdapi.api_search(14, keyWord='商厦', specify='156110108'))

    # 驾车导航示例
    result = asyncio.run(tdapi.api_drive_plan('116.35506,39.92277', '116.39751,39.90854', type=0))

    # 公交导航示例
    result = asyncio.run(tdapi.api_trans_plan('116.427562,39.939677', '116.349329,39.939132'))
    print(json.dumps(result, ensure_ascii=False))