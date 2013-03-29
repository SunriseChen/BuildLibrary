// 本文件必须在所有其他 STL 头文件前被包含，建议在 stdafx.h 的 #include "targetver.h" 下面包含。
#pragma once
#ifndef _STL_PORT_H_
#define _STL_PORT_H_

// STLport 启用 Debug 模式下的检查功能
#ifdef _DEBUG
#define _STLP_DEBUG
#endif

// STLport 与 Boost 库配合使用
#define _STLP_USE_BOOST_SUPPORT

// 据说以下代码用于解决 VS2010 使用 STLport 的某个问题，但是暂时未发现有实际作用。
//#if !defined(_STLP_NATIVE_CPP_C_HEADER)
//#define _STLP_NATIVE_CPP_C_HEADER(header) <D:\\Program Files\\Microsoft Visual Studio 10.0\\VC\\include\\##header##>
//#endif

#endif
