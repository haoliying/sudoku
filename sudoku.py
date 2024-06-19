import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
import tkinter.font as font
from tkinter import filedialog
from functools import partial
import copy
from remind import remindAll, checkNumber, checkSuccess, array2str, array992array2727
from excel import importExcel, exportExcel, exportRemindExcel

# 重构数独
def buildSudoku(newSudoku):
	global sudoku,currentSudoku,dataSudokus,btnSudokus,picSudokus,markSudokus,currentRow,currentColumn
	global frames,picBGNormal,picBGFixed,array33
	sudoku=copy.deepcopy(newSudoku)
	currentSudoku = copy.deepcopy(sudoku) 
	dataSudokus=[[None for _ in range(9)] for _ in range(9)]
	btnSudokus=[[None for _ in range(9)] for _ in range(9)]
	picSudokus=[[None for _ in range(9)] for _ in range(9)]
	markSudokus=[[False for _ in range(9)] for _ in range(9)]
	for r,row in enumerate(sudoku):
		for c,col in enumerate(row):
			fr = r//3
			cr = r%3
			fc = c//3
			cc = c%3
			if sudoku[r][c]==0:
				btnSudokus[r][c]=ttk.Button(frames[fr][fc],image=picBGNormal,command=partial(btnSudokuClicked,r,c),style='NUMBER.TButton',compound='center')
				dataSudokus[r][c]=copy.deepcopy(array33)
			else:
				btnSudokus[r][c]=ttk.Button(frames[fr][fc],image=picBGFixed,command=partial(btnSudokuClicked,r,c),style='FIXED.TButton',compound='center',text=sudoku[r][c])
				dataSudokus[r][c]=copy.deepcopy(array33)
				dataSudokus[r][c][cr][cc]=sudoku[r][c]
			btnSudokus[r][c].grid(row=cr, column=cc, sticky="nsew")
			picSudokus[r][c]=btnSudokus[r][c].cget('image')
	currentRow = -1
	currentColumn = -1

# 功能按钮
def btnClicked(which):
	global sudoku, array33, currentSudoku, dataSudokus, btnSudokus, currentRow, currentColumn

	if which=="open":
		# 打开
		fn=filedialog.askopenfilename(filetypes=[("Excel/WPS格式表格", '.xls .xlsx .csv .xlsm .xlsb'), ('全部文件', '*.*')], defaultextension='.xlsx')
		if fn=='':
			return
		buildSudoku(importExcel(fn))
	elif which=="save":
		# 保存
		fn=filedialog.asksaveasfilename(filetypes=[("Excel/WPS格式表格", '.xls .xlsx .csv .xlsm .xlsb'), ('全部文件', '*.*')], defaultextension='.xlsx')
		if fn=='':
			return
		exportExcel(currentSudoku,fn)
	elif which=="export":
		fn=filedialog.asksaveasfilename(filetypes=[("Excel/WPS格式表格", '.xls .xlsx .csv .xlsm .xlsb'), ('全部文件', '*.*')], defaultextension='.xlsx')
		if fn=='':
			return
		exportRemindExcel(array992array2727(dataSudokus),fn)
	elif which=="reset":
		if messagebox.askyesno("警告","确定要重新开始吗！",default='no'):
			buildSudoku(sudoku)
	elif which=="remind":
		# 提示全部
		sudoku99, sudoku2727 = remindAll(currentSudoku)
		for r99, row99 in enumerate(sudoku99):
			for c99, sudoku33 in enumerate(row99):
				if currentSudoku[r99][c99]==0:
					dataSudokus[r99][c99]=copy.deepcopy(sudoku33)
					btnSudokus[r99][c99].config(text=array2str(dataSudokus[r99][c99]),style='REMIND.TButton')
	elif which=="cleanall":
		for r in range(9):
			for c in range(9):
				if currentSudoku[r][c]==0:
					dataSudokus[r][c]=copy.deepcopy(array33)
					btnSudokus[r][c].config(text='')
		btnSudokuClicked(currentRow,currentColumn)
	elif which=="clean":
		if currentRow>=0 and currentColumn>=0:
			if sudoku[currentRow][currentColumn]==0:
				dataSudokus[currentRow][currentColumn]=copy.deepcopy(array33)
				currentSudoku[currentRow][currentColumn]=0
				btnSudokus[currentRow][currentColumn].config(text='')
				btnSudokuClicked(currentRow,currentColumn)
		else:
			messagebox.showinfo("提示：","请选择要清除的单元格!")
	elif which=="mark":
		# 标注单元格
		if currentRow>=0 and currentColumn>=0:
			markSudokus[currentRow][currentColumn]=not markSudokus[currentRow][currentColumn]
			if markSudokus[currentRow][currentColumn]:
				btnSudokus[currentRow][currentColumn].config(image=picBGMark)
			else:
				if currentSudoku[currentRow][currentColumn]>0:
					btnSudokus[currentRow][currentColumn].config(image=picBGSame)
				else:
					btnSudokus[currentRow][currentColumn].config(image=picBGRelated)
		else:
			messagebox.showinfo("提示：","请选择要标注的单元格!")
	elif which=="undo":
		messagebox.showinfo("提示：","撤销按钮（%s）被按下！"%which)
	elif which=="redo":
		messagebox.showinfo("提示：","重做按钮（%s）被按下！"%which)
	else:
		messagebox.showinfo("关于...","简单数独 V1.0")

