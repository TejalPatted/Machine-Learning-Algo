# -*- coding: utf-8 -*-
"""
Created on Fri Jan 27 18:39:01 2017

@author: Tejal
"""

import pandas as pd
import math
depth = 0
treeList = []
dec_out = []

def calEntropy1(data,dec_field):
    ent_array = []
    cnt = 0
    total = 0.0
    entropy = 0.0
    val = set(data[dec_field])
    for i in val:
        cnt = len(data[data[dec_field]==i])
        if cnt != 0:
            ent_array.append(cnt)
            total = total + cnt
    for i in ent_array:                  
        entropy += i/total * math.log(total/i,2)
    return(entropy)

def find_subset(data,value,field,dec_field):
    return_val ={}
    new_df = pd.DataFrame()
    for i in range(len(data)):
# if the value of row for field is as desired, add row to new DF        
        if data.iat[i,field]==value:
            new_df = new_df.append(data.ix[i],ignore_index=True)
            
# Rearrage columns as in original data            
    new_df= new_df[list(data.columns)]
    return_val['Frame']= new_df
    return_val['Entropy'] = calEntropy1(new_df,dec_field)
    return(return_val)

def attr_selection(data,dec_field):
    subset1 = {}
    base_entropy = calEntropy1(data,data.columns[data.shape[1]-1])
    attr_entropy = 0.0
    inf_gain = 0.0
    max_gain = 0.0
    sel_attr = 'N/A'

# Iterate on all attributes present except 'Enjoy' in data to check the entropy. Hence len -1
    for i in range(0,len(data.columns)-2):
       # print data.columns[i]
        for j in set(data[data.columns[i]]):
            subset1 = find_subset(data,j,i,dec_field)
            attr_entropy += len(subset1['Frame'])/float(len(data))*subset1['Entropy']        
        inf_gain = base_entropy - attr_entropy
        attr_entropy = 0.0
        if(inf_gain > max_gain):
            max_gain = inf_gain
            sel_attr = data.columns[i]
    return(sel_attr)

# if pure class could not be reached and no attributes are remaining to split further    
def majority(data,dec_field):
    val = set(list(data[dec_field]))
    l = []
    d={}
    for i in val:
        d[i]=list(data[dec_field]).count(i)
        l.append(list(data[dec_field]).count(i))
    l.sort()
    if l[0]==l[-1]:
        return('Tie')
    else:
        return(max(d,key=d.get))
    
def tree(data,labels,depth):
    global treeList
    
    dec_attr_val = []   
    new_df = pd.DataFrame()
  
    for i in range(0,len(data)):
        dec_attr_val.append(data.iat[i,data.shape[1]-1])

# Check if it is a pure class ie all values in decision attribute are equal         
    if dec_attr_val.count(dec_attr_val[0]) == len(dec_attr_val):
        dec_out.append(dec_attr_val[0])
        return dec_attr_val[0]

# After all attributes are used for splitting
    if len(labels) == 1:
        dec = majority(data,data.columns[data.shape[1]-1])
        dec_out.append(dec)
        return dec

# If algo hasnt reached termination point

# Select the attribute for splitting
    bestFeatLabel = attr_selection(data,data.columns[data.shape[1]-1])
    if bestFeatLabel == 'N/A':
        return majority(data,data.columns[data.shape[1]-1])

# Insert the node into treeList for printing
    depth+=1
    treeList.append(str(depth)+'-'+bestFeatLabel)

    bestFeat = list(data.columns).index(bestFeatLabel)
    theTree = {bestFeatLabel:{}}
    del(labels[labels.index(bestFeatLabel)])
    uniqueVals = set(data[bestFeatLabel])

    for value in uniqueVals:
        subLabels = labels[:]
        new_df = find_subset(data,value,bestFeat,data.columns[data.shape[1]-1])['Frame']
        
        theTree[bestFeatLabel][value] = tree(new_df,subLabels,depth)
    return theTree

# Print tree hierarchy    
def printTree(): 
    i = 1
    item_count = len(treeList)+1      
    while i <= item_count:  
        print('\n\nLevel%d-'%i)
        for j in treeList:
            if(j.startswith(str(i)+'-')):
                print ('%s'%j[2:]),
                item_count-=1
        i+=1
    print ("\n\nDecision values")
    for j in dec_out:
        print j,
        
    
file_path = raw_input("Enter training file path")        
data = pd.read_csv(file_path)
Tr = tree(data,list(data.columns[0:data.shape[1]-1]),depth)
print(Tr)
printTree()
