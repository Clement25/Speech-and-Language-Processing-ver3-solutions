import operator
from utils import get_grammar, display_grammar, display_table

def FindGrammar(grammar, word=None, prod1=None, prod2=None):
    """Find a pair in grammar
    @param word (string): the word to be searched as a terminal
    @param prod1, prod2 (list of tuple): cell in CKY table, each tuple is in the format (head, probability, backnode)
    @return 
    """
    if word:
        # (head probability back)
        heads = [(head, probability, None) for (head, probability, symbol) in grammar if symbol==[word]]
        return heads
    # Find the maximum probability
    elif prod1 and prod2:
        result = None
        max_prob = 0
        for B in prod1:    # The last element is probability
            for C in prod2:
                if B and C:
                    for (head, prob, symbol) in grammar:
                        if symbol==[B[0], C[0]] and prob*B[1]*C[1] > max_prob:
                                max_prob = prob*B[1]*C[1]
                                result = [(head, max_prob, [B[0],C[0]])]
                        # For unit productions
                        for(head_, prob_, symbol_) in grammar:
                            if symbol_ == head:
                                result.append(head_, max_prob*prob_, [B[0],C[0]])

        if not result:
            return None
        return result
    else:
        return None
        # raise ValueError("Either word or nt1 and nt2 must not be none")  

def CKY(words, grammar):
    words = [" "] + words
    table = [[list() for _ in range(len(words))] for _ in range(len(words))]
    for j in range(1, len(words)):
        res = FindGrammar(grammar, word=words[j])
        if res:
            table[j-1][j] =  res
        for i in range(j-2, -1, -1):
            max_prob = 0
            for k in range(i+1, j):
                result = FindGrammar(grammar, prod1=table[i][k], prod2=table[k][j])
                if result:
                    table[i][j] += result
            # Find the maximum probability
    return table

if __name__ == '__main__':
    # grammar = get_grammar('''\
    # S -> NP VP 0.8 | Aux NP VP 0.15 | VP 0.05
    # NP -> Pronoun 0.35 | Proper-Noun 0.30 | Det Noun 0.20 | Nominal 0.15
    # Nominal -> Noun 0.75 | Nominal Noun 0.20 | Nominal PP 0.05
    # VP -> Verb 0.35 | Verb NP 0.20 | Verb NP PP 0.10 | Verb PP 0.15 | VP PP 0.15 | Verb NP NP 0.05
    # PP -> Preposition NP 1.0
    # Det -> that 0.10 | a 0.30 | the 0.60
    # Noun -> book 0.10 | flight 0.70 | meal 0.05 | money 0.05 | dinner 0.10
    # Verb -> book 0.30 | include 0.30 | prefer 0.40
    # Pronoun -> I 0.40 | she 0.05 | me 0.15 | you 0.40
    # Proper-Noun -> Houston 0.60 | TWA 0.40
    # Aux -> does 0.60 | can 0.40
    # Preposition -> from 0.30 | to 0.30 | on 0.20 | near 0.15 | through 0.05''')

    grammar = get_grammar('''\
    S -> NP VP 0.8
    NP -> Det N 0.3
    VP -> V NP 0.2
    V -> includes 0.05
    Det -> a 0.40 | the 0.40
    N -> meal 0.1 | flight 0.2''')

    display_grammar(grammar)
    words = "the flight includes a meal".split()
    table = CKY(words, grammar)
    print(table)
    # display_table(words, table)