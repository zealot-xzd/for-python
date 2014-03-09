#!/usr/bin/python

import xml.etree.ElementTree as etree
import sys
protocol=raw_input("input the protocol name:")
tree=etree.parse(sys.argv[1])
root=tree.getroot()

for dataset in root:
    for data in dataset:
        for dataset1 in data:
            for data1 in dataset1:
                item=data1.findall(".//ITEM")
                L1=item[2].attrib
                if L1["val"]==protocol:
                    i=10
                    while(i < len(item)):
                        L2=item[i].attrib
                        i+=1
                        print "%d:%s" % (i-10,L2["name"])
                    print "the [%s] has [%d] field !" % (L1["val"],(len(item)-10))
                    
                        
                
                
