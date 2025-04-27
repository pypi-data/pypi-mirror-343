# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2025-01-06 00:00:00
:LastEditTime: 2025-01-06 00:00:00
:LastEditors: yy
:Description: 
"""

from .base_handler import *

# third package import
from pycket.session import SessionManager


class BaseCookieHandler(BaseHandler):
    """
    :Description: api base handler. have session
    :last_editors: yy
    """

    def __init__(self, *argc, **argkw):
        """
        :Description: 初始化
        :last_editors: yy
        """
        super(BaseCookieHandler, self).__init__(*argc, **argkw)
        self.session = SessionManager(self)

    def prepare_ext(self):
        """
        :Description: 置于任何请求方法前被调用扩展
        :last_editors: yy
        """
        pass

    # 根据key 获取Session 内容
    def get_session_value(self, key):
        """
        :Description: 二次封装获取session，无则返回默认值
        :param key: session key
        :return: session value
        :last_editors: yy
        """
        if key in self.session:
            return self.session[key]
        else:
            return None
