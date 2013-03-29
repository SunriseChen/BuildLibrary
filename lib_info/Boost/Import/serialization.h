// 本文件包装了 Boost 的 Serialization 库的头文件。
// 应该总是包含此文件，而不要直接使用 Serialization 库的头文件。
// Boost.Serialization 会产生一些已知无害的编译器警告。
// 在改正以后，我们将删除以下的编译指示，但此头文件仍然存在。

// 添加 C++11 标准库的扩展支持
#include "Extended/unique_ptr.hpp"
#include "Extended/shared_ptr_helper.hpp"
#include "Extended/shared_ptr.hpp"

#pragma warning(push)	// 仅禁用此头文件
#pragma warning(disable : 4244 4310)
#include <boost/archive/binary_iarchive.hpp>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
// 由于宽字符版本的静态库暂时不知道如何引入，所以暂时无法使用宽字符版本相关的功能。
//#include <boost/archive/text_wiarchive.hpp>
//#include <boost/archive/text_woarchive.hpp>
//#include <boost/archive/xml_wiarchive.hpp>
//#include <boost/archive/xml_woarchive.hpp>
#pragma warning(pop)	// 恢复最初的警告级别

// 对于各种 archive，提供具体的实例化
#ifndef BOOST_SERIALIZATION_ARCHIVE_INSTANTIATE_FREE
#define BOOST_SERIALIZATION_ARCHIVE_INSTANTIATE_FREE(T)										\
	template void serialize<binary_iarchive>(binary_iarchive &, T &, const unsigned int);	\
	template void serialize<binary_oarchive>(binary_oarchive &, T &, const unsigned int);	\
	template void serialize<text_iarchive>(text_iarchive &, T &, const unsigned int);		\
	template void serialize<text_oarchive>(text_oarchive &, T &, const unsigned int);		\
	template void serialize<xml_iarchive>(xml_iarchive &, T &, const unsigned int);			\
	template void serialize<xml_oarchive>(xml_oarchive &, T &, const unsigned int);
#endif
#ifndef BOOST_SERIALIZATION_ARCHIVE_INSTANTIATE_MEMBER
#define BOOST_SERIALIZATION_ARCHIVE_INSTANTIATE_MEMBER(T)									\
	template void T::serialize<binary_iarchive>(binary_iarchive &, const unsigned int);		\
	template void T::serialize<binary_oarchive>(binary_oarchive &, const unsigned int);		\
	template void T::serialize<text_iarchive>(text_iarchive &, const unsigned int);			\
	template void T::serialize<text_oarchive>(text_oarchive &, const unsigned int);			\
	template void T::serialize<xml_iarchive>(xml_iarchive &, const unsigned int);			\
	template void T::serialize<xml_oarchive>(xml_oarchive &, const unsigned int);
#endif
