N=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
Lable=[False for i in range(26)]
class label(object):
    def __init__(self,val,type,right):
        self.value=val
        self.terminal=type
        self.right=right
    def op(self):
        return self.value[0]
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
def cin():
    print("请输入文法，例如：A->a|Ab,输入exit结束输入:")
    gramma=[]
    while True:
        r=input()
        if r!='exit':
            r=r.split("->")
            temp=label(r[0],False,r[1].split("|"))
            gramma.append(temp)
        else:
            break
    print("解析输入文法：")
    printGramma(gramma)
    return gramma
def printGramma(gramma):
    for i in gramma:
        print((i.value,i.right))
    print("-------------------------------")
def RemoveLeftRecursion(gramma):
    print("消除左递归：")
    i=0
    length=len(gramma)
    while i <length:
        j=0
        while j<i:
            tempright=[]
            for k in gramma[i].right:
                if k[0]==gramma[j].value:
                    for m in gramma[j].right:
                        tempright.append(m+k[1:len(k)])
                else:
                    tempright.append(k)
            gramma[i].right=tempright
            j+=1
        a=[]
        b=[]
        for k in gramma[i].right:
            #不构成左递归:
            if k[0]!=gramma[i].value:
                b.append(k)
            else:
                a.append(k)

        if len(a)==0:
            pass
        #如果存在左递归:
        else:
            newright=[]
            for k in b:
                newright.append(k+gramma[i].value+'~')
            gramma[i].right=newright
            newelemright=[]
            for k in a:
                newelemright.append(k[1:len(k)]+gramma[i].value+'~')
            newelemright.append("ε")
            newgramma=label(gramma[i].value+'~',False,newelemright)
            gramma.append(newgramma)
        i+=1
    gramma.sort(key=label.op)
    printGramma(gramma)
    return gramma
def removeLeftFactor(gramma):
    cnt=0
    length=len(gramma)
    for i in gramma:
        if cnt>=length:
            break
        maxlength=len(i.right[0])
        j=0
        while j<=maxlength:
            flag=True
            for k in i.right:
                if i.right[0][0:j]!=k[0:j]:
                    flag=False
                    if i.right[0][0:j]=="~" or i.right[0][0:j]=="^" or k[0:j]=="~" or k[0:j]=="^":
                        j-=1
                    break
            if flag:
                j+=1
            else:
                break
        maxsubstr=i.right[0][0:j-1]
        if len(maxsubstr)==0:
            continue
        newelemright=[]
        for k in i.right:
            if len(k[j-1:len(k)])==0:
                newelemright.append("ε")
            else:
                newelemright.append(k[j-1:len(k)])
        newgramma=label(i.value+'^',False,newelemright)
        gramma.append(newgramma)
        i.right=[maxsubstr+maxsubstr+i.value+'^']
        cnt+=1
    print("提取左因子：")
    gramma.sort(key=label.op)
    printGramma(gramma)
    newgramma={}
    for i in gramma:
        newgramma[i.value]=i.right
    return (newgramma,gramma)
#获取终结符和非终结符号：
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
def Except(arr,elem):
    res=[]
    contain=False
    for i in arr:
        if i!=elem:
            res.append(i)
        else:
            contain=True
    return (res,contain)
def add(arr,lists):
    change=False
    for i in lists:
        if i not in arr:
            arr.append(i)
            change=True
    return arr,change
def getFirst(tset,nset,newgramma):
    First={}
    for i in tset:
        First[i]=[i]
    for i in newgramma:
        First[i]=[]
    loop=True
    while True:
        if not loop:
            break
        loop = False
        for Nlabel in newgramma:
            for production in newgramma[Nlabel]:
                print(production)
                Continue=True
                n=len(production)
                labelindex=0
                while Continue and labelindex<n:
                    if len(First[production[labelindex]])==0:
                        Continue=False
                    else:
                        res,Continue=Except(First[production[labelindex]],"ε")
                        First[Nlabel],ischange=add(First[Nlabel],res)
                        if ischange:
                            loop=True
                if Continue:
                    First[Nlabel],ischange=add(First[Nlabel],["ε"])
    return First
def getFollow():
    pass
def main():
    gramma=cin()
    #消除左递归：
    gramma=RemoveLeftRecursion(gramma)
    #提取左因子：
    newgramma,gramma=removeLeftFactor(gramma)
    #获取终结符和非终结符号的集合：
    Tset,Nset=getSet(gramma)
    #获取First集合：
    First=getFirst(Tset,Nset,newgramma)
    # for i in First:
    #     print((i,First[i]))
if __name__=='__main__':
    main()

# A->B a|A a|c
# B->B b|A b|d
# exit