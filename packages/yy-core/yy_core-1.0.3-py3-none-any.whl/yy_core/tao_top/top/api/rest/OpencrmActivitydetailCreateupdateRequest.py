'''
Created by auto_sdk on 2023.12.19
'''
from yy_core.tao_top.top.api.base import RestApi
class OpencrmActivitydetailCreateupdateRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.activity_id = None
		self.nodes = None

	def getapiname(self):
		return 'taobao.opencrm.activitydetail.createupdate'
