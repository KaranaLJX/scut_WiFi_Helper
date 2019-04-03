#-*- coding:UTF-8 -*-
import requests
import sys

primes = []
vis = [False for i in range(100000)]
counter = 0

def getPrime(x):
    global counter
    for y in range(2,x):
        if vis[y] == False:
            primes.append(y)
            counter += 1
            print(hex(id(counter)))
        for t in range(0,counter):
            if(y * primes[t] > x):
                break
            else:
                vis[y * primes[t]] = True
                if y % primes[t] == 0:
                    break

r = requests.get("http://www.baidu.com")
print(r.encoding)
print(r.text.encode("iso-8859-1").decode("utf8","ignore"))
