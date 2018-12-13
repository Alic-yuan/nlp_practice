# -*- coding:utf-8 -*-
'''

预处理人名

'''
import pandas as pd
import numpy as np
import logging

log_path = "log/preprocess_per.log"
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    filename=log_path,
                    filemode='a')

CLEANED_FILE = open("/home/yanwii/SocialCredits/CompanyName/contacts_name_cleaned.csv", "w")
DUP_LIST = []

def load_per():
    iterr = pd.read_csv("~/SocialCredits/CompanyName/contacts_name.csv", iterator=True, error_bad_lines=False, header=None)
    chunk = iterr.get_chunk(10000)
    total = 0
    while not chunk.empty:
        total += 10000
        print "processing {}".format(total)
        logging.info("processing {}".format(total))
        chunk.columns = ["name"]
        process(chunk)
        chunk = iterr.get_chunk(10000)

def process(chunk):
    for _, group in chunk.iterrows():
        name = decode(group["name"])
        if isinstance(name, float): continue
        if len(name) < 5:
            DUP_LIST.append(name)
            CLEANED_FILE.write("{}\n".format(name.encode("utf-8")))

def decode(name):
    if isinstance(name, str):
        name = name.decode("utf-8")
    return name

load_per()
CLEANED_FILE.close()






