from random import random
import matplotlib.pyplot as plt
from copy import deepcopy
 
SIZE = 7
BASE_WEIGHT = 1
EPS = 0.01

def f(x, n):
    return x ** n

def generate_table():
    table = []

    x = random() * 5
 
    for _ in range(SIZE):
        y = random() * 5

        table.append([x, y, BASE_WEIGHT])
        x += 1

    return table

def print_table(table):
    print("\n   Сгенерированная таблица\n")
    print("  №    |     x     |     y    |   w   ")
    print("--------------------------------------")

    for i in range(len(table)):
        print("  %-3d  |   %-5.2f   |   %-4.2f   |   %-5.2f   " %(i + 1, table[i][0], table[i][1], table[i][2]))

def change_weight(table):
    global changed
    changed = True
    
    try:
        place = int(input("\nВведите номер точки в таблице: "))
        new_weight =  float(input("\nВведите новый вес точки: "))
    except:
        return 

    table[place - 1][2] = new_weight

    return table

def print_menu():
    print("\nМеню\n \
    \n1. Распечатать таблицу\
    \n2. Изменить вес точки\
    \n3. Вывести результаты\n\
    \n0. Выйти")

def init_matrix(size):
    return [[0 for i in range(size + 2)] for i in range(size + 1)]

def make_slae_matrix(table, power):
    size_tab = len(table)
    matrix = init_matrix(power)
    for i in range(power + 1):
        for j in range(power + 1):
            a_koef = 0.0
            rightside_koef = 0.0
            for k in range(size_tab):
                weight = table[k][2]
                x = table[k][0]
                y = table[k][1]
                a_koef += weight * f(x, (i + j)) # p*x**(k+m)
                rightside_koef += weight * y * f(x, i)
            matrix[i][j] = a_koef
            matrix[i][power + 1] = rightside_koef
 
    return matrix
 
 
def solve_matrix_gauss(matrix):
    size_mat = len(matrix)
 
    for i in range(size_mat):
        for j in range(i + 1, size_mat):
            if (i == j):
                continue
            k = matrix[j][i] / matrix[i][i]
            for q in range(i, size_mat + 1):
                matrix[j][q] -= k * matrix[i][q]
 
    result = [0 for i in range(size_mat)]
 
    for i in range(size_mat - 1, -1, -1):
        for j in range(size_mat - 1, i, -1):
            matrix[i][size_mat] -= result[j] * matrix[i][j]
        result[i] = matrix[i][size_mat] / matrix[i][i]

    return result

def get_coords(table):
    x_arr = []
    y_arr = []
    for i in range(len(table)):
        x_arr.append(table[i][0])
        y_arr.append(table[i][1])

    return x_arr, y_arr

def find_graph(table, cur_power):
    matrix = make_slae_matrix(table, cur_power)
    result = solve_matrix_gauss(matrix)

    x, y = [], []
    k = table[0][0] - EPS
 
    while (k <= table[len(table) - 1][0] + EPS):
        y_cur = 0
        for j in range(0, cur_power + 1):
            y_cur += result[j] * f(k, j)
 
        x.append(k)
        y.append(y_cur)
        k += EPS
 
    return x, y
 
 
def make_equal_weights_table(table):
    for i in range(len(table)):
        table[i][2] = 1

    return table
 
 
def solve(table):
    try:
        power = int(input("\nВведите степень аппроксимирующего многочлена: "))
    except:
        return 
 
    if changed:
        changed_table = deepcopy(table)
        table = make_equal_weights_table(table)
 
    for cur_power in range(1, power + 1):
        if (cur_power > 2 and cur_power < power):
            continue
 
        x, y = find_graph(table, cur_power)
        plt.plot(x, y, label = "Equal weights:\nn = %d" %(cur_power))

        if changed:
            x, y = find_graph(changed_table, cur_power)
            plt.plot(x, y, label = "Diff weights:\nn = %d" %(cur_power))

    x_arr, y_arr = get_coords(table)
    plt.plot(x_arr, y_arr, 'o', label = "Date")

    plt.legend()
    plt.grid()
    plt.xlabel("Axis X")
    plt.ylabel("Axis Y")
    plt.show()
 
    if changed:
        return changed_table

    return table

if __name__ == "__main__":
    changed = False

    table = generate_table()

    punkt = -1

    while (punkt != 0):
        print_menu()

        try:
            punkt = int(input("\nВведите пункт меню: "))
        except:
            continue
 
        if (punkt == 1):
            print_table(table)
        elif (punkt == 2):
            table = change_weight(table)
        elif (punkt == 3):
            table = solve(table)