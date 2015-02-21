# -*- coding: utf-8 -*-
__author__ = 'wu'
import random
import math
import string
import xlwt
import xlrd
from operator import itemgetter
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getdata(filename):
    fp = open(filename,"r")
    data = []
    for i in range(1,5000):
        data.append(fp.readline())
    return data

def SplitData(data, M, k, seed):
    test = {}
    train = {}
    random.seed(seed)
    count = 0
    for line in data:
        if(line==""):
            break
        temp = line.split('::')
        #print temp
        count += 1
        if ( count % M == k+10):
            if(not test.has_key(temp[0])):
                test[temp[0]] = dict()
            test[temp[0]][temp[1]]=string.atof(temp[2].strip('\n'))
        else:
            if(not train.has_key(temp[0])):
                train[temp[0]] = dict()
            train[temp[0]][temp[1]]=string.atof(temp[2].strip('\n'))
    #print train

    return train, test


def Mean(train):
    sumrating = 0
    sumdir = 0
    userscore = dict()
    for u,tt in train.items():
        sumrating = 0
        sumdir = 0
        for i, rating in tt.items():
            sumrating += rating
            sumdir += 1
        userscore[u] = sumrating / (sumdir * 1.0)

    return userscore

def Similarity(train):
    w = dict()
    sumrating = 0
    sumdir = 0
    userscore = dict()
    for u,tt in train.items():
        sumrating = 0
        sumdir = 0
        for i, rating in tt.items():
            sumrating += rating
            sumdir += 1
        userscore[u] = sumrating / (sumdir * 1.0)

    sq = dict()
    for u,tt in train.items():
        for i,rui in tt.items():
            if u not in sq:
                sq[u] = 0
            sq[u] += math.pow((rui - userscore[u]), 2)
        #print u,sq[u]

    demo = 0
    
    for u,tt in train.items():
        w[u] = dict()
        for v, ff in train.items():
            demo = 0
            fenmu1 = 0
            fenmu2 = 0
            for aa in ff.keys():
                if aa in tt.keys():
                    fenmu1 += (train[u][aa]-userscore[u])**2
                    fenmu2 += (train[v][aa]-userscore[u])**2
                    demo += (tt[aa] - userscore[u])*(ff[aa] - userscore[v])

            #w[u][v] = demo / math.sqrt(sq[u] * sq[v])
            if(fenmu2 == 0 or fenmu1 == 0):
                w[u][v] = 0
            else:
                w[u][v] = demo / math.sqrt(fenmu1 * fenmu2)

    return w

def Recomend(train, w, K):
    # build inverse table for item_users
    item_users = dict()
    for u, items in train.items():
        for i in items.keys():
            if i not in item_users:
                item_users[i] = set()
            item_users[i].add(u)


    predict = dict()
    userscore = dict()
    userscore = Mean(train)

    #此处建立相似度矩阵的副本，该副本的wuv值为原值的绝对值，在下面用来排序
    tew = w

    for u,tt in tew.items():
        for v,wuv in tt.items():
            tew[u][v] = math.fabs(wuv)

    temp1 = 0
    temp2 = 0
    for u, tt in train.items():
        predict[u] = dict()
        for i, user in item_users.items():
            if i in tt.keys():
                continue
            cc = 0
            temp1 = 0
            temp2 = 0
            for v, wuv in sorted(tew[u].iteritems(), key=itemgetter(1), reverse=True):
                if v not in user:
                    continue
                cc += 1
                if cc > K:
                    continue
                temp1 += w[u][v] * (train[v][i] - userscore[v])
                temp2 += math.fabs(w[u][v])
            #print temp2,cc
            if(temp2 == 0):
                continue
            predict[u][i] = userscore[u] + temp1 / temp2

    return predict
'''
    sigtem = 0
    count = 0
    for u, tt in test.items():
        for i, rating in tt.items():
            if i not in predict[u].keys():
                continue
            sigtem += (rating - predict[u][i])**2
            count += 1
            #print count
            #print sigtem
            #print u,i,predict[u][i]
    RMSE = math.sqrt(sigtem / (count * 1.0))
    print RMSE
'''

def topN(predict, sex):
    data = xlrd.open_workbook("201321010511.xlsx")
    if(sex == "girl"):
        fp = open("boyTop5.txt","w+")
        table = data.sheets()[0]
    else:
        fp = open("girlTop5.txt","w+")
        table = data.sheets()[1]

    for u, tt in predict.items():
        if(int(string.atof(u)) < 501):
            continue

        ss = ("===============================学生:%s ===============================\n\n") %(u)
        fp.write(ss)
        for i, rat in sorted(predict[u].iteritems(), key=itemgetter(1), reverse=True)[0:5]:
            for j in range(13):
                if j == 2 or j==0:
                    continue
                temp = str(table.cell(int(string.atof(i)),j).value)
                #temp = temp.decode('unicode-escape')
                #fp.write(str((table.cell(int(string.atof(i))+1,j).value)).decode('unicode-escape'))

                fp.write(temp)
                fp.write("\n")
            fp.write("\n\n")
                
        
        #fp.write("\n\n===============================================\n\n\n")

'''
for u,tt in predict.items():
    for i,rat in tt.items():
        print u,i,rat
'''

def boy2girl(predict):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('boy2girl')
    for u, tt  in predict.items():
        for i,rat in tt.items():
            sheet.write(int(string.atof(i)),int(string.atof(u))-500,string.atof(rat))

    wbk.save("jieguo.xls")


def girl2boy(predict):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('girl2boy')
    for u, tt  in predict.items():
        for i,rat in tt.items():
            sheet.write(int(string.atof(i)),int(string.atof(u))-500,string.atof(rat))

    wbk.save("jieguonv.xls")

sex = "boy"

if(sex == "boy"):
    data = getdata("boy2girl.txt")
else:
    data = getdata("girl2boy.txt")
    
data = SplitData(data,8,1,1)
train = data[0]
test = data[1]


w = Similarity(train)

predict = Recomend(train,w ,10 )
topN(predict,sex)
