import mytools.calc
from mytools import strhelper
from mytools.calc import add,div

def main():
    print(add(12,8))
    print(div(10,0))

    print(strhelper.upper_all("qwe"))
    print(strhelper.reverse_str("qwe"))
    print(strhelper.count_char("qwe","q"))

main()