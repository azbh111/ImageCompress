# -*- encoding=utf8 -*-

import cv2
import numpy as np
import shutil
import os


def compressPngquant(inputPath, outputPath, quality: int):
    os.system("./pngquant --quality 0-%s --force --speed 1 --output %s -- %s" % (quality, outputPath, inputPath))


def test(inputPath, quality: int):
    inputImg = cv2.imread(inputPath)
    cv2.imwrite("log/tmp.jpg", inputImg, (cv2.IMWRITE_JPEG_QUALITY, 60))
    compressPngquant("log/tmp.jpg", "log/output.png", quality)
    outputImg = cv2.imread("log/output.png")
    absImg = np.abs(inputImg.astype(np.int8) - outputImg.astype(np.int8))
    absImg = absImg.astype(np.int32)
    absImg = absImg * absImg
    diff = np.sum(absImg) / (inputImg.shape[0] * inputImg.shape[1])
    outputSize = os.path.getsize("log/output.png")
    inputSize = os.path.getsize(inputPath)
    print("quality=%s, diff=%s, inputSize=%s, outputSize=%s, 压缩率=%s" % (quality, diff, inputSize, outputSize, 100*(1-outputSize/inputSize)))


inputPath = "log/18a91fdb-5e52-4ac3-ae22-3532662852c5.zip.png"
test(inputPath, 98)
exit()
