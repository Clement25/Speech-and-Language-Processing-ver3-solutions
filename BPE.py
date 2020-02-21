import re, collections

def get_stats(vocab):
    """ get frequencies from adjacent pairs
    @param vocab: a vocabulary with sequential pairs
    
    @returns pairs: a dictionary with counted byte pairs
    """
    pairs = collections.defaultdict(int) 
    for word, freq in vocab.items():
        symbols = word.split('_')
        for i in range(len(symbols)-1):
            pairs[symbols[i], symbols[i+1]] += freq
    return pairs

def merge_vocab(pair, v_in):
    v_out = {}
    print(v_in)
    bigram = re.escape('_'.join(pair))  # re.escape()用于字符转义
    print(bigram)
    p = re.compile(r'(<!\S)?' + bigram + r'(!\S)?')
    for word in v_in:
        w_out = re.sub(pattern=p, repl=''.join(pair), string=word)
        print(p, word, w_out, pair)
        v_out[w_out] = v_in[word]
    return v_out

vocab = {
    'l_o_w_</w>': 5, 'l_o_w_e_s_t_</w>':2,
    'n_e_w_e_r_</w>': 6, 'w_i_d_e_r_</w>':3, 'n_e_w_</w>':2
}
num_merges = 8

for i in range(num_merges):
    pairs = get_stats(vocab)
    best = max(pairs, key=pairs.get)
    vocab = merge_vocab(best, vocab)
    print(vocab)