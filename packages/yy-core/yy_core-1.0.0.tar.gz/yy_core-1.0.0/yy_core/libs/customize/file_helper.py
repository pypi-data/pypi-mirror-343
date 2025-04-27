# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2021-07-15 11:30:45
@LastEditTime: 2023-11-20 17:40:50
@LastEditors: yy
@Description: 
"""
from yy_core import *
from yy_core.libs.common import *


class OSSHelper:
    """
    :description: 阿里云存储帮助类 上传文件、数据导入excel并返回下载地址
    :param {type} 
    :return: 
    :last_editors: yy
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_oss_config(self):
        oss_config = share_config.get_value("oss_config", {})
        self.ak_id = oss_config.get("ak_id", "")
        self.ak_secret = oss_config.get("ak_secret", "")
        self.bucket_name = oss_config.get("bucket_name", "")
        self.end_point = oss_config.get("end_point", "")
        self.domain = oss_config.get("domain", "")
        if not self.domain:
            self.domain = oss_config.get("demain", "")
        self.folder = oss_config.get("folder", "")

    @classmethod
    def upload(self, file_name, local_file='', folder='', is_auto_name=True, data=None):
        """
        :description: 上传文件
        :param file_name：文件名称
        :param local_file：本地文件地址
        :param folder：本地文件地址
        :param is_auto_name：是否生成随机文件名
        :param data：需要上传的数据
        :return: 
        :last_editors: yy
        """
        import oss2
        import os
        self.get_oss_config()
        # 文件名
        file_name = os.path.basename(local_file) if local_file != "" else file_name

        if is_auto_name:
            file_extension = os.path.splitext(file_name)[1]
            file_name = str(int(time.time())) + UUIDHelper.get_uuid() + file_extension

        auth = oss2.Auth(self.ak_id, self.ak_secret)
        bucket = oss2.Bucket(auth, self.end_point, self.bucket_name)
        if not folder:
            folder = self.folder
        folder = folder.strip('/')
        folder = folder + "/" if folder != "" else folder
        file_name = folder + file_name

        # 上传文件
        # 如果需要上传文件时设置文件存储类型与访问权限，请在put_object中设置相关headers, 参考如下。
        # headers = dict()
        # headers["x-oss-storage-class"] = "Standard"
        # headers["x-oss-object-acl"] = oss2.OBJECT_ACL_PRIVATE
        # result = bucket.put_object('<yourObjectName>', 'content of object', headers=headers)
        if local_file:
            result = bucket.put_object_from_file(file_name, local_file)
        else:
            result = bucket.put_object(file_name, data)

        resource_path = ''
        if result.status == 200:
            resource_path = self.domain + file_name
            # # HTTP返回码。
            # print('http status: {0}'.format(result.status))
            # # 请求ID。请求ID是请求的唯一标识，强烈建议在程序日志中添加此参数。
            # print('request_id: {0}'.format(result.request_id))
            # # ETag是put_object方法返回值特有的属性。
            # print('ETag: {0}'.format(result.etag))
            # # HTTP响应头部。
            # print('date: {0}'.format(result.headers['date']))

        return resource_path

    @classmethod
    def export_excel(self, import_data):
        """
        :description: 把数据导入excel并返回下载地址
        :param import_data:导入数据
        :return excel下载地址
        :last_editors: yy
        """
        resource_path = ""
        if import_data:
            try:
                if not os.path.exists("temp"):
                    os.makedirs("temp")
                path = "temp/" + UUIDHelper.get_uuid() + ".xlsx"
                ExcelHelper.export(import_data, path)
                resource_path = self.upload("", path, share_config.get_value("oss_folder"), False)
                os.remove(path)
            except Exception as ex:
                self.logger_error.error("【数据导入excel】" + traceback.format_exc())
        return resource_path


class COSHelper:
    """
    :description: 腾讯云存储帮助类 上传文件、数据导入excel并返回下载地址
    :param {type} 
    :return: 
    :last_editors: yy
    """
    logger_error = Logger.get_logger_by_name("log_error")

    @classmethod
    def get_cos_config(self):
        oss_config = share_config.get_value("cos_config", {})
        self.access_key = oss_config.get("access_key", "")
        self.secret_key = oss_config.get("secret_key", "")
        self.bucket_name = oss_config.get("bucket_name", "")
        if not self.bucket_name:
            self.bucket_name = oss_config.get("bucket", "")
        self.end_point = oss_config.get("end_point", "")
        self.domain = oss_config.get("domain", "")
        self.folder = oss_config.get("folder", "")

    @classmethod
    def upload(self, file_name, data=None, is_auto_name=True):
        """
        :description:上传文件
        :param file_name：文件名称
        :param data：需要上传的数据
        :param is_auto_name: 是否生成随机文件名
        :return: 
        :last_editors: yy
        """
        from yy_core.file import COSHelper
        self.get_cos_config()
        if is_auto_name == True:
            file_extension = os.path.splitext(file_name)[1]
            file_name = str(int(time.time())) + UUIDHelper.get_uuid() + file_extension
        object_name = self.folder + "/" + file_name
        result = COSHelper(self.access_key, self.secret_key, self.end_point).put_file(self.bucket_name, object_name, data)
        if result == True:
            return self.domain + "/" + object_name
        else:
            return ""

    @classmethod
    def put_file_from_file_path(self, local_file=''):
        """
        :description:上传文件根据路径
        :param local_file：本地文件地址
        :return: 
        :last_editors: yy
        """
        from yy_core.file import COSHelper
        self.get_cos_config()
        file_name = os.path.basename(local_file)
        object_name = self.folder + "/" + file_name
        result = COSHelper(self.access_key, self.secret_key, self.end_point).put_file_from_file_path(self.bucket_name, object_name, local_file)
        if result == True:
            return self.domain + "/" + object_name
        else:
            return ""

    @classmethod
    def export_excel(self, import_data):
        """
        :description: 把数据导入excel并返回下载地址
        :param import_data:导入数据
        :return excel下载地址
        :last_editors: yy
        """
        resource_path = ""
        if import_data:
            try:
                if not os.path.exists("temp"):
                    os.makedirs("temp")
                path = "temp/" + UUIDHelper.get_uuid() + ".xlsx"
                ExcelHelper.export(import_data, path)
                resource_path = self.put_file_from_file_path(path)
                os.remove(path)
            except Exception as ex:
                self.logger_error.error("【数据导入excel】" + traceback.format_exc())
        return resource_path
