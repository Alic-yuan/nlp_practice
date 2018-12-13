# -*- coding:utf-8 -*-
'''
@Author: yuan
@Date: 2018-03-26 14:59:39

NER方法通用模型

'''
from bussiness.predictModel import bilsm_crf_model, process_data
from sclog.logger import get_logger
import os
import numpy as np


base_Path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
open_model = os.path.join(base_Path, "nlp-service", "resource", "models", "ner_pro", "crf.h5")


LOGGER = get_logger()
class Model(object):
    """
    实体抽取通用模型
    """
    def __init__(self):
        self.model, (self.vocab, self.tag_map) = bilsm_crf_model.create_model(train=False)

    def predict(self, content, tags=[]):
        """
        预测
        """
        str, length = process_data.process_data(content, self.vocab)
        self.model.load_weights(open_model)
        raw = self.model.predict(str)[0]
        result = [np.argmax(row) for row in raw]
        resp = {}
        for tag in tags:
            ner = self.get_tags(result, tag, self.tag_map)
            ner_entity = self.format_result(ner, content, tag)
            resp[tag] = ner_entity.get("entities", [])
        return resp

    def format_result(self, result, text, tag): 
        entities = [] 
        for i in result: 
            begin, end = i
            entities.append({ 
                "start":begin, 
                "stop":end + 1, 
                "word":text[begin:end+1],
                "type":tag
            }) 
        return {"entities":entities} 

    def get_tags(self, path, tag, tag_map):
        """
        整理tag
        """
        begin_tag = tag_map.get("B-" + tag)
        mid_tag = tag_map.get("I-" + tag)
        end_tag = tag_map.get("E-" + tag)
        single_tag = tag_map.get("S")
        all_tag = [begin_tag, end_tag, single_tag]
        o_tag = tag_map.get("O")
        begin = -1
        end = 0
        tags = []
        last_tag = 0

        for index, tag in enumerate(path):
            if tag == begin_tag and index == 0:
                begin = 0
            elif tag == begin_tag:
                begin = index
            elif tag == end_tag and last_tag in [mid_tag, begin_tag] and begin > -1:
                end = index
                tags.append([begin, end])
            elif tag == o_tag or tag == single_tag:
                begin = -1
            last_tag = tag
        return tags