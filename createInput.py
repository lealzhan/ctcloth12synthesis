import numpy as np


def createInputSimple(I, V, M, P):
    '''I: posterized image with n different integers([0,n)) repsenting pixel color
       V: elementary pattern, [V1, V2, ... Vn]
       M: warp and weft ID maps of elementary pattern, that is, spectrum map id
       P: mapping, assigned a weave pattern to each of the colors, one dimension numpy array
    '''
    h, w = I.shape
    V_n = len(V)
    M_n = len(M)

    # tile V and M up to resolution of I
    V_tile = np.zeros((V_n, h, w), dtype=np.bool)
    for i in range(0, V_n):
        V_i = V[i]
        h_i, w_i = V_i.shape
        V_tile[i] = np.tile(V_i, ((h+h_i)/h_i, (w+w_i)/w_i))[0:h, 0:w]

    M_tile = np.zeros((M_n, h, w), dtype='int32')
    for i in range(0, M_n):
        M_i = M[i]
        h_i, w_i = M_i.shape
        M_tile[i] = np.tile(M_i, ((h+h_i)/h_i, (w+w_i)/w_i))[0:h, 0:w]

    W = np.zeros_like(I, dtype=np.bool)
    tileSpectrum = np.zeros_like(I, dtype='int32')

    for i in range(0, I.shape[0]):
        for j in range(0, I.shape[1]):
            id = P[I(i, j)]
            W[i, j] = V_tile[id, i, j]
            tileSpectrum = M_tile[id, i, j]
    
    return (W, tileSpectrum)


if __name__ == '__main__':
    pass
