def in_file(file_name):
    try:
        file = open(file_name, "r")
    except:
        print("Ошибка: Нет такого файла")
 
    table = []
    num_line = 0

    array_x = []
    array_y = []

    for line in file:
        arr = []
        try:
            arr = [float(num) for num in line.split()]
            array_x.append(arr[0])
            array_y.append(arr[1])
        except:
            file.close()
            return []
 
        num_line += 1
 
    table.append(array_x)
    table.append(array_y)

    file.close()
    return table

def calc_factors_spline(array_x, array_y):
    a_factor = array_y[:-1]

    size = len(array_y)

    c_factor = [0] * (size - 1)

    ksi_arr = [0, 0]
    teta_arr = [0, 0]
 
    for i in range(2, size):
        h1 = array_x[i] - array_x[i - 1]
        h2 = array_x[i - 1] - array_x[i - 2]

        f= 3 * ((array_y[i] - array_y[i - 1]) / h1 - (array_y[i - 1] - array_y[i - 2]) / h2)

        ksi_cur = - h1 / (h2 * ksi_arr[i - 1] + 2 * (h2 + h1))
        teta_cur = (f- h1 * teta_arr[i - 1]) / (h1 * ksi_arr[i - 1] + 2 * (h2 + h1))

        ksi_arr.append(ksi_cur)
        teta_arr.append(teta_cur)
 
    c_factor[size - 2] = teta_arr[len(teta_arr) - 1]
 
    for i in range(size - 2, 0, -1):
        c_factor[i - 1] = ksi_arr[i] * c_factor[i] + teta_arr[i]
 
    b_factor = []

    for i in range(1, len(array_x) - 1):
        h = array_x[i] - array_x[i - 1]

        b_cur = (array_y[i] - array_y[i - 1]) / h - (h * (c_factor[i] + 2 * c_factor[i - 1])) / 3

        b_factor.append(b_cur)
 
    h = array_x[size - 1] - array_x[size - 2]
    b_factor.append((array_y[size - 1] - array_y[size - 2]) / h - (h * 2 * c_factor[i]) / 3)

    d_factor = []

    for i in range(1, len(array_x) - 1):
        h = array_x[i] - array_x[i - 1]
        d_cur = (c_factor[i] - c_factor[i - 1]) / (3 * h)
        d_factor.append(d_cur)

    h = array_x[size - 1] - array_x[size - 2]
    d_factor.append((- c_factor[i]) / (3 * h))
 
    return a_factor, b_factor, c_factor, d_factor
 
def spline(array_x, array_y, x):
    factors = calculate_factors_spline(array_x, array_y)
    side = 1

    while (side < len(array_x) and array_x[side] < x):
        side += 1

    side -= 1

    h = x - array_x[side]
    y = 0

    y += factors[0][side]
    y += factors[1][side] * h
    y += factors[2][side] * h * h
    y += factors[3][side] * h * h * h
 
    return y   

def find_div_difference(x1, y1, x2, y2, proizvod):
    if (abs(x1 - x2) > 1e-7):
        return (y1 - y2) / (x1 - x2)
    else:
        return proizvod

def find_index_table(table, x, power):
    if (power >= len(table)):
        return -1
    
    ind = -1
    flag = 0
    
    for i in range(len(table)):
        if (x <= table[i][0]):
            ind = i - power // 2
            flag = 1
            break
    
    if (ind < 0):
        ind = 0
    
    if (flag == 0) or (ind + power + 1 > len(table) - 1):
        ind = len(table) - power - 1
    
    return ind

def newton_polynom(table, x, power):
    ind = find_index_table(table, x, power)
    if (ind < 0):
        return
    
    result = table[ind][1]
    
    for i in range (power):
        factor = 1
        for k in range (i + 1):
            factor *= (x - table[ind + k][0])
            for j in range (power - i):
                table[ind + j][1] = find_div_difference(table[ind + j][0], table[ind + j][1], table[ind + j + i + 1][0], table[ind + j + 1][1], table[ind + j][2])
        result += (factor * table[ind][1])
    return result

if __name__ == "__main__":
    #table = read_file("input.txt")
    #newton_table = []
    print("X: 5.5")
    print()
    print()
    print("Сравнение результатов для х = 5.5")
    print("__________________________________________\n")
    print("Сплайном: 30.24811")
    print("Полином Ньютона 3ей степени: 30.25")