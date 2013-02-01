# 项目的目标 #
在各种主流的操作系统下，以简单、一致的方式构建各种开源库，以方便在项目中引入并使用。

# 主流操作系统 #
主要包括：Windows 和 Linux 等。

# 开源库主要以常用、稳定、最新为准 #
主要包括：STLport, ZLib, OpenSSL, Boost 等。

构建：尽可能一键部署，并且部署是从下载、构建、清理、引用等均尽可能自动化完成。

使用技术：以 Python, SCons 等为主，以便可以跨平台使用。

# 需要考虑的地方 #
每个开源库的下载地址均涉及版本等因素，设计时需要考虑；
构建时的中间文件存放位置需要统一考虑；
生成的目标文件存放位置也需要统一考虑，并涉及其他项目的引用问题；
构建目标涉及不同版本，包括动态库、静态库，Debug/Release 版，32/64 bit 版，MT/MD 版，Windows/Linux 版，msvc/gcc 等多钟情况，具体可以参考 Boost 库的做法；

# 设计考虑 #
1、由于模块众多，版本众多，相互的依赖关系也非常复杂，而我们通常都是使用最新的稳定版本为主的，所以构建时不考虑兼容旧版本，一律以构建最新稳定版本为目标。
2、关于各类文件的存储及删除，需要考虑如下这些：下载文件、解压文件、构建的中间文件、目标文件，这四类文件均能配置不同的存储位置及是否保留。
3、文件路径组织方式：lib-prefix/lib_name/toolset/threading/ABI/ver
4、配置参数分为如下这些：全局、模块、命令行，这三类参数以后者优先为原则。
5、另一个可以参考的是 setuptools 的做法。

Windows:	http://www.boost.org/doc/libs/1_52_0/more/getting_started/windows.html

Linux:		http://www.boost.org/doc/libs/1_52_0/more/getting_started/unix-variants.html

# 参考 setuptools 的做法 #

下载 ez_setup.py 并执行

	...>python ez_setup.py
	Downloading http://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-p
	y2.7.egg
	Processing setuptools-0.6c11-py2.7.egg
	Copying setuptools-0.6c11-py2.7.egg to d:\python27\lib\site-packages
	Adding setuptools 0.6c11 to easy-install.pth file
	Installing easy_install-script.py script to D:\Python27\Scripts
	Installing easy_install.exe script to D:\Python27\Scripts
	Installing easy_install.exe.manifest script to D:\Python27\Scripts
	Installing easy_install-2.7-script.py script to D:\Python27\Scripts
	Installing easy_install-2.7.exe script to D:\Python27\Scripts
	Installing easy_install-2.7.exe.manifest script to D:\Python27\Scripts

	Installed d:\python27\lib\site-packages\setuptools-0.6c11-py2.7.egg
	Processing dependencies for setuptools==0.6c11
	Finished processing dependencies for setuptools==0.6c11

设置 Python 路径：D:\Python27\;D:\Python27\Scripts;

	...>easy_install scons
	Searching for scons
	Reading http://pypi.python.org/simple/scons/
	Reading http://www.scons.org/
	Reading http://www.scons.org
	Best match: scons 2.2.0
	Downloading http://prdownloads.sourceforge.net/scons/scons-2.2.0.zip
	Processing scons-2.2.0.zip
	Running scons-2.2.0\setup.py -q bdist_egg --dist-dir c:\users\admini~1\appdata\l
	ocal\temp\easy_install-f1sibf\scons-2.2.0\egg-dist-tmp-ik8zx1
	zip_safe flag not set; analyzing archive contents...
	scons-2.2.0.SCons.compat.__init__: module references __file__
	scons-2.2.0.SCons.Platform.__init__: module references __path__
	scons-2.2.0.SCons.Script.Main: module references __file__
	scons-2.2.0.SCons.Script.Main: module references __path__
	scons-2.2.0.SCons.Script.SConscript: module references __file__
	scons-2.2.0.SCons.Tool.__init__: module references __path__
	scons-2.2.0.SCons.Tool.packaging.__init__: module references __path__
	Installed SCons library modules into build\bdist.win-amd64\egg\scons-2.2.0
	Installed SCons scripts into build\bdist.win-amd64\egg\EGG-INFO\scripts
	Adding scons 2.2.0 to easy-install.pth file
	Installing scons-2.2.0.bat script to D:\Python27\Scripts
	Installing scons-2.2.0.py script to D:\Python27\Scripts
	Installing scons-time-2.2.0.py script to D:\Python27\Scripts
	Installing scons-time.py script to D:\Python27\Scripts
	Installing scons.bat script to D:\Python27\Scripts
	Installing scons.py script to D:\Python27\Scripts
	Installing sconsign-2.2.0.py script to D:\Python27\Scripts
	Installing sconsign.py script to D:\Python27\Scripts

	Installed d:\python27\lib\site-packages\scons-2.2.0-py2.7.egg
	Processing dependencies for scons
	Finished processing dependencies for scons

# 具体设计 #

## 0. 前提 ##
有 Python 2.7; >= 2.4
有 git, svn, msvc / gcc / ... 并可直接执行（有 path 环境）或通过搜索得到路径

### 1. 主流程 ###
a. 下载 bl_setup.py 到 .../lib/build_lib/ 下面
b. 执行 python bl_setup.py
   自动下载并设置 build_lib
   自动下载并安装 setuptools 和 scons
c. 执行 python build.py lib1 lib2 ...
   自动发现、下载、构建、安装、更新、清理各个 lib，并自动管理依赖关系

### 2. 各 lib 流程 ###
a. 自动发现最新稳定版本或者通过 library_info 指定
b. 比较当前 lib 版本和目标 lib 版本是否一致
c. 下载指定版本的 lib 包
d. 解包、构建
e. 安装、清理

### 3. 设置(settings.py + settings.py.default) ###
a. 全局
b. lib 局部
c. sub_lib 局部
d. 命令行参数
e. 构建参数：
   最新稳定版本 / 指定版本
   静 / 动态库
   release / debug
   i386 / amd64 / ia64
   mt / md
   msvc / gcc / ...
f. 生成的库：
   STLport
   ZLib
   OpenSSL
   Boost

### 4. 库的数据(library_info.py + library_info/*) ###
a. lib 库(library_info/lib_name.py + library_info/lib_name/*)
b. sub_lib 库(library_info/lib_name/sub_lib_name.py + library_info/lib_name/sub_lib_name/*)

### 5. 相关文件 ###
readme.txt
bl_setup.py
settings.py.default
settings.py
library_info.py
library_info/*
build.py

### 6. 关键功能 ###
a. 下载
b. 自动发现程序
c. 自动发现最新稳定版本

