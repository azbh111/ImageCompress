# -*- encoding=utf8 -*-

import cv2
import numpy as np
import shutil
import os
import sys
from Classes import Config, CompressSummary

workDir = sys.path[0]
pngquantPath = os.path.join(workDir, "pngquant/pngquant")
tmpDir = os.path.join(workDir, "tmp")

summary = CompressSummary()


def help():
    print("用法: sh ImageCompress.sh <inputDir>")


def mkdirs(dir):
    if os.path.exists(dir):
        return
    mkdirs(os.path.dirname(dir))
    os.mkdir(dir, )


def printResult(config: Config, inputPath, outputPath, inputImg, outputImg):
    global inputTotalSize
    global outputTotalSize

    if inputImg.shape[2] == 4:
        inputImgFormat = "png"
    else:
        inputImgFormat = "jpg"

    if outputImg.shape[2] == 4:
        outputImgFormat = "png"
        quality = config.pngquality
    else:
        outputImgFormat = "jpg"
        quality = config.jpgquality

    inputFileFormat = inputPath[inputPath.rindex(".") + 1:]
    outputFileFormat = outputPath[outputPath.rindex(".") + 1:]

    pixelCount = inputImg.shape[0] * inputImg.shape[1]
    inputSize = os.path.getsize(inputPath)
    outputSize = os.path.getsize(outputPath)
    if inputImg.shape[2] == 4:
        summary.inputPngCount += 1
        if outputImg.shape[2] == 4:
            summary.outputPngCount += 1
        else:
            inputImg = inputImg[:, :, 0:3]  # 被压缩成了jpg
            summary.outputJpgCount += 1
    else:
        summary.inputJpgCount += 1
        summary.outputJpgCount += 1

    absImg = np.abs(inputImg.astype(np.int32) - outputImg.astype(np.int32))  # 计算图片失真
    absImg = absImg * absImg
    diff = np.sum(absImg) / (pixelCount)

    summary.inputTotalSize += inputSize
    summary.outputTotalSize += outputSize
    compressRatio = 100 * (1 - outputSize / inputSize)

    print("输入(文件:%s, 格式:%s, 大小:%s, 像素:%s), 输出(后缀名:%s, 格式:%s, 大小:%s, 压缩质量:%s， 压缩率:%.2f, 失真:%.2f, 像素/字节:%.2f) "
          % (config.getRelativeInputPath(inputPath), inputImgFormat, inputSize, pixelCount,
             outputFileFormat, outputImgFormat, outputSize, quality, compressRatio, diff, pixelCount / outputSize))


def handleImage(config: Config, inputDir, outputDir, file, inputImg):
    fileName = file[0:file.rindex(".")]
    inputFileFormat = file[file.rindex(".") + 1:]
    inputPath = os.path.join(inputDir, file)  # 输出目录

    outputFileFormat = inputFileFormat

    if inputImg.shape[2] == 3:  # 输入的是jpg格式图片
        tmpPath = os.path.join(tmpDir, "tmp.jpg")  # 临时文件
        cv2.imwrite(tmpPath, inputImg, (cv2.IMWRITE_JPEG_QUALITY, config.jpgquality))
        if config.fixformat:
            outputFileFormat = "jpg"
        outputPath = os.path.join(outputDir, "%s.%s" % (fileName, outputFileFormat))  # 输出路径
        if os.path.getsize(inputPath) <= os.path.getsize(tmpPath):  # 压缩后没有变小
            shutil.copy(inputPath, outputPath)
        else:
            shutil.move(tmpPath, outputPath)
        printResult(config, inputPath, outputPath, inputImg, cv2.imread(outputPath, cv2.IMREAD_UNCHANGED))
        return
    else:  # 输入的是png图片
        filter = np.where(inputImg[:, :, 3] == 0)
        inputImg[filter] = 0  # 把透明的地方， rgb值设置成0， 净化图片
        tmpPath = os.path.join(tmpDir, "tmp.png")  # 临时文件
        cv2.imwrite(tmpPath, inputImg)  # 把净化后的图片写到临时目录

        tmpPath2 = os.path.join(tmpDir, "tmp2.png")  # 临时文件
        command = "%s --quality 0-%s --force --speed 1 --output %s -- %s" \
                  % (pngquantPath, config.pngquality, tmpPath2, tmpPath)  # pngquant压缩的指令
        os.system(command)  # pngquant压缩

        outputImg = cv2.imread(tmpPath2, cv2.IMREAD_UNCHANGED)
        if outputImg.shape[2] == 3:  # 被压缩成了jpg, 直接使用jpg原生算法进行压缩
            tmpPath2 = os.path.join(tmpDir, "tmp2.jpg")
            cv2.imwrite(tmpPath2, inputImg, (cv2.IMWRITE_JPEG_QUALITY, config.jpgquality))
            outputImg = cv2.imread(tmpPath2, cv2.IMREAD_UNCHANGED)
            if config.fixformat:
                outputFileFormat = "jpg"
        else:
            outputImg[filter] = 0
        outputPath = os.path.join(outputDir, "%s.%s" % (fileName, outputFileFormat))  # 输出路径
        if os.path.getsize(inputPath) <= os.path.getsize(tmpPath2):  # 压缩后没有变小
            shutil.copy(inputPath, outputPath)
        else:
            shutil.copy(tmpPath2, outputPath)

        printResult(config, inputPath, outputPath, inputImg, outputImg)


def copy(inputDir, outputDir, file):
    shutil.copy(os.path.join(inputDir, file), os.path.join(outputDir, file))


def handleFile(config: Config, inputDir, outputDir, file):
    path = os.path.join(inputDir, file)
    if file.endswith(".jpg"):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        handleImage(config, inputDir, outputDir, file, img)
    elif file.endswith(".png"):
        img = cv2.imread(path, cv2.IMREAD_UNCHANGED)
        handleImage(config, inputDir, outputDir, file, img)
    else:
        if config.keepOtherFile:
            copy(inputDir, outputDir, file)


def run(config: Config, inputDir, outputDir):
    mkdirs(outputDir)
    files = os.listdir(inputDir)
    for file in files:
        path = os.path.join(inputDir, file)
        if os.path.isfile(path):
            handleFile(config, inputDir, outputDir, file)
        else:
            run(config, path, os.path.join(outputDir, file))


mkdirs(tmpDir)
