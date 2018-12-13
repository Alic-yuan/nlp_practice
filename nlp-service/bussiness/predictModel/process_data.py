import numpy
from collections import Counter
from keras.preprocessing.sequence import pad_sequences
import pickle
import platform


def load_data():
    tag_map = {}
    vocab = {}
    train = _parse_data(open('data/train', 'rb'))
    # print(train)
    test = _parse_data(open('data/test', 'rb'))

    word_counts = Counter(row[0].lower() for sample in train for row in sample)
    word_counts2 = Counter(row[1] for sample in train for row in sample)
    # print(word_counts2)
    vocabs = [w for w, f in iter(word_counts.items()) if f >= 2]
    for v in vocabs:
        if v not in vocab.keys():
            vocab[v] = len(vocab) + 1
    print(vocab)
    chunk_tags = [w for w, f in iter(word_counts2.items()) if f >= 2]
    # print(chunk_tags)
    for chunk_tag in chunk_tags:
        if chunk_tag not in tag_map.keys():
            tag_map[chunk_tag] = len(tag_map) + 1
    print(tag_map)

    # save initial config data
    with open('model/config.pkl', 'wb') as outp:
        pickle.dump((vocab, tag_map), outp)

    train = _process_data(train, vocab, tag_map)
    test = _process_data(test, vocab, tag_map)
    return train, test, (vocab, tag_map)


def _parse_data(fh):
    data = []
    sentence = []
    line = fh.readline().decode('utf-8')
    while line:
        line = line.strip()
        row = line.split()
        if line == "end":
            if len(sentence) > 0 and len(sentence) < 500:
                data.append(sentence)
            sentence = []
            line = fh.readline().decode('utf-8')
            continue
        sentence.append(row)
        line = fh.readline().decode('utf-8')
    fh.close()
    return data



def _process_data(data, vocab, chunk_tags, maxlen=None, onehot=False):
    if maxlen is None:
        maxlen = max(len(s) for s in data)
    print(maxlen)
    x = [[vocab.get(w[0].lower(), 1) for w in s] for s in data]  # set to <unk> (index 1) if not in vocab
    y_chunk = [[chunk_tags.get(w[1]) for w in s] for s in data]
    x = pad_sequences(x, maxlen)  # left padding
    print(x.shape)

    y_chunk = pad_sequences(y_chunk, maxlen)

    if onehot:
        y_chunk = numpy.eye(len(chunk_tags), dtype='float32')[y_chunk]
    else:
        y_chunk = numpy.expand_dims(y_chunk, 2)
    print(y_chunk.shape)
    return x, y_chunk


def process_data(data, vocab, maxlen=100):
    x = [vocab.get(w.lower(), 1) for w in data]
    length = len(x)
    x = pad_sequences([x], length)  # left padding
    return x, length

if __name__ == '__main__':
    load_data()
