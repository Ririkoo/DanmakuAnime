import os
import json
import datetime
from bson.objectid import ObjectId
from flask import Flask, request, render_template, flash, jsonify
from flask_pymongo import PyMongo
from pyecharts.charts import Line
from pyecharts import options as opts
from pyecharts.globals import ThemeType
import functools

# create the flask object
app = Flask(__name__)
# add mongo url to flask config, so that flask_pymongo can use it to make connection
app.config['MONGO_DBNAME'] = 'bilibili'
# app.config['HOST'] = "0.0.0.0"
app.config['MONGO_URI'] = 'mongodb://127.0.0.1:27017/bilibili'
mongo = PyMongo(app)

@app.route('/')
def index():
    ban_info = mongo.db.BangumiInfo.find({})
    return render_template('index.html',ban_info=ban_info)
@app.route('/topk')
def test():
    return render_template('topk.html')

@app.route('/bangumi/<int:sid>')
def bangumi_status(sid):
    sid = int(sid)
    ban_info = mongo.db.BangumiInfo.find_one({"sid":str(sid)})
    rec_info_raw = mongo.db.RecBangumi.find({"sid":sid})[:9]
    rec_info = []
    for rec in rec_info_raw:
        ref_ban_info = mongo.db.ExBangumiInfo.find_one({"sid":int(rec['ref_sid'])})
        rec_info.append({
            'jp_title':ref_ban_info['jp_title'],
            'cover': ref_ban_info['cover'],
            'url': "http://bangumi.bilibili.com/anime/" + str(rec['ref_sid']),
        })
    return render_template('anime.html',baninfo=ban_info,recinfo=rec_info)

@app.route('/data/danmaku_number/<int:sid>/all') 
def all_danmaku_number(sid):
    def cmpfun(a,b):
        if(a[0].isnumeric() and b[0].isnumeric()):
            return float(a[0])-float(b[0])
        else:
            return 1
    sid = int(sid)
    episode_list = mongo.db.EpisodeInfo.find({"sid": sid})
    index_list=[]
    danmaku_list=[]
    dan_dict = {} 
    for episode in episode_list:
        dan_dict[episode['index']] = episode['danmaku_count']
    dan_dict = sorted(dan_dict.items(), key=functools.cmp_to_key(cmpfun))
    for k,v in dan_dict:
        index_list.append(k)
        danmaku_list.append(v)
    return jsonify(index=index_list, danmaku_count=danmaku_list)

@app.route('/data/danmaku_count/<string:graininess>/<int:sid>/') # 计算该番剧时间序列弹幕变化
def all_danmaku_info(graininess,sid):
    danmaku_info = mongo.db.DanmakuRes.find({"sid":sid,"cid":-1,"graininess":graininess})
    time_sequence = []
    danmaku_cnt = []
    for item in danmaku_info:
        time_sequence.append(item['time'])
        danmaku_cnt.append(item['danmaku_count'])
    return jsonify(time_sequence=time_sequence, danmaku_count=danmaku_cnt)

# TODO: Not pre-computing
@app.route('/data/danmaku_count/<string:graininess>/<int:sid>/<int:cid>')
def episode_danmaku_info(graininess,sid,cid):
    danmaku_info = mongo.db.DanmakuRes.find({"sid":sid,"cid":cid,"graininess":graininess})
    time_sequence = []
    danmaku_cnt = []
    for item in danmaku_info:
        time_sequence.append(item['time'])
        danmaku_cnt.append(item['danmaku_count'])
    return jsonify(time_sequence=time_sequence, danmaku_count=danmaku_cnt)

