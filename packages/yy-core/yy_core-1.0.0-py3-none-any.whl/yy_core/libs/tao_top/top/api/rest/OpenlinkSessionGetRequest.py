'''
Created by auto_sdk on 2018.10.12
'''
from yy_core.tao_top.top.api.base import RestApi
class OpenlinkSessionGetRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.code = None

	def getapiname(self):
		return 'taobao.openlink.session.get'
