本项目的目标是：
在各种主流的操作系统下，以简单、一致的方式构建各种开源库，以方便在项目中引入并使用。

主流操作系统包括：
Windows 和 Linux 等。

开源库主要以常用、稳定、最新为准，主要包括：
STLPort, Boost, ZLib, OpenSSL 等。

构建：尽可能一键部署，并且部署是从下载、构建、清理、引用等均尽可能自动化完成。

使用技术：以 SCons, Python 等为主，以便可以跨平台使用。

需要考虑的地方：
每个开源库的下载地址均涉及版本等因素，设计时需要考虑；
构建时的中间文件存放位置需要统一考虑；
生成的目标文件存放位置也需要统一考虑，并涉及其他项目的引用问题；
构建目标涉及不同版本，包括动态库、静态库，Debug/Release 版，32/64 bit 版，MT/MD 版，Windows/Linux 版，msvc/gcc 等多钟情况，具体可以参考 Boost 库的做法；

设计考虑：
1、由于模块众多，版本众多，相互的依赖关系也非常复杂，而我们通常都是使用最新的稳定版本为主的，所以构建时不考虑兼容旧版本，一律以构建最新稳定版本为目标。
2、关于各类文件的存储及删除，需要考虑如下这些：下载文件、解压文件、构建的中间文件、目标文件，这四类文件均能配置不同的存储位置及是否保留。
3、文件路径组织方式：lib-prefix/lib_name/toolset/threading/ABI/ver
4、配置参数分为如下这些：全局、模块、命令行，这三类参数以后者优先为原则。
5、

Windows:	http://www.boost.org/doc/libs/1_52_0/more/getting_started/windows.html

Linux:		http://www.boost.org/doc/libs/1_52_0/more/getting_started/unix-variants.html
