# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-08-02 14:25:02
@LastEditTime: 2025-04-23 15:00:05
@LastEditors: yy
@Description: 价格档位模块
"""
from yy_core.models.price_base_model import *
from yy_core.handlers.frame_base import *
from yy_core.models.enum import *
from yy_core.models.db_models.price.price_gear_model import *


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
        :param is_del：是否回收站1是0否
        :param business_type:业务类型
        :return: list
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        page_index = self.get_param_int("page_index", 0)
        page_size = self.get_param_int("page_size", 20)
        is_del = self.get_param_int("is_del", 0)
        business_type = self.get_param_int("business_type", -1)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc"
        page_list, total = PriceBaseModel(context=self).get_price_gear_list(app_id, act_id, page_size, page_index, order_by, is_del=is_del, is_cache=False, business_type=business_type)
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params={}))
        return self.response_json_success(page_info)

