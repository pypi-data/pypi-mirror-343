'''
Created by auto_sdk on 2020.10.14
'''
from yy_core.tao_top.top.api.base import RestApi
class AlibabaBenefitDrawRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.app_name = None
		self.ename = None
		self.ip = None

	def getapiname(self):
		return 'alibaba.benefit.draw'
