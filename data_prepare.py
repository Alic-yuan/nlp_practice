import jieba
import jieba.posseg as psg


# train_data_io = open("data/trainset", "a")


THRESHOLD = 4
def make_tag(sent, entities, tag, entity_tag=[]):
    b_tag = "B-" + tag
    m_tag = "I-" + tag
    e_tag = "E-" + tag

    if not entities:
        return entity_tag

    if not entity_tag:
        entity_tag = ["O"] * len(sent)

    for match in entities:
        begin = match["begin"]
        end = match["end"]

        for index, i in enumerate(range(begin, end)):
            if entity_tag[i] not in ["O", "S"]:
                break
            if index == 0:
                entity_tag[i] = b_tag
            elif i == (end - 1):
                entity_tag[i] = e_tag
            else:
                entity_tag[i] = m_tag
        # prethreshold = THRESHOLD if THRESHOLD <= begin else end
        # aftthreshold = THRESHOLD if THRESHOLD <= len(sent) - end else len(sent) - end
        #
        # if b_tag not in entity_tag:
        #     continue
        #
        # for j in range(begin - prethreshold, begin):
        #     if j < 0: continue
        #     if entity_tag[j] == "O":
        #         entity_tag[j] = "S"
        # for j in range(end, end + aftthreshold):
        #     if j >= len(entity_tag):break
        #     if entity_tag[j] == "O":
        #         entity_tag[j] = "S"
    # print(entity_tag)
    return entity_tag

def entity(a):
    e = []
    d = {}
    b = [(x.word,x.flag) for x in psg.lcut(a)]
    for s in b:
        # print(s[0], s[1])
        if s[1] == 'nt':
            c = len(s[0])
            d['begin'] = a.index(s[0])
            d['end'] = a.index(s[0]) + c
            d['entity'] = s[0]
            e.append(d)
    return e

def save(tagged):
    if tagged:
        for word, tag in tagged:
            print("%s %s\n" % (word, tag))
        #     train_data_io.write("%s %s\n" % (word, tag))
        # train_data_io.write("end\n")

a = '张远在周日去拜访了中国外交部部长'

b = entity(a)
c = make_tag(a, b, 'ORG')
tagged = list(zip(a, c))
save(tagged)