# 数字按钮
def btnNumberClicked(num):
	# 如果还未点击数独单元格，则什么也不做
	if currentRow+currentColumn<0:
		messagebox.showerror("警告","请先选择数独单元格！")
		return
	
	# 判断是否是不可更改的固定位置
	if sudoku[currentRow][currentColumn]==0:
		# 判断是否可以填入该数字（num）
		if checkNumber(num,currentRow,currentColumn,currentSudoku):
			dataSudokus[currentRow][currentColumn]=copy.deepcopy(array33)
			cr,cc = divmod(num-1,3)
			dataSudokus[currentRow][currentColumn][cr][cc]=num
			btnSudokus[currentRow][currentColumn].config(text=num,style='NUMBER.TButton')
			currentSudoku[currentRow][currentColumn]=num
			for r in range(9):
				for c in range(9):
					fr = currentRow//3
					fc = currentColumn//3
					if r==currentRow or c==currentColumn or (r>=fr*3 and r<=fr*3+2 and c>=fc*3 and c<=fc*3+2):
						style=btnSudokus[r][c].cget('style')
						if style=='REMIND.TButton':
							btnSudokus[r][c].config(text=btnSudokus[r][c].cget('text').replace('%d'%num,' '))
			if checkSuccess(currentSudoku):
				messagebox.showinfo("胜利","恭喜！您已成功完成本数独！")
		else:
			messagebox.showerror("警告","数字%s不能填入该位置！"%num)
	else:
		messagebox.showerror("警告","该位置不能修改！")

# 提示按钮
def btnRemindClicked(num):
	# 如果还未点击数独单元格，则什么也不做
	if currentRow+currentColumn<0:
		messagebox.showerror("警告","请先选择数独单元格！")
		return

	# 判断是否是不可更改的固定位置
	if sudoku[currentRow][currentColumn]==0:
		# 判断是否可以填入该数字（num）
		if checkNumber(num,currentRow,currentColumn,currentSudoku):
			# 看是否已经提示该数字
			r,c = divmod(num-1,3)
			if dataSudokus[currentRow][currentColumn][r][c]==0:
				dataSudokus[currentRow][currentColumn][r][c]=num
			else:
				dataSudokus[currentRow][currentColumn][r][c]=0
			btnSudokus[currentRow][currentColumn].config(text=array2str(dataSudokus[currentRow][currentColumn]),style='REMIND.TButton')
			currentSudoku[currentRow][currentColumn]=0
		else:
			messagebox.showerror("警告","数字%s不能填入该位置！"%num)
	else:
		messagebox.showerror("警告","该位置不能修改！")

# 数度表格
def btnSudokuClicked(row,col):
	global currentRow, currentColumn
	# messagebox.showinfo("提示：","数独位置（%s，%s）被按下！（%s，%s）"%(r,c,currentRow,currentColumn))
	#imgTemp=imgSudokus[r][c].covert('RGBA')
	#Image.blend(imgTemp,imgBlue,0.5)
	#if currentRow>=0 and currentColumn>=0:
	#	btnSudokus[currentRow][currentColumn].config(image=picLast)	
	#picLast=btnSudokus[r][c].cget('image')
	#picTemp=ImageTk.PhotoImage(Image.alpha_composite(picBGSame.get(0,0),picLast))
	#btnSudokus[r][c].config(image=picTemp)
	for r in range(9):
		for c in range(9):
			if not markSudokus[r][c]:
				# 处理非标注单元格背景
				btnSudokus[r][c].config(image=picSudokus[r][c])
				fr = row//3
				fc = col//3
				if r==row or c==col or (r>=fr*3 and r<=fr*3+2 and c>=fc*3 and c<=fc*3+2):
					# 横、竖、正方形单元格，背景为picBGRelated
					btnSudokus[r][c].config(image=picBGRelated)
				if currentSudoku[r][c]>0 and currentSudoku[r][c]==currentSudoku[row][col]:
					# 数字相同单元格，背景为picBGSame
					btnSudokus[r][c].config(image=picBGSame)

	currentRow = row
	currentColumn = col
	
