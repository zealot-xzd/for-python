# -*- coding: utf-8 -*-

import sys
import os
import xlrd
import lxml.etree as et

item_attrib=["run_name", "ga_code", "ch_name", "type", "len", "isnull",
             "db_name", "output", "ignore", "from", "value"]
table_attrib=["key", "protocol", "tabname", "markname", "expand_fields",
              "common_fields", "mark_fields", "oracle", "hbase", "basedata"]

tab_dic={
16:["WA_SOURCE_0001","DATA_HTTP","http_tb","http,wap","true","true","true","true","true","true"],
17:["WA_SOURCE_0002","DATA_EMAIL","email_tb","email,webmail","true","true","true","true","true","true"],
18:["WA_SOURCE_0003","DATA_FTP","ftp_tb","ftp","true","true","true","true","true","true"], 
19:["WA_SOURCE_0004","DATA_TELNET","telnet_tb","telnet","true","true","true","true","true","true"],
20:["WA_SOURCE_0005","DATA_IM","im_tb","im","true","true","true","true","true","true"], 
21:["WA_SOURCE_0006","DATA_GAME","game_tb","game","true","true","true","true","true","true"],
22:["WA_SOURCE_0007","DATA_WEBCHAT","webchat_tb","webchat","true","true","true","true","true","true"],
23:["WA_SOURCE_0008","DATA_WEBBBS","webbbs_tb","webbbs","true","true","true","true","true","true"], 
24:["WA_SOURCE_0009","DATA_VOIP","voip_tb","voip","true","true","true","true","true","true"],
25:["WA_SOURCE_0010","DATA_HTTPS","https_tb","https","true","true","true","true","true","true"],
26:["WA_SOURCE_0011","DATA_VPN","vpn_tb","vpn","true","true","true","true","true","true"],
27:["WA_SOURCE_0012","DATA_STREAMMEDIA","streammedia_tb","streammedia","true","true","true","true","true","true"],
28:["WA_SOURCE_0013","DATA_P2P","p2p_tb","p2p","true","true","true","true","true","true"],
29:["WA_SOURCE_0014","DATA_REMOTECTRL","remotectrl_tb","remotectrl","true","true","true","true","true","true"],
30:["WA_SOURCE_0015","DATA_SNSINFO","snsinfo_tb","snsinfo","true","true","true","true","true","true"],
31:["WA_SOURCE_0016","DATA_SNSFRIENDS","snsfriends_tb","snsfriends","true","true","true","true","true","true"],
32:["WA_SOURCE_0017","DATA_ANTIPROXY","antiproxy_tb","antiproxy","true","true","true","true","true","true"],
33:["WA_SOURCE_0018","DATA_SMS","SMS_tb","sms","true","true","true","true","true","true"],

34:["WA_SOURCE_0020","DATA_PROXY","PROXY_tb","proxy","true","true","true","true","true","true"],
35:["WA_SOURCE_0021","DATA_BET","bet_tb","bet","true","true","true","true","true","true"],
36:["WA_SOURCE_0022","DATA_BLOG","blog_tb","blog","true","true","true","true","true","true"],
37:["WA_SOURCE_0023","DATA_WMMS","wmms_tb","wmms","true","true","true","true","true","true"],
38:["WA_SOURCE_0024","DATA_SEARCH","search_tb","search","true","true","true","true","true","true"],
39:["WA_SOURCE_0025","DATA_SHOP","shop_tb","shop","true","true","true","true","true","true"],
40:["WA_SOURCE_0026","DATA_HOTEL","hotel_tb","hotel","true","true","true","true","true","true"],
41:["WA_SOURCE_0027","DATA_DELIVERY","delivery_tb","delivery","true","true","true","true","true","true"],
42:["WA_SOURCE_0028","DATA_TICKET","ticket_tb","ticket","true","true","true","true","true","true"],
43:["WA_SOURCE_0029","DATA_WEBUSER","webuser_tb","webuser","true","true","true","true","true","true"],

44:["WA_SOURCE_0034","DATA_CLOUDADDRESS","cloudaddress_tb","cloudaddress","true","true","true","true","true","true"],
45:["WA_SOURCE_0035","DATA_WEIBO","weibo_tb","weibo","true","true","true","true","true","true"],
46:["WA_SOURCE_0038","DATA_WEBMEDIA","webmedia_tb","webmedia","true","true","true","true","true","true"],
47:["WA_SOURCE_0039","DATA_PICTURE","PICTURE_tb","picture","true","true","true","true","true","true"],
48:["WA_SOURCE_0040","DATA_TERMINALID","terminalid_tb","terminalid","true","true","true","true","true","true"],
49:["WA_SOURCE_9999","DATA_OTHER","other_tb","other","true","true","true","true","true","true"],

50:["RUN_SOURCE_9988","DATA_USERDEFINE","userdefine_tb","userdefine","true","true","true","true","true","true"],
51:["RUN_SOURCE_9990","DATA_DNS","DNS_tb","dns","true","true","true","true","true","true"],
52:["RUN_SOURCE_9991","DATA_IMMEDIA","IMMEDIA_tb","immedia","true","true","true","true","true","true"],
53:["RUN_SOURCE_9992","DATA_LOCATION","LOCATION_tb","location","true","true","true","true","true","true"],
54:["RUN_SOURCE_9993","DATA_SNSREG","SNSREG_tb","snsreg","true","true","true","true","true","true"],
55:["RUN_SOURCE_9994","DATA_IRC","IRC_tb","irc","true","true","true","true","true","true"],
56:["RUN_SOURCE_9995","DATA_RELATIONSHIP","RELATIONSHIP_tb","relationship","true","true","true","true","true","true"],
57:["RUN_SOURCE_9996","DATA_EXCHANGE","EXCHANGE_tb","exchange","true","true","true","true","true","true"],
58:["RUN_SOURCE_9998","DATA_PERSONINFO","PERSONINFO_tb","personinfo","true","true","true","true","true","true"]
}

