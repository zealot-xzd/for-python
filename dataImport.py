from pypinyin import pinyin, lazy_pinyin, Style

from xlrd import open_workbook
import sys
import os
import cx_Oracle
from cx_Oracle import DatabaseError,InterfaceError



def get_capital_letter(srcCharSeq):
	tmpCharSeq=srcCharSeq.replace(' ','')
	tmpCharSeq=tmpCharSeq.replace('\n','')
	tmpCharSeq=tmpCharSeq.replace('/','')
	tmpCharSeq=tmpCharSeq.replace('(','')
	tmpCharSeq=tmpCharSeq.replace(')','')
	tmpCharSeq=tmpCharSeq.replace('）','')
	tmpCharSeq=tmpCharSeq.replace('（','')
	tmpCharSeq=tmpCharSeq.replace('：','')
	tmpCharSeq=tmpCharSeq.replace('、','')
	tmpCharSeq=tmpCharSeq.replace('㎡','')
	a=pinyin(tmpCharSeq,style=Style.FIRST_LETTER)
	b=[]
	for i in range(len(a)):
		b.append(a[i][0])
	c=''.join(b)
	return c.upper()

def get_cols_names(sheetbook,sheetname,colpos, rowpos_begin):
    sheet_cols = sheetbook.sheet_by_name(sheetname)
    cols_name = sheet_cols.col_values(colpos,rowpos_begin)
    return cols_name

def get_rows_value(sheetbook,sheetname):
    rows_values=[]
    sheet_row = sheetbook.sheet_by_name(sheetname)
    for i in range(1,sheet_row.nrows):
        rows_values.append(sheet_row.row_values(i))
    return sheet_row.nrows,rows_values


def get_first_rows_value(sheetbook,index):
    rows_values=[]
    sheet_row = sheetbook.sheets()[index]
    rows_values.append(sheet_row.row_values(0))
    return rows_values

createTable="create table {0} ("
insert_str="insert into {0} ("
insert_values="values ("
insert_field="{0},"
field="{0} VARCHAR2(255),"

comment_table="comment on table {0} is '{1}'"
comment_col="comment on column {0}.{1} is '{2}'"

def get_create_table_sql(tableName,header):

	table=get_capital_letter(tableName)
	#table=tableName
	create_table_sql=createTable.format(table,tableName)
	insert_str_sql=insert_str.format(table)
	insert_values_sql=insert_values
	comment_list=[]
	comment_list.append(comment_table.format(table,tableName))
	count=0
	for item in header:
		count=count+1
		field_name=get_capital_letter(item)
		field_tmp=field.format(field_name)
		create_table_sql=create_table_sql + field_tmp

		insert_str_sql=insert_str_sql + insert_field.format(field_name)
		insert_values_sql = insert_values_sql + ":"+str(count)+","

		comment_tmp=comment_col.format(table,field_name,item)
		comment_list.append(comment_tmp)
	create_table_sql=create_table_sql[:-1]+")"
	insert_str_sql=insert_str_sql[:-1]+") " + insert_values_sql[:-1]+")"

	return create_table_sql,comment_list,insert_str_sql


def get_workbook(xlsFile):
	excel_input = open_workbook(xlsFile)
	return excel_input


def get_connect():
	oracle_tns = cx_Oracle.makedsn('12.6.80.26', 1521,'orcl')
	connectObj = cx_Oracle.connect('runjck', 'runco', oracle_tns)
	return connectObj



def main():
	if len(sys.argv) < 3:
		print("error of input argv")
		exit(1)

	fileNames=[]
	if os.path.isdir(sys.argv[1]):
		for root,dirs,files in os.walk(sys.argv[1]):
			for name in files:
				fileNames.append(os.path.join(root,name))
	else:
		fileNames.append(sys.argv[1])
	print(fileNames)
	for file in fileNames:
		print("handleing file: " +file)
		wb=get_workbook(file)
		header=get_first_rows_value(wb,0)
		sql=get_create_table_sql(sys.argv[2],header[0])
		print(sql)

		connectObj=get_connect()
		cursor=connectObj.cursor()
		try:
			cursor.execute(sql[0])
			connectObj.commit()
			for comment in sql[1]:
				cursor.execute(comment)
			connectObj.commit()
		except DatabaseError:
			print("create table error")

		sheets=wb.sheet_names()
		cursor.prepare(sql[2])
		for sheet in sheets:
			nunAndValues=get_rows_value(wb, sheet)
			#print(nunAndValues[1])
			for item in nunAndValues[1]:
				length=0
				for index in range(1,len(item)):
					length=length+len(str(item[index]))
				if length <= 0:
					continue;
				tmp=[];
				tmp.append(item)
				#print(tmp)
				try:
					cursor.executemany(None, tmp,batcherrors=True)
					#cursor.executemany(None, tmp)
					#error=cursor.getbatcherrors()
					#print(error)
				except DatabaseError as e:
					print("errror 1: %s" % e)
				except InterfaceError as e:
					print("errror 2: %s" % e)
			connectObj.commit()
		connectObj.close()
		print("end file: " +file)

if __name__ == '__main__':
	main()


