# 引入包
import random
import jieba
import pandas as pd
import numpy as np

# 加载停用词
stopwords = pd.read_csv('stopwords2.txt', index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
stopwords = stopwords['stopword'].values

# 加载语料
laogong_df = pd.read_csv('beilaogongda.csv', encoding='utf-8', sep=',')
laopo_df = pd.read_csv('beilaogongda.csv', encoding='utf-8', sep=',')
erzi_df = pd.read_csv('beierzida.csv', encoding='utf-8', sep=',')
nver_df = pd.read_csv('beinverda.csv', encoding='utf-8', sep=',')
# print(laogong_df)
# 删除语料的nan行
laogong_df.dropna(inplace=True)
laopo_df.dropna(inplace=True)
erzi_df.dropna(inplace=True)
nver_df.dropna(inplace=True)
# 转换
laogong = laogong_df.segment.values.tolist()
laopo = laopo_df.segment.values.tolist()
erzi = erzi_df.segment.values.tolist()
nver = nver_df.segment.values.tolist()
# print(laogong)

# 定义分词和打标签函数preprocess_text
# 参数content_lines即为上面转换的list
# 参数sentences是定义的空list，用来储存打标签之后的数据
# 参数category 是类型标签
def preprocess_text(content_lines, sentences, category):
    for line in content_lines:
        try:
            segs = jieba.lcut(line)
            segs = [v for v in segs if not str(v).isdigit()]  # 去数字
            segs = list(filter(lambda x: x.strip(), segs))  # 去左右空格
            segs = list(filter(lambda x: len(x) > 1, segs))  # 长度为1的字符
            segs = list(filter(lambda x: x not in stopwords, segs))  # 去掉停用词
            sentences.append((" ".join(segs), category))  # 打标签
        except Exception:
            print(line)
            continue

        # 调用函数、生成训练数据


sentences = []
preprocess_text(laogong, sentences, 0)
preprocess_text(laopo, sentences, 1)
preprocess_text(erzi, sentences, 2)
preprocess_text(nver, sentences, 3)
# print(sentences)
# 打散数据，生成更可靠的训练集
random.shuffle(sentences)
#
# 控制台输出前10条数据，观察一下
# for sentence in sentences[:10]:
#     print(sentence[0], sentence[1])
# 所有特征和对应标签
all_texts = [sentence[0] for sentence in sentences]
all_labels = [sentence[1] for sentence in sentences]
#
# 引入需要的模块
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.utils import to_categorical
from keras.layers import Dense, Input, Flatten, Dropout
from keras.layers import LSTM, Embedding, GRU
from keras.models import Sequential
#
# 预定义变量
MAX_SEQUENCE_LENGTH = 100  # 最大序列长度
EMBEDDING_DIM = 200  # embdding 维度
VALIDATION_SPLIT = 0.16  # 验证集比例
TEST_SPLIT = 0.2  # 测试集比例
# # keras的sequence模块文本序列填充
tokenizer = Tokenizer()
tokenizer.fit_on_texts(all_texts)
sequences = tokenizer.texts_to_sequences(all_texts)
# print(sequences)
word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))
data = pad_sequences(sequences, maxlen=MAX_SEQUENCE_LENGTH)
# print(data)
# print(all_labels)
# print(np.asarray(all_labels))
labels = to_categorical(np.asarray(all_labels))
# print(labels)
print('Shape of data tensor:', data.shape)
print('Shape of label tensor:', labels.shape)
#
# # 数据切分
p1 = int(len(data) * (1 - VALIDATION_SPLIT - TEST_SPLIT))
p2 = int(len(data) * (1 - TEST_SPLIT))
x_train = data[:p1]
y_train = labels[:p1]
x_val = data[p1:p2]
y_val = labels[p1:p2]
x_test = data[p2:]
y_test = labels[p2:]
# print(labels.shape[0])
#
# LSTM训练模型
model = Sequential()
model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
model.add(LSTM(200, dropout=0.2, recurrent_dropout=0.2))
model.add(Dropout(0.2))
model.add(Dense(64, activation='relu'))
model.add(Dense(labels.shape[1], activation='softmax'))
model.summary()
# 模型编译
model.compile(loss='categorical_crossentropy',
              optimizer='rmsprop',
              metrics=['acc'])
print(model.metrics_names)
model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, batch_size=128)
model.save('lstm.h5')
# 模型评估
print(model.evaluate(x_test, y_test))
#
# model = Sequential()
# model.add(Embedding(len(word_index) + 1, EMBEDDING_DIM, input_length=MAX_SEQUENCE_LENGTH))
# model.add(GRU(200, dropout=0.2, recurrent_dropout=0.2))
# model.add(Dropout(0.2))
# model.add(Dense(64, activation='relu'))
# model.add(Dense(labels.shape[1], activation='softmax'))
# model.summary()
#
# model.compile(loss='categorical_crossentropy',
#               optimizer='rmsprop',
#               metrics=['acc'])
# print(model.metrics_names)
# model.fit(x_train, y_train, validation_data=(x_val, y_val), epochs=10, batch_size=128)
# model.save('lstm.h5')
#
# print(model.evaluate(x_test, y_test))
