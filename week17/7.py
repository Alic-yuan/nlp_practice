import pandas as pd
import numpy as np
import jieba
import random
import keras
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.layers import Embedding
from keras.layers import Conv1D, GlobalMaxPooling1D
from keras.datasets import imdb
from keras.models import model_from_json
from keras.utils import np_utils
import matplotlib.pyplot as plt



stopwords=pd.read_csv("stopwords.txt",index_col=False,quoting=3,sep="\t",names=['stopword'], encoding='utf-8')
stopwords=stopwords['stopword'].values
df_data1 = pd.read_csv("data1.csv",encoding='utf-8')
df_data1.head()

#把内容有缺失值的删除
df_data1.dropna(inplace=True)
#抽取文本数据和标签
data_1 = df_data1.loc[:,['content','label']]
#把消极  中性  积极分别为0、1、2的预料分别拿出来
data_label_0 = data_1.loc[data_1['label'] ==0,:]
data_label_1 = data_1.loc[data_1['label'] ==1,:]
data_label_2 = data_1.loc[data_1['label'] ==2,:]

#定义分词函数
def preprocess_text(content_lines, sentences, category):
    for line in content_lines:
        try:
            segs=jieba.lcut(line)
            segs = filter(lambda x:len(x)>1, segs)
            segs = [v for v in segs if not str(v).isdigit()]#去数字
            segs = list(filter(lambda x:x.strip(), segs)) #去左右空格
            segs = filter(lambda x:x not in stopwords, segs)
            temp = " ".join(segs)
            if(len(temp)>1):
                sentences.append((temp, category))
        except Exception:
            print(line)
            continue

#获取数据
data_label_0_content = data_label_0['content'].values.tolist()
data_label_1_content = data_label_1['content'].values.tolist()
data_label_2_content = data_label_2['content'].values.tolist()
#生成训练数据
sentences = []
preprocess_text(data_label_0_content, sentences, 0)
preprocess_text(data_label_1_content, sentences, 1)
preprocess_text(data_label_2_content, sentences,2)
#我们打乱一下顺序，生成更可靠的训练集
random.shuffle(sentences)

#所以把原数据集分成训练集的测试集，咱们用sklearn自带的分割函数。
from sklearn.model_selection import train_test_split
x, y = zip(*sentences)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3,random_state=1234)

#抽取特征，我们对文本抽取词袋模型特征
from sklearn.feature_extraction.text import CountVectorizer
vec = CountVectorizer(
    analyzer='word', #tokenise by character ngrams
    max_features=4000,  #keep the most common 1000 ngrams
)
vec.fit(x_train)

# 设置参数
max_features = 5001
maxlen = 100
batch_size = 32
embedding_dims = 50
filters = 250
kernel_size = 3
hidden_dims = 250
epochs = 10
nclasses = 3

x_train = vec.transform(x_train)
x_test = vec.transform(x_test)
x_train = x_train.toarray()
x_test = x_test.toarray()
y_train = np_utils.to_categorical(y_train,nclasses)
y_test = np_utils.to_categorical(y_test,nclasses)
x_train = sequence.pad_sequences(x_train, maxlen=maxlen)
x_test = sequence.pad_sequences(x_test, maxlen=maxlen)
print('x_train shape:', x_train.shape)
print('x_test shape:', x_test.shape)

class LossHistory(keras.callbacks.Callback):
    def on_train_begin(self, logs={}):
        self.losses = {'batch':[], 'epoch':[]}
        self.accuracy = {'batch':[], 'epoch':[]}
        self.val_loss = {'batch':[], 'epoch':[]}
        self.val_acc = {'batch':[], 'epoch':[]}

    def on_batch_end(self, batch, logs={}):
        self.losses['batch'].append(logs.get('loss'))
        self.accuracy['batch'].append(logs.get('acc'))
        self.val_loss['batch'].append(logs.get('val_loss'))
        self.val_acc['batch'].append(logs.get('val_acc'))

    def on_epoch_end(self, batch, logs={}):
        self.losses['epoch'].append(logs.get('loss'))
        self.accuracy['epoch'].append(logs.get('acc'))
        self.val_loss['epoch'].append(logs.get('val_loss'))
        self.val_acc['epoch'].append(logs.get('val_acc'))

    def loss_plot(self, loss_type):
        iters = range(len(self.losses[loss_type]))
        plt.figure()
        # acc
        plt.plot(iters, self.accuracy[loss_type], 'r', label='train acc')
        # loss
        plt.plot(iters, self.losses[loss_type], 'g', label='train loss')
        if loss_type == 'epoch':
            # val_acc
            plt.plot(iters, self.val_acc[loss_type], 'b', label='val acc')
            # val_loss
            plt.plot(iters, self.val_loss[loss_type], 'k', label='val loss')
        plt.grid(True)
        plt.xlabel(loss_type)
        plt.ylabel('acc-loss')
        plt.legend(loc="upper right")
        plt.show()

history = LossHistory()
print('Build model...')
model = Sequential()

model.add(Embedding(max_features,
                        embedding_dims,
                        input_length=maxlen))
model.add(Dropout(0.5))
model.add(Conv1D(filters,
                     kernel_size,
                     padding='valid',
                     activation='relu',
                     strides=1))
model.add(GlobalMaxPooling1D())
model.add(Dense(hidden_dims))
model.add(Dropout(0.5))
model.add(Activation('relu'))
model.add(Dense(nclasses))
model.add(Activation('softmax'))
model.compile(loss='categorical_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
model.fit(x_train, y_train,
              batch_size=batch_size,
              epochs=epochs,
              validation_data=(x_test, y_test),callbacks=[history])