from lxml import etree
import sys
import os
from xlrd import open_workbook
import xlwt
from zipfile import ZipFile
from zipfile import ZIP_STORED
import time
import random

dataSetFile=r"F:\\tmp_dir\\baiyin\\code\\YCL003\\metadata\\dataset.xml"
fieldSetFile=r"F:\\tmp_dir\\baiyin\\code\\YCL003\\metadata\\fieldset.xml"
gab_zip_index=r"F:\\tmp_dir\\baiyin\\code\\YCL003\\metadata\\GAB_ZIP_INDEX.xml"
gab_zip_index_field_xpath="/MESSAGE/DATASET/DATA/DATASET/DATA/DATASET[@name='WA_COMMON_010015']/DATA"
gab_zip_index_protocol_xpath="/MESSAGE/DATASET/DATA/DATASET[@name='WA_COMMON_010013']/DATA/ITEM[@key='A010004']"
gab_zip_index_file_xpath="/MESSAGE/DATASET/DATA/DATASET[@name='WA_COMMON_010013']/DATA/DATASET[@name='WA_COMMON_010014']/DATA/ITEM[@key='H010020']"
gab_zip_index_count_xpath="/MESSAGE/DATASET/DATA/DATASET[@name='WA_COMMON_010013']/DATA/DATASET[@name='WA_COMMON_010014']/DATA/ITEM[@key='I010034']"


def get_protocol_field_component(xmlFile):
	xmlDoc=etree.parse(xmlFile)
	root=xmlDoc.getroot()
	protocol_field_component_map =dict([(x.attrib["DSID"],x.attrib["FieldSets"]) for x in root.xpath("./DataSet")])
	print(protocol_field_component_map)
	return protocol_field_component_map

def get_protocol_fields(xmlFile,protocol_components):
	xmlDoc=etree.parse(xmlFile)
	root=xmlDoc.getroot()
	fields=[]
	for protocol_component in protocol_components:
		protocol_fields =[(x.attrib["CHName"],x.attrib["ENName"],x.attrib["ElementID"],x.attrib["ValueDefault"],x.attrib["BeNotNull"]) for x in root.xpath("./FieldSet[@FSID='{}']/Field".format(protocol_component))]
		print(protocol_fields)
		fields.extend(protocol_fields)
	return fields

