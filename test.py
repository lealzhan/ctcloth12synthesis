import numpy as np
import matplotlib.pyplot as plt
from synthesize import structAwareSynthesize

def loadExamplarPattens():
    N = 8
    w = 5
    h = 5
    S = np.zeros((N, h, w), dtype=np.bool)

    S[0] = S[1] = S[2] = S[3] = False
    for i in range(0, h):
        for j in range(0, w):
            # twill D1
            if not (i + j == 4):
                S[0, i, j] = True

            # twill E1
            if i + j < 3 or (i + j > 4 and i + j < 8):
                S[1, i, j] = True

            # twill F1
            if i + j < 2 or (i + j > 4 and i + j < 7):
                S[2, i, j] = True

            # twill G1
            if i + j == 4:
                S[3, i, j] = True
    
    # satin A2
    S[4] = True
    E = S[4]
    E[0, 2] = E[1, 4] = E[2, 1] = E[3, 3] = E[4, 0] = False

    # satin E2
    S[5] = True
    E = S[5]
    E[0, 1] = E[0, 2] = E[1, 3] = E[1, 4] = E[2, 0] = E[2, 1] = False
    E[3, 2] = E[3, 3] = E[4, 0] = E[4, 4] = False

    # satin F2
    S[6] = False
    E = S[6]
    E[0, 3] = E[0, 4] = E[1, 0] = E[1, 1] = E[2, 2] = E[2, 3] = True
    E[3, 0] = E[3, 4] = E[4, 1] = E[4, 2] = True

    # satin G2
    S[7] = False
    E = S[7]
    E[0, 2] = E[1, 4] = E[2, 1] = E[3, 3] = E[4, 0] = True

    return S


def pp(p):
    '''Print examplar pattern.'''
    h, w = p.shape
    plt.imshow(p, cmap=plt.cm.gray, interpolation='nearest')


def test1():
    S = loadExamplarPattens()
    a = np.random.rand(100).reshape(10,10)
    W = a > 0.5
    
    C = structAwareSynthesize(S, W)
    return C


def generateTwillSimple1(p, starts, up=True, val=True):
    h, w = p.shape

    if up:
        offset = [-1, 1]
    else:
        offset = [1, 1]
    
    for (r, c) in starts:
        rn = r
        cn = c
        while rn >= 0 and rn < h and cn >= 0 and cn < w:
            p[rn, cn] = val
            rn += offset[0]
            cn += offset[1]


def generteTwill1():
    W = np.zeros((16, 16), dtype=np.bool)
    
    # left half
    W[:, 0:8] = True
    starts = [(0,0), (3, 0), (4, 0), (7, 0),
              (8,0), (11, 0), (12, 0), (15, 0),
              (15,1),(15,4),(15,5)]
    generateTwillSimple1(W[:, 0:8], starts, up=True, val=False)
    
    W[:, 8:16] = True
    starts = [(2,0),(3,0),(6,0),(7,0),(10,0),(11,0),(14,0),(15,0),
              (0,1),(0,2),(0,5),(0,6)]
    generateTwillSimple1(W[:, 8:16], starts, up=False, val=False)
    
    return W


def test2():
    S = loadExamplarPattens()
    W = generteTwill1()
    #W = np.tile(W, (1, 3))
    C = structAwareSynthesize(S, W)
    return C


def pbyc(C):
    S = loadExamplarPattens()
    W = np.zeros((C.shape[0], C.shape[1]), dtype=np.bool)
    for r in range(C.shape[0]):
        for c in range(C.shape[1]):
            W[r, c] = S[C[r,c,0],C[r,c,1],C[r,c,2]]

    return W


def indexToTriple(t, k, h, w):
    u = t / (h * w)
    r = (t - u * h * w) / w
    c = t % w
    return (u, r, c)


def tripleToIndex(u, r, c, h=5, w=5):
    return u*h*w + r*w + c


if __name__ == '__main__':
    pass
