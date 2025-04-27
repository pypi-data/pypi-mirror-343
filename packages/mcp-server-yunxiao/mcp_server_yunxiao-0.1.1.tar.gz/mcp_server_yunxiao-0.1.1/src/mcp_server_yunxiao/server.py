"""
云霄服务工具定义和路由处理
"""
from asyncio.log import logger
from typing import Any, Dict, List, Optional
from mcp.server.models import InitializationOptions
import mcp.types as types
from mcp.server import NotificationOptions, Server
import mcp.server.stdio
from . import tool_yunxiao


server = Server("yunxiao")

TOOL_DESCRIPTIONS = {
    "DescribeSalePolicies": {
        "description": "查询售卖策略和整体库存情况",
        "input_schema": {
            "type": "object",
            "required": ["PageNumber", "PageSize"],
            "properties": {
                "Customhouse": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "境内外",
                },
                "RegionAlias": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域别名",
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域",
                },
                "ZoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID",
                },
                "Zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区",
                },
                "InstanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族",
                },
                "InstanceCategory": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["CVM", "GPU", "FPGA", "BARE_METAL"]
                    },
                    "description": "实例分组",
                },
                "InstanceFamilyState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "PRINCIPAL",
                            "PRESALE",
                            "SECONDARY",
                            "SPECIAL",
                            "OFFLINE",
                            "UNAVAILABLE",
                            "LIMIT_NEW",
                            "CLEARANCE"
                        ]
                    },
                    "description": "实例族状态",
                },
                "InstanceFamilySupplyState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["LTS", "EOL"]
                    },
                    "description": "实例族供货状态",
                },
                "ZoneState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "PRINCIPAL",
                            "SECONDARY",
                            "WITHDRAWING",
                            "WITHDRAW",
                            "SPECIAL",
                            "OTHER"
                        ]
                    },
                    "description": "可用区状态",
                },
                "StockState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "WithStock",
                            "ClosedWithStock",
                            "WithoutStock"
                        ]
                    },
                    "description": "库存状态",
                },
                "SalesPolicy": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "售卖建议",
                },
                "PageNumber": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "分页页码",
                },
                "PageSize": {
                    "type": "integer",
                    "maximum": 1000,
                    "default": 500,
                    "description": "每页数量",
                }
            }
        }
    },
    "DescribeInventory": {
        "description": "查询实时的库存数据",
        "input_schema": {
            "type": "object",
            "properties": {
                "Region": {
                    "type": "string",
                    "description": "地域"
                },
                "Zone": {
                    "type": "string",
                    "description": "可用区"
                },
                "InstanceFamily": {
                    "type": "string",
                    "description": "实例族"
                },
                "InstanceType": {
                    "type": "string",
                    "description": "实例类型"
                },
                "Offset": {
                    "type": "integer",
                    "description": "偏移量",
                    "default": 0
                },
                "Limit": {
                    "type": "integer",
                    "description": "每页数量",
                    "default": 200
                }
            },
            "required": ["Region"]
        }
    },
    "GetUserOwnedGrid": {
        "description": "统计单个用户的预扣资源",
        "input_schema": {
            "type": "object",
            "properties": {
                "AppId": {
                    "type": "integer",
                    "description": "APPID"
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域列表"
                }
            },
            "required": ["AppId"]
        }
    },
    "GetCustomerAccountInfo": {
        "description": "根据 AppID 和 UIN 来查询客户账号信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "CustomerIds": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "客户ID列表"
                }
            },
            "required": ["CustomerIds"]
        }
    },
    "QueryQuota": {
        "description": "查询配额信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "Region": {
                    "type": "string",
                    "description": "地域"
                },
                "ProductCode": {
                    "type": "string",
                    "description": "产品码"
                },
                "Limit": {
                    "type": "integer",
                    "description": "页长度",
                    "default": 20
                },
                "Offset": {
                    "type": "integer",
                    "description": "偏移量",
                    "default": 0
                },
                "RegionAlias": {
                    "type": "string",
                    "description": "地域别名"
                },
                "ZoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID列表"
                },
                "AppId": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "用户AppID列表"
                },
                "PayMode": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "计费模式列表"
                },
                "InstanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "InstanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "机型族列表"
                }
            },
            "required": ["Region"]
        }
    },
    "QueryInstanceFamilies": {
        "description": "查询实例族信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "InstanceFamily": {
                    "type": "string",
                    "description": "实例族"
                },
                "States": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "状态列表"
                },
                "SupplyStates": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "供货状态列表"
                },
                "InstanceCategories": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例分类列表"
                },
                "TypeNames": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "类型名称列表"
                },
                "InstanceClass": {
                    "type": "string",
                    "description": "实例规格"
                },
                "PageNumber": {
                    "type": "integer",
                    "description": "页码",
                    "default": 1
                },
                "PageSize": {
                    "type": "integer",
                    "description": "每页数量",
                    "default": 20
                }
            }
        }
    },
    "GetInstanceCount": {
        "description": "获取实例数量统计",
        "input_schema": {
            "type": "object",
            "properties": {
                "Region": {
                    "type": "string",
                    "description": "地域"
                },
                "NextToken": {
                    "type": "string",
                    "description": "分页标记",
                    "default": ""
                },
                "Limit": {
                    "type": "integer",
                    "description": "每页数量",
                    "default": 20
                },
                "AppIds": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "APPID列表"
                },
                "Uins": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "UIN列表"
                },
                "InstanceTypes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "InstanceFamilies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                }
            },
            "required": ["Region"]
        }
    },
    "QueryInstances": {
        "description": "查询实例列表",
        "input_schema": {
            "type": "object",
            "properties": {
                "Region": {
                    "type": "string",
                    "description": "地域"
                },
                "NextToken": {
                    "type": "string",
                    "description": "分页标记",
                    "default": ""
                },
                "Limit": {
                    "type": "integer",
                    "description": "每页数量",
                    "default": 20
                },
                "AppIds": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "APPID列表"
                },
                "Uins": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "UIN列表"
                },
                "InstanceTypes": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "InstanceFamilies": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                }
            },
            "required": ["Region"]
        }
    },
    "GetInstanceDetails": {
        "description": "获取实例详细信息",
        "input_schema": {
            "type": "object",
            "properties": {
                "Region": {
                    "type": "string",
                    "description": "地域"
                },
                "InstanceId": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例ID"
                },
            },
            "required": ["Region", "InstanceId"]
        }
    },
    "DescribeStockMetrics": {
        "description": "查询库存观测指标以及库存水位",
        "input_schema": {
            "type": "object",
            "required": ["PageNumber", "PageSize"],
            "properties": {
                "Customhouse": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "境内外列表",
                },
                "MainInstanceFamily": {
                    "type": "boolean",
                    "description": "是否主力机型",
                },
                "MainZone": {
                    "type": "boolean",
                    "description": "是否主力园区",
                },
                "RegionAlias": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域别名列表",
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域列表",
                },
                "ZoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID列表",
                },
                "Zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区列表",
                },
                "InstanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表",
                },
                "DeviceClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "设备类型列表",
                },
                "SellThroughRateGreaterThan": {
                    "type": "number",
                    "description": "售罄率阈值",
                },
                "SellOutInstanceTypeCountGreaterThan": {
                    "type": "integer",
                    "description": "售罄机型数阈值",
                },
                "InstanceCategory": {
                    "type": "string",
                    "enum": ["CVM", "GPU", "FPGA", "BARE_METAL"],
                    "description": "实例分组",
                },
                "ZoneSalesStrategy": {
                    "type": "string",
                    "enum": ["PRINCIPAL", "SECONDARY", "WITHDRAWING", "WITHDRAW", "SPECIAL", "OTHER"],
                    "description": "可用区状态",
                },
                "InstanceFamilyState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["PRINCIPAL", "PRESALE", "SECONDARY", "SPECIAL", "OFFLINE", "UNAVAILABLE", "LIMIT_NEW", "CLEARANCE"],
                    },
                    "description": "实例族状态列表",
                },
                "InstanceFamilySupplyState": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["LTS", "EOL"],
                    },
                    "description": "实例售卖状态列表",
                },
                "Ds": {
                    "type": "string",
                    "format": "date",
                    "description": "日期",
                },
                "Sort": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "排序规则",
                },
                "PageNumber": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "分页页码",
                },
                "PageSize": {
                    "type": "integer",
                    "maximum": 100,
                    "default": 20,
                    "description": "分页大小",
                },
            },
        },
    },
    "DescribeStockMetricsHistory": {
        "description": "查询库存观测指标以及库存水位的历史数据",
        "input_schema": {
            "type": "object",
            "required": ["Customhouse", "InstanceFamily", "Limit", "NextToken", "Region", "TopicId", "Zone"],
            "properties": {
                "Customhouse": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "境内外列表",
                },
                "InstanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表",
                },
                "Limit": {
                    "type": "integer",
                    "maximum": 10000,
                    "default": 200,
                    "description": "页数",
                },
                "NextToken": {
                    "type": "string",
                    "description": "分页Token",
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域列表",
                },
                "TopicId": {
                    "type": "string",
                    "description": "Topic",
                },
                "Zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区列表",
                },
                "DeviceClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "设备类型列表",
                },
                "Metrics": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "展示指标列表",
                },
                "StartTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "起始时间",
                },
                "EndTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "结束时间",
                },
                "StartTimestamp": {
                    "type": "integer",
                    "format": "int64",
                    "description": "起始时间戳",
                },
                "EndTimestamp": {
                    "type": "integer",
                    "format": "int64",
                    "description": "结束时间戳",
                },
                "LastHours": {
                    "type": "integer",
                    "description": "过去的几小时",
                },
            },
        },
    },
    "DescribeBuyFlowPromiseInfo": {
        "description": "查询预计交付情况",
        "input_schema": {
            "type": "object",
            "required": ["PageNumber", "PageSize"],
            "properties": {
                "StartTime": {
                    "type": "string",
                    "format": "date",
                    "description": "开始日期",
                },
                "EndTime": {
                    "type": "string",
                    "format": "date",
                    "description": "结束日期",
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域列表",
                },
                "RegionAlias": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域别名列表",
                },
                "Zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区列表",
                },
                "ZoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID列表",
                },
                "InstanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表",
                },
                "Customhouse": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "境内外列表",
                },
                "StockChangeUnexpectMin": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "库存异动最小值",
                },
                "StockChangeUnexpectMax": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "库存异动最大值",
                },
                "Sort": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "排序规则",
                },
                "PageNumber": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "分页页码",
                },
                "PageSize": {
                    "type": "integer",
                    "maximum": 100,
                    "default": 20,
                    "description": "分页大小",
                },
            },
        },
    },
    "DescribeCvmTypeConfig": {
        "description": "多地域批量查询库存",
        "input_schema": {
            "type": "object",
            "required": ["HasTotalCount", "Limit", "NextToken"],
            "properties": {
                "InstanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表",
                },
                "InstanceFamily": {
                    "type": "string",
                    "description": "实例族",
                },
                "ZoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID列表",
                },
                "Zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区列表",
                },
                "Cpu": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "CPU核数列表",
                },
                "Gpu": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "GPU数量列表",
                },
                "Mem": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "内存大小列表",
                },
                "StorageBlock": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "存储块大小列表",
                },
                "SellOut": {
                    "type": "boolean",
                    "description": "是否售罄",
                },
                "Status": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "状态列表",
                },
                "Region": {
                    "type": "string",
                    "description": "地域",
                },
                "RegionAlias": {
                    "type": "string",
                    "description": "地域别名",
                },
                "Sort": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "排序规则",
                },
                "NextToken": {
                    "type": "string",
                    "description": "分页Token",
                },
                "Offset": {
                    "type": "integer",
                    "description": "偏移量",
                },
                "Limit": {
                    "type": "integer",
                    "description": "分页大小",
                },
                "HasTotalCount": {
                    "type": "boolean",
                    "description": "是否返回总数",
                },
            },
        },
    },
    "DescribeReservationForms": {
        "description": "查询资源预扣单",
        "input_schema": {
            "type": "object",
            "required": [],
            "properties": {
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "机型族列表,可选"
                },
                "instanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "机型列表,可选"
                },
                "pageNumber": {
                    "type": "integer",
                    "minimum": 1,
                    "default": 1,
                    "description": "页码"
                },
                "pageSize": {
                    "type": "integer",
                    "maximum": 100,
                    "default": 20,
                    "description": "每页数量"
                },
                "orderId": {
                    "type": "string",
                    "description": "关联预约单ID"
                },
                "orderCreated": {
                    "type": "boolean",
                    "description": "是否预约单创建"
                },
                "creator": {
                    "type": "string",
                    "description": "创建者"
                },
                "appId": {
                    "type": "string",
                    "description": "客户AppID"
                },
                "appName": {
                    "type": "string",
                    "description": "客户名称"
                },
                "uin": {
                    "type": "string",
                    "description": "UIN"
                },
                "region": {
                    "type": "string",
                    "description": "地域"
                },
                "zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区列表"
                },
                "status": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["APPROVAL_PENDING", "WAITING", "CREATE_PENDING", "CREATED", "PARTIAL_CREATED", 
                                "DESTROY_PENDING", "DESTROYED", "DESTROY_FAILED", "PARTIAL_DESTROYED", "FAILED", 
                                "IGNORED", "REJECTED", "CLOSED"]
                    },
                    "description": "状态列表"
                },
                "instanceCategory": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["CVM", "GPU", "FPGA", "BARE_METAL"]
                    },
                    "description": "实例分组列表"
                }
            }
        }
    },
    "DescribePurchaseFailedAlarms": {
        "description": "查询VStation购买失败记录",
        "input_schema": {
            "type": "object",
            "required": [],
            "properties": {
                "distinct": {
                    "type": "boolean",
                    "description": "去重"
                },
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                },
                "limit": {
                    "type": "integer",
                    "maximum": 100,
                    "default": 20,
                    "description": "分页大小"
                },
                "sort": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "排序规则"
                },
                "taskName": {
                    "type": "string",
                    "description": "任务名称"
                },
                "startTimestamp": {
                    "type": "integer",
                    "description": "起始时间戳"
                },
                "endTimestamp": {
                    "type": "integer",
                    "description": "结束时间戳"
                },
                "errorCode": {
                    "type": "string",
                    "description": "错误码"
                },
                "errorMessage": {
                    "type": "string",
                    "description": "错误信息"
                }
            }
        }
    },
    "DescribeVstationEvents": {
        "description": "查询VStation任务事件",
        "input_schema": {
            "type": "object",
            "required": ["region"],
            "properties": {
                "taskName": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "任务类型列表"
                },
                "pool": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "资源池列表"
                },
                "appId": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "客户APPID列表"
                },
                "success": {
                    "type": "boolean",
                    "description": "是否成功"
                },
                "errorCode": {
                    "type": "string",
                    "description": "错误码"
                },
                "errorMessage": {
                    "type": "string",
                    "description": "错误信息"
                }
            }
        }
    },
    "DescribeUserActivityTopDecrease": {
        "description": "查询TOP资源退还",
        "input_schema": {
            "type": "object",
            "required": [],
            "properties": {
                "deviceClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "deviceClass列表"
                },
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                },
                "instanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "limit": {
                    "type": "integer",
                    "description": "分页大小"
                },
                "startTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "起始时间"
                },
                "endTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "结束时间"
                }
            }
        }
    },
    "DescribeUserActivityTopIncrease": {
        "description": "查询TOP资源增长",
        "input_schema": {
            "type": "object",
            "required": [],
            "properties": {
                "deviceClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "deviceClass列表"
                },
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                },
                "instanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "limit": {
                    "type": "integer",
                    "description": "分页大小"
                },
                "startTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "起始时间"
                },
                "endTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "结束时间"
                }
            }
        }
    },
    "DescribeUserActivityTopActive": {
        "description": "查询TOP活跃（包含增长和退还）",
        "input_schema": {
            "type": "object",
            "required": ["deviceClass", "instanceFamily", "instanceType", "limit", "pool", "region", "zone"],
            "properties": {
                "deviceClass": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "deviceClass列表"
                },
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族列表"
                },
                "instanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型列表"
                },
                "limit": {
                    "type": "integer",
                    "description": "分页大小"
                },
                "startTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "起始时间"
                },
                "endTime": {
                    "type": "string",
                    "format": "date-time",
                    "description": "结束时间"
                }
            }
        }
    },
    "GetUserOwnedInstances": {
        "description": "统计单个用户的实例",
        "input_schema": {
            "type": "object",
            "properties": {
                "AppId": {
                    "type": "integer",
                    "description": "APPID"
                },
                "Region": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "地域列表"
                }
            },
            "required": ["Region"]
        }
    },
    "DescribeGridByZoneInstanceType": {
        "description": "按照可用区和实例族统计预扣资源",
        "input_schema": {
            "type": "object",
            "required": ["region"],
            "properties": {
                "reservePackage": {
                    "type": "boolean",
                    "description": "是否预扣资源包"
                },
                "reserveMode": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "fault_reserved",
                            "not_reserved",
                            "reserved_from_host",
                            "reserved_longtime",
                            "reserved_onetime"
                        ]
                    },
                    "description": "预扣类型"
                },
                "status": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "idle",
                            "occupied",
                            "unassigned",
                            "unreachable"
                        ]
                    },
                    "description": "状态"
                },
                "greaterThanDays": {
                    "type": "integer",
                    "description": "大于天数"
                },
                "lessThanDays": {
                    "type": "integer",
                    "description": "小于天数"
                },
                "healthy": {
                    "type": "boolean",
                    "description": "是否健康"
                },
                "hasPico": {
                    "type": "boolean",
                    "description": "是否有Pico标记"
                },
                "hasMatchRule": {
                    "type": "boolean",
                    "description": "是否有MatchRule"
                },
                "gridOwner": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "块Owner"
                },
                "gridId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "块Id"
                },
                "zone": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "可用区"
                },
                "instanceFamily": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例族"
                },
                "disasterRecoverTag": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "置放群组"
                },
                "instanceType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "实例类型"
                },
                "hypervisor": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": ["baremetal", "kvm"]
                    },
                    "description": "hypervisor"
                },
                "hostIp": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "IP地址"
                },
                "hostType": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "母机机型"
                },
                "zoneId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "可用区ID"
                },
                "rackId": {
                    "type": "array",
                    "items": {"type": "integer"},
                    "description": "机架号"
                },
                "pool": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "enum": [
                            "qcloud",
                            "qcloud_bm_backup",
                            "qcloud_buffer",
                            "qcloud_cdc",
                            "qcloud_eks",
                            "qcloud_supp",
                            "qcloud_vpc_supp",
                            "qcloud_ziyan",
                            "qcloud_ziyan_eks",
                            "Speed_supp",
                            "Storage_supp",
                            "zhiyun_supp",
                            "APD_supp",
                            "cbs_supp",
                            "DNS_supp",
                            "qcloud_underwrite"
                        ]
                    },
                    "description": "资源池"
                },
                "region": {
                    "type": "string",
                    "description": "地域"
                },
                "regionAlias": {
                    "type": "string",
                    "description": "地域别名"
                },
                "nextToken": {
                    "type": "string",
                    "description": "分页标记"
                },
                "offset": {
                    "type": "integer",
                    "description": "偏移量"
                },
                "limit": {
                    "type": "integer",
                    "description": "分页大小"
                },
                "hasTotalCount": {
                    "type": "boolean",
                    "description": "是否返回总数"
                }
            }
        }
    },
}

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """获取支持的工具列表"""
    return [
        types.Tool(
            name=tool_name,
            description=TOOL_DESCRIPTIONS[tool_name]["description"],
            inputSchema=TOOL_DESCRIPTIONS[tool_name]["input_schema"]
        )
        for tool_name in TOOL_DESCRIPTIONS
    ]

