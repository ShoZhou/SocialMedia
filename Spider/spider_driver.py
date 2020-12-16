import re
import os
import pandas as pd
import pymongo
from pandas import DataFrame
import pandas as pd
import matplotlib.pyplot as plt
import random
import time
import likes
import replies
import reposts
from comment_spider import patch_spider_comment
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

myclient = pymongo.MongoClient(IP, port)
mydb = myclient["weibo"]
test_collection = mydb["weibo_topic"]

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

#确定起始日期
time_stamp = unix_time('2020-07-01 00:00:00')
out_like = 'C:/Users/57194/Desktop/社交媒体/spider/mongo/activities/like.json'
out_reply = 'C:/Users/57194/Desktop/社交媒体/spider/mongo/activities/reply.json'
out_repost = 'C:/Users/57194/Desktop/社交媒体/spider/mongo/activities/repost.json'
def get_userslist_and_patchspider():
    userlist = []
    weibolist = []
    cols = test_collection.find({"timestamp": {"$gt": time_stamp}},sort=[("timestamp", pymongo.ASCENDING)])
    for col in cols:
        uid = col["user_id"]
        mid = col["m_id"]
        attitudes_count = col["attitudes_count"]
        comments_count = col["comments_count"]
        reposts_count = col["reposts_count"]
        if (uid not in userlist):
            userlist.append(uid)
        weibolist.append(mid)
        if (attitudes_count>0):
            likes.patch_spider_like(mid,out_like,uid)
        if (comments_count>0):
            # patch_spider_comment(uid, mid)
            replies.patch_spider_comment(mid,1,out_reply,uid)
        if (reposts_count>0):
            reposts.patch_spider_repost(mid,out_repost,uid)
    return userlist,weibolist


if __name__ == '__main__':
    get_userslist_and_patchspider()
