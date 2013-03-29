// 本文件包装了 Boost 的 Spirit 库的头文件。
// 应该总是包含此文件，而不要直接使用 Spirit 库的头文件。
// Boost.Spirit 会产生一些已知无害的编译器警告。
// 在改正以后，我们将删除以下的编译指示，但此头文件仍然存在。

#pragma warning(push)	// 仅禁用此头文件
#pragma warning(disable : 4189 4512 4819)
#include <boost/spirit/include/classic.hpp> 
#include <boost/spirit/include/karma.hpp> 
#include <boost/spirit/include/lex.hpp> 
#include <boost/spirit/include/phoenix.hpp> 
#include <boost/spirit/include/qi.hpp> 
#include <boost/spirit/include/support.hpp> 
#pragma warning(pop)	// 恢复最初的警告级别
