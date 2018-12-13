import jieba
#定义停用词、标点符号
punctuation = ["，","。", "：", "；", "？"]
#定义语料
content = ["机器学习带动人工智能飞速的发展。",
           "深度学习带动人工智能飞速的发展。",
           "机器学习和深度学习带动人工智能飞速的发展。"
          ]

#分词
segs_1 = [jieba.lcut(con) for con in content]

tokenized = []
for sentence in segs_1:
    words = []
    for word in sentence:
        if word not in punctuation:
            words.append(word)
    tokenized.append(words)

#求并集
bag_of_words = [ x for item in segs_1 for x in item if x not in punctuation]
#去重
bag_of_words = list(set(bag_of_words))

bag_of_word2vec = []
for sentence in tokenized:
    tokens = [1 if token in sentence else 0 for token in bag_of_words]
    bag_of_word2vec.append(tokens)

print(bag_of_word2vec)