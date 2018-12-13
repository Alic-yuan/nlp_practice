import bilsm_crf_model
import process_data
import numpy as np

model, (vocab, chunk_tags) = bilsm_crf_model.create_model(train=False)
predict_text = '张远去拜访了俄罗斯外交部部长'
print(vocab)
print(chunk_tags)
str, length = process_data.process_data(predict_text, vocab)
print(str)
print(length)
model.load_weights('model/crf.h5')
raw = model.predict(str)[0][-length:]
print(len(raw))
print(raw)
result = [np.argmax(row) for row in raw]
result_tags = [chunk_tags[i] for i in result]

per, loc, org = '', '', ''

for s, t in zip(predict_text, result_tags):
    if t in ('B-PER', 'I-PER'):
        if t == 'B-PER':
            per = per + ' ' +  s
        else:
            per = per + s
#         per += ' ' + s if (t == 'B-PER') else s
    if t in ('B-ORG', 'I-ORG'):
        org += ' ' + s if (t == 'B-ORG') else s
    if t in ('B-LOC', 'I-LOC'):
        loc += ' ' + s if (t == 'B-LOC') else s

print(['person:' + per, 'location:' + loc, 'organzation:' + org])

