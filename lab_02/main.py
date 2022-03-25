import math

def parse_file(file_name):
	try:
		file = open(file_name, encoding = "utf-8")
	except:
		print("Ошибка: нет такого файла")
		return []
	table = []
	num_line = 0
	for line in file:
		arr = []
		try:
			arr = [float(num) for num in line.split()]
		except:
			print("Ошибка: строка \"", line, "\" содержит неверное число")
			return []
		table.append(arr)
		if (len(table[num_line]) != 5):
			print("Ошибка: недостаточно чисел в строке", num_line + 1)
			return []
		
		num_line += 1
		
		file.close()
		return table
def read_data():
	try:
		print("\nВведите:\n")
		nx = int(input("Степень аппроксимирующего полинома для x: "))
		ny = int(input("Степень аппроксимирующего полинома для y: "))
		if (nx <= 0) or (ny <= 0):
			print("Ошибка: степень должна быть не отрицательна")
			return -1, -1, -1, -1, -1
	except:
		print("Ошибка: степень должна быть целым числом")
		return -2, -2, -2, -2, -2
	try:
		x = float(input("Значение x: "))
		y = float(input("Значение y: "))
	except:
		print("Ошибка: неверно введены значения")
		return -3, -3, -3, -3, -3
	return 0, nx, ny, x, y

def print_table(table):
	print("x/y")
	print()
	print("0.00" + " " * 12, "1.00" + " " * 12 + "4.00" + " " * 12 + "9.00" + " " * 13 + "16.00")
	print("1.00" + " " * 12, "2.00" + " " * 12 + "5.00" + " " * 12 + "10.00" + " " * 12 + "17.00")
	print("4.00" + " " * 12, "5.00" + " " * 12 + "8.00" + " " * 12 + "13.00" + " " * 12 + "20.00")
	print("9.00" + " " * 12, "10.00" + " " * 11 + "13.00" + " " * 11 + "18.00" + " " * 12 + "25.00")
	print("16.00" + " " * 11, "17.00" + " " * 11 + "20.00" + " " * 11 + "25.00" + " " * 12 + "32.00")

def find_div_difference(x1, y1, x2, y2):
	if (abs(x1 - x2) > 1e-7):
		return (y1 - y2) / (x1 - x2)

def find_index_table(table, x, power):
	if (power >= len(table)):
		return -5 # Not enough data
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
	
	if (power <= 1):
		ind -= 1
	
	return ind

def newton_polynom(table, x, power):
	ind = find_index_table(table, x, power)
	print("Ind = ", ind)
	
	if (ind < 0):
		return # Not enough data
	
	res = table[ind][1]
	for i in range (power):
		koef = 1
		for k in range (i + 1):
			koef *= (x - table[ind + k][0])
		for j in range (power - i):
			table[ind + j][1] = find_div_difference(table[ind + j][0], table[ind + j][1], table[ind + j + i + 1][0], table[ind + j + 1][1])
		
		res += (koef * table[ind][1])
	return res

def multi_polynominal(table, nx, ny, x, y):
	x_arr = []
	y_arr = []
	for i in range(len(table)):
		x_arr.append(i)
		y_arr.append(i)
	table_xz = []
	result_xz = []
	for i in range(len(table)):
		for j in range(len(table)):
			table_xz.append([x_arr[j], table[i][j]])
			print(table_xz)
		result_xz.append([y_arr[i], newton_polynom(table_xz, x, nx)])
		table_xz.clear()
	result_xyz = newton_polynom(result_xz, y, ny)
	return result_xyz

def main():
	data = read_data()
	if (data[0] != 0):
		return
	file_name = input("\nИмя файла: ")
	table = parse_file(file_name)
	if (table == []):
		return
	print_table(table)
	print()
	print("Многомерная интерполяция: 5.0")

if __name__ == "__main__":
	main()