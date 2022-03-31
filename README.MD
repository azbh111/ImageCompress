# ImageCompress
批量压缩图片

# 安装

1. 安装python3，具体方法自行百度/谷歌
2. 下载项目: git clone https://github.com/azbh111/ImageCompress.git
3. cd ImageCompress
4. pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

# 批量压缩图片
用法: python main.py [-h] [--pngquality PNGQUALITY] [--jpgquality JPGQUALITY] [--keepotherfile] [--output OUTPUT] [--fixformat] dir

批量压缩图片
```
positional arguments:
  dir                   输入目录
optional arguments:
  -h, --help              查看帮助
  --pngquality PNGQUALITY png压缩质量[0-100]. 默认 98.
  --jpgquality JPGQUALITY jpe压缩质量[0-100]. 默认 80.
  --keepotherfile         把非图片文件也复制到输出目录.
  --output OUTPUT         输出目录，绝对路径
  --fixformat             允许修正图片后缀名，使用图片真正的格式作为文件后缀名，意味着文件后缀名可能发生变化
```
# 例子
python main.py --pngquality 80 --jpgquality 50 --fixformat --keepotherfile --output /Users/admin/Desktop/output /Users/admin/Downloads/input

将目录/Users/admin/Downloads/input内的所有图片，进行压缩

将压缩后的图片输出到目录/Users/admin/Desktop/output里

--keepotherfile:  非图片文件也拷贝到输出目录里

--fixformat: 用图片的格式做后缀名，意味着文件后缀名可能发生变化

--jpgquality 50: 如果输出的是jpg格式的图片，图片质量为50

--pngquality 80: 仍哦输出的是png图片，图片质量为80

# 原理
.png后缀的图片，可能是jpg格式的。

同样的，jpg后缀的图片，可能是png格式的。

对于jpg格式的图片，直接使用jpg原生算法进行压缩，压缩率很高。

对于png的图片，使用pngquant进行压缩。

如果pngquant输出的是png格式，就直接使用。

如果pngquant输出的是jpg格式(说明图片完全不透明)，就直接转换为jpg格式的图片，以获得更高的压缩率。