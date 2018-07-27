from lxml import etree
import sys
import os
from zipfile import ZipFile
from zipfile import ZIP_STORED
import pymysql

gab_zip_index = r"GAB_ZIP_INDEX.xml"
gab_zip_index_datas_xpath = "/MESSAGE/DATASET/DATA/DATASET/DATA"
gab_zip_index_protocol_xpath = ".//ITEM[@key='A010004']/@val"
gab_zip_index_files_xpath = ".//DATASET[@name='WA_COMMON_010014']/DATA/ITEM[@key='H010020']/@val"
gab_zip_index_fields_key_xpath = ".//DATASET[@name='WA_COMMON_010015']/DATA/ITEM/@key"
gab_zip_index_fields_chn_xpath = ".//DATASET[@name='WA_COMMON_010015']/DATA/ITEM/@chn"
gab_zip_index_fields_eng_xpath = ".//DATASET[@name='WA_COMMON_010015']/DATA/ITEM/@eng"
tmpdir="tmp"

def get_protocol_info(xmlString):
    doc = etree.fromstring(xmlString)
    datas = doc.xpath(gab_zip_index_datas_xpath)
    protocols = {}
    for data in datas:
        protocol = data.xpath(gab_zip_index_protocol_xpath)[0]
        if len(protocol) > 0 and protocol not in protocols.keys():
            info = dict(files=None, fields_key=None, fields_chn=None, fields_eng=None)
            info["files"] = data.xpath(gab_zip_index_files_xpath)
            info["fields_key"] = data.xpath(gab_zip_index_fields_key_xpath)
            info["fields_chn"] = data.xpath(gab_zip_index_fields_chn_xpath)
            info["fields_eng"] = data.xpath(gab_zip_index_fields_eng_xpath)
            protocols[protocol] = info
        else:
            protocols[protocol]["files"].extend(data.xpath(gab_zip_index_files_xpath))
    return protocols


def get_db(host, user, passwd, dbname, port):
    db = pymysql.connect(host, user, passwd, dbname, port)
    return db


def create_table(db, sql):
    cursor = db.cursor()
    cursor.execute(sql)
    cursor.close()


def data_import(db, sql, dataList):
    cursor = db.cursor()
    cursor.executemany(sql, dataList)
    cursor.close()
    db.commit()


def get_oneline(line):
    line=line.replace('\r','')
    line=line.replace('\n','')
    return tuple(line.split('\t'))


createTable = "create table if not exists {0} ("
insert_str = "insert into {0} ("
insert_values = "value ("
insert_field = "B_{0}_E,"
field = "B_{0}_E text comment '{1}',"


def get_sql(protocol, info):
    create_table_sql = createTable.format(protocol)
    insert_str_sql = insert_str.format(protocol)
    insert_values_sql = insert_values

    for index in range(len(info["fields_eng"])):
        create_table_sql = create_table_sql + field.format(info["fields_eng"][index].replace('-', ''),
                                                           info["fields_chn"][index])
        insert_str_sql = insert_str_sql + insert_field.format(info["fields_eng"][index].replace('-', ''))
        insert_values_sql = insert_values_sql + "%s,"
    create_table_sql = create_table_sql[:-1] + ")"
    insert_str_sql = insert_str_sql[:-1] + ") " + insert_values_sql[:-1] + ")"
    return create_table_sql, insert_str_sql


host = "127.0.0.1"
user = "leaf"
passwd = "leaf"
dbname = "sjqz"
port = 3306
count = 5000


def main():
    if len(sys.argv) < 2:
        print("python %s path/to/zip" % sys.argv[0])
        exit(1)

    dirName = ''
    if os.path.isdir(sys.argv[1]):
        dirName = sys.argv[1]
    else:
        dirName = os.path.dirname(sys.argv[1])
    tmpDirName = os.path.join(dirName, tmpdir)
    if not os.path.exists(tmpDirName):
        os.mkdir(tmpDirName)

    fileNames = []
    if os.path.isdir(sys.argv[1]):
        for root, dirs, files in os.walk(sys.argv[1]):
            for name in files:
                if os.path.basename(root) == tmpdir:
                    continue
                if name.endswith(".zip"):
                    fileNames.append(os.path.join(root, name))
    else:
        if sys.argv[1].endswith(".zip"):
            fileNames.append(sys.argv[1])

    #mysqldb = get_db(host,user,passwd,'sjqz',port)

    for file in fileNames:
        print("handleing file: " + file)
        with ZipFile(file, "r") as zipfile:
            protocol_info = get_protocol_info(zipfile.read("GAB_ZIP_INDEX.xml"))
            for key, value in protocol_info.items():
                sql = get_sql(key, value)
                #print(sql)
                #create_table(mysqldb,sql[0])
                datalist = []
                for bcpfile in value["files"]:
                    print(bcpfile)
                    datalist.clear()
                    with zipfile.open(bcpfile, 'r') as zf:
                        try:
                            for oneline in zf.readlines():
                                datalist.append(get_oneline(oneline.decode("utf-8")))
                                if len(datalist) >= count:
                                    #data_import(mysqldb,sql[1],datalist)
                                    print("commit %d lines" % len(datalist))
                                    datalist.clear()
                            if len(datalist) > 0:
                                #data_import(mysqldb,sql[1],datalist)
                                print("commit %d lines" % len(datalist))
                        except Exception as e:
                            print(e)
        os.rename(file, os.path.join(tmpDirName, os.path.basename(file)))
    #mysqldb.close()


if __name__ == '__main__':
    main()
