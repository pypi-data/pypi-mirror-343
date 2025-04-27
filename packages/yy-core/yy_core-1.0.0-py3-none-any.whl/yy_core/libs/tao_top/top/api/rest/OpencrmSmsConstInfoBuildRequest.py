'''
Created by auto_sdk on 2023.03.14
'''
from yy_core.tao_top.top.api.base import RestApi
class OpencrmSmsConstInfoBuildRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.request_info = None

	def getapiname(self):
		return 'taobao.opencrm.sms.const.info.build'
