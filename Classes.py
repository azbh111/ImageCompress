# -*- encoding=utf8 -*-

import cv2
import numpy as np
import shutil
import os
import sys


class Config(object):
    pngquality = None
    jpgquality = None
    fixformat = None
    inputDir = None
    outputDir = None
    keepOtherFile = None
    def __init__(self, pngquality, jpgquality, fixformat, keepOtherFile, inputDir, outputDir):
        self.pngquality = pngquality
        self.jpgquality = jpgquality
        self.fixformat = fixformat
        self.keepOtherFile = keepOtherFile
        inputDir = os.path.join(inputDir, "a")  # 给目录结尾拼接上分隔符
        inputDir = inputDir[0:len(inputDir) - 1]
        self.inputDir = inputDir
        outputDir = os.path.join(outputDir, "a")
        outputDir = outputDir[0:len(outputDir) - 1]
        self.outputDir = outputDir

    def getRelativeInputPath(self, path):
        return path[len(self.inputDir):]

    def getRelativeOutputPath(self, path):
        return path[len(self.outputDir):]


class CompressSummary(object):
    inputTotalSize = 0  # 压缩前总大小
    outputTotalSize = 0  # 压缩后总大小
    inputPngCount = 0  # 压缩前png个数
    inputJpgCount = 0  # 压缩前jpg个数
    outputPngCount = 0  # 压缩后png个数
    outputJpgCount = 0  # 压缩后jpg个数
