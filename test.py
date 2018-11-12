"""
write by 高谦  未完成

底下注释非常详细，因为我健忘，怕给老师讲的时候自己忘了当初自己咋想的了
"""


class label(object):
    def __init__(self, val, right):
        # 指示当前边的值
        self.value = val
        # 指向下一个状态：转移后的状态。
        self.right = right


class Item(object):
    def __init__(self, val, sets):
        # 指示当前点的位置：
        self.index = 0
        # 指示状态中的产生式中的左边的非终结符。
        self.left = val
        # list[str] 一个字符串的列表：
        self.right = sets
        self.maxindex = len(self.right)

    # 修改当前点的位置的函数，新建状态的时候会用到：
    def setIndex(self, ind):
        self.index = ind


class Status(object):
    id = 0

    def __init__(self):
        # line
        self.line = []
        # Item
        self.productionSet = []
        self.static_id = Status.id
        Status.id += 1

    def addline(self, singleline):
        self.line.append(singleline)

    def addProduction(self, production):
        self.productionSet.append(production)

    def setStatusid(self, ids):
        self.static_id = ids


class Line(object):
    def __init__(self, tranval, next):
        self.next = next
        self.tranval = tranval


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
        print((i.value, i.right))
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
    temp = label(start + "*", [[start]])
    gramma.insert(0, temp)
    print("解析输入文法：")
    printGramma(gramma)
    return (gramma, start)


def getSet(gramma):
    Tset = []
    Nset = []
    for i in gramma:
        Nset.append(i.value)
        for j in i.right:
            for k in j:
                if isTerminal(k):
                    Tset.append(k)
    Tset = set(Tset)
    Tset = list(Tset)
    Tset.sort()
    return (Tset, Nset)


def getProductionSet(gramma):
    productionset = {}
    i = 0
    # 构造productionSet 集合：
    for row in gramma:
        for production in row.right:
            productionset[i] = [row.value, production]
            i += 1
    return productionset


def PrintProductionSet(productionset):
    print("产生式编号如下所示：")
    for i in productionset:
        print("{:2d}".format(int(i)) + " : ", end="")
        print(productionset[i][0] + " -> ", end="")
        res = ""
        for elem in productionset[i][1]:
            res += elem + " "
        print(res)


def checkRepeat(status, netstatus, gramma, nset):
    for i in status.productionSet:  # 遍历所有的item：
        # 如果真的是一个非终结符号：
        if i.right[i.index] in nset:
            # 添加这个非终结符号的所有的产生式到这个状态的productionSet中：
            for row in gramma:
                if row.value == i.right[i.index]:
                    status.productionSet.append(Item(row.value, row.right))
    return True


def Closure(status, nset, tset, gramma):
    # 首先判断是不是中指状态：status 的production中只有一个产生式，并且产生式的点在最右端
    # 是终止状态直接返回
    if len(status.productionSet) == 1 and status.productionSet[0].index == status.productionSet[0].maxindex:
        return
    # 如果不是终止状态：遍历productionSet
    # 查看哪一个产生式的右端的点后面是一个非终结符号，将这个非终结符号的所有产生式添加到这个集合的产生式
    # index是当前点所处的位置。
    for i in status.productionSet:  # 遍历所有的item：
        # 如果真的是一个非终结符号：
        if i.right[i.index] in nset:
            # 添加这个非终结符号的所有的产生式到这个状态的productionSet中：
            for row in gramma:
                if row.value == i.right[i.index]:
                    status.productionSet.append(Item(row.value, row.right))
    for i in status.productionSet:
        print((i.left, i.right, i.index))
    # 遍历当前状态productionSet中的所有item
    # 根据点的位置创造出下一个状态
    # 用一条边将当前状态和下一个状态连接在一起（边的next指向下一个状态，边的值就是当前index所指的符号的值）
    # 将边添加到当前状态的出边集合中
    # 这里特别需要注意的是判断一下新的状态是不是可能就是当前状态，是的话就别创建了，如果不行stackoverflow的话
    for i in status.productionSet:  # 遍历所有的item
        pass


def getDFA(productionset, tset, nset, gramma):
    start = Status()
    start.productionSet.append(Item(productionset[0][0], productionset[0][1]))
    Closure(start, nset, tset, gramma)


def main():
    gramma, start = cin()
    productionSet = getProductionSet(gramma)
    PrintProductionSet(productionSet)
    tset, nset = getSet(gramma)
    getDFA(productionSet, tset, nset, gramma)


if __name__ == '__main__':
    main()

# S->a A|b B
# A->c A|d
# B->c B|d
# exit

