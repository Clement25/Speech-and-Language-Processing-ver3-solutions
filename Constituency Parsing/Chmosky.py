from utils import get_grammar, display_grammar
import copy

"""TODO: Buildup a non-terminal list 
"""

def Chmosky(grammar):
    """ Convert arbitrary grammar to a CNF grammar
    @param grammar: list of tuples, each of which is in type: (str, list[str])
    """
    # grammar = set(grammar)
    nonterminals = list(g[0] for g in grammar)

    def isTerminal(p):
        return not p in nonterminals

    new_grammar = copy.deepcopy(grammar)
    temp_grammar = copy.deepcopy(grammar)
    # A flag indicating if the processing happens
    process = True
    # remove epsilon rules
    while process:
        process = False
        # remove single symbol nonterminal rules
        for l, r in temp_grammar:
            if l != 'S' and not r:
                process = True
                new_grammar.remove((l,r))
                temp_grammar = copy.deepcopy(new_grammar)
                for l_, r_ in temp_grammar:
                    if r in r_:
                        new_grammar.remove((l_, r_))
                        new_grammar.append((l_, r_.pop(r)))
        temp_grammar = copy.deepcopy(new_grammar)
    
    process = True
    # remove single symbol nonterminal rules
    while process:
        process = False
        for l, r in temp_grammar:
            if len(r) == 1 and not isTerminal(r[0]):
                process = True
                new_grammar.remove((l,r))
                for l_, r_ in temp_grammar:
                    if l_ == r[0]:
                        new_grammar.append((l, r_))
        temp_grammar = copy.deepcopy(new_grammar)
    
    """     process = True
    # move terminals to their own rules
    while process:
        process = False
        for l, r in temp_grammar:
            if len(r) > 1:
                for i, rr in enumerate(r):
                    if isTerminal(rr):
                        process = True
                        new_l = rr.upper()
                        new_grammar.append((new_l, [rr]))
                        new_grammar.remove(l, r)
                        new_grammar.append((l, r[:i]+[new_l]+r[i+1:]))
        temp_grammar = copy.deepcopy(new_grammar) """

    process = True
    # ensure there are only two nonterminals per rule
    index = 1
    while process:
        process = False
        # remove single symbol nonterminal rules
        for l, r in temp_grammar:
            if len(r) > 2:
                process = True
                unknown = True
                # if rule exists, don't create a new rule
                new_r = r[0:2]
                for l_, r_ in temp_grammar:
                    if r_ == new_r and l_[0]=='X':
                        unknown = False
                        new_l = l_
                        break
                if unknown:
                    new_l = 'X%d'%index
                    index += 1
                    new_grammar.append((new_l, new_r))
                # replace all
                new_grammar.remove((l,r))
                new_grammar.append((l,[new_l]+r[2:]))
            temp_grammar = copy.deepcopy(new_grammar)

    return new_grammar

if __name__ == '__main__':
    grammar = get_grammar('''\
    S -> NP VP | Aux NP VP | VP
    NP -> Pronoun | Proper-Noun | Det Nominal
    Nominal -> Noun | Nominal Noun | Nominal PP
    VP -> Verb | Verb NP | Verb NP PP | Verb PP | VP PP
    PP -> Preposition NP
    Det -> that | this | a
    Noun -> book | flight | meal | money
    Verb -> book | include | prefer
    Pronoun -> I | she | me
    Proper-Noun -> Houston | TWA
    Aux -> does
    Preposition -> from | to | on | near | through''')
    new_grammar = Chmosky(grammar)
    