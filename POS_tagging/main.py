from taggers import BLTagger, HMMTagger
import ipdb

filepath = './data/conll2000/'
file_name_train, file_name_test = 'train.txt', 'test.txt'

train_file, test_file = open(filepath+file_name_train),open(filepath+file_name_test)
train_data = [line.strip() for line in train_file]
test_data = [line.strip() for line in test_file]

# Baseline model, "most likely tag"
train_pairs = [(pair.split()[0], pair.split()[1]) for pair in train_data if pair]
test_pairs = [(pair.split()[0], pair.split()[1]) for pair in test_data if pair]

Base_Tagger = BLTagger(train_pairs)
Base_Tagger.test(test_pairs)

# HMM model
train_pairs_bi = [((train_data[i].split()[0], train_data[i].split()[1]),(train_data[i+1].split()[0], train_data[i+1].split()[1])) \
    for i in range(len(train_data)-1) if train_data[i+1] and train_data[i]]
# test_pairs_bi = [((test_data[i].split()[0], test_data[i].split()[1]),(test_data[i+1].split()[0], test_data[i+1].split()[1])) \
#     for i in range(len(test_data)-1) if test_data[i+1] and test_data[i]]

# exclude the last word in each scentence because they have no contribution to the transition probability
train_pairs_hmm = [pair[0] for pair in train_pairs_bi]

train_starts = [train_data[i].split()[1] for i in range(len(train_data)) if i == 0 or not train_data[i-1]]
# test_pairs_hmm = [pair[0] for pair in test_pairs_bi]
test_sents = []
test_tags = []
sent = []
sent_tags = []
for pair in test_data:
    if pair:
        sent.append(pair.split()[0])
        sent_tags.append(pair.split()[1])
    else:
        test_sents.append(sent)
        test_tags.append(sent_tags)
        sent = []
        sent_tags = []

vocab = [pair.split()[0] for pair in train_data if pair]
vocab = list(set(vocab))

# all tags
tags = [pair[1] for pair in train_pairs]
all_tags = list(set(tags))

HMM_Tagger = HMMTagger(train_pairs, train_pairs_bi, train_starts, all_tags, len(vocab))
HMM_Tagger.test(test_sents, test_tags)
ipdb.set_trace()
# display the confusion matrix
HMM_Tagger.display_conf()

