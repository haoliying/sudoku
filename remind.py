import copy

def checkSuccess(sudoku):
	# 判断是否完成数独
	for r in range(9):
		for c in range(9):
			if sudoku[r][c]==0:
				return False
	return True

def checkNumber(n, r, c, sudoku):
	# 判断数字n是否能填入sudoku数独的(r,c)单元格中
	arrayrow = sudoku[r]
	arraycol = [row[c] for row in sudoku]
	arraysquare = [0 for row in range(9)]
	br,_ = divmod(r,3)
	bc,_ = divmod(c,3)
	for i in range(3):
		for j in range(3):
			arraysquare[i*3+j] = sudoku[br*3+i][bc*3+j] 

	if (n in arrayrow) or (n in arraycol) or (n in arraysquare):
		return False
	else:
		return True

def countNumber(array33):
	# 判断3X3的单元格里有几个1-9的数字
	c = 0
	s = 0
	for row in array33:
		for item in row:
			if item > 0:
				c = c + 1
				s = s + item
	return c, s

def findNumber(n, array33):
	# 判断数字n是否在3x3数组中
	for r, row in enumerate(array33):
		for c, item in enumerate(row):
			if item == n:
				return True, r, c 
	return False, 0, 0

def remindAll(sudoku):
	# 填充数独sudoku所有单元格的所有可能性
	# 转为计算数独（9X9包含3X3）
	array33 = [[0 for col in range(3)] for row in range(3)]
	array99 = [[array33 for col in range(9)] for row in range(9)]
	array2727 = [[0 for col in range(27)] for row in range(27)]
	arraynumber = [1,2,3,4,5,6,7,8,9]

	for nr, row in enumerate(sudoku):
		for nc, item in enumerate(row):
			if item > 0:
				r,c = divmod(item-1,3)
				arraytmp=copy.deepcopy(array33)
				arraytmp[r][c]=item
				array99[nr][nc]=copy.deepcopy(arraytmp)

	# 填充所有可能性
	for r99, row99 in enumerate(array99):
		for c99, arrayitem in enumerate(row99):
			if sudoku[r99][c99] == 0:
				for num in arraynumber:
					r,c = divmod(num-1,3)
					if checkNumber(num, r99, c99, sudoku):
						arrayitem[r][c] = num
					else:
						arrayitem[r][c] = 0
					array2727[r99*3+r][c99*3+c] = arrayitem[r][c]
				array99[r99][c99]=copy.deepcopy(arrayitem)
			else:
				r,c = divmod(sudoku[r99][c99]-1,3)
				array2727[r99*3+r][c99*3+c] = sudoku[r99][c99]

	return array99, array2727

def array2str(array33)->str:
	s = ''
	b = ''
	for r, rows in enumerate(array33):
		for c, num in enumerate(rows):
			if num!=0:
				cell = '%s%s'%(b,num)
			else:
				cell = '%s '%b
			s = s + cell
			b = ' '
		if r != 2:
			s = s + '\n'
		b = ''
	return s

def array992array2727(array99):
	array2727 = [[0 for col in range(27)] for row in range(27)]
	for r, rows in enumerate(array99):
		for c, cell in enumerate(rows):
			for cr, crows in enumerate(cell):
				for cc, v in enumerate(crows):
					array2727[r*3+cr][c*3+cc]=v
	return array2727
