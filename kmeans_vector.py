# -*- coding: utf-8 -*-
"""
Created on Tue Sep  1 23:16:47 2020

@author: Tejal
"""
import pandas as pd
import numpy as np


def find_center(clus):
    for i in range(k):
        k_mean[i]=np.average(clus[i],axis=0)
    return k_mean
    

def calc_dist(k_mean,data,k):
    clus={}
    for i in range(k):
        clus[i]=[]
    for data_pt in data:
        dist =[]
        for k in k_mean:
            dist.append(sum((k-data_pt)**2)**0.5)
        clus[dist.index(min(dist))].append(data_pt)
    return clus

df = pd.read_csv('C:\Users\Tejal\Documents\Tejal\College\INF552\Clustering\clusters.txt',
                   encoding='utf-8',sep=',',names=['x','y'])
# Convert to numpy
data = df.values

k=3
k_mean =[]

# Initialize initial centroids
for i in range(k):
    k_mean.append(data[i])
    

for iter in range(50):
    clus = calc_dist(k_mean,data,k)
    k_mean = find_center(clus)
print(k_mean)