path=".\\xml"
filename_fmt=path+"\\fmt.xml"
filename_index=path+"\\index.xml"      
def my_mkdir(path):

    path=path.strip()
    path=path.rstrip("\\")
    isexist=os.path.exists(path)
 
    if not isexist:        
        os.makedirs(path)
        return True
    else:
        return False

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
        if row[2]!="":
            app = []
            for i in range(ncols):
                app = row[2:17]
            list.append(app)
    return list
    

#convert the excel file to xml file.
def create_xml_file():
    
    file_name_fmt=open(filename_fmt, "wb+")  
    root_fmt = et.Element("MESSAGE", attrib={"key":"", "description":""})
    
    
    #read expand,mark,common fields.
    
    L = excel_table_byindex("excel.xls",2,3)
    run_expand=et.SubElement(root_fmt,"RUN_EXPAND_FIELDS",attrib={"key":"", "description":""})
    for i in range(6):
        item=et.SubElement(run_expand,"ITEM")
        for j in range(6):  
            item.set(item_attrib[j],unicode(L[i][j]).strip())
        for k in range(6,len(item_attrib)):
                item.set(item_attrib[k],"")
                            
    mark_fields=et.SubElement(root_fmt,"MARK_FIELDS",attrib={"key":"", "description":""})    
    for i in range(6,len(L)):
        item=et.SubElement(mark_fields,"ITEM")
        for j in range(6):
            item.set(item_attrib[j],unicode(L[i][j]).strip())
        for k in range(6,len(item_attrib)):
                item.set(item_attrib[k],"")
            
    L = excel_table_byindex("excel.xls",2,15)
    protocol_common=et.SubElement(root_fmt,"PROTOCOL_COMMON_FIELDS",attrib={"key":"", "description":""})
    for i in range(len(L)):
        item=et.SubElement(protocol_common,"ITEM")
        for j in range(6):          
            item.set(item_attrib[j],unicode(L[i][j]).strip())
        for k in range(6,len(item_attrib)):
                item.set(item_attrib[k],"")   
           
    #read private fields of each protocol.
                
    protocol_private=et.SubElement(root_fmt,"PROTOCOL_PRIVATE_FIELDS",attrib={"key":"", "description":""})


    file_name_index=open(filename_index, "wb+")
    root_index = et.Element("MESSAGE")
    dataset=et.SubElement(root_index,"DATASET",attrib={"name":"WA_COMMON_010017", "rmk":""})
    data=et.SubElement(dataset,"DATA")
    dataset1=et.SubElement(data,"DATASET",attrib={"name":"WA_COMMON_010013", "rmk":""})

    
    for index in range(16,58):     
        print "%s: %s" % (tab_dic[index][0],tab_dic[index][3])
        
        L2 = excel_table_byindex("excel.xls",2,index)
        table=et.SubElement(protocol_private,"TABLE")
        for i in range(len(table_attrib)):
            table.set(table_attrib[i],tab_dic[index][i].strip())

        for i in range(len(L2)):
            item=et.SubElement(table,"ITEM")
            for j in range(6):               
                item.set(item_attrib[j],unicode(L2[i][j]).strip())
            for k in range(6,len(item_attrib)):
                item.set(item_attrib[k],"")

        
        data1=et.SubElement(dataset1,"DATA")
        item=et.SubElement(data1,"ITEM",attrib={"key":"I010032", "val":"", "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"I010033", "val":"", "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"A010004", "val":unicode(tab_dic[index][3]).strip(), "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"B050016", "val":"111", "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"F010008", "val":"441900", "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"I010038", "val":"1", "rmk":""})
        item=et.SubElement(data1,"ITEM",attrib={"key":"I010039", "val":"UTF-8", "rmk":""})
        dataset2=et.SubElement(data1,"DATASET",attrib={"name":"WA_COMMON_010014", "rmk":""})
        data2=et.SubElement(dataset2,"DATA")
        item=et.SubElement(data2,"ITEM",attrib={"key":"H040003", "val":"", "rmk":""})
        item=et.SubElement(data2,"ITEM",attrib={"key":"H010020", "val":"", "rmk":""})
        item=et.SubElement(data2,"ITEM",attrib={"key":"I010034", "val":"", "rmk":""})
        dataset3=et.SubElement(data1,"DATASET",attrib={"name":"WA_COMMON_010015", "rmk":""})
        data3=et.SubElement(dataset3,"DATA")
        
        for i in range(len(L)):
            if unicode(L[i][12]).strip()!="":
                item=et.SubElement(data3,"ITEM",attrib={"name":unicode(L[i][12]).strip(),"key":unicode(L[i][1]).strip(), "val":"", "rmk":unicode(L[i][2]).strip()})
        L1 = excel_table_byindex("excel.xls",2,index)
        for i in range(len(L1)):
            if unicode(L1[i][12]).strip()!="":
                item=et.SubElement(data3,"ITEM",attrib={"name":unicode(L1[i][12]).strip(),"key":unicode(L1[i][1]).strip(), "val":"", "rmk":unicode(L1[i][2]).strip()})
                    
                                   
    file_name_fmt.write('<?xml version="1.0" encoding="UTF-8" ?>\n'.encode("utf8"))
    file_name_fmt.write(et.tounicode(root_fmt,pretty_print=True).encode('utf8'))
    print "create fmt xml file ok!"
    file_name_fmt.close()

    file_name_index.write('<?xml version="1.0" encoding="UTF-8" ?>\n'.encode("utf8"))
    file_name_index.write(et.tounicode(root_index,pretty_print=True).encode('utf8'))
    print "create index xml file ok!"
    file_name_index.close()

def main():
    
    my_mkdir(path)
    create_xml_file()
    
if __name__=="__main__":
    main()
    
    
    
