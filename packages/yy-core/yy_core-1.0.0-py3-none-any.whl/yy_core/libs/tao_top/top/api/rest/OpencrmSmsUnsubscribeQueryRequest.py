'''
Created by auto_sdk on 2022.10.13
'''
from yy_core.tao_top.top.api.base import RestApi
class OpencrmSmsUnsubscribeQueryRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.mobile = None

	def getapiname(self):
		return 'taobao.opencrm.sms.unsubscribe.query'
