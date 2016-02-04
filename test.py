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
    W = S[2].copy()
    
    C = structAwareSynthesize(S, W)
    return C


def indexToTriple(t, k, h, w):
    u = t / (h * w)
    r = (t - u * h * w) / w
    c = t % w
    return (u, r, c)


def tripleToIndex(u, r, c, h, w):
    return u*h*w + r*w + c


if __name__ == '__main__':
    pass
