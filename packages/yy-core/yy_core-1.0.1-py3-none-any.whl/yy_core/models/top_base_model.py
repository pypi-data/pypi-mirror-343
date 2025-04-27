# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2020-08-12 09:06:24
@LastEditTime: 2025-04-27 13:54:54
@LastEditors: HuangJianYi
:description: 淘宝top接口基础类
"""
from yy_core.libs.common import *
from yy_core.libs.customize.core_helper import CoreHelper
from yy_core.tao_top import top
from yy_core.models.db_models.app.app_info_model import *
from yy_core.models.core_model import *

class TopBaseModel():
    """
    :description: 淘宝top接口业务模型
    """
    def __init__(self, context=None, logging_error=None, logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info


    def get_sku_name(self, num_iids, sku_id, access_token, app_key, app_secret,is_log=False):
        """
        :description: 获取sku名称
        :param num_iids：num_iids
        :param sku_id：sku_id
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        invoke_result_data.data = ""
        if not num_iids or not sku_id:
            return invoke_result_data
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.ItemsSellerListGetRequest()
            req.fields = "num_iid,title,nick,input_str,property_alias,sku,props_name,pic_url"
            req.num_iids = num_iids
            resp = req.getResponse(access_token)
            if is_log:
                log_info = str(resp) + "【access_token】：" + access_token + "【获取sku名称】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if "items_seller_list_get_response" in resp.keys():
                if "items" in resp["items_seller_list_get_response"].keys():
                    props_names = resp["items_seller_list_get_response"]["items"]["item"][0]["props_name"].split(';')
                    if "skus" in resp["items_seller_list_get_response"]["items"]["item"][0]:
                        for sku in resp["items_seller_list_get_response"]["items"]["item"][0]["skus"]["sku"]:
                            if sku["sku_id"] == sku_id:
                                props_name = [i for i in props_names if sku["properties"] in i]
                                if len(props_name) > 0:
                                    invoke_result_data.data = props_name[0][(len(sku["properties"]) + 1):]
                                else:
                                    invoke_result_data.data = sku["properties_name"].split(':')[1]
                                return invoke_result_data
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_buy_order_info(self, order_no, access_token, app_key, app_secret,is_log=False):
        """
        :description: 获取单笔订单
        :param order_no：订单编号
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return: InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.OpenTradeGetRequest()

            req.fields = "tid,status,payment,price,created,orders,num,pay_time,buyer_open_uid"
            req.tid = order_no
            resp = req.getResponse(access_token)
            if is_log:
                log_info = str(resp) + "【access_token】：" + access_token + "【获取单笔订单】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if "open_trade_get_response" in resp.keys():
                if "trade" in resp["open_trade_get_response"]:
                    invoke_result_data.data = resp["open_trade_get_response"]["trade"]
                    return invoke_result_data
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_buy_order_list(self, open_id, access_token, app_key, app_secret, start_created="", end_created="", page_size=50, is_log=False, type="fixed,step",field="tid,status,payment,price,created,orders,num,pay_time,step_trade_status,step_paid_fee,type,outer_iid", page_count = None):
        """
        :description: 获取淘宝购买订单，出现API字段映射错误，请提供参数信息联系小二处理。字段名:buyer_nick，说明open_id跟app_key没对应上，不是app_key下产品的open_id
        :param open_id：open_id
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param start_created：开始时间
        :param end_created：结束时间
        :param page_size：页大小
        :param is_log：是否记录返回信息
        :param type：订单类型
        :param field：返回字段
        :param page_count：循坏获取的页数
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        all_order = []
        has_next = True
        if page_size > 100:
            page_size = 100
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.OpenTradesSoldGetRequest()
            req.fields = field
            req.type = type
            req.buyer_open_id = open_id
            req.page_size = page_size
            req.page_no = 1
            req.use_has_next = "true"

            if start_created == "":
                start_timestamp = TimeHelper.get_now_timestamp() - 90 * 24 * 60 * 60
                start_created = TimeHelper.timestamp_to_format_time(start_timestamp)
            req.start_created = start_created
            if end_created != "":
                req.end_created = end_created

            while has_next:
                resp = req.getResponse(access_token)
                if is_log:
                    log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取购买订单】"
                    if self.context:
                        self.context.logging_link_info(log_info)
                    elif self.logging_link_info:
                        self.logging_link_info(log_info)
                if "open_trades_sold_get_response" in resp.keys():
                    if "trades" in resp["open_trades_sold_get_response"].keys():
                        all_order = all_order + resp["open_trades_sold_get_response"]["trades"]["trade"]
                    req.page_no += 1
                    has_next = resp["open_trades_sold_get_response"]["has_next"]
                    if page_count and req.page_no > page_count:
                        has_next = False
            invoke_result_data.data = all_order
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.data = []
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_refund_order_list(self, open_id, access_token, app_key, app_secret, start_modified="", end_modified="", page_size=50, is_log=False):
        """
        :description: 获取淘宝退款订单
        :param open_id：open_id
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param start_modified：开始时间
        :param end_modified：结束时间
        :param page_size：页大小
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        all_order = []
        has_next = True
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.RefundsReceiveGetRequest()
            req.fields = "refund_id,tid,oid,title,total_fee,status,created,refund_fee,modified,num"
            # refund_id：退款单号, tid：淘宝交易单号, oid：子订单号, title：商品名称 , total_fee：订单总价, status：退款状态,
            # created：退款申请时间, refund_fee：退款金额, modified：更新时间, num: 购买数量
            req.type = "fixed"
            req.page_size = page_size
            req.page_no = 1
            req.use_has_next = "true"
            if open_id:
                req.buyer_open_uid = open_id
            if start_modified == "":
                start_timestamp = TimeHelper.get_now_timestamp() - 90 * 24 * 60 * 60
                start_modified = TimeHelper.timestamp_to_format_time(start_timestamp)
            req.start_modified = start_modified
            if end_modified != "":
                req.end_modified = end_modified
            while has_next:
                resp = req.getResponse(access_token)
                if is_log:
                    log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取退单订单】"
                    if self.context:
                        self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
                if "refunds_receive_get_response" in resp.keys():
                    if "refunds" in resp["refunds_receive_get_response"].keys():
                        all_order = all_order + resp["refunds_receive_get_response"]["refunds"]["refund"]
                    req.page_no += 1
                    has_next = resp["refunds_receive_get_response"]["has_next"]
            invoke_result_data.data = all_order
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.data = []
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_shop(self, access_token, app_key, app_secret, is_log=False):
        """
        :description: 获取店铺信息
        :param access_token：access_token
        :param app_key：app_key
        :param app_secret：app_secret
        :param is_log：是否记录返回信息
        :return: InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.ShopSellerGetRequest()
            req.fields = "sid,title,pic_path"
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取店铺信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_user_seller(self, access_token, app_key, app_secret, is_log=False):
        """
        :description: 查询卖家用户信息
        :param access_token：access_token
        :param app_key：app_key
        :param app_secret：app_secret
        :param is_log：是否记录返回信息
        :return: InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.UserSellerGetRequest()
            req.fields = "user_id,nick,sex"
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【查询卖家用户信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_dead_date(self, user_nick, access_token, app_key, app_secret, is_log=False):
        """
        :description: 获取订购过期时间
        :param user_nick：用户昵称
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            vas_subscribe_get_response = self.get_vas_subscribe(user_nick, access_token, app_key, app_secret, is_log)
            if not vas_subscribe_get_response:
                invoke_result_data.data = "expire"
                return invoke_result_data
            if "article_user_subscribe" not in vas_subscribe_get_response["article_user_subscribes"].keys():
                invoke_result_data.data = "expire"
                return invoke_result_data
            invoke_result_data.data = vas_subscribe_get_response["article_user_subscribes"]["article_user_subscribe"][0]["deadline"]
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_goods_list_by_goodsids(self, num_iids, access_token,app_key, app_secret, field="num_iid,title,nick,pic_url,price,input_str,property_alias,sku,props_name,outer_id,prop_img",is_log=False):
        """
        :description: 获取在售商品列表(num_iids上限20个，超过淘宝会报错)
        :param num_iids：商品id列表
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param field：返回字段
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        num_iid_list = num_iids.split(',')
        page_size = 20
        page_count = int(len(num_iid_list) / page_size) if len(num_iid_list) % page_size == 0 else int(len(num_iid_list) / page_size) + 1
        goods_list = []
        for i in range(0, page_count):
            cur_num_iids = ",".join(num_iid_list[i * page_size:page_size * (i + 1)])
            try:
                top.setDefaultAppInfo(app_key, app_secret)
                req = top.api.ItemsSellerListGetRequest()
                req.fields = field
                req.num_iids = cur_num_iids
                resp = req.getResponse(access_token)
                if is_log:
                    log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取在售商品列表by_goodsids】"
                    if self.context:
                        self.context.logging_link_info(log_info)
                    elif self.logging_link_info:
                        self.logging_link_info(log_info)

                if "items_seller_list_get_response" in resp.keys():
                    if "items" in resp["items_seller_list_get_response"].keys():
                        if "item" in resp["items_seller_list_get_response"]["items"].keys():
                            goods_list.extend(resp["items_seller_list_get_response"]["items"]["item"])
            except Exception as ex:
                if self.context:
                    self.context.logging_link_error(traceback.format_exc())
                elif self.logging_link_error:
                    self.logging_link_error(traceback.format_exc())
                invoke_result_data.success = False
                if "submsg" in str(ex):
                    content_list = str(ex).split()
                    for content in content_list:
                        if "submsg=该子帐号无此操作权限" in content:
                            invoke_result_data.error_code = "no_power"
                            invoke_result_data.error_message = content[len("submsg="):]
                            return invoke_result_data
                        if "submsg=num_iid有误，必须大于0" in content:
                            invoke_result_data.error_code = "param_error"
                            invoke_result_data.error_message = content[len("submsg="):]
                            return invoke_result_data
                        if "submsg=" in content:
                            invoke_result_data.error_code = "error"
                            invoke_result_data.error_message = content[len("submsg="):]
                            return invoke_result_data
                return invoke_result_data
        invoke_result_data.data = {"items_seller_list_get_response": {"items": {"item": goods_list}}}
        return invoke_result_data

    def get_goods_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token,app_key, app_secret, field="num_iid,title,nick,price,input_str,property_alias,sku,props_name,pic_url", is_log=False):
        """
        :description: 获取在售商品列表（获取当前会话用户出售中的商品列表）
        :param page_index：页索引
        :param page_size：页大小
        :param goods_name：商品名称
        :param order_tag：order_tag
        :param order_by：排序类型
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param field:查询字段
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()

        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.ItemsOnsaleGetRequest()
            req.fields = field
            req.page_no = page_index + 1
            req.page_size = page_size
            if goods_name != "":
                req.q = goods_name
            if order_tag !="" and order_by !="":
                req.order_by = order_tag + ":" + order_by
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取在售商品列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_goods_info(self, num_iid, access_token,app_key, app_secret, field="num_iid,title,nick,pic_url,price,item_img.url,outer_id,sku,approve_status,prop_img", is_log=False):
        """
        :description: 获取单个商品详细信息
        :param num_iid：num_iid
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param field：查询字段
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.ItemSellerGetRequest()

            req.fields = field
            req.num_iid = num_iid
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取单个商品详细信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_goods_inventory_list(self, page_index, page_size, goods_name, order_tag, order_by, access_token,app_key, app_secret, field="num_iid,title,nick,price,input_str,property_alias,sku,props_name,pic_url", is_log=False):
        """
        :description: 获取仓库商品列表（获取当前用户作为卖家的仓库中的商品列表）
        :param page_index：页索引
        :param page_size：页大小
        :param goods_name：商品名称
        :param order_tag：order_tag
        :param order_by：排序类型
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param field：查询字段
        :param is_log：是否记录返回信息
        :return InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.ItemsInventoryGetRequest()

            req.fields = field
            req.page_no = page_index
            req.page_size = page_size
            if goods_name != "":
                req.q = goods_name
            req.order_by = order_tag + ":" + order_by

            resp = req.getResponse(access_token)
            if resp:
                resp["pageSize"] = page_size
                resp["pageIndex"] = page_index
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取仓库商品列表】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def alibaba_benefit_query(self, right_ename, access_token, app_key, app_secret, is_log=False):
        """
        :description: 查询优惠券详情信息
        :param right_ename:奖池ID
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return: InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.AlibabaBenefitQueryRequest()
            req.ename = right_ename
            req.app_name = "promotioncenter-" + share_config.get_value("server_template_id")
            req.award_type = "1"
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【查询优惠券详情信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def alibaba_benefit_send(self, right_ename, open_id, access_token,app_key, app_secret, is_log=False):
        """
        :description: 发放优惠劵
        :param right_ename:奖池ID
        :param open_id:open_id
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return: InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.AlibabaBenefitSendRequest()
            req.right_ename = right_ename
            req.receiver_id = open_id
            req.user_type = "taobao"
            req.unique_id = str(open_id) + str(right_ename) + str(TimeHelper.get_now_timestamp())
            req.app_name = "promotioncenter-" + share_config.get_value("server_template_id")
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【发放优惠劵】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def get_member_info(self, mix_nick, nick, access_token, app_key, app_secret, is_log=False):
        """
        :description: 获取淘宝会员信息
        :param mix_nick:mix_nick
        :param nick:nick（淘宝废弃使用）
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return:InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.CrmMemberIdentityGetRequest()
            if mix_nick:
                req.mix_nick = mix_nick
            if nick:
                req.nick = nick
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取淘宝会员信息】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            invoke_result_data.data = resp
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def check_is_member(self, mix_nick, nick, access_token, app_key, app_secret, is_log=False):
        """
        :description: 实时查询当前是否店铺会员
        :param mix_nick:mix_nick
        :param nick:nick（淘宝废弃使用）
        :param access_token:access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :return:True是会员 False不是会员
        :last_editors: yy
        """
        is_member = False
        invoke_result_data = self.get_member_info(mix_nick, nick, access_token, app_key, app_secret, is_log)
        if invoke_result_data.success == False:
            return is_member
        resp = invoke_result_data.data
        if "crm_member_identity_get_response" in resp.keys():
            if "result" in resp["crm_member_identity_get_response"].keys():
                if "member_info" in resp["crm_member_identity_get_response"]["result"].keys():
                    is_member = True
        return is_member

    def get_crm_point_available(self, mix_nick, access_token, app_key, app_secret, is_log=False, open_id=""):
        """
        :description: 获取店铺会员积分
        :param mix_nick：混淆昵称
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param is_log：是否记录返回信息
        :param open_id：open_id
        :return 返回店铺会员积分
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.CrmPointAvailableGetRequest()
            if mix_nick:
                req.mix_nick = mix_nick
            if open_id:
                req.open_uid = open_id
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【获取店铺会员积分】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if "crm_point_available_get_response" not in  resp:
                invoke_result_data.success = False
                return invoke_result_data
            if "result" not in resp["crm_point_available_get_response"]:
                invoke_result_data.success = False
                return invoke_result_data
            invoke_result_data.data = resp["crm_point_available_get_response"]["result"]
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data

    def change_crm_point(self, open_id, mix_nick, change_type, opt_type, quantity, access_token, app_key, app_secret, activity_id=0, activity_name="", is_log=False, account_date=""):
        """
        :description: 操作店铺会员积分
        :param open_id：买家open_id
        :param mix_nick：混淆昵称
        :param change_type：变更类型：0交易，1：互动活动，2：权益兑换，3：手工调整
        :param opt_type：操作类型，0：增加，1：扣减
        :param quantity：积分数量
        :param access_token：access_token
        :param app_key:app_key
        :param app_secret:app_secret
        :param activity_id：活动Id
        :param activity_name：活动名称
        :param is_log：是否记录返回信息
        :param account_date：积分有效期，主要用于互动场景,示例值：2017-07-30
        :return 返回操作结果
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        try:
            top.setDefaultAppInfo(app_key, app_secret)
            req = top.api.CrmPointChangeRequest()
            if activity_id > 0:
                req.activity_id = activity_id
            if activity_name:
                req.activity_name = activity_name
            if account_date:
                req.account_date = account_date
            else:
                crm_point_account_date = share_config.get_value("crm_point_account_date", 0)
                if crm_point_account_date > 0:
                    req.account_date = TimeHelper.add_days_by_format_time(day=crm_point_account_date, format='%Y-%m-%d')
            req.change_type = change_type
            req.opt_type = opt_type
            req.quantity = quantity
            if open_id:
                req.open_id = open_id
            if mix_nick:
                req.mix_nick = mix_nick
            resp = req.getResponse(access_token)
            if is_log:
                log_info = "【req】:" + CoreHelper.json_dumps(req) + "【resp】:" + CoreHelper.json_dumps(resp) + "【access_token】：" + access_token + "【操作店铺会员积分】"
                if self.context:
                    self.context.logging_link_info(log_info)
                elif self.logging_link_info:
                    self.logging_link_info(log_info)
            if "crm_point_change_response" not in resp:
                invoke_result_data.success = False
                return invoke_result_data
            if "result" not in resp["crm_point_change_response"]:
                invoke_result_data.success = False
                return invoke_result_data
            invoke_result_data.data = resp["crm_point_change_response"]["result"]
            return invoke_result_data
        except Exception as ex:
            if self.context:
                self.context.logging_link_error(traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error(traceback.format_exc())
            invoke_result_data.success = False
            if "submsg" in str(ex):
                content_list = str(ex).split()
                for content in content_list:
                    if "submsg=该子帐号无此操作权限" in content:
                        invoke_result_data.error_code = "no_power"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
                    if "submsg=" in content:
                        invoke_result_data.error_code = "error"
                        invoke_result_data.error_message = content[len("submsg="):]
                        return invoke_result_data
            return invoke_result_data