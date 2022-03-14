
def some_func():
    try:
        print("try_func")
        some_func2()
    except:
        print("except_func")

def some_func2():
    try:
        print("try_func2")
        raise("Exception")
    except:
        print("except_func2")
        exit()
        print("except_func")

for i in range(0,10):
    print()
    print(i)
    try:
        print("try1")
        some_func()
    except:
        print("except1")
