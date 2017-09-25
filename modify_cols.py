#-*- coding=utf-8 -*-

from xlrd import open_workbook
from xlwt import easyxf
from xlutils.copy import copy
from xlwt import Workbook

peizhi_excel_input_file = u'配置信息.xlsx'
oracle_table_input_file = u'oracle_table.xlsx'


def get_cols_names(sheetbook,sheetname,colpos, rowpos_begin):
    sheet_cols = sheetbook.sheet_by_name(sheetname)
    cols_name = sheet_cols.col_values(colpos,rowpos_begin)
    return cols_name

def get_rows_value(sheetbook,sheetname):
    rows_values=[]
    sheet_row = sheetbook.sheet_by_name(sheetname)
    for i in range(sheet_row.nrows):
        rows_values.append(sheet_row.row_values(i))
    return sheet_row.nrows,rows_values

def modify_sheet_lines(colsname,colsnamecmp):
    modify_list=[]
    pos2 = 0
    for item in colsname:
        pos = -1
        findflag = False
        for item2 in colsnamecmp:
            pos+=1
            if item.upper() == item2.upper():
                modify_list.append(pos)
                findflag = True
                break
        if not findflag:
            modify_list.append([pos2,item])
        pos2+=1
        
    return modify_list

def write_line(sht,vals,row,col=0):
    for i in range(len(vals)):
        sht.write(row,col+i,vals[i])


def main():

    peizhi_excel_input = open_workbook(peizhi_excel_input_file)
    oracle_table_input = open_workbook(oracle_table_input_file)
#获取数据集(u'配置信息.xlsx'中的第7列第3行开始）
    dataset_name_ch =get_cols_names(peizhi_excel_input,u'数据集',6,2)

#处理每个数据集sheet页
    wb = copy(peizhi_excel_input)
    for sheetname in dataset_name_ch:

#获取目标字段顺序（各个表的第4列）
        if sheetname in oracle_table_input.sheet_names():
            cols = get_cols_names(oracle_table_input,sheetname,3,0)
        else:
            print "%s is not in %s" % (sheetname,oracle_table_input_file)
            continue

#获取原始字段顺序
        if sheetname in peizhi_excel_input.sheet_names():
            colscmp = get_cols_names(peizhi_excel_input,sheetname,3,0)
        else:
            print "%s is not in %" % (sheetname,peizhi_excel_input_file)
            continue

        print "modify %s sheet" % (sheetname,)        
#字段顺序调整映射关系
        posmap = modify_sheet_lines(cols,colscmp)
        #print posmap

#生成新的"配置信息.xlsx"
       
        sheet = wb.get_sheet(sheetname)
        rows,rows_values = get_rows_value(peizhi_excel_input,sheetname)

        #for row in range(rows):
        for row in range(len(posmap)):
            tmpvalue=[]
            if not isinstance(posmap[row],list):                 
                write_line(sheet,rows_values[posmap[row]],row)
            else:
                tmpvalue=['',row,posmap[row][1],posmap[row][1],posmap[row][1],'string',512]
                write_line(sheet,tmpvalue,row)
#隐藏不需要的行
        for i in range(len(posmap),rows):
            sheet.row(i).hidden = True 

        wb.save(peizhi_excel_input_file + '_new.xlsx')

if __name__ == '__main__':
    main()

