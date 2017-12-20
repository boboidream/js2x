# js2x：简书 to Hexo 格式转换器。

下载「简书」文章内容及图片，并转换为 Hexo 博客可以直接解析的 Markdown 格式。使「简书」文章快捷同步到自己 Hexo 博客。

## 开发初衷
喜欢使用「简书」编辑器写文章，图片也会被压缩到合适大小，而之后又想同时把文章发布到自己 Hexo 作为备份。

每次都要重复，复制粘贴，拖图片，改图片名字，为图片添加七牛前缀等……为逃脱这种苦力劳动，遂开发此小工具。

## 安装

### 1. 直接下载
[boboidream/js2x](https://github.com/boboidream/js2x/tree/master/js2x)

### 2. pip 安装

     pip install js2x

## 使用
在 js2x.py 脚本所在目录运行，将自动下载文章到桌面

    python js2x.py post_url
    # 例如：python js2x.py http://www.jianshu.com/p/7017bfd4dd56

为便于全局调用，可以参考 [OS X 系统下实现python脚本工具在任意目录下直接使用](http://blog.csdn.net/ldstartnow/article/details/53616154)

### 其他选项

可运行 `python js2x.py -h` 查看帮助信息。

    # 指定图片路径前缀，用于图片 CDN。默认图片路径 `./img/日期-index`
    python js2x.py http://www.jianshu.com/p/7017bfd4dd56 -p 'http://image.cdn.com/'

    # 指定下载目录
    python js2x.py http://www.jianshu.com/p/7017bfd4dd56 -o your_path

## 最后

项目地址：https://github.com/boboidream/js2x
反馈地址：https://github.com/boboidream/js2x/issues
