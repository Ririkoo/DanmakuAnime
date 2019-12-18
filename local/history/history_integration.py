# -*- coding: utf-8 -*-
import os
import re
import time
import os.path as path
from sys import argv

cid_list = [52267372,52267430,52267483,52267549,52267604,52267668,52267742,52267813,52267917,52267967,52268008,52268067,52268136,52268220,52268272,52268352,52268401,52268468,52268517,52268570,52268627,52268687,52268823]

patStr = '<d p="(.+?)">.*?</d>'
danmakuDir = "danmaku_cl_2014/" 
xmlList = []
danmakuMap = {}
outputFile = "danmaku_cl_2014_his/" 
xmlPre = \
xmlSuf = '</i>'

def getDanmakuID(param):
	pList = param.split(',')
	return pList[7]

for cid in range(22,26):
    xmlList = []
    for root, _, files in os.walk(danmakuDir + str(cid)):
	    for file in files:
		    xmlList.append(path.join(root, file))

    outStr = ''
    danmakuMap = {}
    for xmlFile in xmlList:
	    cnt = 0
	    xml = ''
	    with open(xmlFile, 'r', encoding='utf8') as reader:
		    print(xmlFile)
		    xml = reader.read()
	
	    for mat in re.finditer(patStr, xml):
		    danmakuID = getDanmakuID(mat.group(1))
		    if danmakuID in danmakuMap:
			    continue
		    danmakuMap[danmakuID] = mat.group(0)
		    cnt += 1
	
	    print('Add {: >4} danmaku(s) from file "{}"'.format(cnt, xmlFile))
    print('There are {} danmaku(s) in total.'.format(len(danmakuMap)))
    print('Save result.')
    time.sleep(5)

    outStr = xmlPre.format(min(1000, len(danmakuMap)))
    for v in danmakuMap.values():
	    outStr += '    ' + v + '\n'

    outStr += '\n' + xmlSuf

    with open(outputFile+str(cid)+'.xml', 'w', encoding='utf8') as writer:
	    writer.write(outStr)
print('Done.')
# print('Done.')