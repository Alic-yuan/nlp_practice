import random
import jieba
import pandas as pd

# 加载停用词
stopwords = pd.read_csv('stopwords2.txt', index_col=False, quoting=3, sep="\t", names=['stopword'], encoding='utf-8')
stopwords = stopwords['stopword'].values

# 加载语料
laogong_df = pd.read_csv('beilaogongda.csv', encoding='utf-8', sep=',')
laopo_df = pd.read_csv('beilaopoda.csv', encoding='utf-8', sep=',')
erzi_df = pd.read_csv('beierzida.csv', encoding='utf-8', sep=',')
nver_df = pd.read_csv('beinverda.csv', encoding='utf-8', sep=',')
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

sentences = []
preprocess_text(laogong, sentences,0)
preprocess_text(laopo, sentences, 1)
preprocess_text(erzi, sentences, 2)
preprocess_text(nver, sentences, 3)

random.shuffle(sentences)

for sentence in sentences[:10]:
    print(sentence[0], sentence[1])  # 下标0是词列表，1是标签
# from sklearn.feature_extraction.text import CountVectorizer
#
# vec = CountVectorizer(
#     analyzer='word',  # tokenise by character ngrams
#     max_features=4000,  # keep the most common 1000 ngrams
# )
#
# from sklearn.model_selection import train_test_split
#
# x, y = zip(*sentences)
# x_train, x_test, y_train, y_test = train_test_split(x, y, random_state=1256)
#
# vec.fit(x_train)
#
# from sklearn.naive_bayes import MultinomialNB
#
# classifier = MultinomialNB()
# classifier.fit(vec.transform(x_train), y_train)
#
# print(classifier.score(vec.transform(x_test), y_test))