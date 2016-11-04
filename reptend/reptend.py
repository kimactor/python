# -*- coding: cp936 -*-
#����ѭ�����㷨
#winxos 2012-06-25

import math
import rho #������������ֽ�

#������ֵݹ���������
#����nΪ�����б�,��������[1,2]
#�����['00', '01', '02', '10', '11', '12']
def combination(n):
    if len(n)==1:
        return range(0,n[0]+1)
    ret=[] #�����Ͻ��
    for i in range(0,n[0]+1):
        for li in combination(n[1:]):
            ret.append(str(i)+str(li))
    return ret

#�����������Ӽ�����Ŀ���������ȫ������
#���� 36=2^2 x 3^2
#�������Ǹ���ָ��[2 2]��ȫ�������������������õ�
def allfactors(c,n):
    if len(n)==1:
        ret=[]
        for i in range(0,n[0]+1):
            ret.append(c[0]**i)
        return ret
    ret=[] #ÿ�ε��������������б�
    for i in range(0,n[0]+1): #��c^a�η���aΪ0-n��Χ�ڵ�����
        for li in allfactors(c[1:],n[1:]):
            ret.append(c[0]**i*li) #�����б��С
    ret.sort()
    return ret

# from http://www.haogongju.net/art/750012
# by wander@xjtu copyleft
def montgomery(n,p,m):
    if (p==0):
        return 1
    k=montgomery(n,p>>1,m)
    if (p & 0x01 == 0):
        return k*k % m
    else:
         return n*k*k % m

#С����׼��
#http://caterpillar.onlyfun.net/Gossip/AlgorithmGossip/GCDPNumber.htm
primes=[] #С������
startnum=10001
def prepare_factor():
    max=startnum-1
    prime = [1] * max
    for i in range(2, int(math.sqrt(max))):
        if prime[i] == 1:
            for j in range(2 * i, max):
                if j % i == 0:
                    prime[j] = 0
    global primes
    primes = [i for i in range(2, max) if prime[i] == 1]
    
#���ӷֽ�,�ȹ���С��������
def factor(num):
    if len(primes)==0:
        prepare_factor()
        print "initial small primes:",len(primes)
    list = []
    i = 0
    while i<len(primes):
        if num<primes[i]:break
        if num % primes[i] == 0:
            list.append(primes[i])
            num //= primes[i]
        else:
            i += 1
    if num<startnum: #û�д����ӣ�����
        return list
    upnum=math.sqrt(num)+1
    i=startnum #��С�����Ӷ�Ҫ��
    while i<=upnum:
        if num<i:break
        if num%i==0:
            list.append(i)
            num//=i
        else:
            i+=2
    if num!=1:
        list.append(num)
    return list
def isprime(num):
    if len(factor(num))==1:return True
    return False
#�������ӱ�ת���ɵ�����ָ����
def normfactor(li):
    dict={}
    for i in li:
        if dict.has_key(i):
            dict[i]+=1
        else:
            dict[i]=1
    l_c=[]
    l_e=[]
    for key in dict:
        l_c.append(key)
        l_e.append(dict[key])
    return (l_c,l_e)
#��ѭ���ڳ�
def reptend(n):
    #if isprime(n)==False:return -1
    maxr=n-1
    lc,le=normfactor(rho.factor(maxr)) #����rho�ļ��е����ӷֽ�
    lif= allfactors(lc,le)#���ظ�����ȫ������
    for i in lif:
        if montgomery(10,i,n)==1:
            return i
#������Ѱ�ң�ȫ����ѭ��������)
def test():
    startbit=40
    searchw=3
    i=10**startbit+1 #���ҷ�Χ��ʼ
    while i<10**startbit+10**searchw:
        if rho.rabin_miller(i): #���Բ���
            print i,":",reptend(i)
        i+=2
    print ""
#main 
if __name__ == '__main__':
    from timeit import Timer
    t=Timer("test()","from __main__ import test")
    print t.timeit(1) #��ʱ
    
    
