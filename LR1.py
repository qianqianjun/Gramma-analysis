from LR1function import *
def main():
    gramma,start=cin()
    tset,nset=getSet(gramma)
    first=getFirst(gramma,tset,nset)
    gramma.insert(0,label(start+"*",[[start]]))
    printGramma(gramma)
    DFA,productionSet=getLR1DFA(gramma,first,nset)
    table=getLR1Table(DFA,productionSet,tset,nset,start)
    Parsing(DFA,tset,nset,productionSet,table)
if __name__ == '__main__':
    main()

# A->a A a|ε
# exit

# S->id|V = E
# V->id
# E->V|n
# exit

# A->( A )|a
# exit

# S->C C
# C->c C|d
# exit

# S->a A d|b B d|a B e|b A e
# A->c
# B->c
# exit

# S->L = R|R
# L->* R|id
# R->L
# exit