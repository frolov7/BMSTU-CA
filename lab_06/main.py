def center_side(y, step, ind):
    if ind > 0 and ind < len(y) - 1:
        return (y[ind + 1] - y[ind - 1]) / 2 / step
    else:
        return '---'


def left_side(y, step, ind):
    if ind > 0:
        return (y[ind] - y[ind - 1]) / step
    else:
        return '---'


def right_side(y, step, ind):
    if ind < len(y) - 1:
        return (y[ind + 1] - y[ind]) / step
    else:
        return '---'


def second_diff(y, step, ind):
    if ind > 0 and ind < len(y) - 1:
        return (y[ind - 1] - 2 * y[ind] + y[ind + 1]) / step ** 2
    else:
        return '---'


def runge_left(y, step, ind):
    if ind < 2:
        return '---'
    f1 = left_side(y, step, ind)
    f2 = (y[ind] - y[ind - 2]) / 2 / step

    return f1 + f1 - f2


def align_vars_diff(y, x, step, ind):
    if ind > len(y) - 2:
        return '---'
    eta_ksi_diff = (1 / y[ind + 1] - 1 / y[ind]) / (1 / x[ind + 1] - 1 / x[ind])
    y = y[ind]
    x = x[ind]

    return eta_ksi_diff * y * y / x / x


x = [1, 2, 3, 4, 5, 6]
y = [0.571, 0.889, 1.091, 1.231, 1.333, 1.412]
methods = [left_side, center_side, runge_left, align_vars_diff, second_diff]

print('-' * (6 + 8 * 5))
for i in range(len(x)):
    print('|', end='')
    for j in range(len(methods) - 2):
        res = methods[j](y, x[1] - x[0], i)
        print(f'{res:.3f}'.center(8) if res != '---' else res.center(8), '|', sep='', end='')
    res = align_vars_diff(y, x, x[1] - x[0], i)
    print(f'{res:.3f}'.center(8) if res != '---' else res.center(8), '|', sep='', end='')
    res = second_diff(y, x[1] - x[0], i)
    print(f'{res:.3f}'.center(8) if res != '---' else res.center(8), '|', sep='')
    print('-' * (6 + 8 * 5))
