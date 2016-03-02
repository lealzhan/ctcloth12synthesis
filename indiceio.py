import numpy as np
import struct


def saveIndicesSimple(filename, res, aabb, tileId, tileTranslate,
                      spectrumMaps, tileSpectrumMap,
                      glossMap=None, tileGlossMap=None, type='albedo'):
    with open(filename, 'wb') as f:
        f.write(struct.pack('@ii', res[0], res[1]))
        f.write(struct.pack('@3f', aabb[0, 0], aabb[0, 1], aabb[0, 2]))    # aabb_min
        f.write(struct.pack('@3f', aabb[1, 0], aabb[1, 1], aabb[1, 2]))    # aabb_max
        
        # tileId, shape: (res[0], res[1])
        # swap x and y axes for C-style indexing when writing numpy array to bytes, e.g i = y*xres + x
        tileId = tileId.swapaxes(0, 1).astype('int32')
        f.write(tileId.tobytes())

        # tileTranslate, shape: (res[0], res[1], 3)
        tileTranslate = tileTranslate.swapaxes(0, 1).astype('float32')
        f.write(tileTranslate.tobytes())

        if type == 'albedo':
            # spectrumMaps list: (spectrum1, spectrum2, ...)
            # spectrum(i), shape: (nitem, 4), each item reprerents a int-spectrum pair: (int, float, float, float)
            nSpectrums = len(spectrumMaps)
            f.write(struct.pack('@i', nSpectrums))

            for i in range(0, nSpectrums):
                spectrumMap = spectrumMaps[i].astype('float32')
                nitem = spectrumMap.shape[0]
                f.write(struct.pack('@i', nitem))

                for j in range(0, nitem):
                    f.write(struct.pack('@i', int(spectrumMap[j][0])))
                    f.write(struct.pack('@3f', spectrumMap[j][1], spectrumMap[j][2], spectrumMap[j][3]))

            # tileSpectrumMap, shape: (res[0], res[1])
            tileSpectrumMap = tileSpectrumMap.swapaxes(0, 1).astype('int32')
            f.write(tileSpectrumMap.tobytes())
        else:
            pass


if __name__ == '__main__':
    pass
