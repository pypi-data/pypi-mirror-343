# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-08-09 14:11:52
@LastEditTime: 2023-08-15 10:42:40
@LastEditors: yy
@Description: 订单模块
"""
from yy_core.models.enum import *
from yy_core.libs.customize.file_helper import *
from yy_core.handlers.frame_base import *
from yy_core.models.order_base_model import *


class PayOrderListHandler(ClientBaseHandler):
    """
    :description: 用户购买订单列表
    """
    def get_async(self):
        """
        :description: 用户购买订单列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param user_open_id：open_id
        :param nick_name：用户昵称
        :param pay_date_start：订单支付时间开始
        :param pay_date_end：订单支付时间结束
        :param main_pay_order_no：淘宝主订单号
        :param sub_pay_order_no：淘宝子订单号
        :param page_size：页大小
        :param page_index：页索引
        :return:
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        user_open_id = self.get_param("user_open_id")
        user_nick = self.get_param("nick_name")
        pay_date_start = self.get_param("pay_date_start")
        pay_date_end = self.get_param("pay_date_end")
        main_pay_order_no = self.get_param("main_pay_order_no")
        sub_pay_order_no = self.get_param("sub_pay_order_no")
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 20))

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "create_date desc"
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"

        if main_pay_order_no:
            condition += " and " if condition else ""
            condition += "main_pay_order_no=%s"
            params.append(main_pay_order_no)
        if sub_pay_order_no:
            condition += " and " if condition else ""
            condition += "sub_pay_order_no=%s"
            params.append(sub_pay_order_no)

        order_base_model = OrderBaseModel(context=self)
        page_info = order_base_model.get_tao_pay_order_list(app_id, act_id, user_id, user_open_id, user_nick, pay_date_start, pay_date_end, page_size=page_size, page_index=page_index, field=field, order_by=order_by, condition=condition, params=params)
        ref_params = {}
        page_info.data = self.business_process_executed(page_info.data, ref_params)
        return self.response_json_success(page_info)


class PrizeRosterListHandler(ClientBaseHandler):
    """
    :description: 用户中奖记录列表
    """
    def get_async(self):
        """
        :description: 用户中奖记录列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_code：用户标识
        :param user_open_id：open_id
        :param nick_name：用户昵称
        :param module_name：模块名称
        :param prize_name：奖品名称
        :param order_no：订单号
        :param goods_type：物品类型（1虚拟2实物）
        :param prize_type：奖品类型(1现货2优惠券3红包4参与奖5预售)
        :param logistics_status：物流状态（0未发货1已发货2不予发货）
        :param prize_status：奖品状态（0未下单（未领取）1已下单（已领取）2已回购10已隐藏（删除）11无需发货）
        :param pay_status：支付状态(0未支付1已支付2已退款3处理中)
        :param create_date_start：开始时间
        :param create_date_end：结束时间
        :param page_size：页大小
        :param page_index：页索引
        :return 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        user_id = self.get_user_id()
        user_open_id = self.get_param("user_open_id")
        order_no = self.get_param("order_no")
        user_nick = self.get_param("nick_name")
        module_name = self.get_param("module_name")
        prize_name = self.get_param("prize_name")
        goods_type = int(self.get_param("goods_type", -1))
        prize_type = int(self.get_param("prize_type", -1))
        logistics_status = int(self.get_param("logistics_status", -1))
        prize_status = int(self.get_param("prize_status", -1))
        pay_status = int(self.get_param("pay_status", -1))
        create_date_start = self.get_param("create_date_start")
        create_date_end = self.get_param("create_date_end")
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 500))

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_success({"data": []})
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        condition = invoke_result_data.data["condition"] if invoke_result_data.data.__contains__("condition") else ""
        params = invoke_result_data.data["params"] if invoke_result_data.data.__contains__("params") else []
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "create_date desc"
        field = invoke_result_data.data["field"] if invoke_result_data.data.__contains__("field") else "*"
        condition_where = ConditionWhere()
        if condition:
            condition_where.add_condition(condition)
        if module_name:
            condition_where.add_condition("module_name=%s")
            params.append(module_name)
        if prize_name:
            condition_where.add_condition("prize_name=%s")
            params.append(prize_name)

        order_base_model = OrderBaseModel(context=self)
        page_list, total = order_base_model.get_prize_roster_list(app_id, act_id, module_id, user_id, user_open_id, user_nick, order_no, goods_type, prize_type, logistics_status, prize_status, pay_status, page_size, page_index, create_date_start, create_date_end, order_by=order_by, field=field, condition=condition_where.to_string(), params=params, is_cache=False)
        ref_params = {}
        page_info = PageInfo(page_index, page_size, total, self.business_process_executed(page_list, ref_params=ref_params))
        return self.response_json_success(page_info)


class UpdatePrizeOrderSellerRemarkHandler(ClientBaseHandler):
    """
    :description: 更新奖品订单卖家备注
    """
    @filter_check_params("prize_order_id")
    def get_async(self):
        """
        :description: 更新奖品订单卖家备注
        :param app_id：应用标识
        :param act_id：活动标识
        :param prize_order_id：奖品订单标识
        :param seller_remark：卖家备注
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        prize_order_id = int(self.get_param("prize_order_id", 0))
        seller_remark = self.get_param("seller_remark")
        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = order_base_model.update_prize_order_seller_remark(app_id, act_id, prize_order_id, seller_remark)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        title = "修改订单备注；用户昵称：" + invoke_result_data.data["user_nick"] + "，openid：" + invoke_result_data.data["open_id"]
        self.create_operation_log(operation_type=OperationType.operate.value, model_name="prize_order_tb", title=title)
        return self.response_json_success()


class ImportPrizeOrderHandler(ClientBaseHandler):
    """
    :description: 导入奖品订单进行发货
    """
    @filter_check_params("content")
    def post_async(self):
        """
        :description: 导入奖品订单进行发货
        :param app_id：应用标识
        :param content_type：内容类型 1-base64字符串内容 2-json字符串内容
        :param content：字符串内容
        :param act_id：活动标识
        :param ref_head_name：关联表头名称，可不传
        :return 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        content = self.get_param("content")
        content_type = int(self.get_param("content_type", 1))
        ref_head_name = self.get_param("ref_head_name", "小程序订单号")

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        prize_roster_sub_table = invoke_result_data.data["prize_roster_sub_table"] if invoke_result_data.data.__contains__("prize_roster_sub_table") else None
        operate_title = invoke_result_data.data["operate_title"] if invoke_result_data.data.__contains__("operate_title") else "发货列表"
        order_base_model = OrderBaseModel(context=self)
        invoke_result_data = order_base_model.import_prize_order(app_id, act_id, content_type, content, ref_head_name, prize_roster_sub_table)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        self.create_operation_log(operation_type=OperationType.import_data.value, model_name="prize_order_tb", title=operate_title)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success ==False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data)
