def cin():
    while True:
        r=input()
        if r=='exit':
            break
        else:
            print(r)
def secondinput():
    while True:
        r=input()
        if r=='exit':
            break
        else:
            print(r)
def main():
    cin()
    print("第一次输入结束：")
    secondinput()
    print("第二次输入结束：")
if __name__ == '__main__':
    main()

#