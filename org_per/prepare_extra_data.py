# -*- coding:utf-8 -*-

import pydat
from prepare_data import PrepareData

import cProfile
import pstats

org_dat = pydat.Dat()
per_dat = pydat.Dat()

train_data_io = open("data/extra_trainset", "w")

def load_news():
    with open("data/news") as fopen:
        news = fopen.readlines()
        news = [i.strip() for i in news if i.strip()!= "end"]
        return news

def load_entity():
    with open("data/entity") as fopen:
        for line in fopen.readlines():
            name, etype = line.strip().split()
            if etype == "ORG":
                org_dat.add_word(name)
            elif etype == "PER":
                per_dat.add_word(name)
        org_dat.make()
        per_dat.make()

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
            if entity_tag[i] not in ["O", "S"]:
                break
            if index == 0:
                entity_tag[i] = b_tag
            elif i == (end-1):
                entity_tag[i] = e_tag
            else:
                entity_tag[i] = m_tag
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

def save(tagged):
    for word, tag in tagged:
        train_data_io.write("%s %s\n" % (word.encode("utf-8"), tag))
    train_data_io.write("end\n")

def main():
    news = load_news()
    load_entity()

    for one in news:
        one = one.decode("utf-8")
        org = org_dat.search(one.encode("utf-8")).get("entities")
        per = per_dat.search(one.encode("utf-8")).get("entities")
        entity_tag = make_tag(one, org, "ORG")
        entity_tag = make_tag(one, per, "PER", entity_tag=entity_tag)
        if not entity_tag:
            continue
        tagged = list(zip(one, entity_tag))
        save(tagged)

# main()
# train_data_io.close()
cProfile.run('main()', 'restats')
p = pstats.Stats('restats')
p.sort_stats('cumulative').print_stats(30)