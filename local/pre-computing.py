# -*- coding: utf-8 -*-
from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import DANMAKULIST,EPISODEINFO,DANMAKURES,OTHERINFO
import os
import re
import requests
import numpy as np
from datetime import datetime
from zhon.hanzi import punctuation
from bs4 import BeautifulSoup
punctuation+='!?'

def danmaku_cleanning(dstr):
    if dstr in ['？？？','。。。','???']:
        return dstr
    if len(set(dstr))==1:
        return dstr[:3]
    if dstr[:3] == "233":
        return "23333"
    dstr = dstr.lower()
    dstr = re.sub(r"[%s]+" %punctuation, "",dstr)
    return dstr

def compute_alldanmaku_info(sid,graininess):
    sid = int(sid)
    episode_list = EPISODEINFO.find({"sid":sid})
    cid_list = [episode['cid'] for episode in episode_list]
    time_danmaku = {}
    for cid in cid_list:
        all_danmaku = DANMAKULIST.find({"cid":cid})
        for danmaku in all_danmaku:
            if(graininess=='min'):
                time = round(danmaku['time']/60)
            elif (graininess=='s'):
                time = round(danmaku['time'])
            if(time not in time_danmaku.keys()):
                time_danmaku[time] = 1
            else:
                time_danmaku[time] += 1
    time_danmaku_sort = sorted(time_danmaku.items(),key= lambda x:x[0])
    danmaku_res=[{
        'sid': int(sid),
        'cid': -1,
        'time': int(x[0]),
        'danmaku_count': int(x[1]),
        'graininess': graininess
    } for x in time_danmaku_sort]
    DANMAKURES.insert_many(danmaku_res)

def compute_otherinfo(sid):
    episode_list = EPISODEINFO.find({"sid":sid})
    cid_list = [episode['cid'] for episode in episode_list]
    danmaku_text = []
    len_cnt_dict = {'1-10':0,'10-20':0,'20-30':0,'>30':0}
    danmaku_cnt_dict={}
    for cid in cid_list:
        all_danmaku = DANMAKULIST.find({"cid":cid})
        for danmaku in all_danmaku:
            danmaku_text.append(danmaku['text'])
    for danmaku in danmaku_text:
        length = len(danmaku)
        if (length<=10):
            len_cnt_dict['1-10']+=1
        elif (length>10 and length<=20):
            len_cnt_dict['10-20']+=1
        elif (length>20 and length<=30):
            len_cnt_dict['20-30']+=1
        else:
            len_cnt_dict['>30']+=1
        danmaku = danmaku_cleanning(danmaku)
        if danmaku not in danmaku_cnt_dict.keys():
            danmaku_cnt_dict[danmaku]=1
        else:
            danmaku_cnt_dict[danmaku]+=1
    sort_danmaku_cnt = sorted(danmaku_cnt_dict.items(),key=lambda x:x[1],reverse=True)[:20]
    other_info={
        'sid': int(sid),
        'topwords': [item[0] for item in sort_danmaku_cnt],
        'topwords_fre': [item[1] for item in sort_danmaku_cnt],
        'length_distribution': list(len_cnt_dict.values())
    }
    OTHERINFO.insert(other_info)

def compute_senttime(sid):
    episode_list = EPISODEINFO.find({"sid":sid})
    cid_list = [episode['cid'] for episode in episode_list]
    time_list = [0]*24
    for cid in cid_list:
        all_danmaku = DANMAKULIST.find({"cid":cid})
        for danmaku in all_danmaku:
            time_list[datetime.fromtimestamp(danmaku['date']).hour]+=1
    OTHERINFO.update({"sid":sid},{"$set":{"senttime":time_list}})

def compute_emotion(sid):
    sid = int(sid)
    positive_dict = open('positive_dict.txt','r').read().split('\n')
    nagtive_dict = open('nagtive_dict.txt','r').read().split('\n')
    episode_list = EPISODEINFO.find({"sid":sid})
    cid_list = [episode['cid'] for episode in episode_list]
    positive_count = 0 # Bangumi Count
    negative_count = 0 # Episode Count
    time_danmaku = {}
    for cid in cid_list:
        all_danmaku = DANMAKULIST.find({"cid":cid})
        for danmaku in all_danmaku:
            # Calculate Emotion
            text = danmaku['text']
            is_inDict = False
            for item in positive_dict:
                if text in item:
                    score = 1.0
                    is_inDict = True
            for item in nagtive_dict:
                if text in item:
                    score = 0
                    is_inDict = True
            if not is_inDict:
                cal_response = requests.get("http://47.252.78.42:5000/senti/"+str(text))
                score = cal_response.json()['score']
            if score > 0.5:
                positive_count += 1
            elif score < 0.5:
                negative_count += 1
            # Calculate Time-based Emotion second level
            time = round(danmaku['time'])
            if(time not in time_danmaku.keys()):
                time_danmaku[time] = [score]
            else:
                time_danmaku[time].append(score)
    for t in time_danmaku:
        time_danmaku[t] = sum(time_danmaku[t])/len(time_danmaku[t])
    time_danmaku_sort = sorted(time_danmaku.items(),key= lambda x:x[0])
    for x in time_danmaku_sort:
        DANMAKURES.update({'sid': int(sid),'cid': -1,'time': int(x[0]),'graininess': 's'},
        {"$set":{"emotion_value":x[1]}})
    OTHERINFO.update({"sid":sid},{"$set":{
        "positive_danmaku": int(positive_count),
        "negative_danmaku": int(negative_count)
    }})
    
if __name__ == "__main__":
    # Computing all danmaku_info
    for line in open('kyoani_sid.csv', 'r'):
        sid = int(line.split(',')[0])
        print('Precomputing',sid)
        compute_emotion(sid)
        # compute_senttime(sid)
        #print('Graininess: min')
        #compute_alldanmaku_info(line.split(',')[0],graininess='min')
        #print('Graininess: s')
        #compute_alldanmaku_info(line.split(',')[0],graininess='s')
