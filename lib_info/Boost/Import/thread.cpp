// 嵌入源码编译使用 Boost.Thread 库
// 在此直接引入 Boost.Thread 库的源文件。

#ifdef _WIN32_WINNT
	#undef _WIN32_WINNT
#endif

#ifdef WINVER
	#undef WINVER
#endif

#define BOOST_THREAD_NO_LIB

#include <boost/thread.hpp>

#ifdef _MSC_VER
	namespace boost
	{
		extern "C" void tss_cleanup_implemented() {}
	}
	#include <libs/thread/src/win32/thread.cpp>
	#include <libs/thread/src/win32/tss_dll.cpp>
	#include <libs/thread/src/win32/tss_pe.cpp>
#else
	#include <libs/thread/src/pthread/thread.cpp>
	#include <libs/thread/src/pthread/once.cpp>
#endif
