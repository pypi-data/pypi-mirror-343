# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-28 09:54:51
@LastEditTime: 2025-04-23 18:33:02
@LastEditors: yy
@Description: 
"""
from yy_core.libs.customize.core_helper import *
from yy_core.libs.common import *
from yy_core.models.core_model import *
from yy_core.models.db_models.app.app_info_model import *


class AppBaseModel():
    """
    :description: 应用信息业务模型
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def get_app_info_dict(self, app_id, is_cache=True, field="*"):
        """
        :description: 获取应用信息
        :param app_id: 应用标识
        :param is_cache: 是否缓存
        :param field: 查询字段
        :return: 返回应用信息
        :last_editors: yy
        """
        app_info_model = AppInfoModel(context=self.context, is_auto=True)
        if is_cache:
            dependency_key = DependencyKey.app_info(app_id)
            return app_info_model.get_cache_dict(where="app_id=%s",limit="1", field=field, params=[app_id],dependency_key=dependency_key)
        else:
            return app_info_model.get_dict(where="app_id=%s", limit="1",field=field, params=[app_id])









