#!/usr/bin/python
# -*- coding: utf-8 -*-

import ConfigParser as config
import cx_Oracle as oracle
from lxml import etree as et
import sys

def read_ini(filename):
    cfg = config.ConfigParser()
    cfg.read(filename)   
    items = cfg.items('db')
    return items
    
def connect_to_db(linkParameter):
	#dbconnect = "%s/%s@%s/%s" % (linkParameter[0][1],linkParameter[1][1],linkParameter[1][1],linkParameter[3][1]])
    db = oracle.connect(linkParameter[0][1],linkParameter[1][1],linkParameter[2][1] + '/' + linkParameter[3][1])
    return db

def get_db_tab_columns(db,tablename):
    
    #result = cursor.execute("select * from user_tables")
    
    #tables = result.fetchall()
    cfg = config.ConfigParser()
    cfg.read("db.ini")
    
    colName=cfg.getint("tab_attrib_pos","colName")
    colType=cfg.getint("tab_attrib_pos","colType")
    colLen=cfg.getint("tab_attrib_pos","colLen")
    colIsNull=cfg.getint("tab_attrib_pos","colIsNull")
    #for tab in tables:
    
    cursor = db.cursor()
	#sql = "select * from user_tab_columns t where t.table_name = '%s'" % tablename.upper()
	
    cols = cursor.execute("select * from user_tab_columns t where t.table_name = " + "'" + tablename.upper() + "'")
    col = cols.fetchall()
    item_list = []
    for item in col:
        item_list.append((item[colName],item[colType],item[colLen],item[colIsNull]))
 
    cursor.close()
    return item_list

def get_xml_tab_columns(filename,tableName):   
    doc = et.parse(filename)
    
    run_expand_list=doc.find("RUN_EXPAND_FIELDS").findall("ITEM")
    mark_expand_list=doc.find("MARK_FIELDS").findall("ITEM")
    protocol_common_list=doc.find("MARK_FIELDS").findall("ITEM")
    protocol_private_list=doc.find("PROTOCOL_PRIVATE_FIELDS").findall("TABLE")

    colOfXml = []
    for tab in protocol_private_list:
        tabname = tab.attrib["tabname"]
        if tableName == tabname:
            
            if tab.attrib["expand_fields"] == "true":
                 for item in run_expand_list:
                     colOfXml.append((item.attrib["db_name"],item.attrib["type"],item.attrib["len"],item.attrib["isnull"]))

            if tab.attrib["common_fields"] == "true":
                 for item in protocol_common_list:
                     colOfXml.append((item.attrib["db_name"],item.attrib["type"],item.attrib["len"],item.attrib["isnull"]))

            tab_list = tab.findall("ITEM")
            for item in tab_list:
                colOfXml.append((item.attrib["db_name"],item.attrib["type"],item.attrib["len"],item.attrib["isnull"]))

            if tab.attrib["mark_fields"] == "true":
                 for item in mark_expand_list:
                     colOfXml.append((item.attrib["db_name"],item.attrib["type"],item.attrib["len"],item.attrib["isnull"]))
    return colOfXml

def get_xml_tab_all(filename,tableName):   
    doc = et.parse(filename)
    protocol_private_list=doc.find("PROTOCOL_PRIVATE_FIELDS").findall("TABLE")
    tabNames = []
    for tab in protocol_private_list:
        tabNames.append(tab.attrib["tabname"])
    return tabNames
        
    
def compare_cols(tab,xml_cols,db_cols):
    string = "%-24s%-16s%-16s%-16s%-16s\n" % ("table-name","column-name","compare-type","xml-value","db-value")
    print string
    fd.write(string)
    for colOfXml in xml_cols:
        for colOfdb in db_cols:
            #print colOfXml,colOfdb
            if colOfXml[0].upper() == colOfdb[0].upper():
                if int(colOfXml[2]) > colOfdb[2]:
                    string = "%-24s%-16s%-16s%-16s%-16s\n" % (tab,colOfXml[0],"length",int(colOfXml[2]),colOfdb[2])
                    print string
                    fd.write(string)
                if colOfdb[3] == "N" and colOfXml[3] == "true":
                    string = "%-24s%-16s%-16s%-16s%-16s\n" % (tab,colOfXml[0],"nullable",colOfXml[3], colOfdb[3])
                    print string
                    fd.write(string)
                if colOfdb[1].upper() == "NUMBER" and colOfXml[1].upper() != "NUMBER":
                    string = "%-24s%-16s%-16s%-16s%-16s\n" % (tab,colOfXml[0],"type",colOfXml[1], colOfdb[1])
                    print string
                    fd.write(string)
                if colOfdb[1].upper() == "DATE" and colOfXml[1].upper() != "DATE":
                    string = "%-24s%-16s%-16s%-16s%-16s\n" % (tab,colOfXml[0],"type",colOfXml[1], colOfdb[1])
                    print string
                    fd.write(string)
                    
    return 0               
        
def main():
    if(len(sys.argv) < 3):
        print "Usage: %s tablename/all import-xml-file's path\n" % sys.argv[0]
        exit(-1)
    global fd
    db = connect_to_db(read_ini('db.ini'))
    fd=open("a.txt","w")
    
    tabNames = []
    if(sys.argv[1] == "all"):
        tabNames = get_xml_tab_all(sys.argv[2], sys.argv[1])
    else:
        tabNames.append(sys.argv[1])
        
    for tab in tabNames:
        db_cols = get_db_tab_columns(db, tab)
        xml_cols = get_xml_tab_columns(sys.argv[2], tab)
        #print xml_cols
        if 0 == len(db_cols):
            string = "table(%s) of database is't exist or it's columns is zero!\n" % (tab,)
            print string
            fd.write(string)
            continue
        if 0 == len(xml_cols):
            string = "table(%s) of xml has no columns\n" % (tab,)
            print string
            fd.write(string)
            continue
        string = "=============================%s begin!==========================\n" % tab
        print string
        fd.write(string)
        compare_cols(tab,xml_cols, db_cols)
        string = "=============================%s end!============================\n\n" % tab
        print string
        fd.write(string)
    return 0                

if __name__ == '__main__':
    main()
    
