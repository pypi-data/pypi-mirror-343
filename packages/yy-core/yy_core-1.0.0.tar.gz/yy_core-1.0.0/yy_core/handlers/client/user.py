# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-26 18:31:06
@LastEditTime: 2025-04-23 14:29:38
@LastEditors: yy
@Description: 
"""
from yy_core.models.enum import *
from yy_core.handlers.frame_base import *
from yy_core.models.user_base_model import *
from yy_core.models.order_base_model import *
from yy_core.models.stat_base_model import *
from yy_core.models.app_base_model import *
from yy_core.models.asset_base_model import *
from yy_core.models.top_base_model import *
from yy_core.libs.customize.wechat_helper import *
from yy_core.libs.customize.tiktok_helper import *
from yy_core.libs.customize.safe_helper import *

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
        anonymous_code = self.get_param("anonymous_code", "")
        pt = self.get_param("pt", "tb")  #tb淘宝 tt抖音 wx微信 jd京东 qq h5

        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        is_update_user_nick = invoke_result_data.data.get("is_update_user_nick", True) # 是否更新昵称
        is_authenticat_app_id = invoke_result_data.data.get("is_authenticat_app_id", False) # 是否app_id鉴权

        plat_type = share_config.get_value("plat_type", PlatType.tb.value)  # 平台类型
        login_ip = self.get_remote_ip()
        union_id = ""
        if pt == "wx" and code:
            plat_type = PlatType.wx.value
            invoke_result_data = WeChatHelper.code2_session(code, app_id=share_config.get_value("app_id"), app_secret=share_config.get_value("app_secret"))
            if invoke_result_data.success == False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            open_id =  invoke_result_data.data["openid"]
            union_id =  invoke_result_data.data.get("unionid","")
        elif pt == "tt" and code:
            plat_type = PlatType.dy.value
            invoke_result_data = TikTokHelper.code2_session(code, anonymous_code, app_id=share_config.get_value("app_id"), app_secret=share_config.get_value("app_secret"))
            if invoke_result_data.success == False:
                return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
            open_id = invoke_result_data.data["openid"]
        else:
            login_ip = self.get_param("source_ip")

        user_base_model = UserBaseModel(context=self)
        invoke_result_data = user_base_model.save_user_by_openid(app_id, act_id, open_id, user_nick, avatar, union_id, login_ip, is_update_user_nick, mix_nick, plat_type, is_authenticat_app_id=is_authenticat_app_id)
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


class UserAvatarHandler(ClientBaseHandler):
    """
    :description: 修改头像
    """

    @filter_check_params(check_user_code=True)
    def post_async(self):
        """
        :description: 修改头像
        :return:
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        now_date = self.get_now_datetime()

        # 上传图片到资源服务器
        files_data = self.request.files
        if not files_data or not files_data["image"] or not files_data["image"][0] or not files_data["image"][0]['body']:
            return self.response_json_error("error", "未获取到文件")

        file_name = files_data["image"][0]['filename']
        file_storage_type = share_config.get_value("file_storage_type", FileStorageType.cos.value)
        if file_storage_type == FileStorageType.cos.value:
            from yy_core.libs.customize.file_helper import COSHelper
            result = COSHelper.upload(file_name=file_name, data=files_data["image"][0]['body'])
        elif file_storage_type == FileStorageType.oss.value:
            from yy_core.libs.customize.file_helper import OSSHelper
            result = OSSHelper.upload(file_name=file_name, data=files_data["image"][0]['body'])
        else:
            from yy_core.libs.customize.file_helper import BOSHelper
            result = BOSHelper.upload(file_name=file_name, data=files_data["image"][0]['body'])
        if not result:
            return self.response_json_error("error", "上传文件出错")
        user_base_model = UserBaseModel(context=self)
        id_md5 = user_base_model._get_user_info_id_md5(act_id, user_id)
        user_info_model = UserInfoModel(context=self).set_sub_table(app_id)
        user_info = user_info_model.get_entity("id_md5=%s", params=[id_md5])
        if not user_info:
            return self.response_json_error("error", "用户信息不存在")
        invoke_result_data = WeChatHelper.media_check_async(result, 2, 1, user_info.open_id)
        if invoke_result_data.success == False:
            return self.response_json_error("Except", "头像异常,请上传正确的头像")
        # 更新
        user_account_model = UserAccountModel(context=self)
        user_account_model.update_table("avatar=%s,modify_date=%s", "id=%s", params=[result, now_date, user_id])
        user_info.avatar = result
        user_info.modify_date = now_date
        user_info_model.update_entity(user_info, "avatar,modify_date")
        user_base_model._delete_user_info_cache(user_info.act_id, user_info.id_md5)
        return self.response_json_success({"user_avatar": result})