# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-08-02 14:03:12
@LastEditTime: 2024-09-11 17:13:23
@LastEditors: yy
@Description: 
"""
from yy_core.models.enum import PageCountMode
from yy_core.handlers.frame_base import *
from yy_core.models.price_base_model import *
from yy_core.models.stat_base_model import *


class PriceGearListHandler(ClientBaseHandler):
    """
    :description: 获取价格档位列表
    """
    def get_async(self):
        """
        :description: 获取价格档位列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param page_index：页索引
        :param page_size：页大小
        :param page_count_mode：分页模式(0-none 1-total 2-next)
        :param business_type：业务类型
        :return: list
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_size = self.get_param_int("page_size", 20)
        page_index = self.get_param_int("page_index", 0)
        page_count_mode = self.get_param_int("page_count_mode", 1)
        business_type = self.get_param_int("business_type", -1)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_count_mode = CoreHelper.get_enum_key(PageCountMode, page_count_mode)
        page_list = PriceBaseModel(context=self).get_price_gear_list(app_id, act_id, page_size, page_index, order_by, page_count_mode=page_count_mode, business_type=business_type)
        if page_count_mode == "total":
            total = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = PageInfo(page_index, page_size, total, page_list)
        elif page_count_mode == "next":
            is_next = page_list[1]
            page_list = self.business_process_executed(page_list[0], ref_params={})
            return_info = WaterPageInfo(page_list, is_next)
        else:
            return_info = self.business_process_executed(page_list, ref_params={})
        return self.response_json_success(return_info)


class StatReportHandler(ClientBaseHandler):
    """
    :description: 统计上报
    """
    @filter_check_params(check_user_code=True)
    def post_async(self):
        """
        :description: 统计上报
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param object_id:对象标识
        :param user_code:用户标识
        :param open_id:open_id
        :param data:统计数据json 格式：[{"key":"key1","value":1},{"key":"key2","value":1},{"key":"key3","value":1}] 或 {"key1":1,"key2":1,"key3":1}
        :return: 
        :last_editors: HuangJianYi
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("open_id")
        module_id = self.get_param_int("module_id", 0)
        object_id = self.get_param("object_id")
        stat_data = self.get_param("data", [])
        if stat_data:
            stat_data = self.json_loads(stat_data)
        stat_base_model = StatBaseModel(context=self)
        stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, open_id, stat_data, object_id=object_id)
        return self.response_json_success()
