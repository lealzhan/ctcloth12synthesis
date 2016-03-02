import numpy as np
import matplotlib.pyplot as plt


def generateSatinSimple(p, starts, offset, val=True):
    h, w = p.shape
    
    for (r, c) in starts:
        rn = r
        cn = c
        while rn >= 0 and rn < h and cn >= 0 and cn < w:
            p[rn, cn] = val
            rn += offset[0]
            cn += offset[1]


def examplarTranslate(aabb, res, idx):
    extents = aabb[1,:] - aabb[0,:]
    return aabb[0,:] + (idx*1.0)/res * extents;


def printPattern(p):
    h, w = p.shape
    plt.imshow(p, cmap=plt.cm.gray, interpolation='nearest')


def parsePattern(S, C):
    W = np.zeros((C.shape[0], C.shape[1]), dtype=np.bool)
    for r in range(C.shape[0]):
        for c in range(C.shape[1]):
            W[r, c] = S[C[r,c,0],C[r,c,1],C[r,c,2]]

    return W


if __name__ == '__main__':
    pass
