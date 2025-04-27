# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-08-17 11:19:05
@LastEditTime: 2025-04-27 12:00:12
@LastEditors: yy
@Description: 
"""
from yy_core.handlers.frame_base import *
from yy_core.models.task_base_model import *


class TaskInfoListHandler(ClientBaseHandler):
    """
    :description: 获取任务列表
    """
    @filter_check_params(check_user_code=True)
    def get_async(self):
        """
        :description: 获取任务列表
        :param act_id：活动标识
        :param module_id：活动模块标识
        :param user_code：用户标识
        :param task_types:任务类型 多个逗号,分隔
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        mix_nick = self.get_param("mix_nick")
        module_id = self.get_param_int("module_id")
        task_types = self.get_param("task_types")
        is_log = self.get_param_int("is_log", 0)
        is_log = True if is_log == 1 else False
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        order_by = invoke_result_data.data["order_by"] if invoke_result_data.data.__contains__("order_by") else "sort_index desc,id asc"
        result_list, task_info_list, task_count_list = task_base_model.get_client_task_list(app_id, act_id, module_id, user_id, task_types, order_by)
        ref_params = {}
        ref_params["task_info_list"] = task_info_list
        ref_params["task_count_list"] = task_count_list
        return self.response_json_success(self.business_process_executed(result_list, ref_params))


class ReceiveRewardHandler(ClientBaseHandler):
    """
    :description: 处理领取任务奖励
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理领取任务奖励
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :param task_id:任务标识
        :param task_sub_type:子任务类型
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        task_id = self.get_param_int("task_id")
        task_type = self.get_param_int("task_type")
        task_sub_type = str(self.get_param("task_sub_type"))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = task_base_model.process_receive_reward(app_id, act_id, module_id, user_id, login_token, task_id, task_sub_type, self.__class__.__name__, self.request_code, task_type, check_new_user, check_user_nick, 0, is_stat, info_json, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class WeeklySignHandler(ClientBaseHandler):
    """
    :description: 处理每周签到任务
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理每周签到任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else False
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = task_base_model.process_weekly_sign(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_new_user, check_user_nick, 0, is_stat, info_json, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class InviteNewUserHandler(ClientBaseHandler):
    """
    :description: 处理邀请用户任务(被邀请人进入调用)
    """
    @filter_check_params("invite_user_id,login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理邀请用户任务(被邀请人进入调用)
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param invite_user_id:邀请人用户标识
        :param login_token:访问令牌
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.invite_new_user.value
        login_token = self.get_param("login_token")
        from_user_id = int(self.get_param("invite_user_id", 0))
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_new_user = invoke_result_data.data["check_new_user"] if invoke_result_data.data.__contains__("check_new_user") else True
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        check_act_info_release = invoke_result_data.data["check_act_info_release"] if invoke_result_data.data.__contains__("check_act_info_release") else True
        check_act_module_release = invoke_result_data.data["check_act_module_release"] if invoke_result_data.data.__contains__("check_act_module_release") else True
        close_invite_limit = invoke_result_data.data["close_invite_limit"] if invoke_result_data.data.__contains__("close_invite_limit") else False #是否关闭邀请限制
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False #是否直接领取奖励
        response_data_type = invoke_result_data.data["response_data_type"] if invoke_result_data.data.__contains__("response_data_type") else 2  #输出值类型（1-对象 2-奖励值）
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)

        stat_base_model = StatBaseModel(context=self)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"BeInvitedUserCount": 1, "BeInvitedCount": 1})

        invoke_result_data = task_base_model.process_invite_user(app_id, act_id, module_id, user_id, login_token, from_user_id, self.__class__.__name__, check_user_nick, check_new_user, 0, close_invite_limit, check_act_info_release=check_act_info_release, check_act_module_release=check_act_module_release)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if is_stat == True:
            stat_base_model.add_stat_list(app_id, act_id, module_id, user_id, "", {"AddBeInvitedUserCount": 1})
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=from_user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if response_data_type == 1:
            return self.response_json_success(invoke_result_data.data)
        else:
            return self.response_json_success(invoke_result_data.data["reward_value"])


class CollectGoodsHandler(ClientBaseHandler):
    """
    :description: 处理收藏商品任务
    """
    @filter_check_params("login_token,goods_id", check_user_code=True)
    def get_async(self):
        """
        :description: 处理收藏商品任务
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param goods_id:商品ID
        :param login_token:访问令牌
        :return: 
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        task_type = TaskType.collect_goods.value
        goods_id = self.get_param("goods_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else False  #是否统计
        is_receive_reward = invoke_result_data.data["is_receive_reward"] if invoke_result_data.data.__contains__("is_receive_reward") else False #是否直接领取奖励
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = task_base_model.process_collect_goods(app_id, act_id, module_id, user_id, login_token, goods_id, self.__class__.__name__, check_user_nick, 0)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        invoke_result_data.data = invoke_result_data.data if invoke_result_data.data else {}
        invoke_result_data.data["reward_value"] = 0
        if is_receive_reward == True:
            reward_invoke_result_data = task_base_model.process_receive_reward(app_id=app_id, act_id=act_id, module_id=module_id, user_id=user_id, login_token='', task_id=0, task_sub_type='', handler_name=self.__class__.__name__, request_code=self.request_code, task_type=task_type, check_new_user=False, check_user_nick=False, continue_request_expire=0, is_stat=is_stat, info_json=info_json, check_act_info_release=False, check_act_module_release=False)
            if reward_invoke_result_data.success == True:
                invoke_result_data.data["reward_value"] = reward_invoke_result_data.data["reward_value"]
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)

        return self.response_json_success(invoke_result_data.data["reward_value"])


class FavorStoreHandler(ClientBaseHandler):
    """
    :description: 处理关注店铺
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理关注店铺
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = task_base_model.process_favor_store(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])


class JoinMemberHandler(ClientBaseHandler):
    """
    :description: 处理加入店铺会员
    """
    @filter_check_params("login_token", check_user_code=True)
    def get_async(self):
        """
        :description: 处理加入店铺会员
        :param app_id:应用标识
        :param act_id:活动标识
        :param module_id:活动模块标识
        :param user_code:用户标识
        :param login_token:访问令牌
        :return: 直接发放奖励，返回奖励值
        :last_editors: yy
        """
        app_id = self.get_app_id()
        act_id = self.get_act_id()
        user_id = self.get_user_id()
        module_id = self.get_param_int("module_id")
        login_token = self.get_param("login_token")
        invoke_result_data = self.business_process_executing()
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        if not invoke_result_data.data:
            invoke_result_data.data = {}
        check_user_nick = invoke_result_data.data["check_user_nick"] if invoke_result_data.data.__contains__("check_user_nick") else True
        is_stat = invoke_result_data.data["is_stat"] if invoke_result_data.data.__contains__("is_stat") else True
        info_json = invoke_result_data.data["info_json"] if invoke_result_data.data.__contains__("info_json") else None
        task_base_model = TaskBaseModel(context=self)
        invoke_result_data = task_base_model.process_join_member(app_id, act_id, module_id, user_id, login_token, self.__class__.__name__, self.request_code, check_user_nick, 0, is_stat, info_json)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        ref_params = {}
        invoke_result_data = self.business_process_executed(invoke_result_data, ref_params)
        if invoke_result_data.success == False:
            return self.response_json_error(invoke_result_data.error_code, invoke_result_data.error_message)
        return self.response_json_success(invoke_result_data.data["reward_value"])
