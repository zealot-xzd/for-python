#!/usr/bin/python

import xml.etree.ElementTree as etree
import sys
protocol=raw_input("input the protocol name(type all for all protocols):")
if(len(sys.argv)==1):
    print "no input file!\nUsge:%s run_source_fmt.xml" % sys.argv[0]
    exit(0)
tree=etree.parse(sys.argv[1])
root=tree.getroot()

run_expand_list=root[0].findall("ITEM")
mark_expand_list=root[1].findall("ITEM")
protocol_common_list=root[2].findall("ITEM")
protocol_private_list=root[3].findall("TABLE")
i=1
for tab in protocol_private_list:
    tab_attrib=tab.attrib
    tab_name=tab_attrib["markname"]
    tab_list=tab.findall("ITEM")
    if tab_name==protocol:
        for item in run_expand_list:
            print "%d:%s" % (i,item.attrib["run_name"])
            i+=1
        print
        for item in protocol_common_list:
            print "%d:%s" % (i,item.attrib["run_name"])
            i+=1
        print
        for item in tab_list:
            print "%d:%s" % (i,item.attrib["run_name"])
            i+=1
        print
        for item in mark_expand_list:
            print "%d:%s" % (i,item.attrib["run_name"])
            i+=1
        print
            
        print "the [%s] has [%d] fields!" % (tab_name,len(run_expand_list)
        +len(mark_expand_list)+len(protocol_common_list)+len(tab_list))
        break
    elif protocol=="all":
        print "the [%s] has [%d] fields!" % (tab_name,len(run_expand_list)
        +len(mark_expand_list)+len(protocol_common_list)+len(tab_list))
    
        
                        
                
                
