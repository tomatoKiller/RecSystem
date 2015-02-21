# -*- coding: utf-8 -*-
__author__ = 'wu'
import random
import math
from operator import itemgetter
fp = open("rating.txt","r")
data = []
for i in range(1,100000):
    data.append(fp.readline())

def SplitData(data, M, k, seed):
    test = {}
    train = {}
    random.seed(seed)

    for line in data:
        temp = line.split('::')
       #print temp
        if ( random.randint(0,M) == k):
            if(not test.has_key(temp[0])):
                test[temp[0]] = []
            test[temp[0]].append(temp[1])
        else:
             if(not train.has_key(temp[0])):
                 train[temp[0]] = []
             train[temp[0]].append(temp[1])
    #print train, test
    return train, test


def Recall(train, test, N):
    hit = 0
    all_r = 0
    tu = []
    for user in train.keys():
        if(user in test):
            tu = test[user]
            rank = GetRecommendation(user,N)
            for (item, pui) in rank.items():
                if item in tu:
                    hit += 1
            all_r += len(tu)
    return hit / (all_r * 1.0)

def Precision(train, test, N):
    hit = 0
    all = 0
    for user in train.keys():
        if user in test:
            tu = test[user]
            rank = GetRecommendation(user,N)
            for item, pui in rank.items():
                if item in tu:
                    hit += 1
            all += N
    return hit / (all * 1.0)

def Coverage(train, test, N):
    recommend_items = set()
    all_items =set()
    for user in train.keys():
        for item in train[user]:
            all_items.add(item)
        rank = GetRecommendation(user,N)
        #print rank
        for item, pui in rank.items():
            recommend_items.add(item)

    return len(recommend_items) / (len(all_items) * 1.0)


def Popularity(train, test, N):
    item_popularity = dict()
    for user, items in train.items():
        for item in items:
            if item not in item_popularity:
                item_popularity[item] = 0
            item_popularity[item] += 1
    ret = 0
    n = 0
    for user in train.keys():
        rank = GetRecommendation(user, N)
        for item, pui in rank.items():
            ret += math.log(1 + item_popularity[item])
            n += 1
            
    ret /= n * 1.0
    return ret

'''
def UserSimilarity(train):
# build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items:
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    #calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            if u not in N:
                N[u] = 0
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                if u not in C:
                    C[u] = dict()
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1
    #calculate finial similarity matrix W
    W = dict()
    for u, related_users in C.items():
        if u not in W:
            W[u] = {}
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W
'''

def UserSimilarity(train):
# build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items:
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)

    #calculate co-rated items between users
    C = dict()
    N = dict()
    for i, users in item_users.items():
        for u in users:
            if u not in N:
                N[u] = 0
            N[u] += 1
            for v in users:
                if u == v:
                    continue
                if u not in C:
                    C[u] = dict()
                if v not in C[u]:
                    C[u][v] = 0
                C[u][v] += 1/math.log(1+len(users))
    #calculate finial similarity matrix W
    W = dict()
    for u, related_users in C.items():
        if u not in W:
            W[u] = {}
        for v, cuv in related_users.items():
            W[u][v] = cuv / math.sqrt(N[u] * N[v])
    return W

def ItemSimilarity(train):
    #calculate co-rated users between items
    C = dict()
    N = dict()
    for u, items in train.items():
        for i in items:
            N[i] += 1
            for j in items:
                if i == j:
                    continue
                if i not in C:
                    C[i] = dict()
                if j not in C[u]:
                    C[i][j] = 0
                C[i][j] += 1
    #calculate finial similarity matrix W
    W = dict()
    for i,related_items in C.items():
        for j, cij in related_items.items():
            W[i][j] = cij / math.sqrt(N[i] * N[j])
    return W

def Recommendation(train, user_id, W, K):
    rank = dict()
    ru = train[user_id]
    for i in ru:   #此处未考虑评分
        for j, wj in sorted(W[i].items(), key=itemgetter(1), reverse=True)[0:K]:
            if j in ru:
                continue
            rank[j] += wj
    return rank

def Recommend(user, train, W):
    rank = dict()
    global N
    temp = set()
    count = 0
    interacted_items = train[user]
    for v, wuv in sorted(W[user].iteritems(), key=itemgetter(1), reverse=True)[0:10]:
        for i in train[v]:
            if i in interacted_items:
                #we should filter items user interacted before
                continue
            count += 1
            if(count > N):
                break
            if(not rank.has_key(i)):
                rank[i] = 0
            rank[i] += wuv * 1.0
            
    return rank

def GetRecommendation(user, N):
    global train, W
    return Recommend(user, train, W)

N = 100
data = SplitData(data,8,1,1)
train = data[0]
test = data[1]
W= UserSimilarity(train)

print Recall(train,test,N)
print Precision(train,test,N)
print Coverage(train,test,N)
print Popularity(train,test,N)
