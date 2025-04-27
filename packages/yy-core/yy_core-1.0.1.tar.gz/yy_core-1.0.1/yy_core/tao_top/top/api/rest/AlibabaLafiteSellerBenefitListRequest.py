'''
Created by auto_sdk on 2021.07.20
'''
from yy_core.tao_top.top.api.base import RestApi
class AlibabaLafiteSellerBenefitListRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.benefit_read_top_query = None

	def getapiname(self):
		return 'alibaba.lafite.seller.benefit.list'
