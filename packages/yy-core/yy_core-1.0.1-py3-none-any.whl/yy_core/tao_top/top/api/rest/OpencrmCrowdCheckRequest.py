'''
Created by auto_sdk on 2022.05.09
'''
from yy_core.tao_top.top.api.base import RestApi
class OpencrmCrowdCheckRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.crowd_id = None

	def getapiname(self):
		return 'taobao.opencrm.crowd.check'
