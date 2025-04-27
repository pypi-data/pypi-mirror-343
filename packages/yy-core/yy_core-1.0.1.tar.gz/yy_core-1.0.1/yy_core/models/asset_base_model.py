# -*- coding: utf-8 -*-
"""
:Author: yy
:Date: 2020-05-12 20:11:48
@LastEditTime: 2025-03-19 17:54:50
@LastEditors: yy
:description: 
"""
from yy_core.libs.common import *
from yy_core.libs.customize.core_helper import *
from yy_core.libs.customize.safe_helper import SafeHelper
from yy_core.models.db_models.asset.asset_log_model import *
from yy_core.models.db_models.asset.asset_only_model import *
from yy_core.models.db_models.user.user_asset_model import *
from yy_core.models.core_model import *
from yy_core.models.frame_base_model import *


class AssetBaseModel():
    """
    :description: 资产管理业务模型,主要管理用户资产和商家资产
    """
    def __init__(self,context=None,logging_error=None,logging_info=None):
        self.context = context
        self.logging_link_error = logging_error
        self.logging_link_info = logging_info
        self.db_connect_key, self.redis_config_dict = CoreHelper.get_connect_config("db_asset","redis_asset")

    def _delete_asset_dependency_key(self, act_id, user_id, delay_delete_time=0.01):
        """
        :description: 删除资产依赖建
        :param act_id: 活动标识
        :param user_id: 用户标识
        :param delay_delete_time: 延迟删除时间，传0则不进行延迟
        :return: 
        :last_editors: yy
        """
        AssetLogModel().delete_dependency_keys([DependencyKey.asset_log_list(act_id, user_id), DependencyKey.user_asset(act_id, user_id)], delay_delete_time)

    def delete_asset_only(self, act_id, only_id, create_day=0, app_id=''):
        """
        :description: 清除资产唯一标识 从数据库和redis中删除
        :param act_id：活动标识
        :param only_id：资产唯一标识
        :param create_day：整形的创建天20200506
        :param app_id：应用标识
        :return: 
        :last_editors: yy
        """
        redis_init = CoreHelper.redis_init(config_dict=self.redis_config_dict)
        hash_name = f"asset_only_list:{act_id}" if act_id > 0 else f"asset_only_list:{app_id}_0"
        if create_day <= 0:
            hash_name += f"_{CoreHelper.get_now_day_int()}"
        else:
            hash_name += f"_{create_day}"
        if redis_init.hexists(hash_name, only_id):
            redis_init.hdel(hash_name, only_id)
            asset_only_model = AssetOnlyModel(context=self.context)
            asset_only_model.del_entity("only_id=%s", params=[only_id])

    def get_user_asset_id_md5(self, app_id, act_id, user_id, asset_type, asset_object_id):
        """
        :description: 生成用户资产id_md5
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_object_id：对象标识
        :return: 用户资产唯一标识
        :last_editors: yy
        """
        if not user_id or not asset_type:
            return 0
        if act_id > 0:
            return CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{asset_type}_{asset_object_id}")
        else:
            return CryptoHelper.md5_encrypt_int(f"{app_id}_0_{user_id}_{asset_type}_{asset_object_id}")
        
    def get_asset_only_id_md5(self, app_id, act_id, user_id, only_id):
        """
        :description: 生成资产唯一id_md5
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param only_id：only_id
        :return: 资产唯一id_md5
        :last_editors: yy
        """
        if act_id > 0:
            return CryptoHelper.md5_encrypt_int(f"{act_id}_{user_id}_{only_id}")
        else:
            return CryptoHelper.md5_encrypt_int(f"{app_id}_0_{user_id}_{only_id}")
        
    def get_asset_check_code(self, id_md5, asset_value, sign_key):
        """
        :description: 生成资产校验码
        :param id_md5：id_md5
        :param asset_value：当前资产值
        :param sign_key：签名key,目前使用app_id作为签名key
        :return: 用户资产校验码
        :last_editors: yy
        """
        if not id_md5 or not asset_value:
            return ""
        return CryptoHelper.md5_encrypt(f"{id_md5}_{asset_value}", sign_key)
    
    def check_and_reset_asset(self, user_asset_dict: dict, app_id: str):
        """
        :description:检查并重置资产值（如果校验失败）
        :param user_asset_dict: 用户资产字典
        :param app_id: 当前应用ID
        """
        if user_asset_dict and share_config.get_value("is_check_asset", True) == True:
            if SafeHelper.authenticat_app_id(user_asset_dict["app_id"], app_id) == False:
                user_asset_dict["asset_value"] = 0
            else:
                asset_check_code = self.get_asset_check_code(user_asset_dict["id_md5"], user_asset_dict["asset_value"], app_id)
                if asset_check_code != user_asset_dict["asset_check_code"]:
                    user_asset_dict["asset_value"] = 0
        return user_asset_dict

    def update_user_asset(self, app_id, act_id, module_id, user_id, open_id, user_nick, asset_type, asset_value, asset_object_id, source_type, source_object_id, source_object_name, log_title, only_id="",handler_name="",request_code="", info_json={}):
        """
        :description: 变更用户资产
        :param act_id：活动标识
        :param module_id：模块标识，没有填0
        :param user_id：用户标识
        :param open_id：open_id
        :param user_nick：昵称
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_value：变动的资产值，比如原本是100现在变成80，应该传入-20,原本是100现在变成120，应该传入20
        :param asset_object_id：资产对象标识
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param source_object_name：来源对象名称(比如来源类型是任务则对应任务名称)
        :param log_title：资产流水标题
        :param only_id:唯一标识(用于并发操作时校验避免重复操作)由业务方定义传入
        :param handler_name:接口名称
        :param request_code:请求唯一标识，从yy_core框架获取对应request_code
        :param info_json：资产流水详情，用于存放业务方自定义字典
        :return: 返回实体InvokeResultData
        :last_editors: yy
        """

        invoke_result_data = InvokeResultData()

        if not user_id or not asset_type or not asset_value:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "参数不能为空或等于0"
            return invoke_result_data

        if int(asset_type) == 3 and not asset_object_id:
            invoke_result_data.success = False
            invoke_result_data.error_code = "param_error"
            invoke_result_data.error_message = "资产类型为价格档位,参数asset_object_id不能为空或等于0"
            return invoke_result_data
        asset_value = int(asset_value)
        user_asset_id_md5 = self.get_user_asset_id_md5(app_id, act_id, user_id, asset_type, asset_object_id)
        if user_asset_id_md5 == 0:
            invoke_result_data.success = False
            invoke_result_data.error_code = "error"
            invoke_result_data.error_message = "修改失败"
            return invoke_result_data
        #如果only_id已经存在，直接在redis进行拦截,减少数据库的请求，时限1天
        redis_init = CoreHelper.redis_init(config_dict=self.redis_config_dict)
        only_cache_key = ""
        if only_id:
            only_cache_key = f"asset_only_list:{act_id}_{CoreHelper.get_now_day_int()}"  if act_id > 0 else f"asset_only_list:{app_id}_0_{CoreHelper.get_now_day_int()}"
            if redis_init.hexists(only_cache_key, only_id):
                invoke_result_data.success = False
                invoke_result_data.error_code = "error"
                invoke_result_data.error_message = "only_id已经存在"
                return invoke_result_data
        db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key), context=self.context)
        user_asset_model = UserAssetModel(db_transaction=db_transaction, context=self.context)
        asset_log_model = AssetLogModel(db_transaction=db_transaction, context=self.context)
        asset_only_model = AssetOnlyModel(db_transaction=db_transaction, context=self.context)

        acquire_lock_name = f"userasset:{user_asset_id_md5}"
        acquire_lock_status, identifier = CoreHelper.redis_acquire_lock(acquire_lock_name)
        if acquire_lock_status == False:
            invoke_result_data.success = False
            invoke_result_data.error_code = "acquire_lock"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
            return invoke_result_data

        try:
            now_day_int = CoreHelper.get_now_day_int()
            now_datetime = CoreHelper.get_now_datetime()
            old_user_asset_id = 0
            history_asset_value = 0

            user_asset = user_asset_model.get_entity("id_md5=%s",params=[user_asset_id_md5])
            if user_asset:
                if user_asset.asset_value + asset_value < 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "no_enough"
                    invoke_result_data.error_message = "变更后的资产不能为负数"
                    return invoke_result_data
                if user_asset.asset_value + asset_value > 2147483647:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "no_enough"
                    invoke_result_data.error_message = "变更后的资产不能大于整形的最大值"
                    return invoke_result_data

                old_user_asset_id = user_asset.id
                history_asset_value = user_asset.asset_value
            else:
                if asset_value < 0:
                    invoke_result_data.success = False
                    invoke_result_data.error_code = "no_enough"
                    invoke_result_data.error_message = "资产不能为负数"
                    return invoke_result_data
                user_asset = UserAsset()
                user_asset.id_md5 = user_asset_id_md5
                user_asset.app_id = app_id
                user_asset.act_id = act_id
                user_asset.user_id = user_id
                user_asset.open_id = open_id
                user_asset.user_nick = user_nick
                user_asset.asset_type = asset_type
                user_asset.asset_object_id = asset_object_id
                user_asset.create_date = now_datetime

            user_asset.asset_value += asset_value
            user_asset.asset_check_code = self.get_asset_check_code(user_asset_id_md5, user_asset.asset_value, app_id)
            user_asset.modify_date = now_datetime

            asset_log = AssetLog()
            asset_log.app_id = app_id
            asset_log.act_id = act_id
            asset_log.module_id = module_id
            asset_log.user_id = user_id
            asset_log.open_id = open_id
            asset_log.user_nick = user_nick
            asset_log.log_title = log_title
            asset_log.info_json = CoreHelper.json_dumps(info_json) if info_json else {}
            asset_log.asset_type = asset_type
            asset_log.asset_object_id = asset_object_id
            asset_log.source_type = source_type
            asset_log.source_object_id = source_object_id
            asset_log.source_object_name = source_object_name
            asset_log.only_id = only_id
            asset_log.operate_type = 0 if asset_value > 0 else 1
            asset_log.operate_value = asset_value
            asset_log.history_value = history_asset_value
            asset_log.now_value = user_asset.asset_value
            asset_log.handler_name = handler_name
            asset_log.request_code = request_code
            asset_log.create_date = now_datetime
            asset_log.create_day = now_day_int

            if only_id:
                asset_only = AssetOnly()
                asset_only.id_md5 = self.get_asset_only_id_md5(app_id, act_id, user_id, only_id)
                asset_only.app_id = app_id
                asset_only.act_id = act_id
                asset_only.user_id = user_id
                asset_only.open_id = open_id
                asset_only.only_id = only_id
                asset_only.create_date = now_datetime

            db_transaction.begin_transaction()

            if old_user_asset_id != 0:
                user_asset_model.update_entity(user_asset, "asset_value,asset_check_code,modify_date")
            else:
                user_asset_model.add_entity(user_asset)
            if only_id:
                asset_only_model.add_entity(asset_only)
            asset_log_model.add_entity(asset_log)

            result,message = db_transaction.commit_transaction(return_detail_tuple=True)
            if result == False:
                if self.context:
                    self.context.logging_link_error("【变更资产】" + message)
                elif self.logging_link_error:
                    self.logging_link_error("【变更资产】" + message)
                invoke_result_data.success = False
                invoke_result_data.error_code = "fail"
                invoke_result_data.error_message = "系统繁忙,请稍后再试"
                return invoke_result_data
            try:
                if only_id:
                    redis_init.hset(only_cache_key, only_id, 1)
                    redis_init.expire(only_cache_key, 24 * 3600)
                self._delete_asset_dependency_key(act_id,user_id)

            except Exception as ex:
                if self.context:
                    self.context.logging_link_error("【资产队列】" + traceback.format_exc())
                elif self.logging_link_error:
                    self.logging_link_error("【资产队列】" + traceback.format_exc())

            invoke_result_data.data = {"user_asset":user_asset.__dict__}

        except Exception as ex:
            if self.context:
                self.context.logging_link_error("【变更资产】" + traceback.format_exc())
            elif self.logging_link_error:
                self.logging_link_error("【变更资产】" + traceback.format_exc())
            invoke_result_data.success = False
            invoke_result_data.error_code = "exception"
            invoke_result_data.error_message = "系统繁忙,请稍后再试"
        finally:
            CoreHelper.redis_release_lock(acquire_lock_name, identifier)

        return invoke_result_data
    
    def get_user_asset_list(self, app_id, act_id, user_ids, asset_type=0, is_cache=False):
        """
        :description: 获取用户资产列表
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_ids：用户标识 多个逗号,分隔
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param is_cache：是否缓存
        :return: 返回list
        :last_editors: yy
        """
        if not user_ids:
            return []
        condition_where = ConditionWhere()
        params = []
        if app_id:
            condition_where.add_condition("app_id=%s")
            params.append(app_id)
        if act_id != 0:
            condition_where.add_condition("act_id=%s")
            params.append(act_id)
        if asset_type != 0:
            condition_where.add_condition("asset_type=%s")
            params.append(asset_type)
        is_only_one = False
        if user_ids:
            if isinstance(user_ids,str):
                condition_where.add_condition(f"user_id in ({user_ids})")
                if ',' not in user_ids:
                    is_only_one = True
            elif isinstance(user_ids,list):
                condition_where.add_condition(CoreHelper.get_condition_by_int_list("user_id",user_ids))
            else:
                condition_where.add_condition("user_id=%s")
                params.append(user_ids)
                is_only_one = True
        user_asset_model = UserAssetModel(context=self.context)
        if is_cache == True and is_only_one == True:
            user_asset_dict_list = user_asset_model.get_cache_dict_list(condition_where.to_string(), params=params, dependency_key=DependencyKey.user_asset(act_id, user_ids))
        else:
            user_asset_dict_list = user_asset_model.get_dict_list(condition_where.to_string(), params=params)
        if len(user_asset_dict_list) > 0:
            for user_asset_dict in user_asset_dict_list:
                user_asset_dict = self.check_and_reset_asset(user_asset_dict, app_id)
        return user_asset_dict_list

    def get_user_asset(self, app_id, act_id, user_id, asset_type, asset_object_id="", is_cache=False):
        """
        :description: 获取具体的用户资产
        :param app_id：应用标识
        :param act_id：活动标识
        :param user_id：用户标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param asset_object_id：资产对象标识,没有传空
        :param is_cache：是否缓存
        :return: 返回单条字典
        :last_editors: yy
        """
        if not user_id or not asset_type:
            return None
        user_asset_model = UserAssetModel(context=self.context)
        user_asset_id_md5 = self.get_user_asset_id_md5(app_id, act_id, user_id, asset_type, asset_object_id)
        if is_cache == True:
            user_asset_dict = user_asset_model.get_cache_dict("id_md5=%s", limit="1", params=[user_asset_id_md5], dependency_key=DependencyKey.user_asset(act_id, user_id))
        else:
            user_asset_dict = user_asset_model.get_dict("id_md5=%s", limit="1", params=[user_asset_id_md5])
        user_asset_dict = self.check_and_reset_asset(user_asset_dict, app_id)
        return user_asset_dict

    def get_asset_log_list(self, app_id, act_id, asset_type=0, page_size=20, page_index=0, user_id=0, asset_object_id="", start_date="", end_date="", user_nick="", open_id="", source_type=0, source_object_id=None, field="*", is_cache=True, operate_type=-1, page_count_mode="total", module_id=0):
        """
        :description: 获取用户资产流水记录
        :param app_id：应用标识
        :param act_id：活动标识
        :param asset_type：资产类型(1-次数2-积分3-价格档位)
        :param page_size：条数
        :param page_index：页数
        :param user_id：用户标识
        :param asset_object_id：资产对象标识
        :param start_date：开始时间
        :param end_date：结束时间
        :param user_nick：昵称
        :param open_id：open_id
        :param source_type：来源类型（1-购买2-任务3-手动配置4-抽奖5-回购）
        :param source_object_id：来源对象标识(比如来源类型是任务则对应任务类型)
        :param field：查询字段
        :param is_cache：是否缓存
        :param operate_type：操作类型 （0累计 1消耗）
        :param page_count_mode: 分页计数模式 total-计算总数(默认) next-计算是否有下一页(bool) none-不计算
        :param module_id: 模块标识
        :return: 
        :last_editors: yy
        """
        page_list = []

        condition_where = ConditionWhere()
        params = []
        if app_id:
            condition_where.add_condition("app_id=%s")
            params.append(app_id)
        if act_id != 0:
            condition_where.add_condition("act_id=%s")
            params.append(act_id)
        if module_id != 0:
            condition_where.add_condition("module_id=%s")
            params.append(module_id)
        if asset_type != 0:
            condition_where.add_condition("asset_type=%s")
            params.append(asset_type)
        if user_id != 0:
            condition_where.add_condition("user_id=%s")
            params.append(user_id)
        if open_id:
            condition_where.add_condition("open_id=%s")
            params.append(open_id)
        if user_nick:
            condition_where.add_condition("user_nick=%s")
            params.append(user_nick)
        if asset_object_id:
            condition_where.add_condition("asset_object_id=%s")
            params.append(asset_object_id)
        if start_date:
            condition_where.add_condition("create_date>=%s")
            params.append(start_date)
        if end_date:
            condition_where.add_condition("create_date<=%s")
            params.append(end_date)
        if source_type:
            if type(source_type) == str:
                condition_where.add_condition(CoreHelper.get_condition_by_int_list("source_type",[int(item) for item in source_type.split(",")]))
            elif type(source_type) == list:
                condition_where.add_condition(CoreHelper.get_condition_by_int_list("source_type",source_type))
            else:
                condition_where.add_condition("source_type=%s")
                params.append(source_type)
        if operate_type != -1:
            condition_where.add_condition("operate_type=%s")
            params.append(operate_type)
        if source_object_id:
            if type(source_object_id) == str:
                condition_where.add_condition(CoreHelper.get_condition_by_str_list("source_object_id",source_object_id.split(",")))
            elif type(source_object_id) == list:
                condition_where.add_condition(CoreHelper.get_condition_by_str_list("source_object_id",source_object_id))
            else:
                condition_where.add_condition("source_object_id=%s")
                params.append(source_object_id)
        asset_log_model = AssetLogModel(context=self.context, is_auto=True)
        if is_cache:
            page_list = asset_log_model.get_cache_dict_page_list(field, page_index, page_size, condition_where.to_string(), order_by="id desc", params=params, dependency_key=DependencyKey.asset_log_list(act_id, user_id), page_count_mode=page_count_mode)
        else:
            page_list = asset_log_model.get_dict_page_list(field, page_index, page_size, condition_where.to_string(), order_by="id desc", params=params, page_count_mode=page_count_mode)
        result = None
        if page_count_mode in ['total','next']:
            result = page_list[1]
            page_list = page_list[0]
        if len(page_list) > 0:
            for item in page_list:
                if SafeHelper.authenticat_app_id(item["app_id"], app_id) == False:
                    if page_count_mode == 'total':
                        return [], 0
                    elif page_count_mode == 'next':
                        return [], False
                    else:
                        return []
                item["create_day"] = TimeHelper.format_time_to_datetime(str(item["create_date"])).strftime('%Y-%m-%d')
                if item.__contains__("info_json"):
                    item["info_json"] = CoreHelper.json_loads(item["info_json"]) if item["info_json"] else {}
                    if isinstance(item["info_json"], dict):
                        item["operate_user_id"] = item["info_json"].get("operate_user_id","")
                        item["operate_user_name"] = item["info_json"].get("operate_user_name","")
                    else:
                        item["operate_user_id"] = ""
                        item["operate_user_name"] = ""
        if page_count_mode in ['total','next']:
            return page_list, result
        return page_list



        