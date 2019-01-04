train_data_path = 'data/trainset_xianxia2'

open_path = open('data/train_xianxia2', 'w')


def save(tagged):
    if tagged:
        for word, tag in tagged:
            open_path.write("%s %s\n" % (word, tag))



string = open(train_data_path).read()

split_text = '。 O'
for sample in string.strip().split(split_text):
    if len(sample) < 1000:
        if "B-PRO" in sample or "I-PRO" in sample or "E-PRO" in sample:
            for row in sample.split('\n'):
                if len(row.strip()) == 3 or len(row.strip()) == 7:
                    open_path.write(row + "\n")
            open_path.write("end" + "\n")
        else:
            continue

