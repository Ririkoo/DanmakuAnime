from multiprocessing.dummy import Pool as ThreadPool
from bilisupport import BANGUMIINFO, EXTERNAL_BANGUMI, RECOMMENDINFO
import numpy as np
from bert_serving.client import BertClient
import numpy as np
import pickle
GPU_SERVER = '10.113.63.16'
bc = BertClient(ip=GPU_SERVER)
similarity_matrix = []

def cosin_similarity(x,y):
    return np.dot(x,y)/(np.linalg.norm(x)*np.linalg.norm(y))

def get_tag_vector(tag_str):
    emd_sum = np.zeros(768)
    embed = bc.encode(tag_str)
    for i in embed:
        emd_sum += i
    mean_embed = emd_sum/len(tag_str)
    return mean_embed

def compute_similarity(sid,ex_tag_dict):
    similarity_dict = {}
    for ex_anime in ex_tag_dict:
        if(ex_anime==int(sid) or ex_tag_dict[ex_anime] == []):
            continue
        similarity_dict[ex_anime] = cosin_similarity(get_tag_vector(kyoani_tag_dict[sid]),get_tag_vector(ex_tag_dict[ex_anime]))
    similarity_matrix.append(similarity_dict)
    top_recommend = sorted(similarity_dict.items(), key=lambda item: item[1], reverse=True)[:10]
    print(len(top_recommend))
    recommend_data = [{
        'sid': int(sid),
        'ref_sid': x[0],
        'cos_sim': x[1]
    } for x in top_recommend]
    RECOMMENDINFO.insert_many(recommend_data)

if __name__ == "__main__":
    kyoani_query = BANGUMIINFO.find({},{"sid":1,"tag_name":1})
    ex_query = EXTERNAL_BANGUMI.find({},{"sid":1,"tag_name":1})
    kyoani_tag_dict = {}
    ex_tag_dict = {}
    for i in kyoani_query:
        kyoani_tag_dict[i['sid']] = i['tag_name']
    for i in ex_query:
        ex_tag_dict[i['sid']] = i['tag_name']
    
    for kyoani in kyoani_tag_dict:
        print('Computing',kyoani)
        compute_similarity(kyoani,ex_tag_dict)

    f = open('similarity_matrix.pkl', 'wb')
    pickle.dump(similarity_matrix, f)
    f.close()
