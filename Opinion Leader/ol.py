import re
import os
import pandas as pd
import pymongo
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import json

myclient = pymongo.MongoClient("10.69.24.137", 27017)
mydb = myclient["weibo"]
weibo_collection = mydb["weibo_topic"]
rt_collection = mydb["weibo_reposts"]
like_collection = mydb["weibo_attitudes"]

milestones = ['2020-07-26', '2020-08-02', '2020-08-04', '2020-08-09', '2020-08-16', '2020-08-22',
              '2020-08-30', '2020-09-05', '2020-09-12', '2020-09-19', '2020-09-26', '2020-10-03', '2020-10-10']

def unix_time(dt):
    #转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    #转换成时间戳
    timestamp = time.mktime(timeArray)
    return timestamp
 
def local_time(timestamp):
    #转换成localtime
    time_local = time.localtime(timestamp)
    #转换成新的时间格式(2016-05-05 20:28:54)
    dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
    return dt

time_start = unix_time('2020-07-01 00:00:00')
def get_weibo_list():
    userlist = []
    weibolist = []
    #分别保存交互数字大于0的微博id
    attitudelist = []
    # commentlist = []
    repostlist = []
    dates_all = []
    cols = weibo_collection.find({"timestamp": {"$gt": time_start}},sort=[("timestamp", pymongo.ASCENDING)])
    for col in cols:
        uid = col["user_id"]
        mid = col["m_id"]
        attitudes_count = col["attitudes_count"]
        comments_count = col["comments_count"]
        reposts_count = col["reposts_count"]
        date = col["date"]
        if(date not in dates_all):
            dates_all.append(date)
        if (uid not in userlist):
            userlist.append(uid)
        weibolist.append(mid)
        if (attitudes_count>0):
            attitudelist.append(mid)
        # if (comments_count>0):
        #     commentlist.append(mid)
        if (reposts_count>0):
            repostlist.append(mid)
    return userlist,weibolist,attitudelist,repostlist,dates_all
    # return userlist,weibolist,attitudelist,commentlist,repostlist

#统计每个里程碑的微博数量
def get_ms_num():
    res=dict.fromkeys(milestones,0)
    cols = weibo_collection.find({"timestamp": {"$gt": time_start}},sort=[("timestamp", pymongo.ASCENDING)])
    for col in cols:
        uid = col["user_id"]
        mid = col["m_id"]
        attitudes_count = col["attitudes_count"]
        comments_count = col["comments_count"]
        reposts_count = col["reposts_count"]
        date = col["date"]
        if date in milestones:
            res[date] = res[date] +1 
    return res

#计算ot
def get_ot_res(dates,userlist):
    ot_res=dict.fromkeys(userlist)
    for key,val in ot_res.items():
        ot_res[key] = dict.fromkeys(dates,0)
    for date in dates:
        cols = weibo_collection.find({"date":date},sort=[("timestamp", pymongo.ASCENDING)])
        for col in cols:
            uid = col["user_id"]
            date = col["date"]
            ot_res[uid][date] = 1 + ot_res[uid][date]
    return ot_res
#计算rt
def get_rt_res(dates,userlist):
    rt_res=dict.fromkeys(userlist)
    for key,val in rt_res.items():
        rt_res[key] = dict.fromkeys(dates,0)
    for date in dates:
        cols = rt_collection.find({"date":date})
        for col in cols:
            uid = col["repost_fromid"]
            date = col["date"]
            try:
                rt_res[uid][date] = 1 + rt_res[uid][date]
            except:
                print("不需要这个uid")
    return rt_res
#计算likes
def get_lk_res(dates,userlist):
    lk_res=dict.fromkeys(userlist)
    for key,val in lk_res.items():
        lk_res[key] = dict.fromkeys(dates,0)
    for date in dates:
        cols = like_collection.find({"date":date})
        for col in cols:
            uid = col["like_fromid"]
            date = col["date"]
            try:
                lk_res[uid][date] = 1 + lk_res[uid][date]
            except:
                print("不需要这个uid")
    return lk_res

def save(dict,filename):
    if isinstance(dict, str):
        dict = eval(dict)
    with open(filename, 'w', encoding='utf-8') as f:
        # f.write(str(dict))  # 直接这样存储的时候，读取时会报错JSONDecodeError，因为json读取需要双引号{"aa":"BB"},python使用的是单引号{'aa':'bb'}
        str_ = json.dumps(dict, ensure_ascii=False) # TODO：dumps 使用单引号''的dict ——> 单引号''变双引号"" + dict变str
        print(type(str_), str_)
        f.write(str_)

