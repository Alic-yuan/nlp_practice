import bilsm_crf_model
import os

import pickle
import numpy
from keras.callbacks import Callback
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
from keras_contrib.layers import CRF

from keras.models import load_model




from utils import f1_score, get_tags
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


class Metrics(Callback):
    def on_train_begin(self, logs={}):
        with open('model/config.pkl', 'rb') as inp:
            (vocab, tag_map) = pickle.load(inp)
        self.tag_map = tag_map

    def on_epoch_end(self, epoch, logs=None):
        val_predict = numpy.argmax(numpy.asarray(self.model.predict(self.validation_data[0])), axis=2)
        val_targ = self.validation_data[1]
        # print(val_targ)
        val_predict = numpy.reshape(val_predict, [-1])
        val_targ = numpy.reshape(val_targ, [-1])
        # print(val_predict.shape)
        # print(val_targ.shape)
        recall, precision, f1 = f1_score(val_targ, val_predict, 'PRO', self.tag_map)
        # print("recall:{}--precision:{}--f1:{}".format(recall, precision, f1))
        return

# 其他metrics可自行添加
metrics = Metrics()


EPOCHS = 3

model_path = 'model/crf.h5'
model, (train_x, train_y), (test_x, test_y) = bilsm_crf_model.create_model()

# train model
if os.path.exists(model_path):
    print('restore_model:')
    model.load_weights(model_path)
    # model.fit()参数中validation_split作为验证集来更新参数,calidation_data不知道行不行
    model.fit(train_x, train_y,batch_size=16,epochs=EPOCHS, validation_split=0.3, callbacks=[metrics])
else:
    model.fit(train_x, train_y, batch_size=16, epochs=EPOCHS, validation_split=0.3, callbacks=[metrics])
# model.evaluate(test_x, test_y, batch_size=5)
model.save('model/crf.h5')
