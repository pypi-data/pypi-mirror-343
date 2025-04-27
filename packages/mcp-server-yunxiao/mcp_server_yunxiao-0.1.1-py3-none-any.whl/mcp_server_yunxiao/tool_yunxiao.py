"""
云霄服务工具模块
"""
import json
from typing import Any, Dict, List, Optional
from datetime import datetime
from .client import get_yunxiao_client

def _call_api(path: str, params: dict) -> str:
    """调用云霄API并返回JSON格式的响应

    Args:
        path: API路径
        params: 请求参数

    Returns:
        str: API响应的JSON字符串
    """
    print(f"调用API: {path}, 参数: {params}")
    response = get_yunxiao_client().post(path, params)
    return json.dumps(response, ensure_ascii=False)

def describe_sale_policies(
    page_number: int = 1,
    page_size: int = 200,
    customhouse: list[str] = None,
    region_alias: list[str] = None,
    region: list[str] = None,
    zone_id: list[int] = None,
    zone: list[str] = None,
    instance_family: list[str] = None,
    instance_category: list[str] = None,
    instance_family_state: list[str] = None,
    instance_family_supply_state: list[str] = None,
    zone_state: list[str] = None,
    stock_state: list[str] = None,
    sales_policy: list[int] = None
) -> str:
    """查询售卖推荐数据

    Args:
        page_number: 页码，默认1
        page_size: 每页数量，默认20，最大100
        customhouse: 境内外列表
        region_alias: 地域别名列表
        region: 地域列表
        zone_id: 可用区ID列表
        zone: 可用区列表
        instance_family: 实例族列表
        instance_category: 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
        instance_family_state: 实例族状态列表
        instance_family_supply_state: 实例族供货状态列表，可选值：LTS/EOL
        zone_state: 可用区状态列表
        stock_state: 库存状态列表
        sales_policy: 售卖建议列表

    Returns:
        str: 售卖策略和库存信息的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size
    }
    
    if customhouse:
        params["customhouse"] = customhouse
    if region_alias:
        params["regionAlias"] = region_alias
    if region:
        params["region"] = region
    if zone_id:
        params["zoneId"] = zone_id
    if zone:
        params["zone"] = zone
    if instance_family:
        params["instanceFamily"] = instance_family
    if instance_category:
        params["instanceCategory"] = instance_category
    if instance_family_state:
        params["instanceFamilyState"] = instance_family_state
    if instance_family_supply_state:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if zone_state:
        params["zoneState"] = zone_state
    if stock_state:
        params["stockState"] = stock_state
    if sales_policy:
        params["salesPolicy"] = sales_policy
        
    response = get_yunxiao_client().post("/compass/sales-policy/list", params)
    
    # 处理响应数据
    result = {}
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "境内外": item["customhouse"],
            "可用区名称": item["zoneName"],
            "实例族": item["instanceFamily"],
            "售卖状态": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["instanceFamilyState"], item["instanceFamilyState"]),
            "供货策略": {
                "LTS": "持续供应",
                "EOL": "停止供应"
            }.get(item["instanceFamilySupplyState"], item["instanceFamilySupplyState"]),
            "可用区售卖策略": {
                "PRINCIPAL": "主力",
                "SECONDARY": "非主力"
            }.get(item["zoneState"], item["zoneState"]),
            "实例分类": item["instanceCategory"],
            "库存情况": {
                "WithStock": "库存充足",
                "ClosedWithStock": "库存紧张",
                "WithoutStock": "售罄"
            }.get(item["stockState"], item["stockState"]),
            "售卖策略": {
                0: "未知",
                1: "推荐购买",
                2: "正常购买",
                3: "即将售罄",
                4: "联系购买",
                5: "无法购买",
                6: "请预约"
            }.get(item["salesPolicy"], "未知"),
            "库存/核": f"{item.get('stock', 0)}核",
            "十六核以上库存核": f"{item.get('stock16c', 0)}核",
            "数据更新时间": item["updateTime"]
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
        
    return json.dumps(result, ensure_ascii=False)

def describe_inventory(
    region: str,
    zone: Optional[str] = None,
    instance_family: Optional[str] = None,
    instance_type: Optional[str] = None,
    offset: int = 0,
    limit: int = 100
) -> str:
    """查询库存数据
    
    Args:
        region: 地域
        zone: 可用区
        instance_family: 实例族
        instance_type: 实例类型
        offset: 偏移量
        limit: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    client = get_yunxiao_client()
    
    request_body = {
        "chargeType": [2],
        "pool": ["public"],
        "offset": offset,
        "limit": limit,
        "region": region
    }
    
    if zone:
        request_body["zone"] = [zone]
    if instance_family:
        request_body["instanceFamily"] = instance_family
    if instance_type:
        request_body["instanceType"] = [instance_type]
        
    response = client.post("/beacon/ceres/instance-sales-config/list", request_body)
    
    # 处理响应数据
    result = {}
    if "data" in response:
        data = response["data"]
        result["data"] = [{
            "可用区": item["zone"],
            "实例族": item["instanceFamily"],
            "实例类型": item["instanceType"],
            "实例CPU数": f"{item['cpu']}核",
            "实例内存": item["mem"],
            "实例GPU数": item["gpu"],
            "库存": f"{item['inventory']}核",
            "数据更新时间": datetime.fromtimestamp(item["updateTime"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
        } for item in data["data"]]
        result["totalCount"] = data["totalCount"]
        
    return json.dumps(result, ensure_ascii=False)

def get_user_owned_grid(
        app_id: int, 
        region: Optional[List[str]] = None
) -> str:
    """获取用户拥有的网格列表
    
    Args:
        app_id: APPID
        region: 地域列表
        
    Returns:
        str: 网格列表的JSON字符串
    """
    params = {
        "appId": app_id,
        "region": region
    }
    return _call_api("/data360/user360/grid", params)

def get_user_owned_instances(
        app_id: int, 
        region: Optional[List[str]] = None
) -> str:
    """获取用户拥有的实例列表
    
    Args:
        app_id: APPID
        region: 地域列表
        
    Returns:
        str: 实例列表的JSON字符串
    """
    params = {
        "appId": app_id,
        "region": region
    }
    return _call_api("/data360/user360/instance", params)

def get_customer_account_info(customer_ids: List[str]) -> str:
    """获取客户账号信息
    
    Args:
        customer_ids: 客户ID列表
        
    Returns:
        str: 客户账号信息的JSON字符串
    """
    return _call_api("/data360/customer/batch-query-account-info", customer_ids)

def query_quota(
    region: str,
    limit: int = 100,
    offset: int = 0,
    product_code: str = "cvm-instance",
    region_alias: Optional[str] = None,
    zone_id: Optional[List[int]] = None,
    app_id: Optional[List[str]] = None,
    pay_mode: Optional[List[str]] = None,
    instance_type: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None
) -> str:
    """查询配额信息
    
    Args:
        region: 地域
        product_code: 产品码
        limit: 页长度，默认20
        offset: 偏移量，默认0
        region_alias: 地域别名
        zone_id: 可用区ID列表
        app_id: 用户AppID列表
        pay_mode: 计费模式列表
        instance_type: 实例类型列表
        instance_family: 机型族列表
        
    Returns:
        str: 配额信息的JSON字符串
    """
    params = {
        "region": region,
        "productCode": product_code,
        "limit": limit,
        "offset": offset
    }
    
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if zone_id is not None:
        params["zoneId"] = zone_id
    if app_id is not None:
        params["appId"] = app_id
    if pay_mode is not None:
        params["payMode"] = pay_mode
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
        
    return _call_api("/data360/quota/query", params)

def query_instance_families(
    instance_family: Optional[str] = None,
    states: Optional[List[str]] = None,
    supply_states: Optional[List[str]] = None,
    instance_categories: Optional[List[str]] = None,
    type_names: Optional[List[str]] = None,
    instance_class: Optional[str] = None,
    page_number: int = 1,
    page_size: int = 20
) -> str:
    """查询机型族信息
    
    Args:
        instance_family: 实例族名称
        states: 实例族状态列表
        supply_states: 实例族供货状态列表
        instance_categories: 实例分类列表
        type_names: 类型名称列表
        instance_class: 实例类型分类
        page_number: 页码
        page_size: 每页数量
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size,
        "display": True
    }
    
    if instance_family:
        params["instanceFamily"] = instance_family
    if states:
        params["state"] = states
    if supply_states:
        params["supplyState"] = supply_states
    if instance_categories:
        params["instanceCategory"] = instance_categories
    if type_names:
        params["typeName"] = type_names
    if instance_class:
        params["instanceClass"] = instance_class
        
    return _call_api("/data360/instance-family", params)

def get_instance_count(
    region: str,
    next_token: str = "",
    limit: int = 20,
    app_ids: Optional[List[int]] = None,
    uins: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询实例数量
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    
    if app_ids:
        params["appId"] = app_ids
    if uins:
        params["uin"] = uins
    if instance_types:
        params["instanceType"] = instance_types
    if instance_families:
        params["instanceFamily"] = instance_families
        
    return _call_api("/data360/instance/count", params)

def query_instances(
    region: str,
    next_token: str = "",
    limit: int = 20,
    app_ids: Optional[List[int]] = None,
    uins: Optional[List[str]] = None,
    instance_types: Optional[List[str]] = None,
    instance_families: Optional[List[str]] = None
) -> str:
    """查询实例列表
    
    Args:
        region: 地域
        next_token: 分页token
        limit: 每页数量
        app_ids: AppID列表
        uins: UIN列表
        instance_types: 实例类型列表
        instance_families: 实例族列表
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "hasTotalCount": True,
        "nextToken": next_token,
        "limit": limit,
        "region": region
    }
    
    if app_ids:
        params["appId"] = app_ids
    if uins:
        params["uin"] = uins
    if instance_types:
        params["instanceType"] = instance_types
    if instance_families:
        params["instanceFamily"] = instance_families
        
    return _call_api("/data360/instance", params)

def get_instance_details(
    region: str,
    instance_id: Optional[List[str]]
) -> str:
    """查询实例详情
    
    Args:
        region: 地域
        instance_id: 实例ID
        
    Returns:
        查询结果的JSON字符串
    """
    params = {
        "instanceId": instance_id,
        "region": region
    }
        
    return _call_api("/data360/instance/detail", params)

def describe_operation_metrics(
    stat_time: str = None,
    zone: list[str] = None,
    zone_id: list[int] = None,
    device_class: list[str] = None,
    instance_family: list[str] = None,
    customhouse: list[str] = None,
    region_alias: list[str] = None,
    region: list[str] = None,
    instance_category: list[str] = None,
    instance_family_state: list[str] = None,
    instance_family_supply_state: list[str] = None,
    zone_state: list[str] = None
) -> str:
    """查询运营指标数据

    Args:
        stat_time: 日期，格式：YYYY-MM-DD
        zone: 可用区列表
        zone_id: 可用区ID列表
        device_class: 设备类型列表
        instance_family: 实例族列表
        customhouse: 境内外列表
        region_alias: 地域别名列表
        region: 地域列表
        instance_category: 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
        instance_family_state: 实例族状态列表
        instance_family_supply_state: 实例族供货状态列表，可选值：LTS/EOL
        zone_state: 可用区状态列表

    Returns:
        str: 运营指标数据的JSON字符串
    """
    params = {}
    
    if stat_time:
        params["statTime"] = stat_time
    if zone:
        params["zone"] = zone
    if zone_id:
        params["zoneId"] = zone_id
    if device_class:
        params["deviceClass"] = device_class
    if instance_family:
        params["instanceFamily"] = instance_family
    if customhouse:
        params["customhouse"] = customhouse
    if region_alias:
        params["regionAlias"] = region_alias
    if region:
        params["region"] = region
    if instance_category:
        params["instanceCategory"] = instance_category
    if instance_family_state:
        params["instanceFamilyState"] = instance_family_state
    if instance_family_supply_state:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if zone_state:
        params["zoneState"] = zone_state
        
    return _call_api("/compass/operation-metrics/list-all", params)

def describe_stock_metrics(
    stat_time: str,
    zone: Optional[List[str]] = None,
    zone_id: Optional[List[int]] = None,
    device_class: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None,
    customhouse: Optional[List[str]] = None,
    region_alias: Optional[List[str]] = None,
    region: Optional[List[str]] = None,
    instance_category: Optional[List[str]] = None,
    instance_family_state: Optional[List[str]] = None,
    instance_family_supply_state: Optional[List[str]] = None,
    zone_state: Optional[List[str]] = None
) -> str:
    """查询库存观测指标和库存水位
    
    Args:
        stat_time: 统计时间，格式：YYYY-MM-DD
        zone: 可用区列表
        zone_id: 可用区ID列表
        device_class: 设备类型列表
        instance_family: 实例族列表
        customhouse: 境内外列表
        region_alias: 地域别名列表
        region: 地域列表
        instance_category: 实例分组列表，可选值：CVM/GPU/FPGA/BARE_METAL
        instance_family_state: 实例族状态列表
        instance_family_supply_state: 实例族供货状态列表，可选值：LTS/EOL
        zone_state: 可用区状态列表
        
    Returns:
        str: 库存观测指标和库存水位的JSON字符串
    """
    params = {
        "statTime": stat_time
    }
    
    if zone:
        params["zone"] = zone
    if zone_id:
        params["zoneId"] = zone_id
    if device_class:
        params["deviceClass"] = device_class
    if instance_family:
        params["instanceFamily"] = instance_family
    if customhouse:
        params["customhouse"] = customhouse
    if region_alias:
        params["regionAlias"] = region_alias
    if region:
        params["region"] = region
    if instance_category:
        params["instanceCategory"] = instance_category
    if instance_family_state:
        params["instanceFamilyState"] = instance_family_state
    if instance_family_supply_state:
        params["instanceFamilySupplyState"] = instance_family_supply_state
    if zone_state:
        params["zoneState"] = zone_state
        
    return _call_api("/compass/operation-metrics/list-all", params)

def describe_stock_metrics_history(
    customhouse: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None,
    region: Optional[List[str]] = None,
    zone: Optional[List[str]] = None,
    topic_id: Optional[str] = None,
    limit: Optional[int] = None,
    next_token: Optional[str] = None
) -> str:
    """查询库存观测指标和库存水位历史数据
    
    Args:
        customhouse: 境内外列表
        instance_family: 实例族列表
        region: 地域列表
        zone: 可用区列表
        topic_id: 主题ID
        limit: 每页数量
        next_token: 分页标记
        
    Returns:
        str: 库存观测指标和库存水位历史数据的JSON字符串
    """
    params = {}
    
    if customhouse:
        params["customhouse"] = customhouse
    if instance_family:
        params["instanceFamily"] = instance_family
    if region:
        params["region"] = region
    if zone:
        params["zone"] = zone
    if topic_id:
        params["topicId"] = topic_id
    if limit:
        params["limit"] = limit
    if next_token:
        params["nextToken"] = next_token
        
    return _call_api("/compass/operation-metrics/history", params)

def describe_buy_flow_promise_info(
    page_number: int = 1,
    page_size: int = 20,
    region: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None
) -> str:
    """查询预计交付信息
    
    Args:
        page_number: 页码，默认1
        page_size: 每页数量，默认20
        region: 地域列表
        instance_family: 实例族列表
        
    Returns:
        str: 预计交付信息的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size
    }
    
    if region:
        params["region"] = region
    if instance_family:
        params["instanceFamily"] = instance_family
        
    return _call_api("/compass/buy-flow/promise-info", params)

def describe_cvm_type_config(
    has_total_count: bool = True,
    limit: Optional[int] = None,
    next_token: Optional[str] = None,
    region: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None
) -> str:
    """多地域批量查询库存
    
    Args:
        has_total_count: 是否返回总数，默认True
        limit: 每页数量
        next_token: 分页标记
        region: 地域列表
        instance_family: 实例族列表
        
    Returns:
        str: 库存信息的JSON字符串
    """
    params = {
        "hasTotalCount": has_total_count
    }
    
    if limit:
        params["limit"] = limit
    if next_token:
        params["nextToken"] = next_token
    if region:
        params["region"] = region
    if instance_family:
        params["instanceFamily"] = instance_family
        
    return _call_api("/compass/cvm-type-config/list", params)

def describe_reservation_forms(
    page_number: int = 1,
    page_size: int = 20,
    instance_family: Optional[List[str]] = [],
    instance_type: Optional[List[str]] = [],
    order_id: Optional[str] = None,
    order_created: Optional[bool] = None,
    creator: Optional[str] = None,
    app_id: Optional[str] = None,
    app_name: Optional[str] = None,
    uin: Optional[str] = None,
    region: Optional[str] = None,
    zone: Optional[List[str]] = None,
    status: Optional[List[str]] = None,
    instance_category: Optional[List[str]] = None
) -> str:
    """查询资源预扣单
    
    Args:
        page_number: 页码，默认1
        page_size: 每页数量，默认20，最大100
        instance_family: 机型族列表，可选
        instance_type: 机型列表，可选
        order_id: 关联预约单ID
        order_created: 是否预约单创建
        creator: 创建者
        app_id: 客户AppID
        app_name: 客户名称
        uin: UIN
        region: 地域
        zone: 可用区列表
        status: 状态列表
        instance_category: 实例分组列表
        
    Returns:
        str: 预扣单列表的JSON字符串
    """
    params = {
        "pageNumber": page_number,
        "pageSize": page_size
    }
    
    if instance_family:
        params["instanceFamily"] = instance_family
    if instance_type:
        params["instanceType"] = instance_type
    if order_id:
        params["orderId"] = order_id
    if order_created is not None:
        params["orderCreated"] = order_created
    if creator:
        params["creator"] = creator
    if app_id:
        params["appId"] = app_id
    if app_name:
        params["appName"] = app_name
    if uin:
        params["uin"] = uin
    if region:
        params["region"] = region
    if zone:
        params["zone"] = zone
    if status:
        params["status"] = status
    if instance_category:
        params["instanceCategory"] = instance_category
        
    return _call_api("/rubik/reservation-form/list", params)

def describe_purchase_failed_alarms(
    limit: int = 100,
    distinct: bool = True,
    task_name: str = 'instance_launch',
    pool: Optional[List[str]] = ['qcloud'],
    instance_family: Optional[List[str]] = None,
    sort: Optional[List[Dict]] = None,
    start_timestamp: Optional[int] = None,
    end_timestamp: Optional[int] = None,
    app_id: Optional[str] = None,
    owner_uin: Optional[str] = None,
    app_ids: Optional[List[str]] = None,
    uin: Optional[List[str]] = None,
    region: Optional[List[str]] = None,
    zone: Optional[List[str]] = None,
    eks_flag: Optional[bool] = None,
    error_code: Optional[str] = None,
    error_message: Optional[str] = None,
    count: Optional[int] = None,
    only_privilege: Optional[bool] = None,
    next_token: Optional[str] = None
) -> str:
    """查询VStation购买失败记录
    
    Args:
        distinct: 去重
        instance_family: 实例族列表
        limit: 分页大小，最大100
        sort: 排序规则
        task_name: 任务名称
        start_timestamp: 起始时间戳
        end_timestamp: 结束时间戳
        app_id: 客户APPID
        owner_uin: UIN
        pool: 资源池列表
        app_ids: 客户APPID列表
        uin: UIN列表
        region: 地域列表
        zone: 可用区列表
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        count: 错误次数
        only_privilege: 是否仅查询大客户购买失败事件
        next_token: 分页token
        
    Returns:
        str: 购买失败记录的JSON字符串
    """
    params = {
        "limit": limit,
        "distinct": distinct,
        "taskName": task_name,
        "pool": pool
    }
    
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if sort is not None:
        params["sort"] = sort
    if start_timestamp is not None:
        params["startTimestamp"] = start_timestamp
    if end_timestamp is not None:
        params["endTimestamp"] = end_timestamp
    if app_id is not None:
        params["appId"] = app_id
    if owner_uin is not None:
        params["ownerUin"] = owner_uin
    if app_ids is not None:
        params["appIds"] = app_ids
    if uin is not None:
        params["uin"] = uin
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if count is not None:
        params["count"] = count
    if only_privilege is not None:
        params["onlyPrivilege"] = only_privilege
    if next_token is not None:
        params["nextToken"] = next_token
        
    return _call_api("/insight/purchase-failed-alarm/records", params)

def describe_vstation_events(
    limit: int = 100,
    task_name: List[str] = ['instance_launch'],
    pool: List[str] = ['qcloud'],
    app_id: Optional[List[str]] = None,
    uin: Optional[List[str]] = None,
    region: Optional[List[str]] = None,
    zone: Optional[List[str]] = None,
    zone_id: Optional[List[int]] = None,
    cvm_pay_mode: Optional[List[str]] = None,
    instance_id: Optional[List[str]] = None,
    instance_type: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None,
    not_instance_family: Optional[List[str]] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    success: Optional[bool] = None,
    eks_flag: Optional[bool] = None,
    error_code: Optional[str] = None,
    error_message: Optional[str] = None,
    main_zone: Optional[bool] = None,
    inner_user: Optional[bool] = None,
    customhouse: Optional[List[str]] = None,
    next_token: Optional[str] = None,
    offset: Optional[int] = None
) -> str:
    """查询VStation任务事件
    
    Args:
        task_name: 任务类型列表
        pool: 资源池列表
        app_id: 客户APPID列表
        uin: UIN列表
        region: 地域列表
        zone: 可用区列表
        zone_id: 可用区ID列表
        cvm_pay_mode: 支付类型列表
        instance_id: 实例ID列表
        instance_type: 实例类型列表
        instance_family: 实例族列表
        not_instance_family: 排除的实例族列表
        limit: 分页大小
        start_time: 起始时间，格式：YYYY-MM-DD HH:mm:ss
        end_time: 结束时间，格式：YYYY-MM-DD HH:mm:ss
        success: 是否成功
        eks_flag: EKS标记
        error_code: 错误码
        error_message: 错误信息
        main_zone: 是否主力园区
        inner_user: 是否内部客户
        customhouse: 境内外列表
        next_token: 分页Token
        offset: 偏移量
        
    Returns:
        str: VStation任务事件的JSON字符串
    """
    params = {}
    
    if pool is not None:
        params["pool"] = pool
    if limit is not None:
        params["limit"] = limit
    if task_name is not None:
        params["taskName"] = task_name
    if app_id is not None:
        params["appId"] = app_id
    if uin is not None:
        params["uin"] = uin
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if zone_id is not None:
        params["zoneId"] = zone_id
    if cvm_pay_mode is not None:
        params["cvmPayMode"] = cvm_pay_mode
    if instance_id is not None:
        params["instanceId"] = instance_id
    if instance_type is not None:
        params["instanceType"] = instance_type
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if not_instance_family is not None:
        params["notInstanceFamily"] = not_instance_family
    if start_time is not None:
        params["startTime"] = start_time
    if end_time is not None:
        params["endTime"] = end_time
    if success is not None:
        params["success"] = success
    if eks_flag is not None:
        params["eksFlag"] = eks_flag
    if error_code is not None:
        params["errorCode"] = error_code
    if error_message is not None:
        params["errorMessage"] = error_message
    if main_zone is not None:
        params["mainZone"] = main_zone
    if inner_user is not None:
        params["innerUser"] = inner_user
    if customhouse is not None:
        params["customhouse"] = customhouse
    if next_token is not None:
        params["nextToken"] = next_token
    if offset is not None:
        params["offset"] = offset
        
    return _call_api("/insight/vstation-event", params)

def describe_user_activity_top_decrease(
    device_class: Optional[List[str]] = None,
    instance_family: Optional[str] = None,
    instance_type: Optional[str] = None,
    limit: Optional[int] = None,
    pool: Optional[str] = None,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    main_zone: Optional[bool] = None,
    main_instance_family: Optional[bool] = None,
    customhouse: Optional[str] = None,
    instance_category: Optional[str] = None,
    next_token: Optional[str] = None,
    offset: Optional[int] = None
) -> str:
    """查询资源退还TOP
    
    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        
    Returns:
        API调用结果
    """
    params = {}
    
    if device_class is not None:
        params["device_class"] = device_class
    if instance_family is not None:
        params["instance_family"] = instance_family
    if instance_type is not None:
        params["instance_type"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["start_time"] = start_time
    if end_time is not None:
        params["end_time"] = end_time
    if main_zone is not None:
        params["main_zone"] = main_zone
    if main_instance_family is not None:
        params["main_instance_family"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instance_category"] = instance_category
    if next_token is not None:
        params["next_token"] = next_token
    if offset is not None:
        params["offset"] = offset
    
    return _call_api("/insight/user-activity/top-decrease", params)

def describe_user_activity_top_increase(
    device_class: Optional[List[str]] = None,
    instance_family: Optional[str] = None,
    instance_type: Optional[str] = None,
    limit: Optional[int] = None,
    pool: Optional[str] = None,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    main_zone: Optional[bool] = None,
    main_instance_family: Optional[bool] = None,
    customhouse: Optional[str] = None,
    instance_category: Optional[str] = None,
    next_token: Optional[str] = None,
    offset: Optional[int] = None
) -> str:
    """查询资源增长TOP
    
    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        
    Returns:
        API调用结果
    """
    params = {}
    
    if device_class is not None:
        params["device_class"] = device_class
    if instance_family is not None:
        params["instance_family"] = instance_family
    if instance_type is not None:
        params["instance_type"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["start_time"] = start_time
    if end_time is not None:
        params["end_time"] = end_time
    if main_zone is not None:
        params["main_zone"] = main_zone
    if main_instance_family is not None:
        params["main_instance_family"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instance_category"] = instance_category
    if next_token is not None:
        params["next_token"] = next_token
    if offset is not None:
        params["offset"] = offset
    
    return _call_api("/insight/user-activity/top-increase", params)

def describe_user_activity_top_active(
    device_class: Optional[List[str]] = None,
    instance_family: Optional[str] = None,
    instance_type: Optional[str] = None,
    limit: Optional[int] = None,
    pool: Optional[str] = None,
    region: Optional[str] = None,
    zone: Optional[str] = None,
    start_time: Optional[str] = None,
    end_time: Optional[str] = None,
    main_zone: Optional[bool] = None,
    main_instance_family: Optional[bool] = None,
    customhouse: Optional[str] = None,
    instance_category: Optional[str] = None,
    next_token: Optional[str] = None,
    offset: Optional[int] = None
) -> str:
    """查询活跃资源TOP
    
    Args:
        device_class: 设备类型列表
        instance_family: 实例族
        instance_type: 实例类型
        limit: 分页大小
        pool: 资源池
        region: 地域
        zone: 可用区
        start_time: 起始时间
        end_time: 结束时间
        main_zone: 是否主力园区
        main_instance_family: 是否主力机型
        customhouse: 境内外
        instance_category: 实例分类
        next_token: 分页标记
        offset: 偏移量
        
    Returns:
        API调用结果
    """
    params = {}
    
    if device_class is not None:
        params["device_class"] = device_class
    if instance_family is not None:
        params["instance_family"] = instance_family
    if instance_type is not None:
        params["instance_type"] = instance_type
    if limit is not None:
        params["limit"] = limit
    if pool is not None:
        params["pool"] = pool
    if region is not None:
        params["region"] = region
    if zone is not None:
        params["zone"] = zone
    if start_time is not None:
        params["start_time"] = start_time
    if end_time is not None:
        params["end_time"] = end_time
    if main_zone is not None:
        params["main_zone"] = main_zone
    if main_instance_family is not None:
        params["main_instance_family"] = main_instance_family
    if customhouse is not None:
        params["customhouse"] = customhouse
    if instance_category is not None:
        params["instance_category"] = instance_category
    if next_token is not None:
        params["next_token"] = next_token
    if offset is not None:
        params["offset"] = offset
    
    return _call_api("/insight/user-activity/top-active", params)

def describe_grid_by_zone_instance_type(
    region: str,
    has_total_count: Optional[bool] = None,
    limit: Optional[int] = None,
    next_token: Optional[str] = None,
    region_alias: Optional[str] = None,
    reserve_package: Optional[bool] = None,
    reserve_mode: Optional[List[str]] = None,
    status: Optional[List[str]] = None,
    greater_than_days: Optional[int] = None,
    less_than_days: Optional[int] = None,
    healthy: Optional[bool] = None,
    has_pico: Optional[bool] = None,
    has_match_rule: Optional[bool] = None,
    grid_owner: Optional[List[str]] = None,
    grid_id: Optional[List[int]] = None,
    zone: Optional[List[str]] = None,
    instance_family: Optional[List[str]] = None,
    disaster_recover_tag: Optional[List[str]] = None,
    instance_type: Optional[List[str]] = None,
    hypervisor: Optional[List[str]] = None,
    host_ip: Optional[List[str]] = None,
    host_type: Optional[List[str]] = None,
    zone_id: Optional[List[int]] = None,
    rack_id: Optional[List[int]] = None,
    pool: Optional[List[str]] = None,
    offset: Optional[int] = None
) -> str:
    """查询预扣信息根据可用区和实例类型聚合统计分析

    Args:
        has_total_count: 是否返回总数
        limit: 分页大小
        next_token: 分页标记
        region: 地域
        region_alias: 地域别名
        reserve_package: 是否预扣资源包
        reserve_mode: 预扣类型列表
        status: 状态列表
        greater_than_days: 大于天数
        less_than_days: 小于天数
        healthy: 是否健康
        has_pico: 是否有Pico标记
        has_match_rule: 是否有MatchRule
        grid_owner: 块Owner列表
        grid_id: 块Id列表
        zone: 可用区列表
        instance_family: 实例族列表
        disaster_recover_tag: 置放群组列表
        instance_type: 实例类型列表
        hypervisor: hypervisor列表
        host_ip: IP地址列表
        host_type: 母机机型列表
        zone_id: 可用区ID列表
        rack_id: 机架号列表
        pool: 资源池列表
        sort: 排序规则
        offset: 偏移量

    Returns:
        预扣信息聚合统计结果的JSON字符串
    """
    params = {
        "region": region,
        "limit": 200,
        "pool": ["qcloud"],
        "status": ["idle"],
        "hasTotalCount": False,
        "offset": 0,
        "sort": [{"property": "count", "direction": "DESC"}]
    }
    if limit is not None:
        params["limit"] = limit
    if next_token is not None:
        params["nextToken"] = next_token
    if has_total_count is not None:
        params["hasTotalCount"] = has_total_count
    if region is not None:
        params["region"] = region
    if region_alias is not None:
        params["regionAlias"] = region_alias
    if reserve_package is not None:
        params["reservePackage"] = reserve_package
    if reserve_mode is not None:
        params["reserveMode"] = reserve_mode
    if status is not None:
        params["status"] = status
    if greater_than_days is not None:
        params["greaterThanDays"] = greater_than_days
    if less_than_days is not None:
        params["lessThanDays"] = less_than_days
    if healthy is not None:
        params["healthy"] = healthy
    if has_pico is not None:
        params["hasPico"] = has_pico
    if has_match_rule is not None:
        params["hasMatchRule"] = has_match_rule
    if grid_owner is not None:
        params["gridOwner"] = grid_owner
    if grid_id is not None:
        params["gridId"] = grid_id
    if zone is not None:
        params["zone"] = zone
    if instance_family is not None:
        params["instanceFamily"] = instance_family
    if disaster_recover_tag is not None:
        params["disasterRecoverTag"] = disaster_recover_tag
    if instance_type is not None:
        params["instanceType"] = instance_type
    if hypervisor is not None:
        params["hypervisor"] = hypervisor
    if host_ip is not None:
        params["hostIp"] = host_ip
    if host_type is not None:
        params["hostType"] = host_type
    if zone_id is not None:
        params["zoneId"] = zone_id
    if rack_id is not None:
        params["rackId"] = rack_id
    if pool is not None:
        params["pool"] = pool
    if offset is not None:
        params["offset"] = offset

    return _call_api("/rubik/grid/group-by-zone-instance-type", params) 