@server.call_tool()
async def handle_call_tool(
    name: str, arguments: dict[str, Any] | None
) -> list[types.TextContent | types.ImageContent | types.EmbeddedResource]:
    """处理工具调用
    
    Args:
        name: 工具名称
        arguments: 工具参数
        
    Returns:
        工具执行结果的JSON字符串
    """
    logger.info(f"Handling tool call: {name} with arguments: {arguments}")
    
    if name == "DescribeSalePolicies":
        result = tool_yunxiao.describe_sale_policies(
            customhouse=arguments.get("Customhouse", ["境内"]),
            region=arguments.get("Region"),
            zone=arguments.get("Zone"),
            instance_family=arguments.get("InstanceFamily"),
            instance_family_state=arguments.get("InstanceFamilyState"),
            instance_family_supply_state=arguments.get("InstanceFamilySupplyState"),
            zone_state=arguments.get("ZoneState"),
            stock_state=arguments.get("StockState", ["WithStock"]),
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 10)
        )
    elif name == "DescribeInventory":
        result = tool_yunxiao.describe_inventory(
            region=arguments["Region"],
            zone=arguments.get("Zone"),
            instance_family=arguments.get("InstanceFamily"),
            instance_type=arguments.get("InstanceType"),
            offset=arguments.get("Offset", 0),
            limit=arguments.get("Limit", 10)
        )
    elif name == "GetUserOwnedGrid":
        result = tool_yunxiao.get_user_owned_grid(
            app_id=arguments["AppId"],
            region=arguments.get("Region")
        )
    elif name == "GetUserOwnedInstances":
        result = tool_yunxiao.get_user_owned_instances(
            app_id=arguments["AppId"],
            region=arguments.get("Region")
        )
    elif name == "GetCustomerAccountInfo":
        result = tool_yunxiao.get_customer_account_info(
            customer_ids=arguments["CustomerIds"]
        )
    elif name == "QueryQuota":
        result = tool_yunxiao.query_quota(
            region=arguments["Region"],
            product_code=arguments.get("ProductCode", "cvm-instance"),
            limit=arguments.get("Limit", 100),
            offset=arguments.get("Offset", 0),
            region_alias=arguments.get("RegionAlias"),
            zone_id=arguments.get("ZoneId"),
            app_id=arguments.get("AppId"),
            pay_mode=arguments.get("PayMode"),
            instance_type=arguments.get("InstanceType"),
            instance_family=arguments.get("InstanceFamily")
        )
    elif name == "QueryInstanceFamilies":
        result = tool_yunxiao.query_instance_families(
            instance_family=arguments.get("InstanceFamily"),
            states=arguments.get("States"),
            supply_states=arguments.get("SupplyStates"),
            instance_categories=arguments.get("InstanceCategories"),
            type_names=arguments.get("TypeNames"),
            instance_class=arguments.get("InstanceClass"),
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 20)
        )
    elif name == "GetInstanceCount":
        result = tool_yunxiao.get_instance_count(
            region=arguments["Region"],
            next_token=arguments.get("NextToken", ""),
            limit=arguments.get("Limit", 20),
            app_ids=arguments.get("AppIds"),
            uins=arguments.get("Uins"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    elif name == "QueryInstances":
        result = tool_yunxiao.query_instances(
            region=arguments["Region"],
            next_token=arguments.get("NextToken", ""),
            limit=arguments.get("Limit", 20),
            app_ids=arguments.get("AppIds"),
            uins=arguments.get("Uins"),
            instance_types=arguments.get("InstanceTypes"),
            instance_families=arguments.get("InstanceFamilies")
        )
    elif name == "GetInstanceDetails":
        result = tool_yunxiao.get_instance_details(
            region=arguments["Region"],
            instance_id=arguments["InstanceId"]
        )
    elif name == "DescribeStockMetrics":
        result = tool_yunxiao.describe_stock_metrics(
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 20),
            customhouse=arguments.get("Customhouse"),
            main_instance_family=arguments.get("MainInstanceFamily"),
            main_zone=arguments.get("MainZone"),
            region_alias=arguments.get("RegionAlias"),
            region=arguments.get("Region"),
            zone_id=arguments.get("ZoneId"),
            zone=arguments.get("Zone"),
            instance_family=arguments.get("InstanceFamily"),
            device_class=arguments.get("DeviceClass"),
            sell_through_rate_greater_than=arguments.get("SellThroughRateGreaterThan"),
            sell_out_instance_type_count_greater_than=arguments.get("SellOutInstanceTypeCountGreaterThan"),
            instance_category=arguments.get("InstanceCategory"),
            zone_sales_strategy=arguments.get("ZoneSalesStrategy"),
            instance_family_state=arguments.get("InstanceFamilyState"),
            instance_family_supply_state=arguments.get("InstanceFamilySupplyState"),
            ds=arguments.get("Ds"),
            sort=arguments.get("Sort"),
        )
    elif name == "DescribeStockMetricsHistory":
        result = tool_yunxiao.describe_stock_metrics_history(
            customhouse=arguments.get("Customhouse"),
            instance_family=arguments.get("InstanceFamily"),
            limit=arguments.get("Limit"),
            next_token=arguments.get("NextToken"),
            region=arguments.get("Region"),
            topic_id=arguments.get("TopicId"),
            zone=arguments.get("Zone"),
            device_class=arguments.get("DeviceClass"),
            metrics=arguments.get("Metrics"),
            start_time=arguments.get("StartTime"),
            end_time=arguments.get("EndTime"),
            start_timestamp=arguments.get("StartTimestamp"),
            end_timestamp=arguments.get("EndTimestamp"),
            last_hours=arguments.get("LastHours"),
        )
    elif name == "DescribeBuyFlowPromiseInfo":
        result = tool_yunxiao.describe_buy_flow_promise_info(
            page_number=arguments.get("PageNumber", 1),
            page_size=arguments.get("PageSize", 20),
            start_time=arguments.get("StartTime"),
            end_time=arguments.get("EndTime"),
            region=arguments.get("Region"),
            region_alias=arguments.get("RegionAlias"),
            zone=arguments.get("Zone"),
            zone_id=arguments.get("ZoneId"),
            instance_family=arguments.get("InstanceFamily"),
            customhouse=arguments.get("Customhouse"),
            stock_change_unexpect_min=arguments.get("StockChangeUnexpectMin"),
            stock_change_unexpect_max=arguments.get("StockChangeUnexpectMax"),
            sort=arguments.get("Sort"),
        )
    elif name == "DescribeCvmTypeConfig":
        result = tool_yunxiao.describe_cvm_type_config(
            has_total_count=arguments.get("HasTotalCount"),
            limit=arguments.get("Limit"),
            next_token=arguments.get("NextToken"),
            instance_type=arguments.get("InstanceType"),
            instance_family=arguments.get("InstanceFamily"),
            zone_id=arguments.get("ZoneId"),
            zone=arguments.get("Zone"),
            cpu=arguments.get("Cpu"),
            gpu=arguments.get("Gpu"),
            mem=arguments.get("Mem"),
            storage_block=arguments.get("StorageBlock"),
            sell_out=arguments.get("SellOut"),
            status=arguments.get("Status"),
            region=arguments.get("Region"),
            region_alias=arguments.get("RegionAlias"),
            sort=arguments.get("Sort"),
            offset=arguments.get("Offset")
        )
    elif name == "DescribeReservationForms":
        result = tool_yunxiao.describe_reservation_forms(
            instance_family=arguments.get("instanceFamily"),
            instance_type=arguments.get("instanceType"),
            page_number=arguments.get("pageNumber", 1),
            page_size=arguments.get("pageSize", 20),
            order_id=arguments.get("orderId"),
            order_created=arguments.get("orderCreated"),
            creator=arguments.get("creator"),
            app_id=arguments.get("appId"),
            app_name=arguments.get("appName"),
            uin=arguments.get("uin"),
            region=arguments.get("region"),
            zone=arguments.get("zone"),
            status=arguments.get("status"),
            instance_category=arguments.get("instanceCategory")
        )
    elif name == "DescribePurchaseFailedAlarms":
        result = tool_yunxiao.describe_purchase_failed_alarms(
            distinct=arguments.get("distinct", True),
            task_name=arguments.get("taskName", 'instance_launch'),
            limit=arguments.get("limit", 100),
            sort=arguments.get("sort"),
            instance_family=arguments.get("instanceFamily"),
            start_timestamp=arguments.get("startTimestamp"),
            end_timestamp=arguments.get("endTimestamp"),
            error_code=arguments.get("errorCode"),
            error_message=arguments.get("errorMessage")
        )
    elif name == "DescribeVstationEvents":
        result = tool_yunxiao.describe_vstation_events(
            task_name=arguments.get("taskName"),
            pool=arguments.get("pool"),
            app_id=arguments.get("appId"),
            uin=arguments.get("uin"),
            region=arguments.get("region"),
            zone=arguments.get("zone"),
            zone_id=arguments.get("zoneId"),
            cvm_pay_mode=arguments.get("cvmPayMode"),
            instance_id=arguments.get("instanceId"),
            instance_type=arguments.get("instanceType"),
            instance_family=arguments.get("instanceFamily"),
            not_instance_family=arguments.get("notInstanceFamily"),
            limit=arguments.get("limit"),
            start_time=arguments.get("startTime"),
            end_time=arguments.get("endTime"),
            success=arguments.get("success"),
            eks_flag=arguments.get("eksFlag"),
            error_code=arguments.get("errorCode"),
            error_message=arguments.get("errorMessage"),
            main_zone=arguments.get("mainZone"),
            inner_user=arguments.get("innerUser"),
            customhouse=arguments.get("customhouse"),
            next_token=arguments.get("nextToken"),
            offset=arguments.get("offset")
        )
    elif name == "DescribeUserActivityTopDecrease":
        result = tool_yunxiao.describe_user_activity_top_decrease(
            device_class=arguments.get("deviceClass"),
            instance_family=arguments.get("instanceFamily"),
            instance_type=arguments.get("instanceType"),
            limit=arguments.get("limit"),
            pool=arguments.get("pool"),
            region=arguments.get("region"),
            zone=arguments.get("zone"),
            start_time=arguments.get("startTime"),
            end_time=arguments.get("endTime"),
            main_zone=arguments.get("mainZone"),
            main_instance_family=arguments.get("mainInstanceFamily"),
            customhouse=arguments.get("customhouse"),
            instance_category=arguments.get("instanceCategory"),
            next_token=arguments.get("nextToken"),
            offset=arguments.get("offset")
        )
    elif name == "DescribeUserActivityTopIncrease":
        result = tool_yunxiao.describe_user_activity_top_increase(
            device_class=arguments.get("deviceClass"),
            instance_family=arguments.get("instanceFamily"),
            instance_type=arguments.get("instanceType"),
            limit=arguments.get("limit"),
            pool=arguments.get("pool"),
            region=arguments.get("region"),
            zone=arguments.get("zone"),
            start_time=arguments.get("startTime"),
            end_time=arguments.get("endTime"),
            main_zone=arguments.get("mainZone"),
            main_instance_family=arguments.get("mainInstanceFamily"),
            customhouse=arguments.get("customhouse"),
            instance_category=arguments.get("instanceCategory"),
            next_token=arguments.get("nextToken"),
            offset=arguments.get("offset")
        )
    elif name == "DescribeUserActivityTopActive":
        result = tool_yunxiao.describe_user_activity_top_active(
            device_class=arguments.get("deviceClass"),
            instance_family=arguments.get("instanceFamily"),
            instance_type=arguments.get("instanceType"),
            limit=arguments.get("limit"),
            pool=arguments.get("pool"),
            region=arguments.get("region"),
            zone=arguments.get("zone"),
            start_time=arguments.get("startTime"),
            end_time=arguments.get("endTime"),
            main_zone=arguments.get("mainZone"),
            main_instance_family=arguments.get("mainInstanceFamily"),
            customhouse=arguments.get("customhouse"),
            instance_category=arguments.get("instanceCategory"),
            next_token=arguments.get("nextToken"),
            offset=arguments.get("offset")
        )
    elif name == "DescribeGridByZoneInstanceType":
        result = tool_yunxiao.describe_grid_by_zone_instance_type(
            region=arguments["region"],
            has_total_count=arguments.get("hasTotalCount"),
            limit=arguments.get("limit"),
            next_token=arguments.get("nextToken"),
            region_alias=arguments.get("regionAlias"),
            reserve_package=arguments.get("reservePackage"),
            reserve_mode=arguments.get("reserveMode"),
            status=arguments.get("status"),
            greater_than_days=arguments.get("greaterThanDays"),
            less_than_days=arguments.get("lessThanDays"),
            healthy=arguments.get("healthy"),
            has_pico=arguments.get("hasPico"),
            has_match_rule=arguments.get("hasMatchRule"),
            grid_owner=arguments.get("gridOwner"),
            grid_id=arguments.get("gridId"),
            zone=arguments.get("zone"),
            instance_family=arguments.get("instanceFamily"),
            disaster_recover_tag=arguments.get("disasterRecoverTag"),
            instance_type=arguments.get("instanceType"),
            hypervisor=arguments.get("hypervisor"),
            host_ip=arguments.get("hostIp"),
            host_type=arguments.get("hostType"),
            zone_id=arguments.get("zoneId"),
            rack_id=arguments.get("rackId"),
            pool=arguments.get("pool"),
            offset=arguments.get("offset")
        )
    else:
        raise ValueError(f"Unknown tool: {name}")
        
    return [types.TextContent(type="text", text=str(result))] 

async def serve():
    """启动服务"""
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        logger.info("Server running with stdio transport")
        await server.run(
            read_stream,
            write_stream,
            InitializationOptions(
                server_name="cvm",
                server_version="0.1.0",
                capabilities=server.get_capabilities(
                    notification_options=NotificationOptions(),
                    experimental_capabilities={},
                ),
            ),
        ) 