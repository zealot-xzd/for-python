pip安装与使用详解
96 kaley_ma
0.1 2017.05.04 18:54* 字数 992 阅读 2777评论 1喜欢 10
一、安装pip的几种方式

1、 用脚本安装
1）下载 get-pip.py
wget https://bootstrap.pypa.io/get-pip.py 
2）运行python get-pip.py即可
如果setuptools和wheel没有安装，get-pip.py会安装setuptools和wheel。
Options:
1) - -no-setuptools
不安装setuptools
2) - -no-wheel
不安装wheel
2、 从源码安装
1）从http://pypi.python.org/pypi/pip#downloads下载最新的pip包
2）解压
tar xvf pip-x.x.x.tar.gz 
3)python pip-x.x.x/setup.py install
3、 用easy_install安装
easy_install pip
二、升级pip

1、 在linux和macOS上
pip install -U pip
2、 在windows上
python -m pip install -U pip
三、pip安装python包


I. 安装来源
1、 从pypi安装
$ pip install SomePackage             # 安装最新版本
$ pip install SomePackage==1.0.4     # 指定具体某个版本
$ pip install SomePackage>=1.0.4     # 指定最小版本
通过使用==, >=, <=, >, <来指定一个版本号
2、 安装Requirements files中的所有包
$ pip install -r requirements.txt
文件requirements.txt中列出要用pip安装的所有包。

如果想要将一个python环境中安装的包安装到另一个python环境，可以使用pip freeze
例如：
$ env1/bin/pip freeze > requirements.txt
$ env2/bin/pip install -r requirements.txt
3、从wheels安装
1)直接安装一个已有的wheel格式包
$ pip install SomePackage-1.0-py2.py3-none-any.whl

2)为需求和依赖建立本地的wheels库
$ pip wheel --wheel-dir=/local/wheels -r requirements.txt
上面的命令会将requirements.txt中要安装的包及相关依赖下载到/local/wheels目录供以后使用。

$ pip install --no-index --find-links=/local/wheels -r requirements.txt
安装requirements.txt中需要的python包，仅仅使用本地wheels目录，不用PyPI
4、从VCS安装
例：
pip install -e git+https://git.repo/some_pkg.git#egg=SomeProject     # from git
pip install -e hg+https://hg.repo/some_pkg.git#egg=SomeProject  # from mercurial
pip install -e svn+svn://svn.repo/some_pkg/trunk/#egg=SomeProject   # from svn
pip install -e git+https://git.repo/some_pkg.git@feature#egg=SomeProject  # from a branch
5、 从其他index安装
1）pip install --index-url http://my.package.repo/simple/ SomeProject
2）除了PyPI之外，添加其他的index
pip install --extra-index-url http://my.package.repo/simple SomeProject
6、从本地目录安装
例：
pip install ./downloads/SomeProject-1.0.4.tar.gz

II．安装python模块到指定目录
1、 系统拥有不同版本的python
pip install –-target=<dir> packagename

例：
pip 默认安装python模块到python2.7.13,若为python2.7.5安装模块，可：
pip install --target=/usr/lib/python2.7/site-packages
target指定到python2.7.5的site-packages；
或者使用python2.7.5的pip的绝对路径，例：
/usr/bin/pip2  install packagename
/usr/bin/pip2是我的python2.7.5的pip路径，这样也会把python包安装到python2.7.5的site-packages目录
2、 普通用户没有sudo pip权限，不能向全局python的site-packages安装模块
可以直接安装在本地用户
pip install packagename --user
这样安装后的安装包位于$HOME/.local/lib/python2.7/site-packages
四、卸载python包

1）pip uninstall [options] <package>
2）pip uninstall [options] -r <requirements file>
卸载 requirements file文件中列出的所有包。

Options:
-r, --requirement <file>
-y, --yes  不询问，直接卸载
五、其他功能

1、 升级python包
pip install –U <package>
2、 列出已经安装的包
pip list
3、 显示某个已经安装的python包的信息
pip show  <package>
4、 在PyPI中查找包
pip search [options] <query>
寻找名字或描述中含有query的PyPI包

Options:
-i, --index <url>
Python包索引的URL，默认为 https://pypi.python.org/pypi
5、 下载python包
pip download [options] <package>
例：
$ pip download SomePackage   
下载python包到当前目录
$ pip download -d /tmp SomePackage 
下载python包到指定目录
六、支持

1、 pip对于python版本的支持
pip 支持 CPython versions 2.6, 2.7, 3.3, 3.4, 3.5 和pypy.

2、 pip对于操作系统的支持
Unix/Linux, macOS, and Windows

3、 目前pip最新版9.0.1（目前日期2017.5.9）