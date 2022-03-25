from numpy.polynomial.legendre import leggauss
from numpy import arange
from math import pi, cos, sin, exp
import matplotlib.pyplot as plt


def bass_func(param):
    subfunction = lambda x, y: 2 * cos(x) / (1 - (sin(x) ** 2) * (cos(y) ** 2))
    func = lambda x, y: (4 / pi) * (1 - exp(-param * subfunction(x, y))) * cos(x) * sin(x)
    return func


def simpson(func, a, b, nodes):
    if (nodes < 3 or nodes & 1 == 0):
        return

    h = (b - a) / (nodes - 1)
    x = a
    result = 0

    for _ in range((nodes - 1) // 2):
        result += func(x) + 4 * func(x + h) + func(x + 2 * h)
        x += 2 * h

    return result * (h / 3)


def arg_conversion(func2, value):  # преобразуем функцию args в одну функцию arg
    return lambda y: func2(value, y)


def t_to_x(t, a, b):
    return (b + a) / 2 + (b - a) * t / 2


def gauss(func, a, b, nodes):
    args, factor = leggauss(nodes)
    result = 0

    for i in range(nodes):
        result += (b - a) / 2 * factor[i] * func(t_to_x(args[i], a, b))

    return result


def integrate(func, limits, nodes, integrators):
    inside = lambda x: integrators[1](arg_conversion(func, x), limits[1][0], limits[1][1], nodes[1])
    return integrators[0](inside, limits[0][0], limits[0][1], nodes[0])


def tao_graph(integrate_func, arr_params, label):
    x = list()
    y = list()
    for i in arange(arr_params[0], arr_params[1] + arr_params[2], arr_params[2]):
        x.append(i)
        y.append(integrate_func(i))
    plt.plot(x, y, label=label)


def generate_label(n, m, func1, func2):
    result = "N = " + str(n) + ", M = " + str(m) + ", Methods = "
    if func1 == simpson:
        result += "Simpson"
    else:
        "Gauss"
    if func2 == simpson:
        result += "-Simpson"
    else:
        "-Gauss"

    return result


finish = False
while not finish:
    print("Введите")
    N = int(input("N: "))
    M = int(input("M: "))
    param = float(input("Параметр (tao): "))
    mode = bool(int(input("Внешний метод (0 - Гаусс; 1 - Симспсон): ")))

    if mode:
        func1 = simpson
    else:
        func1 = gauss
    mode = bool(int(input("Внутренний метод (0 - Гаусс; 1 - Симспсон): ")))
    if mode:
        func2 = simpson
    else:
        func2 = gauss

    integr_param = lambda tao: integrate(bass_func(tao), [[0, pi / 2], [0, pi / 2]], [N, M], [func1, func2])
    print('Результат с вашим параметром:', integr_param(param))
    try:
        tao_graph(integr_param, [0.05, 10, 0.05], generate_label(N, M, func1, func2))
    except ValueError:
        print("Симпсоном: аргумент должен быть > 2 и не (3, 5...);")
    except ZeroDivisionError:
        print("Нельзя использовать 2 Симпсона, в знаменателе ноль")
    finish = bool(int(input("Конец? (0 - Да, 1 - Нет): ")))

plt.legend()
plt.ylabel("Результат")
plt.xlabel("Значение tao")
plt.show()
