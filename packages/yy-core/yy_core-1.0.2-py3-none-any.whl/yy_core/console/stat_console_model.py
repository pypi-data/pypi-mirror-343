# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-19 13:37:16
@LastEditTime: 2025-04-23 16:34:50
@LastEditors: yy
@Description: 
"""
import threading, multiprocessing
from yy_core.console.base_console import *
from yy_core.libs.common import *
from yy_core.models.frame_base_model import *
from yy_core.libs.customize.core_helper import *
from yy_core.models.db_models.stat.stat_orm_model import *
from yy_core.models.db_models.stat.stat_report_model import *
from yy_core.models.db_models.stat.stat_log_model import *

class StatConsoleModel():
    """
    :description: 统计控制台业务模型
    """
    def __init__(self):
        """
        :description: 初始化
        :return: 
        :last_editors: yy
        """
        self.db_connect_key, self.redis_config_dict = CoreHelper.get_connect_config("db_stat","redis_stat")


    def _process_redis_stat_queue(self, mod_value):
        """
        :description: 处理redis统计队列
        :param mod_value: 当前队列值
        :return: 
        :last_editors: yy
        """
        print(f"{TimeHelper.get_now_format_time()} 统计队列{mod_value}启动")

        while True:
            try:
                time.sleep(0.1)
                redis_init = CoreHelper.redis_init(config_dict=self.redis_config_dict)
                redis_stat_key = f"stat_queue_list:{mod_value}"
                check_redis_stat_key = f"stat_queue_list:check:{mod_value}"
                stat_queue_json = redis_init.rpoplpush(redis_stat_key, check_redis_stat_key)
                if not stat_queue_json:
                    time.sleep(1)
                    continue
                try:
                    stat_queue_dict = CoreHelper.json_loads(stat_queue_json)
                    db_transaction = DbTransaction(db_config_dict=config.get_value(self.db_connect_key))
                    stat_orm_model = StatOrmModel(is_auto=True)
                    stat_report_model = StatReportModel(db_transaction=db_transaction)
                    stat_orm = stat_orm_model.get_cache_entity("((act_id=%s and module_id=%s and object_id=%s) or (act_id=0 and module_id=0 and object_id='')) and key_name=%s", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_queue_dict.get("object_id", ''), stat_queue_dict["key_name"]])
                    if not stat_orm:
                        redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)
                        continue
                    create_date = TimeHelper.format_time_to_datetime(stat_queue_dict["create_date"])
                    create_day_int = int(create_date.strftime('%Y%m%d'))
                    create_month_int = int(create_date.strftime('%Y%m'))
                    create_year_int = int(create_date.strftime('%Y'))
                    stat_log_model = StatLogModel(db_transaction=db_transaction).set_sub_table(stat_queue_dict["app_id"])
                    is_add = True
                    if stat_orm.repeat_type > 0:
                        if stat_orm.repeat_type == 2:
                            stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and object_id=%s", field="id", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_orm.id, stat_queue_dict["user_id"], stat_queue_dict.get("object_id",'')])
                        else:
                            stat_log_dict = stat_log_model.get_cache_dict("act_id=%s and module_id=%s and orm_id=%s and user_id=%s and create_day=%s and object_id=%s", field="id", params=[stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_orm.id, stat_queue_dict["user_id"], create_day_int, stat_queue_dict.get("object_id",'')])
                        if stat_log_dict:
                            is_add = False

                    stat_log = StatLog()
                    stat_log.app_id = stat_queue_dict["app_id"]
                    stat_log.act_id = stat_queue_dict["act_id"]
                    stat_log.module_id = stat_queue_dict["module_id"]
                    stat_log.object_id = stat_queue_dict.get("object_id",'')
                    stat_log.orm_id = stat_orm.id
                    stat_log.user_id = stat_queue_dict["user_id"]
                    stat_log.open_id = stat_queue_dict["open_id"]
                    stat_log.key_value = stat_queue_dict["key_value"]
                    stat_log.create_day = create_day_int
                    stat_log.create_month = create_month_int
                    stat_log.create_date = create_date

                    stat_report_condition = "app_id=%s and act_id=%s and module_id=%s and object_id=%s and key_name=%s and create_day=%s"
                    stat_report_param = [stat_queue_dict["app_id"], stat_queue_dict["act_id"], stat_queue_dict["module_id"], stat_queue_dict.get("object_id",''), stat_queue_dict["key_name"], create_day_int]
                    stat_report_dict = stat_report_model.get_dict(stat_report_condition, params=stat_report_param)

                    if is_add:
                        db_transaction.begin_transaction()
                        if not stat_report_dict:
                            stat_report = StatReport()
                            stat_report.app_id = stat_queue_dict["app_id"]
                            stat_report.act_id = stat_queue_dict["act_id"]
                            stat_report.module_id = stat_queue_dict["module_id"]
                            stat_report.object_id = stat_queue_dict.get("object_id",'')
                            stat_report.key_name = stat_queue_dict["key_name"]
                            stat_report.key_value = stat_queue_dict["key_value"]
                            stat_report.create_date = create_date
                            stat_report.create_year = create_year_int
                            stat_report.create_month = create_month_int
                            stat_report.create_day = create_day_int
                            stat_report_model.add_entity(stat_report)
                        else:
                            key_value = stat_queue_dict["key_value"]
                            stat_report_model.update_table(f"key_value=key_value+{key_value}", stat_report_condition, params=stat_report_param)
                        stat_log_model.add_entity(stat_log)
                        result,message = db_transaction.commit_transaction(True)
                        if result == False:
                            raise Exception("执行事务失败", message)

                    redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)

                except Exception as ex:
                    redis_init.lpush(redis_stat_key, stat_queue_json)
                    redis_init.lrem(check_redis_stat_key, 1, stat_queue_json)
                    if "Duplicate entry" not in traceback.format_exc():
                        logger_error.error(f"统计队列{mod_value}异常,json串:{CoreHelper.json_dumps(stat_queue_dict)},ex:{traceback.format_exc()}")
                    continue

            except Exception as ex:
                logger_error.error(f"统计队列{mod_value}异常,ex:{traceback.format_exc()}")
                time.sleep(5)
