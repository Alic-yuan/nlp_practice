# encoding=utf-8

import csv
import requests
from bs4 import BeautifulSoup
from readability.readability import Document
from pyquery import PyQuery
import re
import pydat
from tqdm import tqdm
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

open_csv_path = 'product_xianshang.csv'
new_file_path = 'product_content.csv'
# train_data_io = open("data/trainset4", "w")

THRESHOLD = 4

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
        # prethreshold = THRESHOLD if THRESHOLD <= begin else end
        # aftthreshold = THRESHOLD if THRESHOLD <= len(sent) - end else len(sent) - end

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
    if tagged:
        for word, tag in tagged:
            # print word, tag
            train_data_io.write("%s %s\n" % (word, tag))
        # train_data_io.write("end\n")
with open(open_csv_path) as file_list:
    hotels_data = csv.reader(file_list)
    with open(new_file_path, "w") as csvfile:
        writer = csv.writer(csvfile)
        for i, keyword in enumerate(hotels_data):
            headers = {"User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
            if i > 9000:
                if i % 10 == 0:
                    print i
                if i == 9600:
                    break
                try:
                    url = 'http://news.baidu.com/ns?rn=20&ie=utf-8&ct=1&bs={}&rsv_bp=1&sr=0&cl=2&f=8&prevct=no&tn=news&word={}'.format(keyword[0], keyword[0])
                    # print url
                    proxies = {'http': None, 'https': None}
                    response = requests.get(url, timeout=30, headers=headers, proxies=proxies)
                    # print response
                    soup = BeautifulSoup(response.text, 'lxml')
                    url = soup.find('div', class_='result', id='1').find('a')['href']
                    # print url
                    res = requests.get(url=url, timeout=30, headers=headers, proxies=proxies)
                    html = res.content
                    # print html
                    readable_article = Document(html).summary()
                    text_p = re.sub(r'</?[div|a].*?>', '', readable_article)
                    text_p = re.sub(r'<select>.*?</select>', '', text_p)
                    content = PyQuery(readable_article).text()
                    # print content
                    if not content:
                        content = None
                        text_p = None
                        print content
                        continue
                    content = content.encode('utf-8')
                    # print keyword[0]
                    # print(content)
                    writer.writerow([content])
                except Exception:
                    print 'fail'
                    continue


