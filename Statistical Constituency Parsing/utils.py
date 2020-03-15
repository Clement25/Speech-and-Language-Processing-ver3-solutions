from prettytable import PrettyTable

def get_grammar(string, probalistic=True):
    """Build up a grammar data structure
    @param string (str): a long string representing all grammar rules with format " A -> B1 | B2 | ... | B_n |", 
        where A is a single grammar element and B_k is either a single and multiple grammar element(s).
    @return grammar (list of tuple): Tuples storing the grammar, each tuple is in the format (A, list[B, B_prob]) 
    """
    grammar = list()
    for line in string.splitlines():
        left, rights = line.split(' -> ')
        for right in rights.split('|'):
            r_sp = right.split()
            if probalistic:
                grammar.append((left.strip(),float(r_sp[-1]),[r.strip() for r in r_sp[:-1]]))
            else:
                grammar.append((left.strip(),1.0,[r.strip() for r in r_sp[:-1]]))
    return grammar

def get_lexcializeg_grammar(string, probalistic=True):
    """Build up a grammar data structure
    @param string (str): a long string representing all grammar rules with format " A -> B1(word) | B2 | ... | B_n |", 
        where A is a single grammar element and B_k is either a single or multiple grammar element(s).
    @return grammar (list of tuple): Tuples storing the grammar, each tuple is in the format (A, list[B, B_prob]) 
    """
    grammar = list()
    for line in string.splitlines():
        left, rights = line.split(' -> ')
        for right in rights.split('|'):
            r_sp = right.split()
            if probalistic:
                grammar.append((left.strip(),float(r_sp[-1]),[r.strip() for r in r_sp[:-1]]))
            else:
                grammar.append((left.strip(),1.0,[r.strip() for r in r_sp[:-1]]))
    return grammar

def display_grammar(grammar):
    disp_dic = {}
    for g in grammar:
        try:
            disp_dic[g[0]].append(g[2])
        except:
            disp_dic[g[0]] = [g[2]]
    for key, value in disp_dic.items():
        print(key+" -> "+" | ".join([" ".join(v) for v in value]))

def display_table(words, table):
    """display CKY result table
    @param (table): list of list of set. Each set contains all possible results from CKY algorithm.
    @return: None
    """
    pt = PrettyTable(words)
    for row in table:
        print(row)
        if row == table[-1]:
            break
        new_row = [','.join(list(item)) for item in row[1:]]
        pt.add_row(new_row)
    print(pt)