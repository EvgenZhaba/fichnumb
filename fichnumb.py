from random import randint, sample
from itertools import product
import sys

def printhelp():
    print(
    "Интерактивная игра FIndCHosenNUMBer - FICHNUMB - Фичнамб.",
    "",
    "Есть N разных чисел, в каждом M разрядов, каждое число в K-ичной системе счисления. Одно из этих чисел считается загаданным, и его номер надо найти.",
    "\tКаждый ход игрока состоит из проверки введённого числа и попытки угадать номер загаданного числа.",
    "Сперва игрок проверяет доступный список чисел введённым числом: игра вычисляет совпадения цифр по правилам игры \"Быки и коровы\":",
    "показывает 2 числа, количество совпадений:  и цифры, и её места; цифры, но не места. Например, для 2011 и 0212 будет: 1 2",
    "\tПо полученной информации игрок может для себя сделать предположения насчёт каждого числа из списка.",
    "После проверки доступного списка чисел игрок делает догадку: какое же число из списка загадано, вводя порядковый номер этого числа в списке.",
    "\tИгра из загаданного числа порязрядно вычитает число-догадку игрока, вычитание производится по модулю системы счисления, и выводит ответ.",
    "Если угадали, то поразрядное вычитание будет из нолей. В этом случае игрок побеждает.",
    "\tЕсли иначе, то загаданное число можно получить поразрядным сложением этого ответа и введённого числа-догадки (если оно известно).",
    "Можно не пытаться сразу угадать число, а выбирать номер того, которое даст наибольшую информацию о загаданном числе.",
    "\tПосле догадки текущий ход заканчивается и начинается следующий ход игрока.",
    "Цель - найти номер загаданного числа за наименьшее количество ходов.",
    ""
    "Автор игры и реализация: EvgenZhaba (связь через telegram). Версия: 0.4beta",
    "В этой версии есть:",
    "-debug - режим отладки, показывающий перед игрой: все числа и загаданное число.",
    "-help  - режим помощи, показывает информацию по возможным значениям чисел.",
    "\tДелает предположения и показывает по каждому числу те его варианты, которые есть в вариантах загаданного.",
    "",
    "Не рекомендуется делать длину числа и основание системы счисления больше 10. Режим помощи может замедлить работу игры.",
    "",
    sep='\n')

def inpfunc(max_len_list, min_digit, max_digit, text):
    while True:
        try:
            inp = input(text)
            inp_int = tuple(map(int, inp.split(" ")))
            if (len(inp_int) != max_len_list):
                raise IndexError
            for i in range(max_len_list):
                if (inp_int[i] > max_digit) or (inp_int[i] < min_digit):
                    raise OverflowError
            break
        except IndexError:
            print("Ошибка: неверное количество введённых элементов")
        except OverflowError:
            print("Ошибка: какое-то число вне диапазона")
        except:
            print("Какая-то ошибка, проверьте строку.")
    return inp_int

def bullsandcows(n1, n2):
    bulls, cows = 0, 0
    numb = [True for _ in range(len_numb)]
    for i in range(len_numb):
        if (n1[i] == n2[i]):
            bulls += 1
            numb[i] = False
            continue
        for j in range(len_numb):
            if (n1[i] == n2[j]) and numb[j]:
                cows += 1
                numb[j] = False
                break
    return bulls, cows

def print_help_list():
    print()
    print("Возможные варианты.")
    for i in range(len_list):
        if list_attempt[i]:
            print("Варианты для", i+1, "числа.")
            counter_magic = 0
            for elem in help_list[i]:
                if (elem in help_magic_number):
                    if (counter_magic < 10):
                        print(elem)
                    counter_magic += 1
            if (counter_magic >= 10):
                print("\tследующие варианты не показаны.")
            print("Всего вариантов:", len(help_list[i]), "- из них совпадает с вариантами загаданного:", counter_magic)
            print()
    print()
    

if __name__ == "__main__":
    printhelp()

    while True:
        len_numb, len_list, number_system = inpfunc(3, 2, 1000, "Введите через пробел длину числа, количество чисел и основание системы счисления(от 2 до 1000): ")
        if (pow(number_system, len_numb) < len_list):
            print("Количество чисел меньше, чем можно представить в этой системе счисления с заданной длиной числа. Попробуйте другие числа.")
        else:
            break

    list_numbers = sample(tuple(product([i for i in range(number_system)], repeat=len_numb)), len_list)    
    magic_number = list_numbers[randint(0, len_list-1)]
    list_attempt = [ True for __ in range(len_list)]
    
    help_list = [tuple(product([i for i in range(number_system)], repeat=len_numb)) for _ in range(len_list)]
    help_magic_number = tuple(product([i for i in range(number_system)], repeat=len_numb))

    
    enable_help = False
    sysargv = set(sys.argv)
    if ("-debug" in sysargv):
        print(list_numbers, magic_number)
    if ("-help" in sysargv):
        enable_help = True

    step = 0
    while True:
        step += 1
        print(step, " ход.")

        number = inpfunc(len_numb, 0, number_system-1, "Введите число-догадку, цифры через пробел: ")
        for i in range(len_list):
            if list_attempt[i]:
                bac = bullsandcows(number, list_numbers[i])
                print(i+1, bac)
                if enable_help:
                    help_list[i] = tuple([elem for elem in help_list[i] if bullsandcows(number, elem) == bac])
        if enable_help:
            print_help_list()

        kill_number_id = inpfunc(1, 1, len_list, "Введите номер числа для исключения: ")[0] - 1
        list_attempt[kill_number_id] = False
        answer = [(number_system + a - b) % number_system for a, b in zip(magic_number, list_numbers[kill_number_id])]
        print("Поразрядное вычитание из загаданного числа:", answer)
        
        if (magic_number == list_numbers[kill_number_id]):
            print("Вы победили!")
            print("Было сделано ходов:", step, "при конфигурации", len_numb, len_list, number_system)
            break
        
        if enable_help:
            help_magic_number = tuple([
                tuple((a + b) % number_system for a, b in zip(elem, answer)) for elem in help_list[kill_number_id] if 
                    tuple((a + b) % number_system for a, b in zip(elem, answer)) in help_magic_number])
            print_help_list()