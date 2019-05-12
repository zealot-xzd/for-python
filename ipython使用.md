# %run命令
你可以用%run命令运行所有的Python程序。假设有一个文件ipython_script_test.py
In [14]: %run ipython_script_test.py

# %load
可以使用%load，它将脚本导入到一个代码格中
>>> %load ipython_script_test.py

    def f(x, y, z):
        return (x + y) / z
    a = 5
    b = 6
    c = 7.5

    result = f(a, b, c)

# 从剪贴板执行程序
最简单的方法是使用%paste和%cpaste函数。%paste可以直接运行剪贴板中的代码：
%cpaste功能类似，但会给出一条提示：
使用%cpaste，你可以粘贴任意多的代码再运行。你可能想在运行前，先看看代码。如果粘贴了错误的代码，可以用Ctrl-C中断。

# 魔术命令

## %debug 在出现异常的语句进入调试模式
Python的调试器用tab补全、语法增强、逐行异常追踪增强了pdb。调试代码的最佳时间就是刚刚发生错误。异常发生之后就输入%debug，就启动了调试器，进入抛出异常的堆栈框架：

进入调试模式的方法：
1.run examples/ipython_bug.py 出现异常是输入%debug
2.run -d examples/ipython_bug.py 

## %reset可以清理交互命名空间，或输入和输出缓存。
   %xdel魔术函数可以去除IPython中对一个特别对象的所有引用
   警告：当处理非常大的数据集时，要记住IPython的输入和输出的历史会造成被引用的对象不被垃圾回收（释放内存），
   即使你使用del关键字从交互命名空间删除变量。在这种情况下，小心使用xdel %和%reset可以帮助你避免陷入内存问题。

## %bookmark
    %bookmark 对目录做书签，方面下次使用
    
## 代码计时：%time 和 %timeit
%time method1 = [x for x in strings if x.startswith('foo')]
%time method2 = [x for x in strings if x[:3] == 'foo']

%timeit特别适合分析执行时间短的语句和函数，即使是微秒或纳秒。
这些时间可能看起来毫不重要，但是一个20微秒的函数执行1百万次就比一个5微秒的函数长15秒。
在上一个例子中，我们可以直接比较两个字符串操作，以了解它们的性能特点：

In [565]: x = 'foobar'
In [566]: y = 'foo'
%timeit x.startswith(y)

详细查看%timeit?


## 基础分析：%prun和%run -p
分析代码与代码计时关系很紧密，除了它关注的是“时间花在了哪里”。Python主要的分析工具是cProfile模块，它并不局限于IPython。cProfile会执行一个程序或任意的代码块，并会跟踪每个函数执行的时间。
使用cProfile的通常方式是在命令行中运行一整段程序，输出每个函数的累积时间。假设我们有一个简单的在循环中进行线型代数运算的脚本（计算一系列的100×100矩阵的最大绝对特征值）：
import numpy as np
from numpy.linalg import eigvals

def run_experiment(niter=100):
    K = 100
    results = []
    for _ in xrange(niter):
        mat = np.random.randn(K, K)
        max_eigenvalue = np.abs(eigvals(mat)).max()
        results.append(max_eigenvalue)
    return results
some_results = run_experiment()
print 'Largest one we saw: %s' % np.max(some_results)

你可以用cProfile运行这个脚本，使用下面的命令行：
python -m cProfile cprof_example.py
运行之后，你会发现输出是按函数名排序的。这样要看出谁耗费的时间多有点困难，最好用-s指定排序：
python -m cProfile -s cumulative cprof_example.py

除了在命令行中使用，cProfile也可以在程序中使用，分析任意代码块，而不必运行新进程。Ipython的%prun和%run -p，有便捷的接口实现这个功能。%prun使用类似cProfile的命令行选项，但是可以分析任意Python语句，而不用整个py文件：
In [4]: %prun -l 7 -s cumulative run_experiment()
         4203 function calls in 0.643 seconds

Ordered by: cumulative time
List reduced from 32 to 7 due to restriction <7>
ncalls  tottime  percall  cumtime  percall filename:lineno(function)
     1    0.000    0.000    0.643    0.643 <string>:1(<module>)
     1    0.001    0.001    0.643    0.643 cprof_example.py:4(run_experiment)
   100    0.003    0.000    0.583    0.006 linalg.py:702(eigvals)
   200    0.569    0.003    0.569    0.003 {numpy.linalg.lapack_lite.dgeev}
   100    0.058    0.001    0.058    0.001 {method 'randn'}
   100    0.003    0.000    0.005    0.000 linalg.py:162(_assertFinite)
   200    0.002    0.000    0.002    0.000 {method 'all' of 'numpy.ndarray'}

