import xlrd


def count(n1, n2, x, y, c, score):
	if x == 0 and y == 0:
		return
	score[n1] += x/(x+y)*c
	score[n2] += y/(x+y)*c


def delp(data, length, col):
	# 淘汰
	j = 0
	for i in range(length):
		if data[j][col] == 0 and data[j][col+1] == 0:
			del (data[j])
		else:
			j += 1
	return j


def getScore(length, col, c, score, data):
	# 评分
	for i in range(length // 2):
		n1 = str(data[i * 2][0])
		n2 = str(data[i * 2 + 1][0])
		x = data[i * 2][col] + data[i * 2][col+1] + data[i * 2][col+2]
		y = data[i * 2 + 1][col] + data[i * 2 + 1][col+1] + data[i * 2 + 1][col+2]
		count(n1, n2, x, y, c, score)


def run(exl: str):
	workbook = xlrd.open_workbook(exl)
	table = workbook.sheet_by_index(0)
	confirm = table.row_values(1, start_colx=1)
	score = {}
	data = []
	length = 16
	for i in range(length):
		data.append(table.row_values(i + 1))
		score[str(data[i][0])] = 0
	getScore(length, 1, 2, score, data)
	length = delp(data, length, 4)
	getScore(length, 4, 4, score, data)
	length = delp(data, length, 7)
	getScore(length, 7, 8, score, data)
	length = delp(data, length, 10)
	getScore(length, 10, 16, score, data)
	return list(score.keys()), score

