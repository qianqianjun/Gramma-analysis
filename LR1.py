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


#7.3
# S->A a|b A c|B c|b B a
# A->d
# B->d

# 7.2
# S->A a|b A c|d c|b d a
# A->d
# exit

# 7.1
# S->E
# E->T|T + E
# T->ε
# exit

# 6.3
# S->A
# A->A b|b B a
# B->a A c|a|a A b
# exit

# 6.2
# S->A a A b|B b B a
# A->ε
# B->ε

# 6.1
# S->S + a T|a T|+ a T
# T->+ a T|+ a
# exit