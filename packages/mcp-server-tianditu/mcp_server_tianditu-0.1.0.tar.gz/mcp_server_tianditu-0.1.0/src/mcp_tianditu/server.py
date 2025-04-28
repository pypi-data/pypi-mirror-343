from mcp.server.fastmcp import FastMCP, Context
from mcp import types
from typing import Any
from .tdapi import api_addr_to_geocode, api_drive_plan, api_geocode_to_addr, api_search, api_trans_plan
 
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
                poiType	(int) poi类型 - 101:POI数据 102:公交站点
                distance (str): 距离（单位 m,km），1千米以下单位为米（m），1千米以上单位为千米（km）

    """
    return await api_search(3, keyWord=query, pointLonlat=f"{longitude},{latitude}", queryRadius=radius)

@mcp.tool('search_by_division')
async def search_by_division(
    query: str,
    division_code: str,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        行政规划区域内搜索
    
    Description:
        设置圆心和半径，检索圆形区域内的地点信息（常用于周边检索场景）。
    
    Args:
        query: 检索关键字, 可直接使用名称或类型, 如'query=天安门'
        division_code: 指定行政区的国标码（行政区划编码表）严格按照行政区划编码表中的（名称，gb码）;9位国标码，如：北京：156110000。
        
    Returns:
        周边查询结果数据字典，包含如下键：
            keyWord (str): 输入的检索关键字
            count (int): 检索结果总数
            resultType (int): 返回结果类型，取值1-5，对应不同的响应类型： 1（普通POI），2（统计），3（行政区)，4（建议词搜索），5（线路结果）
            pois(list[dict]): POI结果元素列表，每个元素包含如下键：
                name (str): Poi点名称
                address (str): Poi点地址
                lonlat (str): 经纬度 (gcj02ll)，格式为：经度,纬度
                phone (str): 联系电话
                poiType	(int) poi类型 - 101:POI数据 102:公交站点

    """
    return await api_search(12, keyWord=query, specify=division_code)

