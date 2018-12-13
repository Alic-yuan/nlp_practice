# -*- coding:utf-8 -*-
'''
@Author: yanwii
@Date: 2018-08-01 10:14:35

计算f1 score
'''

import requests
import json
import sys


class F1Score(object):
    
    def __init__(self):
        self.tag_map = {}
        self.url_map = {
            # "org_per":"http://54.222.133.167:5001/api/nlp/ner",
            # "org_per":"http://192.168.31.116:5000/api/nlp/ner",
            # "S-ORG":"http://192.168.31.116:5000/api/nlp/orgShort"
            "PRO":"http://127.0.0.1:5000/api/nlp/pro"
            # "S-ORG":"http://54.222.133.167:5000/api/nlp/orgShort"
        }

    def get_tags(self, data, tag, tag_map):
        content = "".join([i[0] for i in data])
        path = [i[1] for i in data]
        
        # begin_tag = tag_map.get("B-" + tag)
        # mid_tag = tag_map.get("I-" + tag)
        # end_tag = tag_map.get("E-" + tag)
        begin_tag = "B-" + tag
        mid_tag = "I-" + tag
        end_tag = "E-" + tag

        single_tag = tag_map.get("S", 0)
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
                tags.append({
                    "word":content[begin: end+1],
                    "start":begin,
                    "stop":end+1,
                })
            elif tag == o_tag or tag == single_tag:
                begin = -1
            last_tag = tag
        return tags

    def load_data(self):
        with open("data/test_bosen3") as fopen:
            lines = fopen.readlines()

            begin = 0 
            end = 0

            data = []
            tmp = []
            for line in lines:
                line = line.rstrip()
                if line == "end":
                    data.append(tmp)
                    tmp = []
                    continue
                try:
                    word, tag = line.split()
                    if tag not in self.tag_map:
                        self.tag_map[tag] = len(self.tag_map.keys())
                except Exception:
                    continue
                tmp.append([word, tag])
            return data

    def predict(self, data, url):
        content = "".join([i[0] for i in data])
        # print(content)
        try:
            data = {
                "content": content,
                # "entityType":0
            }
            # print(data)
            page = requests.post(url, timeout=10, data=json.dumps(data))
            # page = requests.post('http://127.0.0.1:5000/api/nlp/ner', timeout=10, data=json.dumps(data))
            entities = page.json().get("data", [])
            if not entities:
                entities = []
            return entities
        except Exception:
            raise Exception("抽取接口请求错误")

    
    def evaluate(self, model="pro"):
        if model == "pro":
            self.pro()
        else:
            self.normal(model)


    def normal(self, entity_type):
        data = self.load_data()
        print("一共有 {} 条语料".format(len(data)))
        origin = 0.
        found = 0.
        right = 0.
        
        url = self.url_map.get(entity_type)
        assert url, Exception("request url error")
        for index, fetch in enumerate(data):
            pre = self.predict(fetch, url)
            [i.pop("type") for i in pre]

            tar_entities = self.get_tags(fetch, entity_type, self.tag_map)

            content = "".join([i[0] for i in fetch])
            
            found += len(pre)
            origin += len(tar_entities)

            for p in pre:
                if p in tar_entities:
                    right += 1
                # else:
                #     print(p)
                #     print(pre)
                #     print(tar_entities)
                #     print(content)
                #     print("-"*50)
            for t in tar_entities:
                if t not in pre:
                    print(pre)
                    print(tar_entities)
                    print(content)
                    print("-"*50)

        self.f1_score(origin, found, right, entity_type)


    def pro(self):
        data = self.load_data()
        print("一共有 {} 条语料".format(len(data)))
        per_origin = 0.
        per_found = 0.
        per_right = 0.

        # org_origin = 0.
        # org_found = 0.
        # org_right = 0.
        #
        # org2_origin = 0.
        # org2_found = 0.
        # org2_right = 0.

        url = self.url_map.get("PRO")
        assert url, Exception("request url not found")
        for index, fetch in enumerate(data):
            # print(fetch, url)
            entities = self.predict(fetch, url)
            entities = entities.get('PRO')
            # pre_org = []
            # pre_org2 = []
            pre_per = []
            for entity in entities:
                tmp = {
                    "word":entity.get("word"),
                    "start":entity.get("start"),
                    "stop":entity.get("stop"),
                }
                if entity.get("type") == "PRO":
                    pre_per.append(tmp)
                # elif entity.get("type") == "ORG2":
                #     pre_org2.append(tmp)
                # else:
                #     pre_per.append(tmp)
            per_tar_entities = self.get_tags(fetch, "PRO", self.tag_map)
            # org_tar_entities = self.get_tags(fetch, "ORG", self.tag_map)
            # org2_tar_entities = self.get_tags(fetch, "ORG2", self.tag_map)
            per_found += len(pre_per)
            # org_found += len(pre_org)
            # org2_found += len(pre_org2)

            per_origin += len(per_tar_entities)
            # org_origin += len(org_tar_entities)
            # org2_origin += len(org2_tar_entities)

            # for pre in pre_org:
            #     if pre in org_tar_entities:
            #         org_right += 1
            #     else:
            #         print(org_tar_entities)
            #         print(pre)
            # for pre in pre_org2:
            #     if pre in org2_tar_entities:
            #         org2_right += 1
                # else:
                #     print(org2_tar_entities)
                #     print(pre)
            for pre in pre_per:
                if pre in per_tar_entities:
                    per_right += 1
                else:
                    content = "".join([i[0] for i in fetch])
                    print(content)
                    print(per_tar_entities)
                    print(pre)
        self.f1_score(per_origin, per_found, per_right, "PRO")
        # self.f1_score(org_origin, org_found, org_right, "ORG")
        # self.f1_score(org2_origin, org2_found, org2_right, "ORG2")

    def f1_score(self, origin, found, right, tag):
        recall = 0 if origin == 0 else right / origin
        precision = 0 if found == 0 else right / found
        f1 = 0 if (recall + precision) == 0 else (2 * recall * precision) / (recall + precision)
        print("{}   total: {}           found: {}              right: {}".format(
            tag, origin, found, right
        ))
        print("{}   recall: {:.2f}      precision: {:.2f}      f1:{:.2f}".format(
            tag, recall, precision, f1
        ))


if __name__ == "__main__":
    f1 = F1Score()
    if len(sys.argv) < 2:
        exit()
    f1.evaluate(sys.argv[1])
    # print(f1.get_tags([["你", 1], ["好", 3]], "PER", {"B-PER":1, "I-PER":2, "E-PER":3, "O":0}))
