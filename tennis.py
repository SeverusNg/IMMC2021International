import xlrd
import xlwt

def count(n1, n2, x, y, c, score,x1,x2):
	if x == 0 and y == 0:
		return
	score[n1] += x/(x+y)*c+c*x2
	score[n2] += y/(x+y)*c+c*x1


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
		x1 = (65-data[i*2][13])/32
		x2 = (65-data[i*2+1][13])/32
		x = data[i * 2][col] + data[i * 2][col+1] + data[i * 2][col+2]
		y = data[i * 2 + 1][col] + data[i * 2 + 1][col+1] + data[i * 2 + 1][col+2]
		count(n1, n2, x, y, c, score,x1,x2)


def run(exl: str):
	workbook = xlrd.open_workbook(exl)
	table = workbook.sheet_by_index(0)
	confirm = table.row_values(1, start_colx=1)
	score = {}
	data = []
	length = 63
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
	return score
res = run("tennis.xls")
print(res)
outbook = xlwt.Workbook()
outsheet = outbook.add_sheet('My Worksheet')
t = 1
for k in res:
	outsheet.write(t,0, label = k)
	outsheet.write(t,1, label = res[k])
	t += 1
outbook.save("out.xls")