

import cv2
import copy
import numpy as np
def QC_simple(mat, dbzTH = 10, areaTH=20):
    mat1 = copy.copy(mat)
    varMask = np.where(mat1 > dbzTH, 1, 0)
    varMask = varMask.astype(np.uint8)

    ret, img_thre = cv2.threshold(varMask, 0, 255, cv2.THRESH_BINARY)
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(img_thre, connectivity=8)
    mask = np.zeros(varMask.shape, dtype=np.uint8)

    for j in range(1, num_labels):
        if stats[j, cv2.CC_STAT_AREA] >= areaTH:
            mask[labels == j] = 255

    mat1[mask != 255] = 0
    return mat1

def QC_ref(mat, dbzTH = 10, areaTH=20,phase = "QC"):
    from shancx.NN import _loggers
    logger = _loggers(phase=phase)
    for i in range(len(mat)):
        logger.info(f"QC {i}")
        mat[i]=QC_simple(mat[i],dbzTH,areaTH)
    return mat


"""
pre = QC_simple(pre,areaTH=30)   二维灰度
pre = QC_ref(pre,areaTH=30)      三维灰度
"""