# 键盘输入
def onKeyPressed(event):
	keycode = event.keycode
	if keycode>=49 and keycode<=57:
		btnNumberClicked(keycode-48)

# 主窗口
root = tk.Tk()
root.title('数独')
root.resizable(False, False)

# 构建区域
frameTools = tk.Frame(root)
frameNumber = tk.Frame(root)
frameSukodu = tk.Frame(root,bd=10,relief=tk.GROOVE)
frameRemind = tk.Frame(root)
frameMessage = tk.Frame(root)

# 设置区域布局，上为工具，左为确定的数字，右为提示的数字，中间为数独，下为消息提示
frameTools.grid(row=0, column=0, columnspan=3, sticky='nsew')
frameNumber.grid(row=1, column=0, sticky='wns')
frameSukodu.grid(row=1, column=1, sticky='ns')
frameRemind.grid(row=1, column=2, sticky='ens')
frameMessage.grid(row=2, column=0, columnspan=3, sticky='nsew')

# 构建工具区域控件
# 初始化按钮图片
picOpen=tk.PhotoImage(file="icons/open.png")
picSave=tk.PhotoImage(file="icons/save.png")
picExport=tk.PhotoImage(file="icons/export.png")
picReset=tk.PhotoImage(file="icons/reset.png")
picRemind=tk.PhotoImage(file="icons/remind.png")
picCleanAll=tk.PhotoImage(file="icons/cleanall.png")
picClean=tk.PhotoImage(file="icons/clean.png")
picMark=tk.PhotoImage(file="icons/mark.png")
picUndo=tk.PhotoImage(file="icons/undo.png")
picRedo=tk.PhotoImage(file="icons/redo.png")
picHelp=tk.PhotoImage(file="icons/help.png")

# 创建功能按钮
btnOpen=ttk.Button(frameTools,image=picOpen,command=partial(btnClicked,'open'),compound='top',text='打开')
btnSave=ttk.Button(frameTools,image=picSave,command=partial(btnClicked,'save'),compound='top',text='保存')
btnExport=ttk.Button(frameTools,image=picExport,command=partial(btnClicked,'export'),compound='top',text='导出')
btnReset=ttk.Button(frameTools,image=picReset,command=partial(btnClicked,'reset'),compound='top',text='重置')
btnRemind=ttk.Button(frameTools,image=picRemind,command=partial(btnClicked,'remind'),compound='top',text='提示')
btnCleanAll=ttk.Button(frameTools,image=picCleanAll,command=partial(btnClicked,'cleanall'),compound='top',text='清空提示')
btnClean=ttk.Button(frameTools,image=picClean,command=partial(btnClicked,'clean'),compound='top',text='清除')
btnMark=ttk.Button(frameTools,image=picMark,command=partial(btnClicked,'mark'),compound='top',text='标注')
btnUndo=ttk.Button(frameTools,image=picUndo,command=partial(btnClicked,'undo'),compound='top',text='撤销')
btnRedo=ttk.Button(frameTools,image=picRedo,command=partial(btnClicked,'redo'),compound='top',text='重做')
btnHelp=ttk.Button(frameTools,image=picHelp,command=partial(btnClicked,'help'),compound='top',text='帮助')

# 设置位置
btnOpen.grid(row=0, column=0, sticky="nsew")
btnSave.grid(row=0, column=1, sticky="nsew")
btnExport.grid(row=0, column=2, sticky="nsew")
btnReset.grid(row=0, column=3, sticky="nsew")
btnRemind.grid(row=0, column=4, sticky="nsew")
btnCleanAll.grid(row=0, column=5, sticky="nsew")
btnClean.grid(row=0, column=6, sticky="nsew")
btnMark.grid(row=0, column=7, sticky="nsew")
btnUndo.grid(row=0, column=8, sticky="nsew")
btnRedo.grid(row=0, column=9, sticky="nsew")
btnHelp.grid(row=0, column=10, sticky="nsew")