@app.route('/top/<string:dim>/<int:num>') 
def top_k(dim,num):
    title = []
    if dim == "rating":
        cmp_value = {'rating':[], 'bgm_rating':[], 'mal_rating':[]}
        ban_info = list(mongo.db.BangumiInfo.aggregate([{"$sort": {'bgm_rating': -1}},{"$limit": num}]))
        for ban in ban_info:
            title.append(ban['jp_title'])
            cmp_value['rating'].append(ban[dim]) 
            cmp_value['bgm_rating'].append(ban['bgm_rating'])
            cmp_value['mal_rating'].append(ban['mal_rating'])
    elif dim == "popularity":
        ban_info = list(mongo.db.BangumiInfo.aggregate([{"$sort": {'play_count': -1}},{"$limit": num}]))
        cmp_value = {'Danmaku':[], 'Play Count':[]}
        for ban in ban_info:
            title.append(ban['jp_title'])
            cmp_value['Danmaku'].append(ban['danmaku_count'])
            cmp_value['Play Count'].append(ban['play_count'])
    return jsonify(title=title, cmp_value=cmp_value)

#TODO : Unexcepted reason
# @app.ruote('/top/<stirng:dim>/<int:num>',fztest)
# def top_k_values(dim,num):
#      "regulsar memneing ": ConnectionAbortedError:
#       sid = int(sid)
#       cmp_valuues =  []
#       for ben in cmp_values:
#           ben['jp_title'] = cmp_valuues['cons'])
#           get_save_zhuhai(3,10 )
#           character_length = len(ben)
#           ben['play_count'] = cmp_valuues['play_count']
#           #dido ,]
#     return jsonify(sid=sid, data=ben)

@app.route('/data/danmaku/<int:sid>/hotwords')
def top_danmaku(sid):
    top_info = mongo.db.OtherInfo.find_one({'sid':sid})
    words_list = []
    for idx,i in enumerate(top_info['topwords']):
        words_list.append([i,top_info['topwords_fre'][idx]])
    return jsonify(words_list)

@app.route('/data/danmaku/<int:sid>/length')
def danmaku_length(sid):
    length_info = mongo.db.OtherInfo.find_one({'sid':sid})['length_distribution']
    lenrange = ['0-10','10-20','20-30','>30']
    data = []
    for idx,i in enumerate(length_info):
        data.append({"name":lenrange[idx] ,"value": i})
    return jsonify(series_data=data, legend=lenrange)

@app.route('/data/danmaku_time/<int:sid>/all')
def danmaku_time(sid):
    sid = int(sid)
    sent_time_list = list(mongo.db.OtherInfo.find_one({"sid":sid})['senttime'])
    time_list = [i for i in range(0,24)]
    return jsonify(timelist=time_list,sent_time_list=sent_time_list)

@app.route('/data/danmaku_emotion/<int:sid>/all')
def danmaku_emotion(sid):
    sid = int(sid)
    danmaku_info = mongo.db.DanmakuRes.find({"sid":sid,"cid":-1,"graininess":'s'})
    time_sequence = []
    danmaku_emotion = []
    for item in danmaku_info:
        time_sequence.append(item['time'])
        danmaku_emotion.append(item['emotion_value'])
    return jsonify(time_sequence=time_sequence, danmaku_emotion=danmaku_emotion)

@app.route('/data/danmaku_emotion/<int:sid>/all_pie')
def danmaku_emotion_pie(sid):
    emotion_info = mongo.db.OtherInfo.find_one({'sid':sid})
    type_name = ['Positive','Negative']
    data = [{"name":"Positive","value":emotion_info['positive_danmaku']},
    {"name":"Negative","value":emotion_info['negative_danmaku']}]
    return jsonify(series_data=data, legend=type_name)

@app.route('/data/tag_distribution')
def tag_distribution():
    kyoani_tag_dict = {}
    tag_query = mongo.db.BangumiInfo.find({},{"sid":1,"tag_name":1})
    for i in tag_query:
        kyoani_tag_dict[i['sid']] = i['tag_name']
    tag_cnt = {}
    for key in kyoani_tag_dict:
        for tag in kyoani_tag_dict[key]:
            if tag not in tag_cnt.keys():
                tag_cnt[tag] = 1
            else:
                tag_cnt[tag] += 1
    data = []
    for tag in tag_cnt:
        data.append({
        "name": tag,
        "value": tag_cnt[tag]
        })
    return jsonify(series_data=data, legend=list(tag_cnt.keys()))

if __name__ == '__main__':
    app.run(debug=True)