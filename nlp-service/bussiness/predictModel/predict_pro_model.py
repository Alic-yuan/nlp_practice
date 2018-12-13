# -*- coding:utf-8 -*-
'''
@Author: yuan
@Date: 2018-06-08 16:24:15
'''
from common.ner_model_gru import Model
import json
import requests
import os




class NerPro():

    def __init__(self):
        self.model = Model()


    def predict(self, content):
        resp = self.model.predict(content, tags=["PRO"])
        return resp
