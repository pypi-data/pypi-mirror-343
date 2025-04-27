# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2021-07-15 14:09:43
@LastEditTime: 2024-11-06 10:48:04
@LastEditors: yy
:description: 通用Handler
"""
from yy_core.config import *
from yy_core.redis import *
from yy_core.web_tornado.base_handler.base_api_handler import *

from yy_core.handlers.frame_base import *


class IndexHandler(FrameBaseHandler):
    """
    :description: 默认页
    """
    def get_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: yy
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")

    def post_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: yy
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")
    
    def head_async(self):
        """
        :description: 默认页
        :param 
        :return 字符串
        :last_editors: yy
        """
        self.write(UUIDHelper.get_uuid() + "_" + config.get_value("run_port") + "_api")

