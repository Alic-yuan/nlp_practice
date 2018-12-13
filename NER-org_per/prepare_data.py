# -*- coding:utf-8 -*-

import json
import os
import requests
import sys
import pydat
from scnlp import ner_extraction
from threading import Lock
import re

LOCK = Lock()

# dat = pydat.Dat()
# dat.add_word("he")
# dat.make()
# print dat.search("sdfsdfhesdfsdfhe")
#
# exit()



THRESHOLD = 4

class PrepareData():
    def __init__(self):
        self.train_path = "data/trainset"
        self.train_data_io = open(self.train_path, "a")
        self.news = []
        self.load_news()
        self.ner_model = ner_extraction.NerOrgandper()

    def load_news(self):
        # list_dir = os.listdir(base_path)
        # for second_path in list_dir:
        #     news_files = os.listdir(os.path.join(base_path, second_path))
        #     for news in news_files:
        #         self.news.append(
        #             os.path.join(base_path, second_path, news)
        #         )
        base_path = "/home/yuan/classifyData_bak"
        news_files = os.listdir(base_path)
        for news in news_files:
            self.news.append(os.path.join(base_path, news))
        print "-"*50
        print "一共有 {} 篇新闻".format(len(self.news))
        print "-"*50

    def read(self, news_path):
        news_path = news_path.replace("s3_data", "raw_news_s3")
        with open(news_path) as f:
            news = f.read()
            news = news.decode("utf-8")
            news = news.strip()
            news = news.replace(" ", "")
            news = news.replace(u" ", "")
            news = re.sub(r"\n", "", news)
            return news
    
    def org_extraction(self, sent):
        org = self.org_model.full_predict(sent)
        replaced = []
        for i in org:
            replaced.append({
                "begin":i.get("start"),
                "end":i.get("stop"),
                "type":i.get("entityType"),
                "entity":i.get("word")
            })
        return replaced
    
    def per_extraction(self, sent):
        per = self.per_model.predict(sent)
        entities = []
        for i in per:
            if i.get("word") not in entities:
                entities.append(i.get("word"))
        dat = pydat.Dat()
        [dat.add_word(i.encode("utf-8")) for i in entities]
        dat.make()
        entities = dat.search(sent.encode("utf-8"))
        for entity in entities.get("entities", []):
            entity["type"] = "PER"
        return entities.get("entities", [])

    def ner_extraction(self, sent):
        ner = self.ner_model.predict(sent)
        for i in ner.get("PER", []):
            i["begin"] = i.pop("start")
            i["end"] = i.pop("stop")
        for i in ner.get("ORG", []):
            i["begin"] = i.pop("start")
            i["end"] = i.pop("stop")
        return ner

    def make_tag(self, sent, entities, tag, entity_tag=[]):
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
                if entity_tag[i] not in ["O", "S"]:
                    break
                if index == 0:
                    entity_tag[i] = b_tag
                elif i == (end-1):
                    entity_tag[i] = e_tag
                else:
                    entity_tag[i] = m_tag
            prethreshold = THRESHOLD if THRESHOLD <= begin else end
            aftthreshold = THRESHOLD if THRESHOLD <= len(sent) - end else len(sent) - end

            if b_tag not in entity_tag:
                continue
            
            # for j in range(begin - prethreshold, begin):
            #     if j < 0: continue
            #     if entity_tag[j] == "O":
            #         entity_tag[j] = "S"
            # for j in range(end, end + aftthreshold):
            #     if j >= len(entity_tag):break
            #     if entity_tag[j] == "O":
            #         entity_tag[j] = "S"
        return entity_tag

    def save(self, tagged):
        for word, tag in tagged:
            if word == "\n" or word == " " or word == u" ":
                print word
            self.train_data_io.write("%s %s\n" % (word.encode("utf-8"), tag))
        self.train_data_io.write("end\n")

    def run(self, news_path):
        print "processing %s" % news_path
        try:
            news = self.read(news_path)
        except:
            return
        if news:
            news_sentences = news.split(u"。")
            for _, sent in enumerate(news_sentences):
                if len(sent) > 500 or not sent.strip():
                    continue
                sent = sent.strip()
                ner = self.ner_extraction(sent)
                org = ner.get("ORG", [])
                per = ner.get("PER", [])
                entity_tag = self.make_tag(sent, org, "ORG")
                entity_tag = self.make_tag(sent, per, "PER", entity_tag)
                if not entity_tag:
                    continue
                tagged = list(zip(sent, entity_tag))
                LOCK.acquire()
                self.save(tagged)
                LOCK.release()
                sys.stdout.flush()

    def main(self):
        import threadpool
        task_pool = threadpool.ThreadPool(20)
        request = threadpool.makeRequests(self.run, self.news)
        [task_pool.putRequest(req) for req in request]
        task_pool.wait()

    def __del__(self):
        self.train_data_io.close()
    
if __name__ == "__main__":
    pd = PrepareData()
    pd.main()
    
