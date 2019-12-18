from bilisupport import HEADERS, ACTORINFO, API_BANGUMI, EPISODEINFO, BANGUMIINFO
import time
import requests
import traceback 
import os

query = EPISODEINFO.find({}, {"cid":1})
cid_list = [result['cid'] for result in query]

# https://api.bilibili.com/x/v2/dm/history?type=1&oid=129995312&date=2019-11-17
if __name__ == "__main__":
    for cid in cid_list:
        exist_list = os.listdir('danmaku/')
        url = 'http://comment.bilibili.com/' + str(cid) + '.xml'
        fn = str(cid) + '.xml'
        if fn not in exist_list:
            time.sleep(2)
            try:
                data = requests.get(url=url, headers=HEADERS, timeout=300)
                file_name = "danmaku/" + str(cid) + '.xml'
                with open(file_name, 'wb') as f:
                    f.write(data.content)
                print('download: '+ fn)
            except:
                print('Error in ' + url)
                traceback.print_exc()