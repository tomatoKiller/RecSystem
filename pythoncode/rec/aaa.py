import numpy
import math
import xlwt
import string
def matrix_factorisation(R, P, Q, K, steps=5000, alpha=0.02, beta=0.02):
    Q = Q.T
    for step in xrange(steps):
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    eij = R[i][j] - numpy.dot(P[i,:],Q[:,j])
                    for k in xrange(K):
                        P[i][k] = P[i][k] + alpha * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alpha * (2 * eij * P[i][k] - beta * Q[k][j])
        eR = numpy.dot(P,Q)
        e = 0
        for i in xrange(len(R)):
            for j in xrange(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - numpy.dot(P[i,:],Q[:,j]), 2)
                    for k in xrange(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        if e < 0.001:
            break
    return P, Q.T

import xlrd

data = xlrd.open_workbook("jiayuanUmark.xlsx")
fp = open("rating.txt","w+")
R=[]
table = data.sheets()[1]

for i in range(1,table.nrows):
    temp = []
    for j in range(1,table.ncols):
        
        if((table.cell(i,j).value != "") and (table.cell(i,j).value != " \n")):
            temp.append((int)(table.cell(i,j).value))
        else:
            temp.append(0)
    R.append(temp)

R = numpy.array(R)


numpy.set_printoptions(threshold='nan')
print R

R = R.T

'''
R = [  
     [5,3,0,1,3,0,1],  
     [4,0,0,1,3,0,1],  
     [1,1,0,5,3,0,1],  
     [1,0,0,4,3,0,1],  
     [0,1,5,4,3,0,1],  
    ]

'''


#(rows, cols) = R.shape




N = len(R)
M = len(R[0])

K = 2

P = numpy.random.rand(N,K)
Q = numpy.random.rand(M,K)
 
nP, nQ = matrix_factorisation(R, P, Q, K)
nR = numpy.dot(nP, nQ.T)


count = 0
sumdiff = 0

nR = nR.T
for i in range(M):
    for j in range(N):
        print nR[i][j]




'''
wbk = xlwt.Workbook()

sheet = wbk.add_sheet('boy2girl')


nR = nR.T
R = R.T
for i in range(M):
    for j in range(N):
        if(R[i][j] != 0):
            sumdiff += (R[i][j]-nR[i][j])**2
            count += 1
        else:
            sheet.write(i,j,nR[i][j])

wbk.save("jieguo.xls")

print math.sqrt((sumdiff) / (count * 1.0))
fp.close()
'''
