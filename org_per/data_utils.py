# -*- coding:utf-8 -*-

import cPickle
from prepare_data import THRESHOLD

class DataBatch():
    def __init__(self, max_length=100, batch_size=20, data_type='train'):
        self.index = 0
        self.input_size = 0
        self.batch_size = batch_size
        self.max_length = max_length
        self.data_type = data_type
        self.data = []
        self.batch_data = []
        self.vocab = {"unk": 0}
        # self.tag_map = {"O":0, "B-ORG":1, "I-ORG":2, "E-ORG":3, "B-PER":4, "I-PER":5, "E-PER":6, "S":7}
        self.tag_map = {}

        if data_type == "train":
            self.data_path = "data/train"
        elif data_type == "dev":
            self.data_path = "data/dev"
            self.load_data_map()
        elif data_type == "test":
            self.data_path = "data/test"
            self.load_data_map()

        self.load_data()
        self.prepare_batch()

    def load_data_map(self):
        f = open("data/data_map.pkl", "rb")
        self.data_map = cPickle.load(f)
        f.close()
        self.vocab = self.data_map.get("vocab", {})
    
    def load_data(self):
        # load data
        # add vocab
        # covert to one-hot
        sentence = []
        target = []
        train_nums = 0
        with open(self.data_path) as f:
            line = f.readline()
            while line:
                train_nums += 1
                line = line.rstrip()
                try:
                    word, tag = line.split()
                    assert word.strip()
                except Exception as error:
                    # word = "unk"
                    # tag = "O"
                    if line == "end":
                        if len(sentence) > 0 and len(sentence) < 500:
                            converted_data = self.convert_tag([sentence, target])
                            self.data.append(converted_data)
                        sentence = []
                        target = []
                    line = f.readline()
                    continue
                #添加字典
                if word not in self.vocab and self.data_type == "train":
                    self.vocab[word] = max(self.vocab.values()) + 1
                sentence.append(self.vocab.get(word, 0))
                target.append(tag)

                # if len(sentence) > self.max_length and tag == "O":
                #     # PAD
                #     converted_data = self.convert_tag([sentence, target])
                #     self.data.append(converted_data)
                #     sentence = []
                #     target = []
                line = f.readline()
        self.input_size = len(self.vocab.values())
        print "-"*50
        print "{} data: {}".format(self.data_type ,len(self.data))
        print "vocab size: {}".format(self.input_size)
        print "unique tag: {}".format(len(self.tag_map.values()))
    
    def convert_tag(self, data):
        # add E-XXX for tags
        # add O-XXX for tags
        _, tags = data
        converted_tags = []
        for _, tag in enumerate(tags[:-1]):
            if tag not in self.tag_map:
                self.tag_map[tag] = len(self.tag_map.keys())
            converted_tags.append(self.tag_map.get(tag))
        converted_tags.append(0)
        data[1] = converted_tags
        assert len(converted_tags) == len(tags), "convert error, the list dosen't match!"
        return data

    def prepare_batch(self):
        '''
            prepare data for batch
        '''
        index = 0
        while True:
            if index+self.batch_size >= len(self.data):
                pad_data = self.pad_data(self.data[-self.batch_size:])
                self.batch_data.append(pad_data)
                break
            else:
                pad_data = self.pad_data(self.data[index:index+self.batch_size])
                index += self.batch_size
                self.batch_data.append(pad_data)
    
    def pad_data(self, data):
        import copy
        pad_data = copy.deepcopy(data)
        max_length = max([len(i[0]) for i in pad_data])
        for i in pad_data:
            i[0] = i[0] + (max_length-len(i[0])) * [0]
            i[1] = i[1] + (max_length-len(i[1])) * [0]
        return pad_data

    def iteration(self):
        idx = 0
        while True:
            yield self.batch_data[idx]
            idx += 1
            if idx > len(self.batch_data)-1:
                idx = 0

    def get_batch(self):
        for data in self.batch_data:
            yield data

    

