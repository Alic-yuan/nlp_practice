from keras.models import Sequential
from keras.layers import Embedding, Bidirectional, LSTM
from keras_contrib.layers import CRF
from bussiness.predictModel import process_data
import pickle
import os

base_Path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
open_data = os.path.join(base_Path, "resource", "data", "ner_pro", "config.pkl")

EMBED_DIM = 200
BiRNN_UNITS = 200


def create_model(train=True):
    if train:
        (train_x, train_y), (test_x, test_y), (vocab, tag_map) = process_data.load_data()
    else:
        with open(open_data, 'rb') as inp:
            (vocab, tag_map) = pickle.load(inp)
    model = Sequential()
    model.add(Embedding(len(vocab) + 1, EMBED_DIM, mask_zero=True))  # mask_zero为True表示要屏蔽0
    model.add(Bidirectional(LSTM(BiRNN_UNITS // 2, return_sequences=True))) #return_sequences为True表示返回全部序列，False表示只返回最后一个序列
    crf = CRF(len(tag_map), sparse_target=True)
    model.add(crf)
    model.summary()
    model.compile('adam', loss=crf.loss_function, metrics=[crf.accuracy])
    if train:
        return model, (train_x, train_y), (test_x, test_y)
    else:
        return model, (vocab, tag_map)
