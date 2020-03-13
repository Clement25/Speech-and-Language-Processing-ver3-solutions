from prettytable import PrettyTable

def get_grammar(string):
    grammar = list()
    for line in string.splitlines():
        left, rights = line.split(' -> ')
        for right in rights.split('|'):
            grammar.append((left.strip(),[r.strip() for r in right.split()]))
    return grammar

def display_grammar(grammar):
    disp_dic = {}
    for g in grammar:
        try:
            disp_dic[g[0]].append(g[1])
        except:
            disp_dic[g[0]] = [g[1]]
    for key, value in disp_dic.items():
        print(key+" -> "+" | ".join([" ".join(v) for v in value]))

def display_table(words, table):
    """display CKY result table
    @param (table): list of list of set. Each set contains all possible results from CKY algorithm.
    @return: None
    """
    pt = PrettyTable(words)
    for row in table:
        if row == table[-1]:
            break
        new_row = [','.join(list(item)) for item in row[1:]]
        pt.add_row(new_row)
    print(pt)