# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2022-04-24 15:15:19
@LastEditTime: 2025-04-22 18:02:06
@LastEditors: yy
@Description: 
"""

from yy_core.web_tornado.base_handler.base_api_handler import *
from yy_core.libs.customize.core_helper import *
from yy_core.libs.customize.cryptography_helper import *
from yy_core.libs.customize.safe_helper import *
from yy_core.models.app_base_model import *
from urllib.parse import parse_qs


def filter_check_params(must_params=None, check_user_code=False):
    """
    :description: 参数过滤装饰器 仅限handler使用,
                  提供参数的检查及获取参数功能
                  装饰器使用方法:
                  @client_filter_check_params("param_a,param_b,param_c")  或
                  @client_filter_check_params(["param_a","param_b,param_c"])
                  参数获取方法:
                  self.request_params[param_key]
    :param must_params: 必须传递的参数集合
    :param check_user_code: 是否校验用户标识必传
    :last_editors: yy
    """
    def check_params(handler):
        def wrapper(self, **args):
            finally_must_params = must_params
            if hasattr(self, "must_params"):
                finally_must_params = self.must_params
            if type(finally_must_params) == str:
                must_array = finally_must_params.split(",")
            if type(finally_must_params) == list:
                must_array = finally_must_params

            if finally_must_params:
                for must_param in must_array:
                    if not must_param in self.request_params or self.request_params[must_param] == "":
                        self.response_json_error("param_error", f"参数错误,缺少必传参数{must_param}")
                        return
            if check_user_code == True and not self.get_user_id():
                self.response_json_error("param_error", f"参数错误,缺少必传参数user_code")
                return

            return handler(self, **args)

        return wrapper

    return check_params


