# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2025-01-06 00:00:00
:LastEditTime: 2025-01-06 00:00:00
:LastEditors: yy
:Description: Handler基础类
"""

# yy_core import
from .base_handler import *


class BaseApiHandler(BaseHandler):
    """
    :Description: api base handler. not session
    :last_editors: yy
    """
    def __init__(self, *argc, **argkw):
        """
        :Description: 初始化
        :last_editors: yy
        """
        super(BaseApiHandler, self).__init__(*argc, **argkw)

    def write_error(self, status_code, **kwargs):
        """
        :Description: 重写全局异常事件捕捉
        :last_editors: yy
        """
        self.logger_error.error(
            traceback.format_exc(),
            extra={"extra": {
                "request_code": self.request_code if hasattr(self,"request_code") else ""
            }})
        return self.response_json_error()

    def prepare_ext(self):
        """
        :Description: 置于任何请求方法前被调用扩展
        :last_editors: yy
        """
        pass
