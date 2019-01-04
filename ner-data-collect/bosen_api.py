# -*- encoding: utf-8 -*-
from __future__ import print_function, unicode_literals
import json
import requests
import pydat
import csv
import sys

csv.field_size_limit(sys.maxsize)


open_csv_path = 'product_content_xianxia.csv'
train_data_io = open("data/trainset_xianxia2", "w")

def make_tag(sent, entities, tag, entity_tag=[]):
    b_tag = "B-" + tag
    m_tag = "I-" + tag
    e_tag = "E-" + tag

    if not entities:
        return entity_tag

    if not entity_tag:
        entity_tag = ["O"] * len(sent)

    for match in entities:
        begin = match["begin"]
        end = match["end"]

        for index, i in enumerate(range(begin, end)):
            if entity_tag[i] not in ["O"]:
                break
            if index == 0:
                entity_tag[i] = b_tag
            elif i == (end - 1):
                entity_tag[i] = e_tag
            else:
                entity_tag[i] = m_tag
        if b_tag not in entity_tag:
            continue
    return entity_tag

def save(tagged):
    if tagged:
        for word, tag in tagged:
            # print(word, tag)
            train_data_io.write("%s %s\n" % (word, tag))
        # train_data_io.write("end\n")


NER_URL = 'http://api.bosonnlp.com/ner/analysis'



with open(open_csv_path) as file_list:
    hotels_data = csv.reader(file_list)
    for i, keyword in enumerate(hotels_data):
        try:
            if i % 10 == 0:
                print(i)
            s = []
            # print(keyword[0])
            s.append(keyword[0])
            data = json.dumps(s)
            headers = {'X-Token': '***'}
            proxies = {'http': None, 'https': None}
            resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'), proxies=proxies)

            for item in resp.json():
                content = ''.join(item['word'])
                pros = []
                tims = []
                locs = []
                pers = []
                orgs = []
                coms = []
                jobs = []
                # print(item)
                # b = make_tag(item['entity'])
                for entity in item['entity']:
                    if entity[2] == 'product_name':
                        product_name = ''.join(item['word'][entity[0]:entity[1]])
                        pros.append(product_name)
                    if entity[2] == 'time':
                        tim = ''.join(item['word'][entity[0]:entity[1]])
                        tims.append(tim)
                    if entity[2] == 'location':
                        loc = ''.join(item['word'][entity[0]:entity[1]])
                        locs.append(loc)
                    if entity[2] == 'person_name':
                        per = ''.join(item['word'][entity[0]:entity[1]])
                        pers.append(per)
                    if entity[2] == 'org_name':
                        org = ''.join(item['word'][entity[0]:entity[1]])
                        orgs.append(org)
                    if entity[2] == 'company_name':
                        com = ''.join(item['word'][entity[0]:entity[1]])
                        coms.append(com)
                    if entity[2] == 'job_title':
                        job = ''.join(item['word'][entity[0]:entity[1]])
                        jobs.append(job)
                pros = sorted(list(set(pros)), reverse=True)
                tims = sorted(list(set(tims)), reverse=True)
                locs = sorted(list(set(locs)), reverse=True)
                pers = sorted(list(set(pers)), reverse=True)
                orgs = sorted(list(set(orgs)), reverse=True)
                coms = sorted(list(set(coms)), reverse=True)
                jobs = sorted(list(set(jobs)), reverse=True)
                # print(pros)
                li1 = []
                li2 = []
                li3 = []
                li4 = []
                li5 = []
                li6 = []
                li7 = []
                for c in pros:
                    dat = pydat.Dat()
                    dat.add_word(c)
                    dat.make()
                    a = dat.search(content)
                    li1.extend(a['entities'])
                for t in tims:
                    dat = pydat.Dat()
                    dat.add_word(t)
                    dat.make()
                    a = dat.search(content)
                    li2.extend(a['entities'])
                for l in locs:
                    dat = pydat.Dat()
                    dat.add_word(l)
                    dat.make()
                    a = dat.search(content)
                    li3.extend(a['entities'])
                for p in pers:
                    dat = pydat.Dat()
                    dat.add_word(p)
                    dat.make()
                    a = dat.search(content)
                    li4.extend(a['entities'])
                for o in orgs:
                    dat = pydat.Dat()
                    dat.add_word(o)
                    dat.make()
                    a = dat.search(content)
                    li5.extend(a['entities'])
                for c in coms:
                    dat = pydat.Dat()
                    dat.add_word(c)
                    dat.make()
                    a = dat.search(content)
                    li6.extend(a['entities'])
                for j in jobs:
                    dat = pydat.Dat()
                    dat.add_word(j)
                    dat.make()
                    a = dat.search(content)
                    li7.extend(a['entities'])
                entity_tag = make_tag(content, li1, 'PRO')
                entity_tag = make_tag(content, li2, 'TIME', entity_tag)
                entity_tag = make_tag(content, li3, 'LOC', entity_tag)
                entity_tag = make_tag(content, li4, 'PER', entity_tag)
                entity_tag = make_tag(content, li5, 'ORG', entity_tag)
                entity_tag = make_tag(content, li6, 'COM', entity_tag)
                entity_tag = make_tag(content, li7, 'JOB', entity_tag)
                tagged = list(zip(content, entity_tag))
                save(tagged)
        except Exception:
            continue

