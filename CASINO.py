from ctypes import *
import time

valuta = "руб"
money = 0
startMoney = 0
playGame = True
defaultMoney= 10000
windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

def pobeda(result):
    color(14)
    print(f"    Рад тебя видеть в моем КАЗИНО 678, дорогой! Выигрыш составил: {result} {valuta}")
    print(f"    У тебя на счету: {money} {valuta} ")

def proigr(result):
    color(12)
    print(f"    К сожалению проигрыш: {result} {valuta}")
    print(f"    У тебя на счету: {money} {valuta} ")
    print(f"comeback")

def loadMoney():
    try:
        f = open("money.dat", "r")
        m = int(f.readline())
        f.close()
    except FileNotFoundError:
        print("error")
        m = defaultMoney
    return m

def saveMoney(moneyToSave):
    try:
        f = open("money.dat", "w")
        f.write(str(moneyToSave))
        f.close()
    except FileExistsError:
        print("error")
        quit(0)

def color(c):
    windll.Kernel32.SetConsoleTextAttribute(h,c)

def colorLine(c,s):
    for i in range(30):
        print()
    color(c)
    print("*" * (len(s)+2))
    print(" "+ s)
    print("*" * (len(s)+2))

def getIntImput(minimum, maximum, message):
    color(7)
    ret=-1
    while (ret<minimum or ret > maximum):
        st = input(message)
        if (st.isdigit()):
            ret = int(st)
        else:
            print("  Error")
    return ret

def getInput(digit, message):
    color(7)
    ret = ""
    while (ret == "" or not ret in digit):
        ret = input(message)
    return ret



def main():
    global money, playGame

    money = loadMoney()
    startMoney = money


    while (playGame and money >0):
        colorLine(10, "Рад тебя видеть в моем КАЗИНО 678, дорогой!")
        color(14)
        print(f"У тебя на счету: {money} {valuta}")

        color(14)
        print(" Ты можешь сыграть в:")
        print("     1. Рулетка")
        print("     2. Кости")
        print("     3. Однорукий бандит")
        print("     0. Выход.Ставка 0 в играх - выход.")
        color(7)

        x= getInput("0123", " Твой выбор?")
        if (x== "0"):
            playGame = False
        elif (x == "1"):
              pass # roulet()
        elif (x == "2"):
              pass # dice()
        elif (x == "3"):
              pass # oneHandBand()

    if (money > 0):  
        colorLine(12, "       Ну давай...       ")
    color(13)
    if (money <= 0):
        print("Пшол вон, нищеброд!")
    color(11)

    saveMoney(money)
    color(7)
    time.sleep(2)
    quit(0)



main()
