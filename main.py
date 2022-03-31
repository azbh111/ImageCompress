# -*- encoding=utf8 -*-

import shutil
import os
import sys
import funs
import Classes
import argparse


def resetDir(dir):
    if os.path.exists(dir):
        print("重置目录: %s" % (dir,))
        shutil.rmtree(dir)
        funs.mkdirs(dir)
    else:
        print("创建目录: %s" % (dir,))
        funs.mkdirs(dir)


def run(argv):
    parser = argparse.ArgumentParser(description='批量压缩图片')  # 首先创建一个ArgumentParser对象
    parser.add_argument('--pngquality', type=int, default=98, help='png压缩质量[0-100]. 默认 98.')
    parser.add_argument('--jpgquality', type=int, default=80, help='jpe压缩质量[0-100]. 默认 80.')
    parser.add_argument('--keepotherfile', action='store_true',  help='把非图片文件也复制到输出目录.')
    parser.add_argument('--output', help='输出目录，绝对路径')
    parser.add_argument('--fixformat', action='store_true', help='允许修正图片后缀名，使用图片真正的格式作为文件后缀名，意味着文件后缀名可能发生变化')
    parser.add_argument('dir', help='输入目录')
    args = parser.parse_args(argv[1:])
    print(args)
    workDir = sys.path[0]
    print("工作目录: %s" % (workDir,))

    inputDir = args.dir

    if not os.path.exists(inputDir):
        print("目录不存在: %s" % (inputDir,))
        exit()

    if not os.path.isdir(inputDir):
        print("请输入正确的目录: %s" % (inputDir,))
        exit()

    outputDir = None
    if args.output is not None:
        outputDir = args.output
    else:
        outputDir = os.path.join(workDir, "output")

    resetDir(outputDir)

    config = Classes.Config(args.pngquality, args.jpgquality, args.fixformat, args.keepotherfile, inputDir, outputDir)
    funs.run(config, inputDir, outputDir)
    summary: Classes.CompressSummary = funs.summary

    print("压缩完成. 压缩前, 总大小:%s, png数量:%s, jpg数量:%s. 压缩后，总大小:%s, png数量:%s, jpg数量:%s"
          % (summary.inputTotalSize, summary.inputPngCount, summary.inputJpgCount,
             summary.outputTotalSize, summary.outputPngCount, summary.outputJpgCount))
    print("整体压缩率:%.2f"
          % (100 * (1 - summary.outputTotalSize / summary.inputTotalSize)), )


run(sys.argv)


exit()
