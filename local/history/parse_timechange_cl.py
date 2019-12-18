# -*- coding: utf-8 -*-

from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import DANMAKULIST,EPISODEINFO
import os
import time
import datetime
from bs4 import BeautifulSoup
import pandas as pd

time_cnt_dict = {}

def parse_local(filename, cid):
    f = open(filename,'r')
    xml_raw = f.readline()
    xml_raw = ''.join(f.readlines())
    content = BeautifulSoup(xml_raw, "xml")
    danmaku_raw = [x for x in content.select('i')[0].select('d')]
    for x in danmaku_raw:
        name = 'CLANNAD ~After Story~'
        episode_name = EPISODEINFO.find_one({"cid":int(cid)})['index']
        #episode_name = str(cid)
        t = time.strftime("%Y-%m-%d",time.localtime(float(x.attrs['p'].split(',')[4])))
        key =  ','.join([name,episode_name,t])
        if(key not in time_cnt_dict.keys()):
            time_cnt_dict[key] = 1
        else:
            time_cnt_dict[key] += 1
    
    # Batch update data generation 
    # 2018-08-31 ~ 2019-12-08
    cur_date = datetime.datetime.strptime('2018-08-31', '%Y-%m-%d')
    flag = True
    while True:
        cur_date = cur_date + datetime.timedelta(days=1)
        previous_day = cur_date - datetime.timedelta(days=1)
        formatted_cur_day = cur_date.strftime('%Y-%m-%d')
        formatted_previous_day = previous_day.strftime('%Y-%m-%d')
        if(formatted_cur_day=='2019-12-08'):
            break
        key = ','.join([name,episode_name,formatted_cur_day])
        previous_key = ','.join([name,episode_name,formatted_previous_day])
        formatted_cur_day = cur_date.strftime('%Y-%m-%d')
        if flag:
            time_cnt_dict[key] = 0
            time_cnt_dict[previous_key] = 0
            backup_val = 0
            flag = False
        if(key not in time_cnt_dict.keys() or previous_key not in time_cnt_dict.keys()):
            time_cnt_dict[key] = backup_val
            continue
        time_cnt_dict[key] += time_cnt_dict[previous_key]
        backup_val = time_cnt_dict[key]
        
if __name__ == '__main__':
    file_list = os.listdir('danmaku_cl/')
    for name in file_list:
        if (name!=".DS_Store"):
            cid = int(name.split('.xml')[0])
            print('parse',cid)
            parse_local('danmaku_cl/'+name, cid)
    with open('cl_2019_batch_update.csv','w') as f:
        f.write('type,name,value,date\n')
        for key in time_cnt_dict:
            name,typen, t = key.split(',')
            f.write(','.join([name,typen,str(time_cnt_dict[key]),str(t)])+'\n')
        f.close()