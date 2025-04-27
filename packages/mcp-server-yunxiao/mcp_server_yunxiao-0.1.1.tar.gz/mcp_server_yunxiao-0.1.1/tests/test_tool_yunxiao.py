"""
云霄服务工具测试模块
"""
import os
import json
import unittest
from src.mcp_server_yunxiao.tool_yunxiao import (
    describe_sale_policies,
    describe_inventory,
    get_user_owned_grid,
    get_user_owned_instances,
    get_customer_account_info,
    query_quota,
    query_instance_families,
    get_instance_count,
    query_instances,
    get_instance_details,
    describe_reservation_forms,
    describe_purchase_failed_alarms,
    describe_vstation_events,
    describe_user_activity_top_decrease,
    describe_user_activity_top_increase,
    describe_user_activity_top_active
)

class TestToolYunxiao(unittest.TestCase):
    """云霄服务工具测试类"""
    
    @classmethod
    def setUpClass(cls):
        """测试类初始化"""
        # 设置环境变量
        os.environ["YUNXIAO_API_URL"] = "http://api.yunxiao.vstation.woa.com"
        os.environ["YUNXIAO_SECRET_ID"] = "ak.xiaoliu"
        os.environ["YUNXIAO_SECRET_KEY"] = "sk.63fc6b1a23e3ab55c3ced2d4"
        
    def test_describe_sale_policies(self):
        """测试查询售卖推荐数据"""
        result = describe_sale_policies(
            instance_family= ['SA5', "SA2"]
        )
        data = json.loads(result)
        print(data)
        
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)
        
        if data["data"]:
            item = data["data"][0]
            self.assertIn("境内外", item)
            self.assertIn("可用区名称", item)
            self.assertIn("实例族", item)
            self.assertIn("售卖状态", item)
            
    def test_describe_inventory(self):
        """测试查询库存数据"""
        result = describe_inventory(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        self.assertIn("data", data)
        self.assertIn("totalCount", data)
        
        if data["data"]:
            item = data["data"][0]
            self.assertIn("可用区", item)
            self.assertIn("实例族", item)
            self.assertIn("实例类型", item)
            self.assertIn("库存", item)
            
    def test_get_user_owned_grid(self):
        """测试获取用户归属预扣统计"""
        result = get_user_owned_grid(app_id=251000022)
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_user_owned_instances(self):
        """测试获取用户归属实例统计"""
        result = get_user_owned_instances(app_id=251000022)
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_customer_account_info(self):
        """测试获取客户账号信息"""
        result = get_customer_account_info(customer_ids=["251000022"])
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_quota(self):
        """测试查询配额信息"""
        result = query_quota(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_instance_families(self):
        """测试查询实例族信息"""
        result = query_instance_families()
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_instance_count(self):
        """测试获取实例数量统计"""
        result = get_instance_count(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_query_instances(self):
        """测试查询实例列表"""
        result = query_instances(region="ap-guangzhou")
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)
        
    def test_get_instance_details(self):
        """测试获取实例详细信息"""
        result = get_instance_details(region="ap-guangzhou", instance_id=["ins-123456"])
        data = json.loads(result)
        
        self.assertIsInstance(data, dict)

    def test_describe_reservation_forms(self):
        """测试查询资源预留单"""
        params = {
        }
        result = describe_reservation_forms(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_describe_purchase_failed_alarms(self):
        """测试查询购买失败告警记录"""
        params = {
        }
        result = describe_purchase_failed_alarms(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_describe_vstation_events(self):
        """测试查询VStation任务事件"""
        params = {}
        result = describe_vstation_events(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_describe_user_activity_top_decrease(self):
        """测试查询资源退还TOP"""
        params = {
        }
        result = describe_user_activity_top_decrease(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_describe_user_activity_top_increase(self):
        """测试查询资源增长TOP"""
        params = {
        }
        result = describe_user_activity_top_increase(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

    def test_describe_user_activity_top_active(self):
        """测试查询活跃资源TOP"""
        params = {
        }
        result = describe_user_activity_top_active(**params)
        self.assertIsInstance(result, str)
        data = json.loads(result)
        self.assertIsInstance(data, dict)

if __name__ == "__main__":
    unittest.main() 