import bilsm_crf_model
import process_data
import numpy as np

model, (vocab, tag_map) = bilsm_crf_model.create_model(train=False)
predict_text = '我喜欢穿耐克8的鞋子'
# print(vocab)
print(tag_map)
str, length = process_data.process_data(predict_text, vocab)
print(str)
print(length)
model.load_weights('model/crf.h5')
raw = model.predict(str)[0]
print(len(raw))
print(raw)
result = [np.argmax(row) for row in raw]
print(result)
# result_tags = [chunk_tags[i] for i in result]

per, loc, org = '', '', ''

for s, t in zip(predict_text, result):
    if t in (tag_map.get('B-PRO'), tag_map.get('I-PRO'), tag_map.get('E-PRO')):
        if t == tag_map.get('B-PRO'):
            per = per + ' ' +  s
        else:
            per = per + s
#         per += ' ' + s if (t == 'B-PER') else s
#     if t in ('B-ORG', 'I-ORG'):
#         org += ' ' + s if (t == 'B-ORG') else s
#     if t in ('B-LOC', 'I-LOC'):
#         loc += ' ' + s if (t == 'B-LOC') else s

print(['product:' + per])

