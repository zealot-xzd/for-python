import sys
import xlrd
import lxml.etree as et

item_attrib=["run_name", "ga_code", "ch_name", "type", "len", "isnull",
             "db_name", "output", "ignore", "from", "value"]
table_attrib=["key", "protocol", "tabname", "markname", "expand_fields",
              "common_fields", "mark_fields", "oracle", "hbase", "basedata"]

#read excel file.
def open_excel(file = "excel.xls"):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception,e:
        print str(e);

#read sheet of excel by index, and return the records of the sheet.
def excel_table_byindex(file="excel.xls", rownameindex=0, by_index=0):
    data = open_excel(file)
    table = data.sheets()[by_index]
    nrows = table.nrows
    ncols = table.ncols
    
    list = []
    for rownum in range(2,nrows):
        row = table.row_values(rownum)
        if row:
            app = []
            for i in range(ncols):
                app = row[2:8]
            list.append(app)
    return list

#convert the excel file to xml file.
def excel_to_xml(L=[],index=0):

    if index==0:
        run_expand=et.SubElement(root,"RUN_EXPAND_FIELDS",attrib={"key":"", "description":""})
        for i in range(6):
            item=et.SubElement(run_expand,"ITEM")
            for j in range(len(L[i])):
                item.set(item_attrib[j],str(L[i][j]))
                for k in range(len(L[i]),len(item_attrib)):
                    item.set(item_attrib[k],"")
                    
        mark_fields=et.SubElement(root,"MARK_FIELDS",attrib={"key":"", "description":""})    
        for i in range(6,len(L)):
            item=et.SubElement(mark_fields,"ITEM")
            for j in range(len(L[i])):
                item.set(item_attrib[j],str(L[i][j]))
                for k in range(len(L[i]),len(item_attrib)):
                    item.set(item_attrib[k],"")

    if index==1:
        protocol_common=et.SubElement(root,"PROTOCOL_COMMON_FIELDS",attrib={"key":"", "description":""})
        for i in range(len(L)):
            item=et.SubElement(protocol_common,"ITEM")
            for j in range(len(L[i])):
                item.set(item_attrib[j],str(L[i][j]))
                for k in range(len(L[i]),len(item_attrib)):
                    item.set(item_attrib[k],"")
    
    if index>1:
        table=et.SubElement(protocol_private,"TABLE")
        for i in range(len(table_attrib)):
            table.set(table_attrib[i],"")

        for i in range(len(L)):
            item=et.SubElement(table,"ITEM")
            for j in range(len(L[i])):
                item.set(item_attrib[j],str(L[i][j]))
                for k in range(len(L[i]),len(item_attrib)):
                    item.set(item_attrib[k],"")
        
def main():

    file_name=open("test.xml", "rb+")
    
    global root
    global protocol_private
    root = et.Element("MESSAGE", attrib={"key":"", "description":""})

#read expand,mark,common fields.
    for i in range(2):
        tables = excel_table_byindex("excel.xls",2,i)
        excel_to_xml(tables,i)

#read private fields of each protocol.
    protocol_private=et.SubElement(root,"PROTOCOL_PRIVATE_FIELDS",attrib={"key":"", "description":""})
    for i in range(2,6):
        tables = excel_table_byindex("excel.xls",2,i)
        excel_to_xml(tables,i)
         
    print(et.tounicode(root,pretty_print=True))
    file_name.write(et.tounicode(root,pretty_print=True).encode('utf8'))
    file_name.close()
    
        
if __name__=="__main__":
    main()
    
    
    
