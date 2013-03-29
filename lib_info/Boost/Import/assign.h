// 本文件包装了 Boost 的 assign.hpp。
// 应该总是包含此文件，而不要直接使用 assign.hpp。
// Boost.Assign 会产生一些已知无害的编译器警告。
// 在改正以后，我们将删除以下的编译指示，但此头文件仍然存在。

#pragma warning(push)	// 仅禁用此头文件
#pragma warning(disable : 4512)
#include <boost/assign.hpp>
#pragma warning(pop)	// 恢复最初的警告级别
