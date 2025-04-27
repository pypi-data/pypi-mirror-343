# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-10-22 13:32:07
@LastEditTime: 2025-04-23 15:42:45
@LastEditors: yy
@Description: 风险控制帮助类
"""
from yy_core import *
from yy_core.models.core_model import InvokeResultData
from yy_core.libs.customize.core_helper import *
from yy_core.models.enum import PlatType
from yy_core.libs.common import *

import re

class SafeHelper:
    """
    :description:安全帮助类
    """

    #sql关键字
    _sql_pattern_key = r"\b(and|like|exec|execute|insert|create|select|drop|grant|alter|delete|update|asc|count|chr|mid|limit|union|substring|declare|master|truncate|char|delclare|or)\b|(\*|;)"
    #Url攻击正则
    _url_attack_key = r"\b(alert|xp_cmdshell|xp_|sp_|restore|backup|administrators|localgroup)\b"

    @classmethod
    def get_redis_config(self, config_dict=None):
        """
        :Description: redis初始化
        :param config_dict: config_dict
        :return: redis_init
        :last_editors: yy
        """
        config_dict = config.get_value("redis_safe")
        if not config_dict:
            config_dict = config.get_value("redis")
        if config_dict and config_dict.get("is_cluster", False):
            self.is_cluster = True
        else:
            self.is_cluster = False
        return config_dict

    @classmethod
    def authenticat_app_id(self, old_value, new_value):
        """
        :description: app_id鉴权
        :param old_value:旧值
        :param new_value:新值
        :return: 是否鉴权成功 True-成功 False-失败
        :last_editors: yy
        """
        safe_config = share_config.get_value("safe_config", {})
        is_authenticat_app_id = safe_config.get("is_authenticat_app_id", True)
        if is_authenticat_app_id == True and old_value != new_value:
            return False
        else:
            return True

    @classmethod
    def is_contain_sql(self, str):
        """
        :description: 是否包含sql关键字
        :param str:参数值
        :return:
        :last_editors: yy
        """
        result = re.search(self._sql_pattern_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def is_attack(self, str):
        """
        :description: 是否攻击请求
        :param str:当前请求地址
        :return:True是 False否
        :last_editors: yy
        """
        if ":" in str:
            return True
        result = re.search(self._url_attack_key, str.lower())
        if result:
            return True
        else:
            return False

    @classmethod
    def filter_routine_key(self, key):
        """
        :description: 过滤常规字符
        :param key:参数值
        :return:
        :last_editors: yy
        """
        routine_key_list = ["\u200b"]
        if not isinstance(key, str):
            return key
        for item in routine_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def filter_sql(self, key):
        """
        :description: 过滤sql关键字
        :param key:参数值
        :return:
        :last_editors: yy
        """
        if not isinstance(key, str):
            return key
        result = re.findall(self._sql_pattern_key, key.lower())
        for item in result:
            key = key.replace(item[0], "")
            key = key.replace(item[0].upper(), "")
        return key

    @classmethod
    def filter_special_key(self, key):
        """
        :description: 过滤sql特殊字符
        :param key:参数值
        :return:
        :last_editors: yy
        """
        if not isinstance(key, str):
            return key
        special_key_list = ["\"", "\\", "/", "*", "'", "=", "-", "#", ";", "<", ">", "+", "%", "$", "(", ")", "%", "@","!"]
        for item in special_key_list:
            key = key.replace(item, "")
        return key

    @classmethod
    def check_params(self, must_params):
        """
        :description: 校验必传参数
        :return:InvokeResultData
        :last_editors: yy
        """
        invoke_result_data = InvokeResultData()
        must_array = []
        if type(must_params) == str:
            must_array = must_params.split(",")
        if type(must_params) == list:
            must_array = must_params
        for must_param in must_array:
            if not must_param in self.request_params or self.request_params[must_param] == "":
                invoke_result_data.success = False
                invoke_result_data.error_code="param_error"
                invoke_result_data.error_message = f"参数错误,缺少必传参数{must_param}"
                break
        return invoke_result_data

    @classmethod
    def check_current_limit_by_time_window(self, limit_name, limit_count, request_limit_time=1):
        """
        :description: 流量限流校验(采用时间窗口滑动算法)
        :param limit_name: 限量名称
        :param limit_count: 限制数
        :param request_limit_time: 限制时间，单位秒
        :return:是否进行限流 True-是 False-否
        :last_editors: yy
        """
        try:
            redis_config = self.get_redis_config()
            redis_init = RedisExHelper.init(config_dict=redis_config, decode_responses=True)
            current_time = int(time.time())
            window_start = current_time // request_limit_time * request_limit_time
            window_start = f"{limit_name}:{window_start}:db_{config.get_value('project_name','')}"
            request_count = redis_init.incr(window_start, 1)
            # 如果当前请求数超过限制数，则返回 True，表示需要限流
            if request_count > limit_count:
                return True
            redis_init.expire(window_start, request_limit_time * 2 )
            return False
        except Exception as ex:
            return False

    @classmethod
    def desensitize_word(self, word):
        """
        :description: 脱敏文字,变成*号
        :param word 文字
        :return:
        :last_editors: yy
        """
        if len(word) == 0:
            return ""
        elif len(word) == 1:
            return "*"
        elif len(word) == 2:
            return word[0:1] + "*"
        elif len(word) == 3:
            return word[0:1] + "*" + word[2:3]
        else:
            num = 3 if len(word) - 3 > 3 else len(word) - 3
            star = '*' * num
            return word[0:2] + star + word[len(word) - 1:len(word)]
        
    @classmethod
    def desensitize_word_v2(self, word, head_chars=1, tail_chars=1):
        """
        :description: 自定义脱敏文字,变成*号
        :param word: 文字
        :param head_chars: 头部保留的字符数，默认为1
        :param tail_chars: 尾部保留的字符数，默认为1
        :return:
        :last_editors: yy
        """
        from math import ceil

        if len(word) <= head_chars + tail_chars:
            if len(word) == 1:
                return '*'  # 对于长度为1的字符串显示为单个星号
            elif len(word) == 2:
                return word[0] + '*'  # 对于长度为2的字符串显示为首字符加一个星号
            else:
                return word  # 当长度不足但大于等于2时直接返回原文
        
        num = ceil((len(word) - head_chars - tail_chars) * 2 / 3)
        star = '*' * num
        return word[:head_chars] + star + word[-tail_chars:]
