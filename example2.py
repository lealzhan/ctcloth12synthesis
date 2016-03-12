import numpy as np
from utils import *
from createInput import *
from examplars import *
from synthesize import structAwareSynthesize
from indiceio import saveIndicesSimple


def setSpectrumMaps():
    nitem1 = 31
    spectrumMap1 = np.zeros((nitem1, 4), dtype='float32')

    for i in range(0, nitem1):
        if i < 11:
            spectrumMap1[i] = [i+1, 0.850000, 0.850000, 0.010000] # golden yellow
        else:
            spectrumMap1[i] = [i+1, 0.850000, 0.010000, 0.010000] # red

    return [spectrumMap1,]


def setElementaryPatternsAndMaps():
    # twill 1/7
    p1 = np.ones((8, 8), dtype=np.bool)
    generateSatinSimple(p1, [(7, 0),], [-1, 1], False)

    map1 = np.zeros_like(p1, dtype='int32')
    for i in range(0, 8):
        for j in range(0, 8):
            map1[i, j] = 0

    # satin 7/1
    p2 = np.zeros((8, 8), dtype=np.bool)
    generateSatinSimple(p2, [(7,0),(4,1),(1,2)], [-1,3], True)

    map2 = np.zeros_like(p2, dtype='int32')
    for i in range(0, 8):
        for j in range(0, 8):
            map2[i, j] = 0

    return [[p1, p2], [map1, map2]]


if __name__ == '__main__':
    print 'create input ..'
    # set spectrum maps
    spectrumMaps = setSpectrumMaps()

    # set elementary pattern and spectrum map
    V, M = setElementaryPatternsAndMaps()

    # load guiding image and posterize it
    img = plt.imread(r'D:\Dataset\round2\ctcloth12\figure13c_Img.png')
    img = np.dot(img[:,:,:3], [0.299, 0.587, 0.114])    # to grayscale
    I = np.zeros_like(img, dtype='int32')
    I[img <= 0.5] = 0
    I[img > 0.5] = 1
    I = I.swapaxes(0, 1)

    # set pattern mapping
    P = np.array([1, 0], dtype='int32')
    W, tileSpectrumMap = createInputSimple(I, V, M, P)
    print 'create input done.'

    print 'load examplars ..'
    examplars_pattern = loadExamplarsPattern()
    examplars_aabb = loadExamplarsAABB()
    examplars_tz = loadExamplarsTranslateZSimple()
    block_extents = loadBlockExtents()
    examplar_res = loadExamplarResolution()


    res = I.shape
    target_pattern = W
    
    print 'synthesis ..'
    C = structAwareSynthesize(examplars_pattern, target_pattern) 
    print 'synthesis done.'

#    print '(checking)target pattern:'
#    printPattern(target_pattern)
#    target_pattern_syn = parsePattern(examplars_pattern, C)
#    print 'synthesis pattern:'
#    printPattern(target_pattern_syn)

    print 'genereate tileId and tileTransform ..'
    tileId = C[:,:,0]

    base = loadExamplarsBaseTranslateXY()

    tileTranslate = np.zeros((res[0], res[1], 3), dtype='float32')
    for i in range(0, res[0]):
        for j in range(0, res[1]):
            tileTranslate[i,j,0:2] = examplarTranslate(examplars_aabb[C[i,j,0]][:,0:2], examplar_res, C[i,j,1:3]) + base[C[i,j,0]]
            tileTranslate[i,j,2] = examplars_tz[C[i,j,0]]

#    print 'set spectrum maps and generate tile spectrum map ..'
#    spectrumMaps = setSpectrumMaps() 
#    tileSpectrumMap = setTileSpectrumMap(res)

    filename = r'figure13c_round3_1.dat'
    print 'dump indices to file: ', filename
    aabb = np.zeros((2, 3), dtype='float32')
    aabb[0] = [0.0, 0.0, 0.0]
    aabb[1] = [res[0]*block_extents[0], res[1]*block_extents[1], block_extents[2]]
    saveIndicesSimple(filename, res, aabb, tileId, tileTranslate, spectrumMaps, tileSpectrumMap, type='albedo')