#计算每个user的general activity, ga_res[user][date]
def cal_general_activity(ot,rt,ga_res):
    for key in ot:
        for date in ot[key]:
            ga_res[key][date] = ot[key][date] + rt[key][date]
    return ga_res

#计算每个user的average general activity, gi_res[user]
def cal_gi(ga_res,gi_res):
    for user in ga_res:
        sum = 0
        for date in ga_res[user]:
            sum = sum + ga_res[user][date]
        gi_res[user] = sum/len(ga_res[user])
    return gi_res

#计算exclusivity, ex_res[user]
def cal_exclusivity(ga_res,gi_res,ex_res):
    for user in ga_res:
        D = 0
        M = 0
        for date in ga_res[user]:
            if (ga_res[user][date]>gi_res[user]):
                D = D + 1
        for date in milestones:
            if (ga_res[user][date]>gi_res[user]):
                M = M + 1
        ex_res[user] = M/D
    return ex_res

#ms_dict保存每一个里程碑的微博数量
ms_dict = {'2020-07-26': 141, '2020-08-02': 75, '2020-08-04': 33, '2020-08-09': 98,
           '2020-08-16': 109, '2020-08-22': 84, '2020-08-30': 89, '2020-09-05': 55,
           '2020-09-12': 45, '2020-09-19': 34, '2020-09-26': 51, '2020-10-03': 31,
           '2020-10-10': 78}

# mw_dict保存每一个里程碑的权重，值在0-1之间
def milestone_weight(ms_dict,mw_dict):
    max_val = max(ms_dict.values())
    for date in ms_dict:
        mw_dict[date] = ms_dict[date]/max_val
    return mw_dict

#计算每个user的interest
def cal_interest(mw_dict,ga_res,gi_res,mw_sum,interest_dict):
    for user in ga_res:
        #user所有milestone的weight求和，interest in milestones: im
        im = 0
        for date in milestones:
            if (ga_res[user][date]>gi_res[user]):
                im = im + mw_dict[date]
        interest_dict[user] = im/mw_sum
    return interest_dict


# 计算排名，传入exclusivity,interest字典以及权重,结果保存在ranking_dict里。
def cal_ranking(ex_res,interest_dict,weight,ranking_dict):
    for user in ex_res:
        ranking_dict[user] = weight*ex_res[user] + (1-weight)*interest_dict[user]
    return ranking_dict



otfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/ot.txt"
rtfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/rt.txt"
lkfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/lk.txt"

if __name__ == '__main__':
    #记录里程碑每一天的总微博数量
    ms_count = get_ms_num()
    print(ms_count)
    userlist,weibolist,attitudelist,repostlist,dates_all = get_weibo_list()

    ot_res = get_ot_res(dates_all,userlist)
    # save(ot_res,otfile)
    rt_res = get_rt_res(dates_all,userlist)
    # save(rt_res,rtfile)
    # lk_res = get_lk_res(dates_all,userlist)
    # save(lk_res,lkfile)

    #存储(average)general activity结果
    ga_res=dict.fromkeys(userlist)
    for key,val in ga_res.items():
        ga_res[key] = dict.fromkeys(dates_all,0)
    gafile = "C:/Users/57194/Desktop/社交媒体/opinion leader/ga.txt"
    ga_res = cal_general_activity(ot_res,rt_res,ga_res)
    gi_res = dict.fromkeys(userlist,0)
    gi_res = cal_gi(ga_res,gi_res)
    print(gi_res)

    exfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/exclusivity.txt"
    # exclusivity字典，ex_res[user]
    ex_res = dict.fromkeys(userlist,0)
    ex_res = cal_exclusivity(ga_res,gi_res,ex_res)
    print(ex_res)
    save(ex_res,exfile)

    #mw_dict保存每一个milestone的权重，mw_dict[date]
    mw_dict = dict.fromkeys(milestones,0)
    mw_dict = milestone_weight(ms_dict,mw_dict)
    # print(mw_dict)
    # mw_sum存放里程碑权重之和
    mw_sum = sum(ms_dict.values())

    intfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/interest.txt"
    # interest字典，intererst_dict[user]
    interest_dict = dict.fromkeys(userlist,0)
    interest_dict = cal_interest(mw_dict,ga_res,gi_res,mw_sum,interest_dict)
    print(interest_dict)
    save(interest_dict,intfile)

    rankingfile = "C:/Users/57194/Desktop/社交媒体/opinion leader/ranking.txt"
    ranking_dict = dict.fromkeys(userlist,0)
    ranking_dict = cal_ranking(ex_res,interest_dict,0.5,ranking_dict)
    print(ranking_dict)
    save(ranking_dict,rankingfile)

    ressss = sorted(ranking_dict.items(), key = lambda kv:(kv[1], kv[0]),reverse=True)
    print(ressss)