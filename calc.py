def add(a,b)->float:
    return a+b
def sub(a,b)->float:
    return a-b
def mul(a,b)->float:
    return a*b
def div(a,b)->str or float:
    try:
        return a/b
    except ZeroDivisionError:
        return "除数不能为0"