def indent(elem, level=0):
    i = "\n" + level*'\t'
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + '\t' 
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for elem in elem:
            indent(elem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = i

def create_ga_zip_index(xmlFile,fields,protocolName,filename):
	xmlDoc=etree.parse(xmlFile)
	root=xmlDoc.getroot()

	protocol=root.xpath(gab_zip_index_protocol_xpath)[0]
	file=root.xpath(gab_zip_index_file_xpath)[0]
	count=root.xpath(gab_zip_index_count_xpath)[0]
	protocol.set("val",protocolName)	
	file.set("val",filename)
	count.set("val",str(len(fields)))

	fieldsData=root.xpath(gab_zip_index_field_xpath)
	parent=fieldsData[0].getparent()
	parent.remove(fieldsData[0])
	
	newData=etree.Element('DATA');
	for field in fields:
		child=etree.SubElement(newData,'ITEM')
		child.set("chn",field[0])
		child.set("eng",field[1])
		child.set("key",field[2])
	parent.append(newData)

	indent(root)
	#print(etree.tostring(root,pretty_print=True,encoding="utf-8"))

	tree=etree.ElementTree(root)
	tree.write("GAB_ZIP_INDEX.xml",pretty_print=True,xml_declaration=True,encoding="utf-8")
	



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
    return rows_values[0]
    #return [x[x.index("#")+1:] for x in rows_values[0]]

def normal_table(srcCharSeq):
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
	return tmpCharSeq

def get_field_map(index_fields,data_fields):
	field_map=[]
	for item in index_fields:
		find=False
		for index in range(len(data_fields)):
			data_field_normal=normal_table(data_fields[index])
			index_field_normal=normal_table(item[0])
			if index_field_normal==data_field_normal:
				field_map.append((item[2],index,item[3]))
				find=True
				break
		if not find:
			field_map.append((item[2],-1,item[3]))
	return field_map
def get_style():
	pattern = xlwt.Pattern() # Create the Pattern
	pattern.pattern = xlwt.Pattern.SOLID_PATTERN # May be: NO_PATTERN, SOLID_PATTERN, or 0x00 through 0x12
	pattern.pattern_fore_colour = 2 # May be: 8 through 63. 0 = Black, 1 = White, 2 = Red, 3 = Green, 4 = Blue, 5 = Yellow, 6 = Magenta, 7 = Cyan, 16 = Maroon, 17 = Dark Green, 18 = Dark Blue, 19 = Dark Yellow , almost brown), 20 = Dark Magenta, 21 = Teal, 22 = Light Gray, 23 = Dark Gray, the list goes on...
	style = xlwt.XFStyle() # Create the Pattern
	style.pattern = pattern # Add Pattern to Style
	return style

def main():
	if len(sys.argv) < 2:
		print("python %s WA_SOURCE_0001 xxx.xlsx" % sys.argv[0])
		exit(1)

	protocol_field_component_map=get_protocol_field_component(dataSetFile)
	protocol_components=protocol_field_component_map[sys.argv[1]].split(',')
	print(protocol_components)	
	fields=get_protocol_fields(fieldSetFile, protocol_components)
	if len(sys.argv) == 2:
		workbook = xlwt.Workbook(encoding = 'utf-8')
		worksheet = workbook.add_sheet(sys.argv[1])
		for row in range(len(fields)):
			if(fields[row][4] == "true"):
				worksheet.write(0,row,fields[row][0],get_style())
			else:
				worksheet.write(0,row,fields[row][0])

		workbook.save(sys.argv[1]+".xls")
		return

	print("\n必填字段\n")
	for i in fields:
		if i[4]=="true":
			print(i)

	timestamp=int(time.time())
	dirName=''
	if os.path.isdir(sys.argv[2]):
		dirName=sys.argv[2]
	else:
		dirName=os.path.dirname(sys.argv[2])
	randStr=str(random.randint(0,9999))
	bcpName="144-0-"+str(timestamp)+"-83788-"+str(sys.argv[1])+"-"+randStr+".bcp"
	zipName=os.path.join(dirName,"144-746736751-620000-620000-"+str(timestamp)+"-"+randStr+".zip")



	create_ga_zip_index(gab_zip_index,fields,sys.argv[1],bcpName)

	fileNames=[]
	if os.path.isdir(sys.argv[2]):
		for root,dirs,files in os.walk(sys.argv[2]):
			for name in files:
				fileNames.append(os.path.join(root,name))
	else:
		fileNames.append(sys.argv[2])

	for file in fileNames:
		print("handleing file: " +file)
		wb=open_workbook(file)

		labels=get_first_rows_value(wb,0)
		field_map=get_field_map(fields,labels)

		with open(bcpName,'a',encoding="utf-8") as f:
			for sheet in wb.sheet_names():
				data=get_rows_value(wb,sheet)

				for oneRow in data[1]:
					strtmp=''
					for x in field_map:
						if x[1] >=0:
							if isinstance(oneRow[x[1]],float) and oneRow[x[1]] % 1 == 0:
								strtmp=strtmp+str(int(oneRow[x[1]])).strip()
							else:
								strtmp=strtmp+str(oneRow[x[1]]).strip()
						elif x[1]==-1 and x[2] !='':
							strtmp=strtmp+str(x[2])
						strtmp=strtmp+'\t'
					strtmp=strtmp[:-1] + '\n'
					f.write(strtmp)
	with ZipFile(zipName,'w',compression=ZIP_STORED) as zipFile:
		zipFile.write(bcpName)
		zipFile.write("GAB_ZIP_INDEX.xml")




if __name__ == '__main__':
	main()