"""
write by 高谦  未完成

底下注释非常详细，因为我健忘，怕给老师讲的时候自己忘了当初自己咋想的了
"""
class label(object):
    def __init__(self,val,right):
        #指示当前边的值
        self.value=val
        #指向下一个状态：转移后的状态。
        self.right=right
class Item(object):
    def __init__(self,val,sets):
        #指示当前点的位置：
        self.index=0
        #指示状态中的产生式中的左边的非终结符。
        self.left=val
        #list[str] 一个字符串的列表：
        self.right=sets
        self.maxindex=len(self.right)
    #修改当前点的位置的函数，新建状态的时候会用到：
    def setIndex(self,ind):
        self.index=ind
class Status(object):
    id=0
    def __init__(self):
        #line
        self.line=[]
        #Item
        self.productionSet=[]
        self.static_id=0
    def initid(self):
        self.static_id=Status.id
        Status.id += 1
    def addline(self,singleline):
        self.line.append(singleline)
    def addProduction(self,production):
        self.productionSet.append(production)
    def setStatusid(self,ids):
        self.static_id=ids
class Line(object):
    def __init__(self,tranval,next):
        self.next=next
        self.tranval=tranval
def isTerminal(k):
    if (k[0] >= 'a' and k[0] <= 'z') or \
            (k[0] >= '0' and k[0] <= '9') or \
            k[0] == 'ε' or \
            k[0] == '(' or \
            k[0] == ')' or \
            k[0] == '+' or \
            k[0] == '-' or \
            k[0] == '*' or \
            k[0] == '/':
        return True
    return False
def printGramma(gramma):
    for i in gramma:
        print((i.value,i.right))
    print("-------------------------------")
def cin():
    print("请输入文法，例如：A->a|A b,输入exit结束输入(注意,不同的符号之间要有空格:")
    gramma = []
    while True:
        r = input()
        if r != 'exit':
            r = r.split("->")
            right = []
            for i in r[1].split("|"):
                right.append(i.split())
            temp = label(r[0], right)
            gramma.append(temp)
        else:
            break
    start = gramma[0].value
    right=[]
    right.append([start])
    temp = label(start + "*", right)
    gramma.insert(0, temp)
    print("解析输入文法：")
    printGramma(gramma)
    return (gramma, start)
def getSet(gramma):
    Tset=[]
    Nset=[]
    for i in gramma:
        Nset.append(i.value)
        for j in i.right:
            for k in j:
                if isTerminal(k):
                    Tset.append(k)
    Tset=set(Tset)
    Tset=list(Tset)
    Tset.sort()
    return (Tset,Nset)
def getProductionSet(gramma):
    productionset={}
    i = 0
    # 构造productionSet 集合：
    for row in gramma:
        for production in row.right:
            productionset[i] = [row.value, production]
            i += 1
    return productionset
def PrintProductionSet(productionset):
    print("拓广文法并给产生式编号：")
    for i in productionset:
        print("{:2d}".format(int(i))+" : ",end="")
        print(productionset[i][0]+" -> ",end="")
        res=""
        for elem in productionset[i][1]:
            res+=elem+" "
        print(res)
def checkRepeat(resultSet,item,gramma,nset,tset):
    newset = []
    newtemp = []
    newitem=Item(item.left,item.right)
    newitem.setIndex(item.index+1)
    newset.append(newitem)
    newtemp.append((newitem.left, newitem.right, newitem.index))
    for i in newset:
        if i.index==i.maxindex:
            continue
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
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
            for i in newtemp:
                if i not in oldtemp:
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
        isrepeat,newset,nextstatus=checkRepeat(resultSet,status.productionSet[i],gramma,nset,tset)
        #如果不是重复的话：
        if not isrepeat:
            #创建新的状态：
            newstatus=Status()
            newstatus.productionSet=newset
            newstatus.initid()
            #添加到最终的结果集合
            resultSet.append(newstatus)
            #创建指向新状态的边：
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
            # 创建指向自己的一个边：
                L1=Line(status.productionSet[i].right[status.productionSet[i].index],status)
                status.line.append(L1)
        i+=1
def getDFA(productionset,tset,nset,gramma):
    start=Status()
    start.productionSet.append(Item(productionset[0][0],productionset[0][1]))
    #创造开始状态的所有产生式：
    for i in start.productionSet:  #遍历item
        if i.right[i.index] in nset:
            for row in gramma:
                if row.value==i.right[i.index]:
                    for k in row.right:
                        start.productionSet.append(Item(row.value,k))
    start.initid()
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
def main():
    gramma,start=cin()
    productionSet=getProductionSet(gramma)
    PrintProductionSet(productionSet)
    tset,nset=getSet(gramma)
    getDFA(productionSet,tset,nset,gramma)

if __name__ == '__main__':
    main()


# S->a A|b B
# A->c A|d
# B->c B|d
# exit