相似的，调用%run -p -s cumulative cprof_example.py有和命令行相似的作用，只是你不用离开Ipython。


## 逐行分析函数

有些情况下，用%prun（或其它基于cProfile的分析方法）得到的信息，不能获得函数执行时间的整个过程，或者结果过于复杂，加上函数名，很难进行解读。对于这种情况，有一个小库叫做line_profiler（可以通过PyPI或包管理工具获得）。它包含IPython插件，可以启用一个新的魔术函数%lprun，可以对一个函数或多个函数进行逐行分析。你可以通过修改IPython配置（查看IPython文档或本章后面的配置小节）加入下面这行，启用这个插件：

# A list of dotted module names of IPython extensions to load.
c.TerminalIPythonApp.extensions = ['line_profiler']

你还可以运行命令：
%load_ext line_profiler

我的经验是用%prun (cProfile)进行宏观分析，%lprun (line_profiler)做微观分析。最好对这两个工具都了解清楚。

使用%lprun必须要指明函数名的原因是追踪每行的执行时间的损耗过多。追踪无用的函数会显著地改变结果。

# A list of dotted module names of IPython extensions to load.
c.TerminalIPythonApp.extensions = ['line_profiler']

你还可以运行命令：
%load_ext line_profiler

line_profiler也可以在程序中使用（查看完整文档），但是在IPython中使用是最为强大的。假设你有一个带有下面代码的模块prof_mod，做一些NumPy数组操作：
from numpy.random import randn

def add_and_sum(x, y):
    added = x + y
    summed = added.sum(axis=1)
    return summed

def call_function():
    x = randn(1000, 1000)
    y = randn(1000, 1000)
    return add_and_sum(x, y)

如果想了解add_and_sum函数的性能，%prun可以给出下面内容：
In [569]: %run prof_mod

In [570]: x = randn(3000, 3000)

In [571]: y = randn(3000, 3000)

In [572]: %prun add_and_sum(x, y)
         4 function calls in 0.049 seconds
   Ordered by: internal time
   ncalls  tottime  percall  cumtime  percall filename:lineno(function)
        1    0.036    0.036    0.046    0.046 prof_mod.py:3(add_and_sum)
        1    0.009    0.009    0.009    0.009 {method 'sum' of 'numpy.ndarray'}
        1    0.003    0.003    0.049    0.049 <string>:1(<module>)

上面的做法启发性不大。激活了IPython插件line_profiler，新的命令%lprun就能用了。使用中的不同点是，我们必须告诉%lprun要分析的函数是哪个。语法是：
%lprun -f func1 -f func2 statement_to_profile

我们想分析add_and_sum，运行：
In [573]: %lprun -f add_and_sum add_and_sum(x, y)
Timer unit: 1e-06 s
File: prof_mod.py
Function: add_and_sum at line 3
Total time: 0.045936 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           def add_and_sum(x, y):
     4         1        36510  36510.0     79.5      added = x + y
     5         1         9425   9425.0     20.5      summed = added.sum(axis=1)
     6         1            1      1.0      0.0      return summed

这样就容易诠释了。我们分析了和代码语句中一样的函数。看之前的模块代码，我们可以调用call_function并对它和add_and_sum进行分析，得到一个完整的代码性能概括：
In [574]: %lprun -f add_and_sum -f call_function call_function()
Timer unit: 1e-06 s
File: prof_mod.py
Function: add_and_sum at line 3
Total time: 0.005526 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     3                                           def add_and_sum(x, y):
     4         1         4375   4375.0     79.2      added = x + y
     5         1         1149   1149.0     20.8      summed = added.sum(axis=1)
     6         1            2      2.0      0.0      return summed
File: prof_mod.py
Function: call_function at line 8
Total time: 0.121016 s
Line #      Hits         Time  Per Hit   % Time  Line Contents
==============================================================
     8                                           def call_function():
     9         1        57169  57169.0     47.2      x = randn(1000, 1000)
    10         1        58304  58304.0     48.2      y = randn(1000, 1000)
    11         1         5543   5543.0      4.6      return add_and_sum(x, y)

我的经验是用%prun (cProfile)进行宏观分析，%lprun (line_profiler)做微观分析。最好对这两个工具都了解清楚。


