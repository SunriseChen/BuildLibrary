// ���ļ��������������� STL ͷ�ļ�ǰ�������������� stdafx.h �� #include "targetver.h" ���������
#pragma once
#ifndef _STL_PORT_H_
#define _STL_PORT_H_

// STLport ���� Debug ģʽ�µļ�鹦��
#ifdef _DEBUG
#define _STLP_DEBUG
#endif

// STLport �� Boost �����ʹ��
#define _STLP_USE_BOOST_SUPPORT

// ��˵���´������ڽ�� VS2010 ʹ�� STLport ��ĳ�����⣬������ʱδ������ʵ�����á�
//#if !defined(_STLP_NATIVE_CPP_C_HEADER)
//#define _STLP_NATIVE_CPP_C_HEADER(header) <D:\\Program Files\\Microsoft Visual Studio 10.0\\VC\\include\\##header##>
//#endif

#endif
