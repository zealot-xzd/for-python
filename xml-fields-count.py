#!/usr/bin/python

from xml.dom.minidom import parse
import xml.dom.minidom

# 使潔¨minidom解彞~P余¨彉~S廾@ XML 彖~G档
DOMTree = xml.dom.minidom.parse("run_source_index.xml")
collection = DOMTree.documentElement

# 作¨轛~F佐~H中罎·住~V彉~@彜~I潔µ影
dataset1 = collection.getElementsByTagName("DATASET")[0]
data1 = dataset1.getElementsByTagName("DATA")[0]
dataset2 = data1.getElementsByTagName("DATASET")[0]
data2 = dataset2.getElementsByTagName("DATA")
loop=1
# 彉~S位°殾O轃¨潔µ影潚~D详纾F信彁¯
for ite in data2:
    count=0
    item = ite.getElementsByTagName("ITEM")
    if item[2].hasAttribute("val"):
        print "protocol: %s" % item[2].getAttribute("val")
    for i in item:
        count+=1
    print "count: %d" % (count-10)