@mcp.tool('drive_plan')
async def drive_plan(
    from_latitude: float,
    from_longitude: float,
    to_latitude: float,
    to_longitude: float,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        驾车路线规划服务

    Description:
        根据输入起点、终点和途经点规划查询驾车路线。
    Args:
        from_latitude: 起点纬度 (gcj02ll)
        from_longitude: 起点经度 (gcj02ll)
        to_latitude: 终点纬度 (gcj02ll)
        to_longitude: 终点经度 (gcj02ll)
    Returns:
        驾车路线规划结果数据字典，包含如下键：
            orig (str): 起点经纬度
            mid (str): 途径点信息
            dest (str): 终点经纬度
            parameters (dict): 请求参数信息
                orig (str): 起点加密经纬度
                dest (str): 终点加密经纬度
                mid (str): 途径点加密经纬度集合
                key (str): 经纬度加密的 key 值
                width (int): 地图宽度
                height (int): 地图高度
                style (str): 导航路线类型
                version (str): 版本控制
                sort (str): 排序方式
            routes (dict): 详细路线分段信息
                count (int): 分段总数
                time (str): 查询时间
                items (list[dict]): 路线分段列表，每个元素包含如下键：
                    id (int): 分段ID
                    strguide (str): 每段线路文字描述
                    signage (str): "路牌"引导提示/高速路收费站出口信息
                    streetName (str): 当前路段名称
                    nextStreetName (str): 下一段道路名称
                    tollStatus (int): 道路收费信息(0=免费路段，1=收费路段，2=部分收费路段)
                    turnlatlon (str): 转折点经纬度
            simple (dict): 简化的路线分段信息
                items (list[dict]): 简化路线分段列表，每个元素包含如下键：
                    id (int): 分段ID
                    strguide (str): 每段线路文字描述
                    streetNames (str): 当前行驶路段名称（含多个路段）
                    lastStreetName (str): 最后一段道路名称
                    linkStreetName (str): 合并段之间衔接的道路名称
                    signage (str): "路牌"引导提示/高速路收费站出口信息
                    tollStatus (int): 道路收费信息(0=免费路段，1=收费路段，2=部分收费路段)
                    turnlatlon (str): 转折点经纬度
                    streetLatLon (str): 线路经纬度
                    streetDistance (int): 行驶总距离（单位：米）
                    segmentNumber (str): 合并后的号段，对应详细描述中的号段
            distance (float): 全长（单位：公里）
            duration (int): 行驶总时间（单位：秒）
            routelatlon (str): 线路经纬度字符串
            mapinfo (dict): 地图显示信息
                center (str): 全部结果同时显示的适宜中心经纬度
                scale (float): 全部结果同时显示的适宜缩放比例
    """
    return await api_drive_plan(f"{from_longitude},{from_latitude}", f"{to_longitude},{to_latitude}")

@mcp.tool('trans_plan')
async def trans_plan(
    from_latitude: float,
    from_longitude: float,
    to_latitude: float,
    to_longitude: float,
    ctx: Context
) -> dict[str, Any]:
    """
    Name:
        公交规划
    Description:
        根据输入起点和终点查询公交地铁规划线路
    Args:
        from_latitude: 起点纬度 (gcj02ll)
        from_longitude: 起点经度 (gcj02ll)
        to_latitude: 终点纬度 (gcj02ll)
        to_longitude: 终点经度 (gcj02ll)
    Returns:
        公交规划结果数据字典，包含如下键：
            resultCode (int): 返回结果状态码
                0	正常返回线路。
                1	找不到起点。
                2	找不到终点。
                3	规划线路失败。
                4	起终点距离200米以内，不规划线路，建议步行。
                5	起终点距离500米内，返回线路。
                6	输入参数错误。
            hasSubway (int): 所有返回线路中，是否有包含地铁的线路
            results (list[dict]): 公交规划结果列表，请求几种结果，返回几种结果，此数组中每个对象为一个请求类型的返回结果Json对象。
                lineType (int):	返回线路结果类型    第0位为1，较快捷；第1位为1，少换乘；第2位为1，少步行；第3位为1，不坐地铁
                lines (list[dict]): 公交结果线路(相对应类型的所有线路，最多5条)，数组中每个对象为一条由起点到终点的公交规划线路，每个元素包含如下键：
                    lineName (str)	单条公交规划结果所有线路名称，如:3路—4路—5路。
                    segments (list[dict])	单条公交结果中的各段线路信息，数组中的每个对象为此换乘线路中的分段线路：
                        segmentType (int)	线路类型1-4
                        stationStart (dict)	起站点内容
                            name (str)	站点名称
                            uuid (str)	站的id信息
                            lonlat (str)	站点坐标
                        stationEnd (dict)	终站点内容
                            name (str)	站点名称
                            uuid (str)	站的id信息
                            lonlat (str)	站点坐标
                        segmentLine	(dict) 线路内容
                            segmentName (str)	此段线路的线路名（不包含括号中的内容）
                            direction (str)	此段线路的完整线路名
                            linePoint (str)	此段线路的坐标
                            segmentDistance (str)	一条线路中每小段距离，如果此段是步行且距离小于20米，不返回此线段
                            segmentStationCount (str)	此段线路需要经过的站点数
                            segmentTime	(int) 此段线路需要的时间
    """
    return await api_trans_plan(f"{from_longitude},{from_latitude}", f"{to_longitude},{to_latitude}")

@mcp.resource('tdt://division-codes', name='行政区划编码表')
async def admin_code() -> str:
    """
    Name:
        行政区划编码表

    Description:
        中国行政区划编码，包括省市区。

    """
    with open('resources/AdminCode.txt', 'r', encoding='utf-8') as f:
        return f.read()

@mcp.resource('tdt://data-types', name='数据分类编码表')
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
