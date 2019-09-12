def log(x):
	print('[log]: ' + str(x))


def conv(x): # if float - makes int;
	for i in range(len(x)):
		itype = str(type(x[i])).split("'")[1]
		if itype == 'float':
			if x[i] % 1 == 0:
				x[i] = int(x[i])
	return x

def qiyamul_layl(x, y):
	m = x
	f = y
	
	f = str(int(f[0:2]) + 24) + f[2:] # Прибавляем 24 к часам фаджра, чтобы удобно было считать время между ним и магрибом

	m = m.split(':') # Разбиваем время намазов на часы и минуты
	f = f.split(':')

	night = [int(f[0]) - int(m[0]), int(f[1]) - int(m[1])] # Массив, хранящий время, которое длится ночь

	if night[1] < 0:
		night[0] -= 1
		night[1] *= -1

	half = [night[0] / 2, night[1] / 2]
	if half[0] % 1 == 0.5:
		half[0] -= 0.5
		half[1] += 30
	if half[1] % 1 == 0.5:
		half[1] -= 0.5

	half = conv(half)

	mid = [int(m[0]) + half[0], int(m[1]) + half[1]]

	if mid[1] >= 60:
		mid[0] += 1
		mid[1] -= 60
	if mid[0] >= 24:
		mid[0] -= 24

	if mid[0] < 10:
		mid[0] = '0' + str(mid[0])
	if mid[1] < 10:
		mid[1] = '0' + str(mid[1])

	mid [0], mid[1] = str(mid[0]), str(mid[1])
	mid = ':'.join(mid)


	twoth = [2 * night[0] / 3, 2 * night[1] / 3]

	if (twoth[0] % 1 > 0.3) and (twoth[0] % 1 < 0.4):
		twoth[0] = twoth[0] // 1
		twoth[1] += 20
	elif (twoth[0] % 1 > 0.6) and (twoth[0] % 1 < 0.7):
		twoth[0] = twoth[0] // 1
		twoth[1] += 40

	if (twoth[1] % 1 > 0.3) and (twoth[1] % 1 < 0.4):
		twoth[1] = twoth[1] // 1
	elif (twoth[1] % 1 > 0.6) and (twoth[1] % 1 < 0.7):
		twoth[1] = 1 + twoth[1] // 1

	twoth = conv(twoth)

	last_third = [int(m[0]) + twoth[0], int(m[1]) + twoth[1]]

	if last_third[1] >= 60:
		last_third[0] += 1
		last_third[1] -= 60
	if last_third[0] >= 24:
		last_third[0] -= 24

	if last_third[0] < 10:
		last_third[0] = '0' + str(last_third[0])
	if last_third[1] < 10:
		last_third[1] = '0' + str(last_third[1])

	last_third [0], last_third[1] = str(last_third[0]), str(last_third[1])
	last_third = ':'.join(last_third)

	return 'Полночь: ' + mid + '\nПоследняя треть ночи: ' + last_third