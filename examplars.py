import numpy as np


def loadExamplarsPattern():
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


def loadExamplarsAABB():
    aabb = np.zeros((8, 2, 3), dtype='float32')
    
    # twillD1
    aabb[0, 0] = [-0.258638, -0.191017, -0.066634]
    aabb[0, 1] = [ 0.308983,  0.154492,  0.115992]

    # twillE1
    aabb[1, 0] = [-0.253208, -0.072063, -0.139191]
    aabb[1, 1] = [ 0.314413,  0.273445,  0.137216]

    # twillF1
    aabb[2, 0] = [-0.268016, -0.278381, -0.127838]
    aabb[2, 1] = [ 0.299605,  0.067127,  0.128825]

    # twillG1
    aabb[3, 0] = [-0.302073, -0.169299, -0.153992]
    aabb[3, 1] = [ 0.265548,  0.176209,  0.131293]

    # satinA2:
    aabb[4, 0] = [-0.242843, -0.048865, -0.134255]
    aabb[4, 1] = [ 0.324778,  0.296644,  0.112537]

    # satinE2:
    aabb[5, 0] = [-0.279368, -0.124877, -0.113031]
    aabb[5, 1] = [ 0.288253,  0.220632,  0.099210]

    # satinF2:
    aabb[6, 0] = [-0.268509, -0.286772, -0.088351]
    aabb[6, 1] = [ 0.299112,  0.058736,  0.148569]

    # satinG2:
    aabb[7, 0] = [-0.243830, -0.126851, -0.096249]
    aabb[7, 1] = [ 0.323791,  0.218657,  0.130800]

    return aabb


def loadExamplarsBaseTranslateXY():
    xy = np.zeros((8, 2), dtype="float32")
    xy[0] = [0.019781, 0.0]
    xy[1] = [0.019751, 0.0]
    xy[2] = [0.019759, 0.0]
    xy[3] = [0.019716, 0.0]
    xy[4] = xy[5] = xy[6] = xy[7] = [0.0, 0.0]  # satin

    return xy


def loadExamplarsTranslateZSimple():
    z = np.zeros((8,), dtype='float32')

    z[0] = -0.175039
    z[1] = -0.195023
    z[2] = -0.1517
    z[3] = -0.1662
    z[4] = -0.16757
    z[5] = -0.153134
    z[6] = -0.1675
    z[7] = -0.1308

    return z


def loadBlockExtents():
    return [0.11352, 0.0691, 0.338];
    

def loadExamplarResolution():
    return [5, 5]


if __name__ == '__main__':
    pass
