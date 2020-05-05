from CvPythonExtensions import *

GC = CyGlobalContext()

class CvAdvancedStartScreen:

	def __init__(self, screenId):
		self.screenId = screenId
		self.m_bSideMenuDirty = False
		self.m_bASItemCostDirty = False
		self.CyGTabCtrl = None
		self.iSelectionIndex = []
		self.iSelectionList = []
		self.m_iCurrentX = -1
		self.m_iCurrentY = -1
		self.m_pCurrentPlot = 0

		self.m_iASCityTabID = 0
		self.m_iASCityListID = 0
		self.m_iASRoutesListID = 0
		self.m_iASUnitTabID = 1
		self.m_iASAutomateListID = 1
		self.m_iASImprovementsListID = 1
		self.m_iASImprovementsTabID = 2
		self.m_iASBuildingsListID = 2
		self.m_iASVisibilityTabID = 3
		self.m_iASTechTabID = 4
		self.m_iCost = 0

	def interfaceScreen(self):

		self.iPlayer = GC.getGame().getActivePlayer()
		self.CyPlayer = GC.getPlayer(self.iPlayer)

		screen = CyGInterfaceScreen("AdvancedStartScreen", self.screenId)
		screen.setCloseOnEscape(False)
		screen.setAlwaysShown(True)

		screen.addPanel("WorldBuilderBackgroundPanel", "", "", True, True, 0, 0, 226, 84, PanelStyles.PANEL_STYLE_MAIN)

		txt = CyTranslator().getText("TXT_KEY_ADVANCED_START_BEGIN_GAME", ())
		screen.setButtonGFC("WorldBuilderExitButton", txt, "", 50, 45, 130, 28, WidgetTypes.WIDGET_WB_EXIT_BUTTON, -1, -1, ButtonStyles.BUTTON_STYLE_STANDARD)

		self.refreshSideMenu()
		self.refreshAdvancedStartTabCtrl(False)

		CyCamera().JustLookAtPlot(self.CyPlayer.getStartingPlot())

		screen.showScreen(PopupStates.POPUPSTATE_IMMEDIATE, True)
		screen.setForcedRedraw(True)

	def mouseOverPlot(self):
		self.m_pCurrentPlot = CyInterface().getMouseOverPlot()
		self.m_iCurrentX = self.m_pCurrentPlot.getX()
		self.m_iCurrentY = self.m_pCurrentPlot.getY()

		if CyInterface().isLeftMouseDown():
			self.placeObject()
		elif CyInterface().isRightMouseDown():
			self.removeObject()

	def getHighlightPlot(self, argsList):
		self.refreshASItemCost()

		if self.m_pCurrentPlot != 0 and self.m_iCost > 0 and isMouseOverGameSurface():
			return (self.m_iCurrentX, self.m_iCurrentY)
		return ()

	# Will update the screen (every 250 MS)
	def updateScreen(self):

		if self.m_bSideMenuDirty:
			self.refreshSideMenu()
		if self.m_bASItemCostDirty:
			self.refreshASItemCost()

		if CyInterface().isDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT):
			self.refreshAdvancedStartTabCtrl(True)
			CyInterface().setDirty(InterfaceDirtyBits.Advanced_Start_DIRTY_BIT, False)


	def refreshASItemCost(self):
		iCost = 0
		if self.getASActiveCity():
			iCost = self.CyPlayer.getAdvancedStartCityCost(True, None)

		elif self.m_pCurrentPlot != 0:
			if self.m_pCurrentPlot.isRevealed(GC.getGame().getActiveTeam(), False):

				if self.getASActiveUnit() != -1:
					iCost = self.CyPlayer.getAdvancedStartUnitCost(self.getASActiveUnit(), True, self.m_pCurrentPlot)
				elif self.getASActivePop() and self.m_pCurrentPlot.isCity():
					iCost = self.CyPlayer.getAdvancedStartPopCost(True, self.m_pCurrentPlot.getPlotCity())
				elif self.getASActiveCulture() and self.m_pCurrentPlot.isCity():
					iCost = self.CyPlayer.getAdvancedStartCultureCost(True, self.m_pCurrentPlot.getPlotCity())
				elif self.getASActiveBuilding() != -1 and self.m_pCurrentPlot.isCity():
					iCost = self.CyPlayer.getAdvancedStartBuildingCost(self.getASActiveBuilding(), True, self.m_pCurrentPlot.getPlotCity())
				elif self.getASActiveRoute() != -1:
					iCost = self.CyPlayer.getAdvancedStartRouteCost(self.getASActiveRoute(), True, self.m_pCurrentPlot)
				elif self.getASActiveImprovement() != -1:
					iCost = self.CyPlayer.getAdvancedStartImprovementCost(self.getASActiveImprovement(), True, self.m_pCurrentPlot)

			elif self.m_pCurrentPlot.isAdjacentNonrevealed(GC.getGame().getActiveTeam()) and self.CyGTabCtrl.getActiveTab() == self.m_iASVisibilityTabID:
				iCost = self.CyPlayer.getAdvancedStartVisibilityCost(self.m_pCurrentPlot)

		if iCost < 0: iCost = 0
		self.m_iCost = iCost
		self.refreshSideMenu()

		self.m_bASItemCostDirty = False

	def getASActiveUnit(self):
		if self.CyGTabCtrl.getActiveTab() == self.m_iASUnitTabID:
			return getASUnit(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
		return -1

	def getASActiveCity(self):
		return self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID \
			and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASCityListID \
			and self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()] == 0

	def getASActivePop(self):
		return self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID \
			and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASCityListID \
			and self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()] == 1

	def getASActiveCulture(self):
		return self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID \
			and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASCityListID \
			and self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()] == 2

	def getASActiveBuilding(self):
		if self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID \
		and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASBuildingsListID:
			return getASBuilding(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
		return -1

	def getASActiveRoute(self):
		if self.CyGTabCtrl.getActiveTab() == self.m_iASImprovementsTabID \
		and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
			iRouteType = getASRoute(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
			if -1 == iRouteType:
				self.iSelectionList[self.CyGTabCtrl.getActiveTab()] = self.m_iASImprovementsListID
			return iRouteType
		return -1

	def getASActiveImprovement(self):
		if self.CyGTabCtrl.getActiveTab() == self.m_iASImprovementsTabID \
		and self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
			iImprovementType = getASImprovement(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
			if -1 == iImprovementType:
				self.iSelectionList[self.CyGTabCtrl.getActiveTab()] = self.m_iASRoutesListID
			return iImprovementType
		return -1

	def placeObject(self):
		if self.m_iCurrentX == -1 or self.m_iCurrentY == -1:
			return
		pPlot = GC.getMap().plot(self.m_iCurrentX, self.m_iCurrentY)
		if self.m_pCurrentPlot.isRevealed(GC.getGame().getActiveTeam(), False):
			# City Tab
			if self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID:
				# City List
				if self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASCityListID:
					iOptionID = self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()]
					# Place City
					if iOptionID == 0:
						if self.CyPlayer.getAdvancedStartCityCost(True, pPlot) > -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CITY, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, True)

					# City Population
					elif iOptionID == 1:
						if pPlot.isCity() and self.CyPlayer.getAdvancedStartPopCost(True, pPlot.getPlotCity()) > -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, True)

					# City Culture
					elif iOptionID == 2:
						if pPlot.isCity() and self.CyPlayer.getAdvancedStartCultureCost(True, pPlot.getPlotCity()) > -1:
							CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_CULTURE, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, True)

				# Buildings List
				elif self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASBuildingsListID and pPlot.isCity():
					iBuildingType = getASBuilding(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
					if iBuildingType != -1 and self.CyPlayer.getAdvancedStartBuildingCost(iBuildingType, True, pPlot.getPlotCity()) != -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iBuildingType, True)

			# Unit Tab
			elif self.CyGTabCtrl.getActiveTab() == self.m_iASUnitTabID:
				iUnitType = getASUnit(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
				if iUnitType > -1 and self.CyPlayer.getAdvancedStartUnitCost(iUnitType, True, pPlot) > -1:
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iUnitType, True)

			# Improvements Tab
			elif self.CyGTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
				# Routes List
				if self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
					iRouteType = getASRoute(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
					if iRouteType > -1 and self.CyPlayer.getAdvancedStartRouteCost(iRouteType, True, pPlot) > -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iRouteType, True)

				# Improvements List
				elif self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
					iImprovementType = getASImprovement(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
					if iImprovementType > -1 and self.CyPlayer.getAdvancedStartImprovementCost(iImprovementType, True, pPlot) > -1:
						CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iImprovementType, True)

		# Adjacent nonrevealed
		elif self.CyGTabCtrl.getActiveTab() == self.m_iASVisibilityTabID and self.CyPlayer.getAdvancedStartVisibilityCost(pPlot) > -1:
			CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_VISIBILITY, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, True)

		self.m_bSideMenuDirty = True
		self.m_bASItemCostDirty = True


	def removeObject(self):
		if self.m_iCurrentX == -1 or self.m_iCurrentY == -1 or not self.m_pCurrentPlot.isRevealed(GC.getGame().getActiveTeam(), False):
			return

		# City Tab
		if self.CyGTabCtrl.getActiveTab() == self.m_iASCityTabID:
			pPlot = GC.getMap().plot(self.m_iCurrentX, self.m_iCurrentY)
			# City List
			if self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASCityListID:
				# City Population
				if self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()] == 1 \
				and pPlot.isCity() and pPlot.getPlotCity().getOwner() == self.iPlayer:

					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_POP, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, -1, False)
			# Buildings List
			elif self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASBuildingsListID \
			and pPlot.isCity() and pPlot.getPlotCity().getOwner() == self.iPlayer:

				iBuildingType = getASBuilding(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
				if -1 != iBuildingType:
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_BUILDING, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iBuildingType, False)

		# Unit Tab
		elif self.CyGTabCtrl.getActiveTab() == self.m_iASUnitTabID:
			iUnitType = getASUnit(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
			if -1 != iUnitType:
				CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_UNIT, self.iPlayer, self.m_pCurrentPlot.getX(), self.m_pCurrentPlot.getY(), iUnitType, False)

		# Improvements Tab
		elif self.CyGTabCtrl.getActiveTab() == self.m_iASImprovementsTabID:
			# Routes List
			if self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASRoutesListID:
				iRouteType = getASRoute(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
				if -1 != iRouteType:
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_ROUTE, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iRouteType, False)

			# Improvements List
			elif self.iSelectionList[self.CyGTabCtrl.getActiveTab()] == self.m_iASImprovementsListID:
				iImprovementType = getASImprovement(self.iSelectionIndex[self.CyGTabCtrl.getActiveTab()])
				if -1 != iImprovementType:
					CyMessageControl().sendAdvancedStartAction(AdvancedStartActionTypes.ADVANCEDSTARTACTION_IMPROVEMENT, self.iPlayer, self.m_iCurrentX, self.m_iCurrentY, iImprovementType, False)
		else: return
		self.m_bSideMenuDirty = True
		self.m_bASItemCostDirty = True

	def setCurrentSelection(self, iTab, iIndex, iList):
		self.iSelectionIndex[iTab] = iIndex
		self.iSelectionList[iTab] = iList
		# Switch focus back to camera after interacting with advanced start panel
		setFocusToCVG() # Allows camera zoom scrolling without clicking the map first

