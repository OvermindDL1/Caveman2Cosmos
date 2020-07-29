/**********************************************************************

File:		CvBugOptions.cpp
Author:		EmperorFool
Created:	2009-01-21

		Copyright (c) 2009 The BUG Mod. All rights reserved.

**********************************************************************/

#include "CvGameCoreDLL.h"
#include "FVariableSystem.h"

bool g_bIsBug = false;


void logMsg(const char* format, ...)
{
	static char buf[2048];
	_vsnprintf(buf, 2048 - 4, format, (char*)(&format + 1));
	gDLL->logMsg("bull.log", buf);
}


bool isBug()
{
	return g_bIsBug;
}

void setIsBug(bool bIsBug)
{
	logMsg("isBug: %s", bIsBug ? "true" : "false");
	g_bIsBug = bIsBug;

	// set the unit and building filters to default state once Bug is available
	UnitFilterList::setFilterActiveAll(UNIT_FILTER_HIDE_UNBUILDABLE, getBugOptionBOOL("RoMSettings__HideUntrainableUnits", false));
	BuildingFilterList::setFilterActiveAll(BUILDING_FILTER_HIDE_UNBUILDABLE, getBugOptionBOOL("RoMSettings__HideUnconstructableBuildings", false));
}


bool getDefineBOOL(const char* xmlKey, bool bDefault)
{
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
	{
		return iResult != 0;
	}
	else
	{
		return bDefault;
	}
}

int getDefineINT(const char* xmlKey, int iDefault)
{
	int iResult = 0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, iResult))
	{
		return iResult;
	}
	else
	{
		return iDefault;
	}
}

float getDefineFLOAT(const char* xmlKey, float fDefault)
{
	float fResult = 0.0;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, fResult))
	{
		return fResult;
	}
	else
	{
		return fDefault;
	}
}

const char * getDefineSTRING(const char* xmlKey, const char * szDefault)
{
	const char * szResult = NULL;
	if (GC.getDefinesVarSystem()->GetValue(xmlKey, szResult))
	{
		return szResult;
	}
	else
	{
		return szDefault;
	}
}


bool getBugOptionBOOL(const char* id, bool bDefault, const char* xmlKey)
{
	PROFILE_FUNC();

	if (isBug())
	{
		return Cy::call<bool>(PYBugOptionsModule, "getOptionBOOL", Cy::Args(id, bDefault));
	}
	else
	{
		CvString tmp;
		if (!xmlKey)
		{
			tmp.append(OPTION_XML_PREFIX);
			tmp.append(id);
			xmlKey = tmp.c_str();
		}
		//logMsg("debug - getBugOptionBOOL %s", xmlKey);
		return getDefineBOOL(xmlKey, bDefault);
	}
}

int getBugOptionINT(const char* id, int iDefault, const char* xmlKey)
{
	PROFILE_FUNC();

	if (isBug())
	{
		return Cy::call<int>(PYBugOptionsModule, "getOptionINT", Cy::Args(id, iDefault));
	}
	else
	{
		CvString tmp;
		if (!xmlKey)
		{
			tmp.append(OPTION_XML_PREFIX);
			tmp.append(id);
			xmlKey = tmp.c_str();
		}
		//logMsg("debug - getBugOptionINT %s", xmlKey);
		return getDefineINT(xmlKey, iDefault);
	}
}
