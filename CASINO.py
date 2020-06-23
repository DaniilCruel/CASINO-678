from ctypes import *
import time
import random

valuta = "руб"
money = 0
startMoney = 0
playGame = True
windll.Kernel32.GetStdHandle.restype = c_ulong
h = windll.Kernel32.GetStdHandle(c_ulong(0xfffffff5))

def pobeda(result):
    color(14)
    print(f"    Выигрыш составил: {result} {valuta}")
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
        print("error R")
        m = 0
    return m

def saveMoney(moneyToSave):
    try:
        f = open("money.dat", "w")
        f.write(str(moneyToSave))
        f.close()
    except FileExistsError:
        print("error W")
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



def getRoulet(visible):
    tickTime = random.randint(100,200) / 100000
    mainTime = 0
    number = random.randint(0,38)
    increaseTickTime = random.randint(100,110) / 5000
    col=1

    while (mainTime < 1.2):
        col +=1
        if (col >15):
            col = 1

        mainTime +=tickTime
        tickTime += increaseTickTime

        color(col)
        number +=1
        if (number >38):
            number=0
        
        printNumber = number
        if (number == 37):
            printNumber = "00"
        elif( number == 38):
            printNumber = "000"

        print("Число >", printNumber, "*"*number, "*"*(79-number*2),   "*"*number)
        
        if (visible):
            time.sleep(mainTime)
    
    return number


def roulet():
    global money
    playGame = True
    

    while (playGame and money >0):
        colorLine (3, "ДОБРО ПОЖАЛАВАТЬ НА ИГРУ В РУЛЕТКУ!")
        color(14)
        print(f"\n У тебя на счету: {money} {valuta} \n")
        color(11)
        print(" Ставлю на...")
        print("     1. Четное    (выигрыш 1:1)")
        print("     2. Нечетное  (выигрыш 1:1)")
        print("     3. Дюжина    (выигрыш 3:1)")
        print("     4. Число     (выигрыш 36:1)")
        print("     0. Возврат в предыдыщие меню")

        x = getInput("01234", "     Твой выбор?" )
        playRoulette = True
        
        if (x == "3"):
            color(2)
            print()
            print("Выбери числа:...")
            print("     1. От 1  до 12")
            print("     1. От 13 до 24")
            print("     1. От 25 до 36")
            print("     0. Назад")

            duzhina = getInput("0123", "     Твой выбор?" )
            
            if   (duzhina == "1"):
                textDuzhina  = "От 1  до 12"
            elif (duzhina == "2"):
                textDuzhina  = "От 13  до 24"
            elif (duzhina == "3"):
                textDuzhina  = "От 25  до 36"
            elif (duzhina == "0"):
                playRoulette = False

        elif (x=="4"):
            chislo = getIntImput(0,36, "На какое число ставишь? (0..36):")

        color(7)
        if (x=="0"):
            return(0)

        if (playRoulette):
            stavka = getIntImput(0,money, f"       Сколько поставишь? (не больше {money}):")
            if (stavka == 0):
                return(0)
            
            number = getRoulet(True)
            print()
            color(11)


            printNumber =""
            if (number<37):
                print(f"    Выпало число {number}! ")
            else:
                if (number == 37):
                    printNumber =="00"
                elif (number == 38):
                    printNumber =="000"
                print(f"    Выпало число {printNumber}! ")
            
            if (x == "1"):
                print("     Ты ставил на Четное!")
                if (number < 37 and number % 2 ==0 and number !=0):
                    money +=stavka
                    pobeda(stavka)
                else:
                    money -=stavka
                    proigr(stavka)
            elif (x == "2"):
                print("     Ты ставил на Нечетное!")
                if (number < 37 and number % 2 !=0):
                    money +=stavka
                    pobeda(stavka)
                else:
                    money -=stavka
                    proigr(stavka)        
            elif (x == "3"):
                print(f"     Ставка сделанна на диапозон {textDuzhina}. ")
                winDuzhine = ""
                if (number < 13 and number >0):
                    winDuzhine = "1"
                elif (number < 25 and number  >12):
                    winDuzhine = "2" 
                elif (number < 37 and number  >24):
                    winDuzhine = "3" 

                if (duzhina == winDuzhine):
                    money +=stavka*2
                    pobeda(stavka*3)
                else:
                    money -=stavka
                    proigr(stavka)
            elif (x == "4"):
                print(f"     Ставка сделана на число {chislo}!")
                if (number == chislo):
                    money +=stavka*35
                    pobeda(stavka*36)
                else:
                    money -=stavka
                    proigr(stavka)  
                    
            saveMoney(money)
            print()
            input(" Нажим Enter для продолжения...")

  



def main():
    global money, playGame
    Triger=False
    money = loadMoney()
    startMoney = money
    if (money<10):
        money+=200
        Triger=True


    while (playGame and money >0):
        colorLine(10, "Рад тебя видеть в моем КАЗИНО 678, дорогой!")
        color(14)
        if(Triger):
            print(f"  Держи 200 {valuta} дружище(нет)! ")
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
              roulet()
        elif (x == "2"):
              pass # dice()
        elif (x == "3"):
              pass # oneHandBand()

    if (money > 0):  
        colorLine(12, "       Ну давай...       ")
  
    if (money <= 0):
       colorLine(13,"      Пшол вон, нищеброд!     ")
    color(11)

    saveMoney(money)
    color(7)
    time.sleep(2)
    quit(0)



main()