# s = ['继前不久始于中国的召回风波，宝马因为车辆的发动机螺栓故障，在全球范围将召回48.9万辆车，在原有中国召回的基础上数量进一步增加。据悉，召回车辆将包括北美市场的15.6万辆，宝马曾于3月宣布在华召回232,098辆发动机螺栓故障车辆。涉及车型包括搭载六缸发动机的宝马5系、5系、X3、X5，。但具体型号Santer并没有透露。宝马发言人Bernhard Santer表示，目前尚无该故障造成事故或伤亡的报告。但他仍建议相关车主及时检查车辆引擎。Santer说，凭借剩余的动力，车辆仍旧可以坚持到最近的修理厂。'
# ]
# data = json.dumps(s)
# headers = {'X-Token': 'QwROUKs8.28048.RnRXWRdn6w-6'}
# resp = requests.post(NER_URL, headers=headers, data=data.encode('utf-8'))
#
#
# for item in resp.json():
#     content = ''.join(item['word'])
#     pros = []
#     tims = []
#     locs = []
#     pers = []
#     orgs = []
#     coms = []
#     jobs = []
#     # print(item)
#     # b = make_tag(item['entity'])
#     for entity in item['entity']:
#         if entity[2] == 'product_name':
#             product_name = ''.join(item['word'][entity[0]:entity[1]])
#             pros.append(product_name)
#         if entity[2] == 'time':
#             tim = ''.join(item['word'][entity[0]:entity[1]])
#             tims.append(tim)
#         if entity[2] == 'location':
#             loc = ''.join(item['word'][entity[0]:entity[1]])
#             locs.append(loc)
#         if entity[2] == 'person_name':
#             per = ''.join(item['word'][entity[0]:entity[1]])
#             pers.append(per)
#         if entity[2] == 'org_name':
#             org = ''.join(item['word'][entity[0]:entity[1]])
#             orgs.append(org)
#         if entity[2] == 'company_name':
#             com = ''.join(item['word'][entity[0]:entity[1]])
#             coms.append(com)
#         if entity[2] == 'job_title':
#             job = ''.join(item['word'][entity[0]:entity[1]])
#             jobs.append(job)
#     pros = sorted(list(set(pros)), reverse=True)
#     tims = sorted(list(set(tims)), reverse=True)
#     locs = sorted(list(set(locs)), reverse=True)
#     pers = sorted(list(set(pers)), reverse=True)
#     orgs = sorted(list(set(orgs)), reverse=True)
#     coms = sorted(list(set(coms)), reverse=True)
#     jobs = sorted(list(set(jobs)), reverse=True)
#     # print(pros)
#     li1 = []
#     li2 = []
#     li3 = []
#     li4 = []
#     li5 = []
#     li6 = []
#     li7 = []
#     for c in pros:
#         dat = pydat.Dat()
#         dat.add_word(c)
#         dat.make()
#         a = dat.search(content)
#         li1.extend(a['entities'])
#     for t in tims:
#         dat = pydat.Dat()
#         dat.add_word(t)
#         dat.make()
#         a = dat.search(content)
#         li2.extend(a['entities'])
#     for l in locs:
#         dat = pydat.Dat()
#         dat.add_word(l)
#         dat.make()
#         a = dat.search(content)
#         li3.extend(a['entities'])
#     for p in pers:
#         dat = pydat.Dat()
#         dat.add_word(p)
#         dat.make()
#         a = dat.search(content)
#         li4.extend(a['entities'])
#     for o in orgs:
#         dat = pydat.Dat()
#         dat.add_word(o)
#         dat.make()
#         a = dat.search(content)
#         li5.extend(a['entities'])
#     for c in coms:
#         dat = pydat.Dat()
#         dat.add_word(c)
#         dat.make()
#         a = dat.search(content)
#         li6.extend(a['entities'])
#     for j in jobs:
#         dat = pydat.Dat()
#         dat.add_word(j)
#         dat.make()
#         a = dat.search(content)
#         li7.extend(a['entities'])
#     entity_tag = make_tag(content, li1, 'PRO')
#     entity_tag = make_tag(content, li2, 'TIME', entity_tag)
#     entity_tag = make_tag(content, li3, 'LOC', entity_tag)
#     entity_tag = make_tag(content, li4, 'PER', entity_tag)
#     entity_tag = make_tag(content, li5, 'ORG', entity_tag)
#     entity_tag = make_tag(content, li6, 'COM', entity_tag)
#     entity_tag = make_tag(content, li7, 'JOB', entity_tag)
#     tagged = list(zip(content, entity_tag))
#     save(tagged)

    #     print(''.join(item['word'][entity[0]:entity[1]]), entity[2])