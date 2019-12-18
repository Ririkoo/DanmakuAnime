from bilisupport import HEADERS, ACTORINFO, API_BANGUMI, EPISODEINFO, BANGUMIINFO
import time
import datetime
import random
import requests
import traceback
import http.cookiejar
import os

query = EPISODEINFO.find({}, {"cid":1})
cid_list = [result['cid'] for result in query]
# https://api.bilibili.com/x/v2/dm/history?type=1&oid=5421319&date=2019-09-18
# https://api.bilibili.com/x/v2/dm/history?type=1&oid=129995312&date=2019-11-17

if __name__ == "__main__":
    # print(len(exist_list))
    # print(len(cid_list))
    start = datetime.datetime(2019, 7, 1) # From 7.1 to 12.7
    end = datetime.datetime(2019, 12, 7)
    delta = end - start
    time_list = []
    
    for i in range(delta.days+1):
        time_list.append((start + datetime.timedelta(days=i)).strftime("%Y-%m-%d"))

    # cid clannad 
    # cid_list = [52267372,52267430,52267483,52267549,52267604,52267668,52267742,52267813,52267917,52267967,52268008,52268067,52268136,52268220,52268272,52268352,52268401,52268468,52268517,52268570,52268627,52268687,52268823]
    for cid in cid_list:
        exist_list = os.listdir('danmaku_history/')
        fn = str(cid)
        FILE_PATH = "danmaku_history/" + str(cid) + "/"
        if fn not in exist_list:
            if(os.path.exists(FILE_PATH)):
                pass
            else:
                os.makedirs(FILE_PATH) 
            for date in time_list:
                url = 'https://api.bilibili.com/x/v2/dm/history?type=1&oid=' + str(cid) + '&date=' +str(date)
                try:
                    data = requests.get(url=url, headers=HEADERS, timeout=300)
                    file_name = FILE_PATH + str(date) + '.xml'
                    with open(file_name, 'wb') as f:
                        f.write(data.content)
                    print('Download: '+ str(cid))
                    sleep_time = random.randint(1,10)
                    time.sleep(sleep_time)
                except:
                    print('Error in ' + url)
                    traceback.print_exc()
            time.sleep(300)
        # else:
            # print(fn+" exists")
