# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 20:05:24 2022

@author: aldis
"""
#strong teams
# n=int(input())
# res=[]
# for i in range(n):
#     input_text=input()
#     a=int(input_text.split(" ")[0].strip())
#     d=int(input_text.split(" ")[1].strip())
#     x=int(input_text.split(" ")[2].strip())
#     teams=0
#     for i in range(min(a,d)):
#         if a*d == 0: 
#             break
#         a-=1
#         d-=1
#         if x != 0:
#             x -= 1
#             teams +=1
#         elif a != 0 or d != 0:
#             if a > d:
#                 a-=1
#                 teams += 1
#             else:
#                 d-=1
#                 teams+=1
#         # print(a, d, x)
#     res.append(teams)
# for j in res:
#     print(j)

#speed typing
# n=int(input())
# res=[]
# for i in range(n):
#     cor = input()
#     att = input()
#     ind = 0
#     backsp = 0
#     finished = False
#     for char in att:
#         if cor[ind] != char:
#             backsp += 1
#         else:
#             ind += 1
#         if ind == len(cor):
#             finished = True
#             backsp+=len(att)-ind
#             break
#     if not finished:
#         res.append("IMPOSSIBLE")
#     else:
#         res.append(backsp)
# for i in range(len(res)):
#     print("Case#", i+1, ": ", res[i] )

#palindrome
# def pal(t):
#     return t == t[::-1]
# n=int(input())
# res=[]
# for i in range(n):
#     x=input()
#     t=input()
#     for j in range(1, len(t)):
#         if pal(t[j:]):
#             res.append(t[:j][::-1])
#             break
# for i in range(len(res)):
#     print("Case#", i+1, ": ", res[i], sep="")

#pcb
input()
nums=[int(i) for i in input().split()]
l=[]
import math
for i in nums:
    if max(nums)-i != 0:
        l.append(max(max(nums)-i, 1))
gcd=l[0]
for j in l:
    gcd=math.gcd(gcd, j)
# print(l)
# print(gcd)
print(sum(l)//gcd, gcd)