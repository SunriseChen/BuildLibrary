// Ƕ��Դ�����ʹ�� Boost.Serialization ��
// ���� Boost.Serialization ���Դ�ļ�������ȡ���ʱ������ÿ⣬���Ծ�̬��ʽ���롣

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

// ��� C++11 ��׼�����չ֧��
#include "Extended/shared_ptr_helper.cpp"
