from pymongo import MongoClient

DATABASE = MongoClient('mongodb://127.0.0.1:27017/', connect=False)

DANMAKULIST = DATABASE['bilibili']['DanmakuData']
BANGUMIINFO = DATABASE['bilibili']['BangumiInfo']
ACTORINFO = DATABASE['bilibili']['ActorInfo']
EPISODEINFO = DATABASE['bilibili']['EpisodeInfo']
DANMAKURES = DATABASE['bilibili']['DanmakuRes']
OTHERINFO = DATABASE['bilibili']['OtherInfo']
EXTERNAL_BANGUMI = DATABASE['bilibili']['ExBangumiInfo']
RECOMMENDINFO = DATABASE['bilibili']['RecBangumi']


CID_DANMAKU = 'http://comment.bilibili.com/{0}.xml'
API_BANGUMI = 'https://www.biliplus.com/api/bangumi?season='

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
    'Cookie': 'SESSDATA=; \
    LIVE_BUVID=; \
    LIVE_BUVID__ckMd5=; \
    DedeUserID=; \
    DedeUserID__ckMd5='
    }

