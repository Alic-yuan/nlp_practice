# -*- coding:utf-8 -*-
# Utils For NER
# Author    yuan


def f1_score(tar_path, pre_path, tag, tag_map):
    tp = 0.
    tn = 0.
    fn = 0.
    fp = 0.
    # for fetch in (tar_path, pre_path):
    tar, pre = tar_path, pre_path
    tar_tags = get_tags(tar, tag, tag_map)
    pre_tags = get_tags(pre, tag, tag_map)
    for t_tag in tar_tags:
        if t_tag in pre_tags:
            tp += 1
        else:
            fn += 1
    for p_tag in pre_tags:
        if p_tag not in tar_tags:
            fp += 1
    recall = 0 if tp+tn == 0 else (tp/(tp+fn))
    precision = 0 if tp+fp == 0 else (tp/(tp+fp))
    f1 = 0 if recall+precision == 0 else (2*precision*recall)/(precision + recall)
    print("\t'{}'\trecall {}\tprecision {}\tf1 {}".format(tag, recall, precision, f1))
    return recall, precision, f1

def get_tags(path, tag, tag_map):
    begin_tag = tag_map.get("B-" + tag)
    mid_tag = tag_map.get("I-" + tag)
    end_tag = tag_map.get("E-" + tag)
    o_tag = tag_map.get("O")
    begin = -1
    end = 0
    tags = []
    last_tag = 0
    
    for index, tag in enumerate(path):
        if tag == begin_tag and index == 0:
            begin = 0
        elif tag == begin_tag:
            begin = index
        elif tag == end_tag and last_tag in [mid_tag, begin_tag] and begin > -1:
            end = index
            tags.append([begin, end])
        elif tag == o_tag:
            begin = -1
        last_tag = tag
    return tags




if __name__ == "__main__":
    chunk_tags = ['O', 'B-PRO', 'I-PRO', 'E-PRO']
    # f1_score([[7, 7, 1, 2, 3, 7, 4, 6, 7, 7, 7, 4, 6]], [[7, 7, 1, 2, 3, 7, 4, 6, 1, 2, 3, 7, 7]], "PER", tag_map)
    print(get_tags([0,0,0,1,2,3,0,1,2,3]))