# python转exe
- 常用方法的有三种：
        cx_freeze,py2exe,PyInstaller
- py2exe打包质量不是很好，PyInstaller有点复杂

# [cx_freeze](http://sourceforge.net/projects/cx-freeze/files/)下载

# 安装cx_freeze
1. 检查cx_freeze是否正确安装
>    cmd->cxfreeze -h
2. 如果失败，进入python的安装目录下的Scripts目录，创建cxfreeze.bat文件
   如d:\Python27\Scripts\cxfreeze.bat
   文件内容如下：

        ```
            @echo off

            D:\Python27\python.exe D:\Python27\Scripts\cxfreeze %*
        ```

3. 打包命令：`cxfreeze hello.py --target-dir dist`

# 注意
   只能指定一个要打包的模块，也就是启动模块
   所有.py文件都不能有中文字符，否则会出现编码异常。
   发布后，可执行文件执行路径不能有中文（最好也不要有空格）。
   启动执行的文件中不要有下面这种判断，否则可执行文件执行会没有任何效果。 

  ``` 
   if __name__ == "__main__": 
   main()
  ```

1、将exe放到其他机子上运行，弹出“找不到msvcr100.dll“。手动将”msvcr100.dll“拷贝到dist目录下即可。也许是cxfreeze的bug
2、要去掉exe里的后面黑色控制台窗口就在前面的命令改成
cxfreeze D:\source\game1.0.py(需打包文件路径） --target-dir D:\a（存放exe的目标文件夹路径）--base-name=win32gui

#document
http://cx-freeze.readthedocs.io/en/latest/script.html 


