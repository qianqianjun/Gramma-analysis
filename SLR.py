from LR0 import cin
from LL1 import getFirst
from LL1 import getFollow
from LL1 import getSet
from LR0 import PrintProductionSet
from LR0 import getProductionSet
from struct import Item
from struct import Line
class Status(object):
    id=0
    def __init__(self):
        #line
        self.line=[]
        #Item
        self.productionSet=[]
        self.static_id=0
        self.fin_pro=[]
        self.unfin_pro=[]
    def initid(self):
        self.static_id=Status.id
        Status.id += 1
    def addline(self,singleline):
        self.line.append(singleline)
    #判断这个产生式是不是结束的产生式。
    def isendStatus(self):
        if len(self.productionSet)!=1:
            return False
        else:
            if self.productionSet[0].index==self.productionSet[0].maxindex:
                return True
        return False
    #整理当前状态有哪些产生式是完成状态的，有哪些产生式不是完成状态:
    def zip(self):
        for i in self.productionSet:
            if i.index==i.maxindex:
                self.fin_pro.append(i)
            else:
                self.unfin_pro.append(i)
def contain(arr,elem):
    for i in arr:
        if i.equals(elem):
            return True
    return False
def checkRepeat(resultSet,productionSet,pro_index,gramma,nset,tset):
    newset = []
    newtemp = []
    #这里有一个坑，注意，产生式可能包括相同的符号，初始的状态可能不是只有一条产生式：
    #需要遍历产生式的集合，找到所有点后面是相同终结符号的产生式，将它们加到新的状态集合中
    #不这样做的话会导致生成的DFA可能会成为NFA
    currentlabel=productionSet[pro_index].right[productionSet[pro_index].index]
    for item in productionSet:
        if item.index==item.maxindex:
            continue
        if item.right[item.index]==currentlabel and item.index<item.maxindex:
            newitem=Item(item.left,item.right)
            newitem.setIndex(item.index+1)
            newset.append(newitem)
            newtemp.append((newitem.left, newitem.right, newitem.index))
    #下面的过程继续得到状态的产生式的集合，这里特别需要注意的是要防止循环将一个相同的产生式的左端重复加到集合中导致电脑蓝屏
    #实际上消除左递归可以避免上面的情况。
    for i in newset:
        #如果是一个完成的状态，那么久不用加进去了。
        if i.index==i.maxindex:
            continue
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        if not contain(newset,Item(row.value,k)):
                            newset.append(Item(row.value, k))
                            newtemp.append((row.value, k, 0))
    m=0
    for i in resultSet:
        oldtemp = []
        for j in i.productionSet:
            oldtemp.append((j.left,j.right,j.index))
        flag=True
        if len(oldtemp)!=len(newtemp):
            flag=False
        else:
            for k in newtemp:
                if k not in oldtemp:
                    flag=False
        if flag:
            return (True,newset,resultSet[m])
        m+=1
    return (False,newset,[])
def getNextStatus(status,tset,nset,gramma,resultSet):
    # 首先判断是不是终止状态：status 的production中只有一个产生式，并且产生式的点在最右端
    # 是终止状态直接返回
    length=len(status.productionSet)
    currentpro=status.productionSet[0]
    if length == 1 and currentpro.index == currentpro.maxindex:
        return
    # 遍历当前状态productionSet中的所有item
    # 根据点的位置创造出下一个状态
    # 用一条边将当前状态和下一个状态连接在一起（边的next指向下一个状态，边的值就是当前index所指的符号的值）
    # 将边添加到当前状态的出边集合中
    # 这里特别需要注意的是判断一下新的状态是不是可能就是当前状态，是的话就别创建了，如果不想stackoverflow的话
    i=0
    plength=len(status.productionSet)
    while i<plength:
        #如果当前的产生式是一个完成产生式，就不用再进行新状态的产生了，直接下一步
        if status.productionSet[i].index==status.productionSet[i].maxindex:
            i+=1
            continue
        isrepeat,newset,nextstatus=checkRepeat(resultSet,status.productionSet,i,gramma,nset,tset)
        #如果不是重复的话：
        if not isrepeat:
            #创建新的状态：
            newstatus=Status()
            newstatus.productionSet=newset
            newstatus.initid()
            #添加到最终的结果集合
            resultSet.append(newstatus)
            #创建指向新状态的边：
            # if status.productionSet[i].right[status.productionSet[i].index]=='T':
            #     print(newstatus.static_id)
            L1=Line(status.productionSet[i].right[status.productionSet[i].index],newstatus)
            status.line.append(L1)
            getNextStatus(newstatus,tset,nset,gramma,resultSet)
        else:
            #如果是一个终结符号：
            if status.productionSet[i].right[status.productionSet[i].index] in tset:
                L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                status.line.append(L1)
            else:
            # 如果是一个非终结符号：
            #如果当前的状态出边集合中没有值为此非终结符的边
            # 创建指向自己的一个边：
                flag=True
                for singleline in status.line:
                    if singleline.tranval==status.productionSet[i].right[status.productionSet[i].index]:
                        flag=False
                        break
                if flag:
                    # if status.productionSet[i].right[status.productionSet[i].index]=='T':
                    #     print(nextstatus.static_id)
                    L1=Line(status.productionSet[i].right[status.productionSet[i].index],nextstatus)
                    status.line.append(L1)
        i+=1
def getDFA(productionset,tset,nset,gramma):
    start=Status()
    start.productionSet.append(Item(productionset[0][0],productionset[0][1]))
    #创造开始状态的所有产生式：
    for i in start.productionSet:  #遍历item
        if i.right[i.index] in nset:
            #修复了产生式不断添加到productionSet 的bug，防止电脑蓝屏：
            # godown=True
            # for temp in start.productionSet:
            #     if temp.left==i.right[i.index]:
            #         godown=False
            # if not godown:
            #     continue
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        if not contain(start.productionSet,Item(row.value,k)):
                            start.productionSet.append(Item(row.value,k))
    start.initid()
    # for i in start.productionSet:
    #     print((i.left,i.right,i.index))
    resultSet=[]
    resultSet.append(start)
    getNextStatus(start,tset,nset,gramma,resultSet)
    print("识别文法活前缀的DFA状态集合：")
    print("———————————————————————————————")
    for i in resultSet:
        print("状态id："+str(i.static_id))
        print("状态产生式集合以及点所处的位置")
        for j in i.productionSet:
            print((j.left,j.right,j.index))
        print("状态的出边和所指向的状态标号")
        for k in i.line:
            print((k.tranval,k.next.static_id))
        print("---------------------------")
    return (resultSet,start)
def main():
    gramma,start=cin()
    tset,nset=getSet(gramma)
    First=getFirst(gramma,tset,nset)
    Follow=getFollow(gramma,tset,nset,First,start)
    productionSet=getProductionSet(gramma)
    PrintProductionSet(productionSet)
    resultSet,start= getDFA(productionSet, tset, nset, gramma)
if __name__ == '__main__':
    main()

# E->E + T|T
# T->T * F|F
# F->( E )|id
# exit