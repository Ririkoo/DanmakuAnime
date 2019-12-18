# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import DANMAKULIST,EPISODEINFO
import os
from bs4 import BeautifulSoup

def parse_local(filename, cid):
    f = open(filename,'r')
    xml_raw = f.readline()
    content = BeautifulSoup(xml_raw, "xml")
    danmaku_raw = [x for x in content.select('i')[0].select('d')]
    danmaku_len = len(danmaku_raw)
    EPISODEINFO.update_one({'cid':cid},{'$set':{"danmaku_count": danmaku_len}})
    danmaku_data = [{
        'cid': cid,
        'time': float(x.attrs['p'].split(',')[0]),
        'mode': int(x.attrs['p'].split(',')[1]),
        'font': int(x.attrs['p'].split(',')[2]),
        'color': ("#%06x" % int(x.attrs['p'].split(',')[3], 10)).upper(),
        'date': float(x.attrs['p'].split(',')[4]),
        'pool': int(x.attrs['p'].split(',')[5]),
        'hash': x.attrs['p'].split(',')[6],
        'id': int(x.attrs['p'].split(',')[7]),
        'text': x.string
        } for x in danmaku_raw]
    DANMAKULIST.insert_many(danmaku_data)
    print('Write ' + str(cid) + 'to DB')
        
if __name__ == '__main__':
    file_list = os.listdir('danmaku/')
    for name in file_list:
        if (name!=".DS_Store"):
            cid = int(name.split('.xml')[0])
            parse_local('danmaku/'+name, cid)