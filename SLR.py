from LL1 import cin
from LL1 import getFirst
from LL1 import getFollow
from LL1 import getSet
from LR0 import *
from public import *
from struct import *
def main():
    gramma,start=cin()
    tset,nset=getSet(gramma)
    First=getFirst(gramma,tset,nset)
    Follow=getFollow(gramma,tset,nset,First,start)
    productionSet=getProductionSet(gramma)
    PrintProductionSet(productionSet)
    print(tset)
    print(nset)

    # resultSet,start= getDFA(productionSet, tset, nset, gramma)
if __name__ == '__main__':
    main()

# E->E + T|T
# T->T * F|F
# F->( E )|id
# exit