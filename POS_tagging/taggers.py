from collections import defaultdict
import time
import ipdb
import numpy as np
from prettytable import PrettyTable

class BLTagger(object):
    def __init__(self, train_pairs):
        self.word_tag_dic = self._build(train_pairs)
        print("Finish building baseline tagger")

    def _build(self, train_pairs):
        freq_dict = {}
        for word, tag in train_pairs:
            if word not in freq_dict:
                word_dict = {}
                word_dict[tag] = 1
                freq_dict[word] = word_dict
            else:
                word_dict = freq_dict[word]
                if tag not in word_dict:
                    word_dict[tag] = 1
                else:
                    word_dict[tag] += 1
        word_tag_dic = {}
        for word, word_dict in freq_dict.items():
            best_tag = max(word_dict, key=word_dict.get)
            word_tag_dic[word] = best_tag
        return word_tag_dic        

    def test(self, test_pairs):
        correct = 0
        start_time = time.time()
        for word, tag in test_pairs:
            if word not in self.word_tag_dic:
                pred_tag = 'NN'
            else:
                pred_tag = self.word_tag_dic[word]
            correct += (pred_tag==tag)
        print("Test %d examples in %.5f seconds"%(len(test_pairs),time.time()-start_time))
        print("Test Accuracy: %.2f%%"%(100*correct/len(test_pairs)))

class HMMTagger(object):
    def __init__(self, train_pairs, train_pairs_bi, train_starts, all_tags, vocab_size):
        self.all_tags = all_tags
        self.tag2id = {tag:index for index,tag in enumerate(all_tags)}
        self.id2tag = {index:tag for index,tag in enumerate(all_tags)}
        self.vocab_size = vocab_size
        self.tag_freq_dic = self._get_tag_freqs(train_pairs)
        self.total_tags = sum([tag_freq for tag_freq in self.tag_freq_dic.values()])
        self._build(train_pairs, train_pairs_bi, train_starts)
        print("Finish building HMM tagger!")
    
    def _build(self, train_pairs, train_pairs_bi, train_starts):
        self.A = self._init_trans_matrix(train_pairs_bi, train_pairs)
        self.B = self._init_emission_prob(train_pairs)
        self.C = self._init_start_distrib(train_starts)

    def _init_trans_matrix(self, train_pairs_bi, train_pairs):
        num_tag = len(self.tag2id)
        A = np.zeros((num_tag, num_tag),dtype=np.float32)
        bigram_freq_dic = {}
        for bigram in train_pairs_bi:
            tag1, tag2 = bigram[0][1], bigram[1][1]
            try:
                bigram_freq_dic[(tag1, tag2)] += 1
            except:
                bigram_freq_dic[(tag1, tag2)] = 1
        for i in range(num_tag):
            for j in range(num_tag):
                try:
                    A[i][j] = bigram_freq_dic[(self.id2tag[i], self.id2tag[j])]/   \
                        self.tag_freq_dic[self.id2tag[i]] # add smoothing
                except:
                    A[i][j] = 0
        return A
    
    def _init_emission_prob(self, train_pairs):
        emission_prob_dic = {}
        for pair in train_pairs:
            try:
                emission_prob_dic[pair] += 1
            except:
                emission_prob_dic[pair] = 1
        for pair in emission_prob_dic:
            # emission_prob_dic[pair] = (emission_prob_dic[pair]+1)/(self.tag_freq_dic[pair[1]] + self.vocab_size)
            emission_prob_dic[pair] = float(emission_prob_dic[pair])/float(self.tag_freq_dic[pair[1]])
        return emission_prob_dic
    
    def _init_start_distrib(self, train_starts):
        count = 0
        start_distrib_dic = {tag:0 for tag in self.all_tags}
        for start in train_starts:
            try:
                start_distrib_dic[start] += 1
            except:
                start_distrib_dic[start] = 1
        for start in start_distrib_dic:
            start_distrib_dic[start] /= len(train_starts)
        return start_distrib_dic

    def _get_tag_freqs(self, train_pairs):
        tag_freq_dic = {}
        for word, tag in train_pairs:
            if tag not in tag_freq_dic:
                tag_freq_dic[tag] = 1
            else:
                tag_freq_dic[tag] += 1
        return tag_freq_dic
    
    def search_word(self, word):
        for pair in self.B:
            if pair[0] == word:
                print(pair,self.B[pair])
    
    def display_conf(self):
        table = PrettyTable(['\t']+[self.id2tag[i] for i in range(len(self.id2tag))])
        for i in range(len(self.id2tag)):
            table.add_row([self.id2tag[i]]+list(self.conf_matrix[i]))
        print(table)

    def test(self, test_sents, test_tags):
        """ Implementation of Veterbi algorithm 
        """
        correct = 0
        total_test = 0
        start_time = time.time()
        self.conf_matrix = np.zeros((len(self.all_tags),len(self.all_tags)),dtype=np.int)
        print_every = 10000
        for idx, sent in enumerate(test_sents):
            T = len(sent)
            num_tag = len(self.tag_freq_dic)
            viterbi = np.zeros((num_tag, T), dtype=np.float)
            back_trace = np.full((num_tag,T), -1, dtype=np.int)

            for s in range(num_tag):
                try:
                    viterbi[s][0] = self.C[self.id2tag[s]]*self.B[(sent[0],self.id2tag[s])]
                except:
                    viterbi[s][0] = self.C[self.id2tag[s]]/self.vocab_size

            for t in range(1,len(sent)):
                for s in range(num_tag):
                    max_score = 0
                    for s_ in range(num_tag):
                        try:
                            score = viterbi[s_][t-1]*self.A[s_][s]*self.B[(sent[t],self.id2tag[s])]
                        except:
                            # score = vciterbi[s_][t-1]*self.A[s_][s]/self.vocab_size
                            score = 0
                        if max_score < score:
                            max_score = score
                            last_tag = s_
                    viterbi[s][t] = max_score
                    try:
                        back_trace[s][t] = last_tag
                    except:
                        back_trace[s][t] = -1
            
            bestpath = [np.argmax(viterbi[:,len(sent)-1])]
            for i in range(T-1):
                bestpath.append(back_trace[bestpath[-1]][T-1-i])
            bestpath.reverse()
            bestpath = [self.id2tag[aa] for aa in bestpath]

            for i in range(T):
                correct += bestpath[i] == test_tags[idx][i]
                self.conf_matrix[self.tag2id[bestpath[i]]][self.tag2id[test_tags[idx][i]]] += 1
            total_test += T
            if idx % print_every == 0:
                print("Processing %d item..."%idx)
        print("Test %d examples in %.5f seconds"%(total_test,time.time()-start_time))
        print("Test Accuracy: %.2f%%"%(100*correct/total_test))
        