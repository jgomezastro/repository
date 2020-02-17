# -*- coding: utf-8 -*-
from Connecter_Component_Label import Connecter_Component_Label
from numpy import zeros
from numpy import unique
from numpy import amin
MAXLAB = 100

class Union(Connecter_Component_Label):    

    def __init__(self):
        self.parent = []
        for _ in range(0, MAXLAB):
            self.parent.append(0)
        self.num_labels = 0;
        
    def union(self, X, Y):
        j = int(X);
        k = int(Y);
        while self.parent[j] != 0:
            j = self.parent[j]
        while self.parent[k] != 0:
            k = self.parent[k]
        if k != j:
            self.parent[k] = j
            
    def find(self, X):
        j = int(X);
        while self.parent[j] != 0:
            j = self.parent[j]
        return j
    
    def prior_neighbors(self, img, i, j):
        neighbors = []
        if i == 0:
            A = img[i, j-1:j]
        elif j == 0:
            A = img[i-1:i, j]
        else:
            A = img[i-1:i+1, j-1:j+2].flatten()[:-2]
        for i in range(A.shape[0]):
            if A[i] == 1:
                neighbors.append(i)
        return neighbors
    
    def get_labels(self, LB, i, j, indices):
        if i == 0:
            labels = LB[i, j-1:j]
        elif j == 0:
            labels = LB[i-1:i+1, j:j+2].flatten()[:-1]
        else:
            labels = LB[i-1:i+1, j-1:j+2].flatten()[:-2]
        neighboring_labels = []
        for index in indices:
            neighboring_labels.append(labels[index])
        return neighboring_labels
    
    def makeLabelsContiguous(self, LB):
        unique_labels = unique(LB)
        self.num_labels = len(unique_labels)
        for i, label in enumerate(unique_labels):
            LB[LB == label] = i
        return LB
        
    def labelComponents(self, B):
        label = 1
        LB = zeros(B.shape)
        MAX_ROWS = B.shape[0]
        MAX_COLS = B.shape[1]
        for i in range(MAX_ROWS):
            for j in range(MAX_COLS):
                if B[i, j] == 1:
                    A = self.prior_neighbors(B, i, j)
                    if len(A) == 0:
                        M = label;
                        label = label + 1
                    else:
                        M = int(amin(self.get_labels(LB, i, j, A)))
                    LB[i, j] = M
                    for X in self.get_labels(LB, i, j, A):
                        if X != M:
                            self.union(M, X)
        for i in range(MAX_ROWS):
            for j in range(MAX_COLS):
                if B[i, j] == 1:
                    LB[i,j] = self.find(LB[i,j])
        LB = self.makeLabelsContiguous(LB)
        return LB
    
    def getNumberOfLabels(self):
        return self.num_labels;
