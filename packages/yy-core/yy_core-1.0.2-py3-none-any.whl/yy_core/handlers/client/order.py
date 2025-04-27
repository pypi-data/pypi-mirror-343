# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-08-09 15:00:05
@LastEditTime: 2025-04-27 10:50:25
@LastEditors: yy
@Description: 
"""
from yy_core.models.enum import PageCountMode
from yy_core.handlers.frame_base import *
from yy_core.models.order_base_model import *
from yy_core.models.stat_base_model import *



class SyncPayOrderHandler(ClientBaseHandler):
    """
    :description: 同步淘宝支付订单给用户加资产
    """
    @filter_check_params("login_token",check_user_code=True)
    def get_async(self):
        """
        :description: 同步淘宝支付订单给用户加资产
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = int(self.get_param("module_id", 0))
        login_token = self.get_param("login_token")
        is_log = int(self.get_param("is_log", 0))
        is_log = True if is_log == 1 else False

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        app_key, app_secret = self.get_app_key_secret()
        order_base_model = OrderBaseModel(context=self)
        asset_type = invoke_result_data.data["asset_type"] if invoke_result_data.data.__contains__("asset_type") else 3
        goods_id = invoke_result_data.data["goods_id"] if invoke_result_data.data.__contains__("goods_id") else ""
        sku_id = invoke_result_data.data["sku_id"] if invoke_result_data.data.__contains__("sku_id") else ""
        ascription_type = invoke_result_data.data["ascription_type"] if invoke_result_data.data.__contains__("ascription_type") else 1
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        continue_request_expire = invoke_result_data.data["continue_request_expire"] if invoke_result_data.data.__contains__("continue_request_expire") else 1
        error_return = invoke_result_data.data["error_return"] if invoke_result_data.data.__contains__("error_return") else True
        invoke_result_data = order_base_model.sync_tao_pay_order(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, asset_type, goods_id, sku_id, ascription_type, app_key, app_secret, is_log, check_user_nick, continue_request_expire)
        if invoke_result_data.success == False and error_return == True:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        ref_params["app_id"] = app_id
        ref_params["act_id"] = act_id
        ref_params["module_id"] = module_id
        ref_params["user_id"] = user_id
        ref_params["open_id"] = open_id

        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)


    def business_process_executed(self, result_data, ref_params):
        """
        :description: 执行后事件
        :param result_data:result_data
        :param ref_params: 关联参数
        :return:
        :last_editors: yy
        """
        stat_base_model = StatBaseModel(context=self)
        key_list_dict = {}
        key_list_dict["PayUserCount"] = 1
        key_list_dict["PayCount"] = result_data.data["pay_num"]
        key_list_dict["PayMoneyCount"] = result_data.data["pay_price"]
        stat_base_model.add_stat_list(ref_params["app_id"], ref_params["act_id"], ref_params["module_id"], ref_params["user_id"], ref_params["open_id"], key_list_dict)
        return result_data

    """
    :description: 中奖记录下单
    """
    @filter_check_params("login_token,real_name,telephone", check_user_code=True)
    def get_async(self):
        """
        :param act_id：活动标识
        :param user_code：用户标识
        :param login_token:用户访问令牌
        :param prize_ids:用户奖品id串，逗号分隔（为空则将所有未下单的奖品进行下单）
        :param real_name:用户名
        :param telephone:电话
        :param province:省
        :param city:市
        :param county:区县
        :param street:街道
        :param address:地址
        :return
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        login_token = self.get_param("login_token")
        prize_ids = self.get_param("prize_ids")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")

        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        prize_ids = invoke_result_data.data["prize_ids"] if invoke_result_data.data.__contains__("prize_ids") else prize_ids
        invoke_result_data = order_base_model.select_prize_order(app_id, act_id, user_id, login_token, prize_ids, real_name, telephone, province, city, county, street, address)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            return self.response_json_success(self.business_process_executed(invoke_result_data, ref_params={}))
