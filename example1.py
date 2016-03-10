import numpy as np
from utils import *
from examplars import *
from synthesize import structAwareSynthesize
from indiceio import saveIndicesSimple


def setWeavePattern(res):
    # p1: 1/15 satin block
    p1 = np.ones((16, 16), dtype=np.bool)
    starts = [(4, 1), (9, 2), (15, 0)]
    offset = [-1, 3]
    generateSatinSimple(p1, starts, offset, False)

    # p2: 15/1 satin block
    p2 = np.zeros((16, 16), dtype=np.bool)
    starts = [(0, 0), (5, 1), (10, 2), (15, 3)]
    offset = [-1, 3]
    generateSatinSimple(p2, starts, offset, True)

    p1 = np.tile(p1, (4, 4))
    p2 = np.tile(p2, (4, 4))

    # T: [p1 p2
    #     p2 p1]
    T = np.zeros((128, 128), dtype=np.bool)
    T[0:64, 0:64] = T[64:128, 64:128] = p1
    T[0:64, 64:128] = T[64:128, 0:64] = p2

    # tile pattern T up to xres * yres 
    tile_x = (res[0] + 128) / 128
    tile_y = (res[1] + 128) / 128
    P = np.tile(T, (tile_x, tile_y))

    return P[0:res[0], 0:res[1]]


def setSpectrumMaps():
    nitem1 = 31
    spectrumMap1 = np.zeros((nitem1, 4), dtype='float32')

    for i in range(0, nitem1):
        spectrumMap1[i] = [i+1, 0.505882, 0.847059, 0.815686]

    return [spectrumMap1,]


def setTileSpectrumMap(res):
    return np.zeros(res, dtype='int32')


if __name__ == '__main__':
    print 'load examplars ..'
    examplars_pattern = loadExamplarsPattern()
    examplars_aabb = loadExamplarsAABB()
    examplars_tz = loadExamplarsTranslateZSimple()
    block_extents = loadBlockExtents()

    print 'load target pattern ..'
    res = [900, 1500]
    target_pattern = setWeavePattern(res)
    
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
            tileTranslate[i,j,0:2] = examplarTranslate(examplars_aabb[C[i,j,0]][:,0:2], res, C[i,j,1:3]) + base[C[i,j,0]]
            tileTranslate[i,j,2] = examplars_tz[C[i,j,0]]

    print 'set spectrum maps and generate tile spectrum map ..'
    spectrumMaps = setSpectrumMaps() 
    tileSpectrumMap = setTileSpectrumMap(res)

    filename = r'tmp.dat'
    print 'dump indices to file: ', filename
    aabb = np.zeros((2, 3), dtype='float32')
    aabb[0] = [0.0, 0.0, 0.0]
    aabb[1] = [res[0]*block_extents[0], res[1]*block_extents[1], block_extents[2]]
    saveIndicesSimple(filename, res, aabb, tileId, tileTranslate, spectrumMaps, tileSpectrumMap, type='albedo')

    print 'Done.'
