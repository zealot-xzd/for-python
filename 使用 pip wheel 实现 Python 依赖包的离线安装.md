使用 pip wheel 实现 Python 依赖包的离线安装
guoqiao 2015-12-12 4062 阅读
pip python 依赖 安装

有时候, 需要部署 Python 应用的服务器没有网络连接, 这时候, 你就要把整个 Python 应用做成离线安装包.
借助 wheel, 很容易就可以实现.

首先, 你的开发机器上要安装 wheel:

pip install wheel

接下来, 下载依赖包的 wheel 文件:

pip wheel -r requirements.txt


默认情况下, 上述命令会下载 requirements.txt 中每个包的 wheel 包到当前目录的 wheelhouse 文件夹, 包括依赖的依赖.

$ pip wheel --wheel-dir=/local/wheels -r requirements.txt
上面的命令会将requirements.txt中要安装的包及相关依赖下载到/local/wheels目录供以后使用。

现在你可以把这个 wheelhouse 文件夹打包到你的安装包中. 在你的安装脚本中执行:

pip install --use-wheel --no-index --find-links=wheelhouse -r requirements.txt

就可以实现离线安装了. 当然, 还要考虑 pip 以及 wheel 自身的安装.

