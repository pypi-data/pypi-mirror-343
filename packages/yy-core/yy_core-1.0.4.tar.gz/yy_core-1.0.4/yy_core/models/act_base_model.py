# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-28 09:54:51
@LastEditTime: 2025-04-23 17:08:46
@LastEditors: yy
@Description: 
"""
from yy_core.libs.customize.core_helper import *
from yy_core.models.core_model import *
from yy_core.models.db_models.app.app_info_model import *
from yy_core.models.db_models.act.act_info_model import *

class ActBaseModel():
    """
    :description: 活动信息业务模型
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info

    def _delete_act_info_dependency_key_v2(self, **args):
        """
        :description: 删除活动信息依赖建
        :param args: 必须指定参数名的可变长度的关键字参数（类似字典）
        :return: 
        :last_editors: yy
        """
        app_id = args.get("app_id", "") # 应用标识
        act_id = args.get("act_id", 0) # 活动标识
        delay_delete_time = args.get("delay_delete_time", 0.01) # 延迟删除时间
        dependency_key_list = []
        if act_id:
            dependency_key_list.append(DependencyKey.act_info(act_id)) 
        if app_id:
            dependency_key_list.append(DependencyKey.act_info_list(app_id))
        return ActInfoModel().delete_dependency_key(dependency_key_list, delay_delete_time)

    def _delete_act_info_dependency_key(self, app_id, act_id, delay_delete_time=0.01):
        """
        :description: 删除活动信息依赖建
        :param app_id: 应用标识
        :param act_id: 活动标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: yy
        """
        return self._delete_act_info_dependency_key_v2(app_id=app_id, act_id=act_id, delay_delete_time=delay_delete_time)

    def get_act_info_dict(self,act_id,is_cache=True,is_filter=True, field="*"):
        """
        :description: 获取活动信息
        :param act_id: 活动标识
        :param is_cache: 是否缓存
        :param is_filter: 是否过滤未发布或删除的数据
        :param field: 查询字段
        :return: 返回活动信息
        :last_editors: yy
        """
        act_info_model = ActInfoModel(context=self.context, is_auto=True)
        if is_cache:
            dependency_key = DependencyKey.act_info(act_id)
            act_info_dict = act_info_model.get_cache_dict_by_id(primary_key_id=act_id, dependency_key=dependency_key, cache_expire=600, field=field)
        else:
            act_info_dict = act_info_model.get_dict_by_id(act_id, field)
        if is_filter == True:
            if not act_info_dict or act_info_dict["is_release"] == 0 or act_info_dict["is_del"] == 1:
                return None
        return act_info_dict



    
  