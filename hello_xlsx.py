import xlsxwriter

workbook = xlsxwriter.Workbook('play/hello.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', 'Hello world')

workbook.close()