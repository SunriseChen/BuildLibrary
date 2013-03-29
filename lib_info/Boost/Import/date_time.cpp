// 嵌入源码编译使用 Boost.DateTime 库
// 在此直接引入 Boost.DateTime 库的源文件。
// Boost.DateTime 会产生一些已知无害的编译器警告。
// 在改正以后，我们将删除以下的编译指示，但此文件仍然存在。

#define BOOST_DATE_TIME_SOURCE

#pragma warning(push)	// 仅禁用此文件
#pragma warning(disable : 4100)
#include <libs/date_time/src/gregorian/greg_names.hpp>
#include <libs/date_time/src/gregorian/date_generators.cpp>
#include <libs/date_time/src/gregorian/greg_month.cpp>
#include <libs/date_time/src/gregorian/greg_weekday.cpp>
#include <libs/date_time/src/gregorian/gregorian_types.cpp>
#pragma warning(pop)	// 恢复最初的警告级别
