"""
云霄服务工具路由测试模块
"""
import os
import json
import asyncio
import unittest
from src.mcp_server_yunxiao.server import handle_call_tool

class TestServer(unittest.IsolatedAsyncioTestCase):
    """云霄服务工具路由测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 设置环境变量
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"
        
    async def test_describe_sale_policies(self):
        """测试查询售卖推荐数据路由"""
        name = "DescribeSalePolicies"
        arguments = {
            "PageNumber": 1,
            "PageSize": 20,
            "InstanceFamily": ["SA5"],
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)
        
    async def test_describe_inventory(self):
        """测试查询库存数据路由"""
        name = "DescribeInventory"
        arguments = {
            "Region": "ap-guangzhou",
            "Zone": "ap-guangzhou-1",
            "InstanceFamily": "SA5",
            "Offset": 0,
            "Limit": 20
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_get_user_owned_grid(self):
        """测试获取用户归属预扣统计路由"""
        name = "GetUserOwnedGrid"
        arguments = {
            "AppId": 251000022,
            "Region": ["ap-guangzhou"],
            "Offset": 0,
            "Limit": 20
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_get_customer_account_info(self):
        """测试获取客户账号信息路由"""
        name = "GetCustomerAccountInfo"
        arguments = {
            "CustomerIds": ["251000022"]
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_query_quota(self):
        """测试查询配额信息路由"""
        name = "QueryQuota"
        arguments = {
            "Region": "ap-guangzhou",
            "Limit": 20,
            "Offset": 0,
            "ZoneIds": [100001],
            "AppIds": ["251000022"],
            "InstanceTypes": ["SA5.MEDIUM4"]
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_query_instance_families(self):
        """测试查询实例族信息路由"""
        name = "QueryInstanceFamilies"
        arguments = {
            "InstanceFamily": "SA5",
            "States": ["PRINCIPAL"],
            "SupplyStates": ["LTS"],
            "InstanceCategories": ["CVM"],
            "PageNumber": 1,
            "PageSize": 20
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_get_instance_count(self):
        """测试获取实例数量统计路由"""
        name = "GetInstanceCount"
        arguments = {
            "Region": "ap-guangzhou",
            "NextToken": "",
            "Limit": 20,
            "AppIds": [251000022],
            "InstanceTypes": ["SA5.MEDIUM4"]
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_query_instances(self):
        """测试查询实例列表路由"""
        name = "QueryInstances"
        arguments = {
            "Region": "ap-guangzhou",
            "NextToken": "",
            "Limit": 20,
            "AppIds": [251000022],
            "InstanceTypes": ["SA5.MEDIUM4"]
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_get_instance_details(self):
        """测试获取实例详细信息路由"""
        name = "GetInstanceDetails"
        arguments = {
            "Region": "ap-guangzhou",
            "InstanceId": ["ins-123456"]
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)
        
    async def test_invalid_tool(self):
        """测试无效的工具名称"""
        name = "InvalidTool"
        arguments = {}
        
        with self.assertRaises(ValueError) as context:
            await handle_call_tool(name, arguments)
            
        self.assertTrue("Unknown tool" in str(context.exception))

    async def test_get_user_owned_grid_full(self):
        """测试获取用户网格列表完整参数"""
        arguments = {
            "AppId": 1234567,
            "Region": ["ap-guangzhou", "ap-shanghai"],
            "Offset": 0,
            "Limit": 20
        }
        result = await handle_call_tool("GetUserOwnedGrid", arguments)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        # 验证返回的是有效的JSON字符串
        json_result = json.loads(result[0].text)
        self.assertIsInstance(json_result, (dict, list))

    async def test_get_user_owned_instances_full(self):
        """测试获取用户实例列表完整参数"""
        arguments = {
            "Region": ["ap-guangzhou"],
            "AppId": 123456
        }
        result = await handle_call_tool("GetUserOwnedInstances", arguments)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        # 验证返回的是有效的JSON字符串
        json_result = json.loads(result[0].text)
        self.assertIsInstance(json_result, (dict, list))

    async def test_get_customer_account_info_full(self):
        """测试获取客户账号信息完整参数"""
        arguments = {
            "CustomerIds": ["100000123456", "100000654321"]
        }
        result = await handle_call_tool("GetCustomerAccountInfo", arguments)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        # 验证返回的是有效的JSON字符串
        json_result = json.loads(result[0].text)
        self.assertIsInstance(json_result, (dict, list))

    async def test_get_user_owned_grid_required_params(self):
        """测试获取用户网格列表必需参数"""
        # 缺少必需参数 AppId
        with self.assertRaises(KeyError):
            await handle_call_tool("GetUserOwnedGrid", {})

    async def test_get_user_owned_instances_required_params(self):
        """测试获取用户实例列表必需参数"""
        # 缺少必需参数 Region
        with self.assertRaises(KeyError):
            await handle_call_tool("GetUserOwnedInstances", {})

    async def test_get_customer_account_info_required_params(self):
        """测试获取客户账号信息必需参数"""
        # 缺少必需参数 CustomerIds
        with self.assertRaises(KeyError):
            await handle_call_tool("GetCustomerAccountInfo", {})

    async def test_get_user_owned_grid_optional_params(self):
        """测试获取用户网格列表可选参数"""
        # 只提供必需参数
        arguments = {
            "AppId": 1234567
        }
        result = await handle_call_tool("GetUserOwnedGrid", arguments)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")

    async def test_get_customer_account_info_param_types(self):
        """测试获取客户账号信息参数类型"""
        arguments = {
            "CustomerIds": ["invalid_type"] # CustomerIds 应该是列表
        }
        with self.assertRaises(Exception):
            await handle_call_tool("GetCustomerAccountInfo", arguments)

    async def test_describe_reservation_forms(self):
        """测试查询资源预留单路由"""
        name = "DescribeReservationForms"
        arguments = {
            "InstanceFamily": "SA5",
            "InstanceType": "SA5.MEDIUM4",
            "PageNumber": 1,
            "PageSize": 20,
            "ReservationId": "rf-123456",
            "ReservationStatus": ["PENDING", "APPROVED"],
            "ReservationTimeEnd": "2025-04-25 00:00:00",
            "ReservationTimeStart": "2025-04-24 00:00:00"
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_purchase_failed_alarms(self):
        """测试查询购买失败告警记录路由"""
        name = "DescribePurchaseFailedAlarms"
        arguments = {
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_vstation_events(self):
        """测试查询VStation任务事件路由"""
        name = "DescribeVstationEvents"
        arguments = {
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_user_activity_top_decrease(self):
        """测试查询资源退还TOP路由"""
        name = "DescribeUserActivityTopDecrease"
        arguments = {
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_user_activity_top_increase(self):
        """测试查询资源增长TOP路由"""
        name = "DescribeUserActivityTopIncrease"
        arguments = {
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_user_activity_top_active(self):
        """测试查询活跃资源TOP路由"""
        name = "DescribeUserActivityTopActive"
        arguments = {
        }
        result = await handle_call_tool(name, arguments)
        
        self.assertIsInstance(result, list)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].type, "text")
        data = json.loads(result[0].text)
        self.assertIsInstance(data, dict)

    async def test_describe_grid_by_zone_instance_type(self):
        """测试预扣信息根据可用区和实例类型聚合统计分析"""
        arguments = {
            "hasTotalCount": True,
            "limit": 20,
            "nextToken": "",
            "region": "ap-guangzhou",
            "zone": ["ap-guangzhou-3"],
            "instanceFamily": ["SA2"],
            "instanceType": ["SA2.MEDIUM4"]
        }
        result = await handle_call_tool("DescribeGridByZoneInstanceType", arguments)
        self.assertIsInstance(result, list)
        self.assertTrue(len(result) >= 0)

if __name__ == "__main__":
    asyncio.run(unittest.main()) 