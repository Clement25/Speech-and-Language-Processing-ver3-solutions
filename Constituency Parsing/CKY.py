from Chmosky import Chmosky, get_grammar, display

def FindGrammar(grammar, word=None, prod1=None, prod2=None):
    """Find a pair in grammar
    @word: the word to be searched as a terminal
    """
    if word:
        heads = [head for (head, symbol) in grammar if symbol==[word]]
        return heads
    # search for 2 productions
    elif prod1 and prod2:
        heads = []
        for B in prod1:
            for C in prod2:
                heads.extend([head for (head, symbol) in grammar if symbol==[B, C]])
        return heads
    else:
        return None
        # raise ValueError("Either word or nt1 and nt2 must not be none")  

def CKY(words, grammar):
    words = [" "] + words
    table = [[[] for _ in range(len(words))] for _ in range(len(words))]
    for j in range(1, len(words)):
        res = FindGrammar(grammar, word=words[j])
        if res:
            table[j-1][j].extend(res)
        for i in range(j-2, -1, -1):
            for k in range(i+1, j):
                res_nt = FindGrammar(grammar, prod1=table[i][k], prod2=table[k][j])
                if res_nt:
                    table[i][j].extend(res_nt)
    return table

if __name__ == '__main__':
    grammar = get_grammar('''\
    S -> NP VP | Aux NP VP | VP
    NP -> Pronoun | Proper-Noun | Det Nominal
    Nominal -> Noun | Nominal Noun | Nominal PP
    VP -> Verb | Verb NP | Verb NP PP | Verb PP | VP PP
    PP -> Preposition NP
    Det -> that | this | a | the
    Noun -> book | flight | meal | money
    Verb -> book | include | prefer
    Pronoun -> I | she | me
    Proper-Noun -> Houston | TWA
    Aux -> does
    Preposition -> from | to | on | near | through''')
    new_grammar = Chmosky(grammar)
    display(grammar)
    display(new_grammar)
    words = "book the flight through Houston".split()
    table = CKY(words, new_grammar)
    print(table)