import xlwings as xw
from remind import countNumber

# 使用Excel
def appExcel()->xw.App:
	try:
		app = xw.App(visible=False)
		return app
	except Exception as e:
		return None

# 使用WPS
def appWPS()->xw.App:
	try:
		#【1】（WPS）下面这句是第（1）句共4句，引入pywin32包中的win32com.client
		from win32com.client import Dispatch 
		#【2】（WPS）下面这句是第（2）句共4句，这4句代替用Office打开Excel那句，改用WPS打开Excel。    
		xl = xw._xlwindows.COMRetryObjectWrapper(Dispatch("Ket.Application")) 
	
		#【3】（WPS）下面这句是第（3）句共4句，这4句代替用Office打开Excel那句，改用WPS打开Excel。
		impl = xw._xlwindows.App(visible=False, add_book=False, xl=xl)
	
		#【4】（WPS）下面这句是第（4）句共4句，这4句代替用Office打开Excel那句，改用WPS打开Excel。         
		app = xw.App(visible=False, add_book=False, impl=impl)
		return app
	except Exception as e:
		return None

def importExcel(fn):
	# 导入Excel数据
	
	app=appExcel()
	if app==None:
		app=appWPS()
		if app==None:
			return

	wb = app.books.open(fn)
	sht = wb.sheets[0]

	arraycol=['A','B','C','D','E','F','G','H','I']
	arrayrow=['1','2','3','4','5','6','7','8','9']
	array99=[[0 for col in range(9)] for row in range(9)]
	for c, sc in enumerate(arraycol):
		for r, sr in enumerate(arrayrow):
			v=sht.range('%s%s'%(sc,sr)).value
			#print('v=%s'%v)
			if isinstance(v, (int, float)):
				if int(v)>0 and int(v)<=9:
					array99[r][c]=int(v)
			elif isinstance(v, (str)):
				if len(v)==1 and v.isdigit():
					if int(v)>0 and int(v)<=9:
						array99[r][c]=int(v)
			#print('%s%s:(%d,%d)=%d'%(sc,sr,r,c,array99[r][c]))
	wb.close()
	app.quit()

	return array99	
	
def exportExcel(array, fn):
	# 导出Excel数据
	app=appExcel()
	if app==None:
		app=appWPS()
		if app==None:
			return

	wb = app.books.add()
	sheet = wb.sheets.add('数独')
	sheet.range('A1').value = array
	sheet.autofit()
	wb.save(fn)
	wb.close()
	app.quit()

def exportRemindExcel(array, fn):
	# 导出excel提示数据
	arraycol = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z','AA']
	arrayrow = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27']

	app=appExcel()
	if app==None:
		app=appWPS()
		if app==None:
			return

	wb = app.books.add()
	sheet = wb.sheets.add('数独')
	sheet.range('A1').value = array
	sheet.autofit()

	# 画小方框
	for cb, cv in enumerate(arraycol):
		for rb, rv in enumerate(arrayrow):
			if cb % 3 == 0 and rb % 3 == 0:
				ce = cb + 2
				re = rb + 2
				square = arraycol[cb]+arrayrow[rb]+':'+arraycol[ce]+arrayrow[re]
				
				sheet.range(square).api.Borders(7).LineStyle = 1
				sheet.range(square).api.Borders(7).Weight = 2
				sheet.range(square).api.Borders(7).ColorIndex = 1
				sheet.range(square).api.Borders(8).LineStyle = 1
				sheet.range(square).api.Borders(8).Weight = 2
				sheet.range(square).api.Borders(8).ColorIndex = 1
				sheet.range(square).api.Borders(9).LineStyle = 1
				sheet.range(square).api.Borders(9).Weight = 2
				sheet.range(square).api.Borders(9).ColorIndex = 1
				sheet.range(square).api.Borders(10).LineStyle = 1
				sheet.range(square).api.Borders(10).Weight = 2
				sheet.range(square).api.Borders(10).ColorIndex = 1

				# 合并单元格
				array33 = sheet.range(square).value
				c, s = countNumber(array33)
				if c == 1:
					sheet.range(square).merge()
					sheet.range(square).color = 244,244,244
					sheet.range(square).value = s
					sheet.range(square).api.Font.ColorIndex = 1
					sheet.range(square).api.Font.Size = 36
					sheet.range(square).api.Font.Bold = True
					sheet.range(square).HorizontalAlignment = -4108
					sheet.range(square).VerticalAlignment = -4108

	# 画大方框
	for cb, cv in enumerate(arraycol):
		for rb, rv in enumerate(arrayrow):
			if cb % 9 == 0 and rb % 9 == 0:
				ce = cb + 8
				re = rb + 8
				square = arraycol[cb]+arrayrow[rb]+':'+arraycol[ce]+arrayrow[re]
				
				sheet.range(square).api.Borders(7).LineStyle = 1
				sheet.range(square).api.Borders(7).Weight = 3
				sheet.range(square).api.Borders(7).ColorIndex = 1
				sheet.range(square).api.Borders(8).LineStyle = 1
				sheet.range(square).api.Borders(8).Weight = 3
				sheet.range(square).api.Borders(8).ColorIndex = 1
				sheet.range(square).api.Borders(9).LineStyle = 1
				sheet.range(square).api.Borders(9).Weight = 3
				sheet.range(square).api.Borders(9).ColorIndex = 1
				sheet.range(square).api.Borders(10).LineStyle = 1
				sheet.range(square).api.Borders(10).Weight = 3
				sheet.range(square).api.Borders(10).ColorIndex = 1

			# 将0设置为空
			if sheet.range(cv+rv).value == 0:
				sheet.range(cv+rv).value = ''

	wb.save(fn)
	wb.close()
	app.quit()

