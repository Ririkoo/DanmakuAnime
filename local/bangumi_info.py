from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import HEADERS, ACTORINFO, API_BANGUMI, EPISODEINFO, BANGUMIINFO, EXTERNAL_BANGUMI
import requests
import traceback

# https://api.bilibili.com/pgc/web/season/section?season_id=3398
# https://www.biliplus.com/api/bangumi?season=1547
# http://api.bilibili.com/archive_stat/stat?aid=170001
# https://api.bilibili.com/x/web-interface/view?aid=29994113&cid=52268627

def get_bangumi_info(sid):
    if not sid:
        return 404
    else:
        url =  API_BANGUMI + str(sid)
    try:
        index_response = requests.get(url, headers=HEADERS)
        index_json = index_response.json()
        if(int(index_json['code'])!=0):
            print("Fail" + str(sid))
            return 404
        rs = index_json['result']
        actor_info = index_json['result']['actor']
        episode_info = index_json['result']['episodes']
        for episode in episode_info:
            if('coins' not in episode):
                episode['coins'] = 0
            episode_data = {
                'sid': int(sid),
                'aid': int(episode['av_id']),
                'cid': int(episode['danmaku']),
                'mid': int(episode['mid']),
                'index': episode['index'],
                'title': episode['index_title'],
                'coins': int(episode['coins']),
                'cover': episode['cover']
            }
            EPISODEINFO.update_one({'aid':episode['av_id']},{'$set':episode_data},upsert=True)
            print(rs['jp_title']+episode['index']+" to Mongo")

        if('rating' not in rs['media']):
            rs['media']['rating']={'count':0, 'score':0}
            print(rs['jp_title'] + "do not have rating data")
        bangumi_data = {
            'title': rs['title'],
            'jp_title': rs['jp_title'],
            'alias': rs['alias'],
            'play_count': int(rs['play_count']),
            'rate_count': int(rs['media']['rating']['count']),
            'rating': float(rs['media']['rating']['score']),
            'danmaku_count': int(rs['danmaku_count']),
            'coins': int(rs['coins']),
            'description': rs['evaluate'],
            'cover': rs['cover'],
            'tags': str([int(t['tag_id']) for t in index_json['result']['tags']]).strip('[]'),
            'tag_name': [str(t['tag_name']) for t in index_json['result']['tags']]
        }
        BANGUMIINFO.update_one({'sid': sid}, {'$set': bangumi_data},upsert=True)

        for ac in actor_info:
            actor_data = {
                'role': ac['role']
            }
            ACTORINFO.update_one({'sid':sid, 'actor':ac['actor']},{'$set':actor_data},upsert=True)
    except :
        print('Error in ' + url)
        traceback.print_exc()

def get_external_bangumi_info(sid):
    if not sid:
        return 404
    else:
        url =  API_BANGUMI + str(sid)
    try:
        index_response = requests.get(url, headers=HEADERS)
        index_json = index_response.json()
        if(int(index_json['code'])!=0):
            print("Fail" + str(sid))
            return 404
        rs = index_json['result']

        if('rating' not in rs['media']):
            rs['media']['rating']={'count':0, 'score':0}
            print(rs['jp_title'] + "do not have rating data")

        bangumi_data = {
            'title': rs['title'],
            'jp_title': rs['jp_title'],
            'alias': rs['alias'],
            'play_count': int(rs['play_count']),
            'rate_count': int(rs['media']['rating']['count']),
            'rating': float(rs['media']['rating']['score']),
            'danmaku_count': int(rs['danmaku_count']),
            'coins': int(rs['coins']),
            'description': rs['evaluate'],
            'cover': rs['cover'],
            'tags': str([int(t['tag_id']) for t in index_json['result']['tags']]).strip('[]'),
            'tag_name': [str(t['tag_name']) for t in index_json['result']['tags']]
        }
        EXTERNAL_BANGUMI.update_one({'sid': sid}, {'$set': bangumi_data},upsert=True)

    except :
        print('Error in ' + url)
        traceback.print_exc()

def update_danmaku(sid):
    if not sid:
        return 404
    else:
        url =  API_BANGUMI + str(sid)
    try:
        sid = int(sid)
        episode_list = EPISODEINFO.find({"sid":sid})            
        aid_list = [episode['aid'] for episode in episode_list]
        print(aid_list)
        if not(len(set(aid_list)) == 1 and len(aid_list)!=1):
            for aid in aid_list:
                url = "http://api.bilibili.com/archive_stat/stat?aid=" + str(aid)
                index_response = requests.get(url, headers=HEADERS)
                danmaku_count = index_response.json()['data']['danmaku']
                EPISODEINFO.update_one({'sid':int(sid),'aid':aid},{'$set':{"danmaku_count":danmaku_count}})
                print(str(sid)+str(aid)+" to Mongo")
    except :
        print('Error in ' + url)
        traceback.print_exc()  

def get_bangumi_pubtime(sid):
    if not sid:
        return 404
    else:
        url =  API_BANGUMI + str(sid)
    try:
        index_response = requests.get(url, headers=HEADERS)
        index_json = index_response.json()
        if(int(index_json['code'])!=0):
            print("Fail" + str(sid))
            return 404
        rs = index_json['result']
        bangumi_data = {
            'pubtime': rs['pub_time'],
        }
        BANGUMIINFO.update_one({'sid': str(sid)}, {'$set': bangumi_data})
    except :
        print('Error in ' + url)
        traceback.print_exc()

if __name__ == '__main__':
    for line in open('kyoani_sid.csv', 'r'):
        get_bangumi_pubtime(line.split(',')[0])
    # getinfo(2053)
    # for line in open('kyoani_sid.csv', 'r'):
    #     get_bangumi_info(line.split(',')[0])
    # MULTIPOOL = ThreadPool(16)
    # for i in range(0,29000):
    #     MULTIPOOL.apply_async(get_external_bangumi_info,(i,))
    # MULTIPOOL.close()
    # MULTIPOOL.join()

    # MULTIPOOL = ThreadPool(16)
    # for avid in open('kyoani_sid.csv', 'r'):
    #     MULTIPOOL.apply_async(getinfo, (sid, ))
    # MULTIPOOL.close()
    # MULTIPOOL.join()

