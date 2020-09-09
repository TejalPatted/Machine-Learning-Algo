# -*- coding: utf-8 -*-
"""
Created on Thu Sep  3 20:53:32 2020

@author: Tejal
"""

from sklearn import datasets
import numpy as np

def get_k_neighbors(k,train_X,test_pt):
    dist = np.sum((train_X-test_pt)**2,axis=1)**0.5
    neig_index = dist.argsort()[:k]
    return neig_index
    
def get_accuracy(test_Y,prediction):
    corr=0
    wrong=0
    for act,pred in zip(test_Y,prediction):
        if act==pred:
            corr+=1
        else:
            wrong+=1
    print('correct = %d'%corr)
    print('wrong = %d'%wrong)

def predict(train_X,train_Y,test_X,test_Y,k,label_set):
    prediction =[]
    for test_pt in test_X:
        max_label = 'NA'
        neig_index = get_k_neighbors(k,train_X,test_pt)
        neigh_label = train_Y[neig_index]
        for l in label_set:
            if(np.count_nonzero(neigh_label== l) > max_label or max_label=='NA'):
                max_label=l
        prediction.append(max_label)
    get_accuracy(test_Y,prediction)
        
if __name__=='__main__':
    
    d = datasets.load_iris()
    data=d['data']
    label=d['target']
    
    k = 3
    index = np.random.choice(data.shape[0], 10, replace=False)
    test_X = np.array([data[i] for i in index])
    test_Y = np.array([label[i] for i in index])
    train_X = np.delete(data,index,axis=0)
    train_Y = np.delete(label,index,axis=0)
    label_set = list(set(train_Y.tolist()))
    predict(train_X,train_Y,test_X,test_Y,k,label_set)
    



        

    
    