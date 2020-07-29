//  $Header:
//------------------------------------------------------------------------------------------------
//
//  FILE:	wchar_utils.cpp
//
//  PURPOSE: wchar utils
//
//------------------------------------------------------------------------------------------------

#include <cwchar>

bool equal(const wchar_t* str1, const wchar_t* str2)
{
	return std::wcscmp(str1, str2) == 0;
}
