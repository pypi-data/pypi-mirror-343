# -*- coding: utf-8 -*-
"""
@Author: yy
@Date: 2024-06-03 09:55:46
@LastEditTime: 2024-06-03 09:56:38
@LastEditors: yy
@Description: 
"""
'''
Created by auto_sdk on 2024.05.22
'''
from yy_core.tao_top.top.api.base import RestApi
class OpenmemberActivitySmsJoinRequest(RestApi):
	def __init__(self,domain='gw.api.taobao.com',port=80):
		RestApi.__init__(self,domain, port)
		self.member_join_ext_dto = None

	def getapiname(self):
		return 'taobao.openmember.activity.sms.join'