# 设置权重
for i in range(11):
	frameTools.columnconfigure(i, weight=1)

# 构建数字区域控件
# 纵向排列数字1-9
picNumbers=[]
btnNumbers=[]
for i in range(9):
	picNumbers.append(tk.PhotoImage(file="icons/number%s.png"%(i+1)))
	btnNumbers.append(ttk.Button(frameNumber,image=picNumbers[i],command=partial(btnNumberClicked,i+1)))
	btnNumbers[i].grid(row=i, column=0, sticky="nsew")
	frameNumber.rowconfigure(i, weight=1)

# 构建数独区域控件
# 构建3X3布局
frames=[[tk.Frame(frameSukodu,bd=5,relief=tk.GROOVE) for _ in range(3)] for _ in range(3)]
for r in range(3):
	for c in range(3):
		frames[r][c].grid(row=r, column=c, sticky='nsew')

# 底色图片
picBGNormal=tk.PhotoImage(file="icons/bgnormal.png")
picBGFixed=tk.PhotoImage(file="icons/bgfixed.png")
picBGSame=tk.PhotoImage(file="icons/bgsame.png")
picBGRelated=tk.PhotoImage(file="icons/bgrelated.png")
picBGMark=tk.PhotoImage(file="icons/bgmark.png")

# 创建一个样式
style = ttk.Style()
# 设置按钮的背景色
fixedFont=font.Font(size=24,weight='bold')
numberFont=font.Font(size=24)
remindFont=font.Font(size=9)
style.configure('FIXED.TButton',font=fixedFont,width=1,borderwidth=1,justify='center')
style.configure('NUMBER.TButton',font=numberFont,width=1,borderwidth=1,justify='center')
style.configure('REMIND.TButton',font=remindFont,width=3,borderwidth=1,justify='center')

# 构建数独
# 开始解数独	
sudoku = [
	[8,0,0,0,0,0,0,0,0],
	[0,0,3,6,0,0,0,0,0],
	[0,7,0,0,9,0,2,0,0],
	[0,5,0,0,0,7,0,0,0],
	[0,0,0,0,4,5,7,0,0],
	[0,0,0,1,0,0,0,3,0],
	[0,0,1,0,0,0,0,6,8],
	[0,0,8,5,0,0,0,1,0],
	[0,9,0,0,0,0,4,0,0]
]
currentSudoku = copy.deepcopy(sudoku) 
array33=[[0 for col in range(3)] for row in range(3)]
dataSudokus=[[any for _ in range(9)] for _ in range(9)]
btnSudokus=[[ttk.Button for _ in range(9)] for _ in range(9)]
picSudokus=[[tk.PhotoImage for _ in range(9)] for _ in range(9)]
markSudokus=[[False for _ in range(9)] for _ in range(9)]
for r,row in enumerate(sudoku):
	for c,col in enumerate(row):
		fr = r//3
		cr = r%3
		fc = c//3
		cc = c%3
		if sudoku[r][c]==0:
			btnSudokus[r][c]=ttk.Button(frames[fr][fc],image=picBGNormal,command=partial(btnSudokuClicked,r,c),style='NUMBER.TButton',compound='center')
			dataSudokus[r][c]=copy.deepcopy(array33)
		else:
			btnSudokus[r][c]=ttk.Button(frames[fr][fc],image=picBGFixed,command=partial(btnSudokuClicked,r,c),style='FIXED.TButton',compound='center',text=sudoku[r][c])
			dataSudokus[r][c]=copy.deepcopy(array33)
			dataSudokus[r][c][cr][cc]=sudoku[r][c]
		btnSudokus[r][c].grid(row=cr, column=cc, sticky="nsew")
		picSudokus[r][c]=btnSudokus[r][c].cget('image')

# 构建提示区域控件
# 控件包括：1-9提示
picReminds=[]
btnReminds=[]
for i in range(9):
	picReminds.append(tk.PhotoImage(file="icons/remind%s.png"%(i+1)))
	btnReminds.append(ttk.Button(frameRemind,image=picReminds[i],command=partial(btnRemindClicked,i+1)))
	btnReminds[i].grid(row=i, column=0, sticky="nsew")
	frameRemind.rowconfigure(i, weight=1)

# 当前位置
currentRow = -1
currentColumn = -1

# 监控按键输入
root.bind("<Key>", onKeyPressed)

root.mainloop()
