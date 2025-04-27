# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-26 18:31:06
@LastEditTime: 2025-04-27 11:30:49
@LastEditors: yy
@Description: 
"""
from yy_core.models.enum import *
from yy_core.handlers.frame_base import *
from yy_core.models.user_base_model import *
from yy_core.models.stat_base_model import *
from yy_core.models.asset_base_model import *


class LoginHandler(ClientBaseHandler):
    """
    :description: 登录处理
    """
    def get_async(self):
        """
        :description: 登录处理
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param avatar：头像
        :return:
        :last_editors: yy
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        user_nick = self.get_user_nick()
        mix_nick = self.get_param("mix_nick")
        act_id = self.get_act_id()
        module_id = int(self.get_param("module_id", 0))
        avatar = self.get_param("avatar")
        code = self.get_param("code", "")
        pt = self.get_param("pt", "tb")  #tb淘宝 tt抖音 wx微信 jd京东 qq h5

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        is_update_user_nick = invoke_result_data.data.get("is_update_user_nick", True) # 是否更新昵称

        plat_type = share_config.get_value("plat_type", PlatType.tb.value)  # 平台类型
        union_id = ""
        login_ip = self.get_param("source_ip")

        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.save_user_by_openid(app_id, act_id, open_id, user_nick, avatar, union_id, login_ip, is_update_user_nick, mix_nick, plat_type)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        invoke_result_data.data["user_nick"] = CryptographyHelper.emoji_base64_to_emoji(invoke_result_data.data["user_nick"])
        if invoke_result_data.data["user_nick_encrypt"]:
            invoke_result_data.data["user_nick"] = CryptographyHelper.base64_decrypt(invoke_result_data.data["user_nick_encrypt"])
        ref_params = {}
        ref_params["app_id"] = app_id
        ref_params["act_id"] = act_id
        ref_params["module_id"] = module_id
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
        user_info_dict = result_data.data
        stat_base_model = StatBaseModel(context=self)
        key_list_dict = {}
        key_list_dict["VisitCountEveryDay"] = 1
        key_list_dict["VisitManCountEveryDay"] = 1
        key_list_dict["VisitManCountEveryDayIncrease"] = 1
        stat_base_model.add_stat_list(ref_params["app_id"], ref_params["act_id"], ref_params["module_id"], user_info_dict["user_id"], user_info_dict["open_id"], key_list_dict)
        return result_data


class UpdateUserInfoHandler(ClientBaseHandler):
    """
    :description: 更新用户信息
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 更新用户信息
        :param act_id：活动标识
        :param user_code：用户标识
        :param avatar：头像
        :param is_member_before：初始会员状态
        :param is_favor_before：初始关注状态
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        open_id = self.get_param("open_id")
        user_nick = self.get_user_nick()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        avatar = self.get_param("avatar")
        is_member_before = int(self.get_param("is_member_before", -1))
        is_favor_before = int(self.get_param("is_favor_before", -1))
        invoke_result_data = InvokeResultData()
        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.update_user_info(app_id, act_id, user_id, open_id, user_nick, avatar, is_member_before, is_favor_before)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        else:
            ref_params = {}
            invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
            if invoke_result_data.success == False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            return self.response_json_success("更新成功")


class UserAssetListHandler(ClientBaseHandler):
    """
    :description: 获取用户资产列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 获取用户资产列表
        :param act_id：活动标识
        :param user_code：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :return list
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        asset_type = int(self.get_param("asset_type", 0))
        asset_base_model = AssetBaseModel(context=self)
        return self.response_json_success(self.business_process_executed(asset_base_model.get_user_asset_list(app_id, act_id, user_id, asset_type), ref_params={}))


class UserAddressListHandler(ClientBaseHandler):
    """
    :description: 收货地址列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :param act_id：活动标识
        :param user_code：用户标识
        :return: list
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        user_base_model = UserBaseModel(context=self)
        return self.response_json_success(user_base_model.get_user_address_list(app_id, act_id, user_id))


class SaveUserAddressHandler(ClientBaseHandler):
    """
    :description: 保存收货地址
    """
    @filter_check_params("real_name,telephone", check_user_code=True)
    def get_async(self):
        """
        :param act_id：活动标识
        :param user_code：用户标识
        :param is_default：是否默认地址（1是0否）
        :param real_name：真实姓名
        :param telephone：手机号码
        :param province：省
        :param city：市
        :param county：区
        :param street：街道
        :param adress：地址
        :param remark：备注
        :return: dict
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        open_id = self.get_param("open_id")
        user_address_id = int(self.get_param("user_address_id", 0))
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        province = self.get_param("province")
        city = self.get_param("city")
        county = self.get_param("county")
        street = self.get_param("street")
        address = self.get_param("address")
        is_default = int(self.get_param("is_default", 0))
        remark = self.get_param("remark")
        user_base_model = UserBaseModel(context=self)
        return self.response_json_success(user_base_model.save_user_address(app_id, act_id, user_id, open_id, user_address_id, real_name, telephone, province, city, county, street, address, is_default, remark))



