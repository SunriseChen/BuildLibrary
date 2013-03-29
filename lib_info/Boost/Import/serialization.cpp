// 嵌入源码编译使用 Boost.Serialization 库
// 由于 Boost.Serialization 库的源文件难以提取，故必须编译该库，并以静态方式引入。

#ifdef BOOST_SERIALIZATION_NO_LIB
#undef BOOST_SERIALIZATION_NO_LIB
#endif

#ifdef BOOST_ARCHIVE_SOURCE
#undef BOOST_ARCHIVE_SOURCE
#endif

#ifdef BOOST_WARCHIVE_SOURCE
#undef BOOST_WARCHIVE_SOURCE
#endif

#ifdef BOOST_SERIALIZATION_SOURCE
#undef BOOST_SERIALIZATION_SOURCE
#endif

#ifdef BOOST_ALL_NO_LIB
#undef BOOST_ALL_NO_LIB
#include <boost/serialization/config.hpp>
#define BOOST_ALL_NO_LIB
#endif

// 添加 C++11 标准库的扩展支持
#include "Extended/shared_ptr_helper.cpp"
