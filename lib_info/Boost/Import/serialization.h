// ���ļ���װ�� Boost �� Serialization ���ͷ�ļ���
// Ӧ�����ǰ������ļ�������Ҫֱ��ʹ�� Serialization ���ͷ�ļ���
// Boost.Serialization �����һЩ��֪�޺��ı��������档
// �ڸ����Ժ����ǽ�ɾ�����µı���ָʾ������ͷ�ļ���Ȼ���ڡ�

// ��� C++11 ��׼�����չ֧��
#include "Extended/unique_ptr.hpp"
#include "Extended/shared_ptr_helper.hpp"
#include "Extended/shared_ptr.hpp"

#pragma warning(push)	// �����ô�ͷ�ļ�
#pragma warning(disable : 4244 4310)
#include <boost/archive/binary_iarchive.hpp>
#include <boost/archive/binary_oarchive.hpp>
#include <boost/archive/text_iarchive.hpp>
#include <boost/archive/text_oarchive.hpp>
#include <boost/archive/xml_iarchive.hpp>
#include <boost/archive/xml_oarchive.hpp>
// ���ڿ��ַ��汾�ľ�̬����ʱ��֪��������룬������ʱ�޷�ʹ�ÿ��ַ��汾��صĹ��ܡ�
//#include <boost/archive/text_wiarchive.hpp>
//#include <boost/archive/text_woarchive.hpp>
//#include <boost/archive/xml_wiarchive.hpp>
//#include <boost/archive/xml_woarchive.hpp>
#pragma warning(pop)	// �ָ�����ľ��漶��

// ���ڸ��� archive���ṩ�����ʵ����
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