#-------------------------------------------------------------#
# Functions called by the exe in this order at initialization #
#-------------------------------------------------------------#
	def getASCityTabID(self):
		return self.m_iASCityTabID

	def getASCityListID(self):
		return self.m_iASCityListID

	def getASBuildingsListID(self):
		return self.m_iASBuildingsListID

	def getASAutomateListID(self):
		return self.m_iASAutomateListID

	def getASUnitTabID(self):
		return self.m_iASUnitTabID

	def getASImprovementsTabID(self):
		return self.m_iASImprovementsTabID

	def getASRoutesListID(self):
		return self.m_iASRoutesListID

	def getASImprovementsListID(self):
		return self.m_iASImprovementsListID

	def getASVisibilityTabID(self):
		return self.m_iASVisibilityTabID

	def getASTechTabID(self):
		return self.m_iASTechTabID

	def refreshSideMenu(self):
		screen = CyGInterfaceScreen("AdvancedStartScreen", self.screenId)
		txt = "<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_POINTS", (self.CyPlayer.getAdvancedStartPoints(),))
		screen.setLabel("AdvancedStartPointsText", "", txt, 1<<0, 50, 15, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		txt = "<font=4>" + CyTranslator().getText("TXT_KEY_WB_AS_COST_THIS_LOCATION", (self.m_iCost, ))
		screen.setLabel("AdvancedStartCostText", "", txt, 1<<0, 30, 85, -2, FontTypes.GAME_FONT, WidgetTypes.WIDGET_GENERAL, -1, -1)
		self.m_bSideMenuDirty = False


	def refreshAdvancedStartTabCtrl(self, bReuse):

		if self.CyGTabCtrl and bReuse:
			iActiveTab = self.CyGTabCtrl.getActiveTab()
			iActiveList = self.iSelectionList[iActiveTab]
			iActiveIndex = self.iSelectionIndex[iActiveTab]
		else:
			iActiveTab = 0
			iActiveList = 0
			iActiveIndex = 0

		self.iSelectionIndex = []
		self.iSelectionList = []

		initWBToolAdvancedStartControl()

		# CyGTabCtrl API
		self.CyGTabCtrl = getWBToolAdvancedStartTabCtrl()

		self.CyGTabCtrl.setNumColumns(2 + GC.getNumBuildingInfos()/10);
		self.CyGTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_CITIES",()));
		self.iSelectionIndex.append(0)
		self.iSelectionList.append(self.m_iASCityListID)

		self.CyGTabCtrl.setNumColumns(2 + GC.getNumUnitInfos()/10);
		self.CyGTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_UNITS",()));
		self.iSelectionIndex.append(0)
		self.iSelectionList.append(0)

		self.CyGTabCtrl.setNumColumns(2 + GC.getNumImprovementInfos()/10);
		self.CyGTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_IMPROVEMENTS",()));
		self.iSelectionIndex.append(0)
		self.iSelectionList.append(self.m_iASRoutesListID)

		self.CyGTabCtrl.setNumColumns(1);
		self.CyGTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_VISIBILITY",()));
		self.iSelectionIndex.append(0)
		self.iSelectionList.append(0)

		self.CyGTabCtrl.setNumColumns(1);
		self.CyGTabCtrl.addTabSection(CyTranslator().getText("TXT_KEY_WB_AS_TECH",()));
		self.iSelectionIndex.append(0)
		self.iSelectionList.append(0)

		addWBAdvancedStartControlTabs()
		self.CyGTabCtrl.setActiveTab(iActiveTab)
		self.setCurrentSelection(iActiveTab, iActiveIndex, iActiveList)


	def leftMouseDown(self, argsList):
		self.placeObject()

	def rightMouseDown(self, argsList):
		self.removeObject()

	def killScreen(self):
		screen = CyGInterfaceScreen("AdvancedStartScreen", self.screenId)
		screen.hideScreen()
		CyEngine().clearColoredPlots(PlotLandscapeLayers.PLOT_LANDSCAPE_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_REVEALED_PLOTS)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_WORLD_BUILDER)
		CyEngine().clearAreaBorderPlots(AreaBorderLayers.AREA_BORDER_LAYER_HIGHLIGHT_PLOT)
		del self.iPlayer, self.CyPlayer