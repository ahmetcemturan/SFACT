# -*- coding: utf-8 -*-

# skFrontend.py - v1.0 - 2012-08-31
#
# A Skeinforge Frontend for 3D Printing
# Copyright 2012 François Delègue
#
# http://reprapide.fr/skfrontend-un-frontal-pour-skeinforge
# http://reprapide.fr/skfrontend-a-skeinforge-frontend
#
# skFrontend.py can't run without config.py into it's directory
#
# This (so little) program is (very) free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details: <http://www.gnu.org/licenses/>.


import Tkinter as tk, tkFileDialog, tkMessageBox, os, re, sys
import config as c
from fabmetheus_utilities import settings
import os

class SkFrontend (tk.Tk):
  def __init__(self, *args, **kwargs):
	tk.Tk.__init__(self, *args, **kwargs)
	self.geometry (c.windowWidth + "x" + c.windowHeight)
	self.protocol ('WM_DELETE_WINDOW', self.quitApplication)
#	self.lastFrametopOffset = 111
	# we quit if no valid path to extrusion profile
	if not (os.path.exists (c.skProfileDirectory)):
		tkMessageBox.showerror (c.titleErrorMsgBox, c.noExtrusionProfileErrorMsg)
		self.destroy ()

	self.resizable (width=False, height=True)
	# finding used profile name
	(self.path, self.profileName) =  os.path.split (c.skProfileDirectory)
	self.title ("skFrontend :: " + self.profileName)

	#-----------------------------------------------------
	''' parenthesis backslash into search expressions '''
	#-----------------------------------------------------
	self.skCarveSearchString = self.backslash (c.skCarveSearchString)
	self.skFeedRateSearchString = self.backslash (c.skFeedRateSearchString)
	self.skFlowRateSearchString = self.backslash (c.skFlowRateSearchString)
	self.skInfillSoliditySearchString = self.backslash (c.skInfillSoliditySearchString)
	self.skMultiplyRowSearchString = self.backslash (c.skMultiplyRowSearchString)
	self.skMultiplyColSearchString = self.backslash (c.skMultiplyColSearchString)
	self.skSkirtLayersSearchString = self.backslash (c.skSkirtLayersSearchString)
	self.skSkirtActivateSearchString = self.backslash (c.skSkirtActivateSearchString)
	self.skExtrusionProfileSearchString = self.backslash (c.skExtrusionProfileSearchString)

	#-----------------------------------------------------
	''' frame containing layer thickness menu '''
	#-----------------------------------------------------
#	settings.LabelDisplay().getFromName('- Extrusion Resolution settings -', self )
#	settings.LabelSeparator().getFromRepository(self)
	self.frame1=tk.Frame (self)
	self.frame1.pack ()
	self.frame1.place (x=c.frameLeftMargin, y=c.frameTopMargin, height=c.frameHeight, width=c.frameWidth)
	self.label=tk.Label (self.frame1, text=c.thicknessListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.layerHeight=tk.StringVar (self)
	self.layerHeight.set (self.getSkSetting (c.skCarveFile, self.skCarveSearchString, c.skDefaultLayerHeight))
	self.layerHeights=tk.OptionMenu (self.frame1, self.layerHeight, *c.layerHeightList, command=self.refreshOptionMenu)
	self.layerHeights.config (width=c.menuWidth)
	self.layerHeights.pack ()
	self.layerHeights.place (y=c.menuMarginTop)

	self.firstLayerHeight = self.layerHeight.get ()
	self.newLayerHeight = self.layerHeight.get ()
	#-----------------------------------------------------
	''' frame containing edge width menu '''
	#-----------------------------------------------------
	self.frame1=tk.Frame (self)
	self.frame1.pack ()
	self.newFrametopoffset = c.frameTopOffset*0
	self.frame1.place (x=c.frameLeftMargin + c.frameRightOffset, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)
	print(self.newFrametopoffset)
	self.label=tk.Label (self.frame1, text=c.edgeWidthListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.edgeWidth=tk.StringVar (self)
	self.edgeWidth.set (self.getSkSetting (c.skCarveFile, self.skCarveSearchString, c.skDefaultEdgeWidth))
	self.edgeWidths=tk.OptionMenu (self.frame1, self.edgeWidth, *c.edgeWidthList, command=self.refreshOptionMenu)
	self.edgeWidths.config (width=c.menuWidth)
	self.edgeWidths.pack ()
	self.edgeWidths.place (y=c.menuMarginTop)

	self.firstEdgeWidth = self.edgeWidth.get ()
	self.newEdgeWidth = self.edgeWidth.get ()

	#-----------------------------------------------------
	''' frame containing feed rate menu '''
	#-----------------------------------------------------
	self.frame2=tk.Frame (self)
	self.frame2.pack ()
	oldFrametopoffset = self.newFrametopoffset
	self.newFrametopoffset += c.frameTopOffset
	self.frame2.place (x=c.frameLeftMargin, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)
	print(self.newFrametopoffset)
	self.label=tk.Label (self.frame2, text=c.infillFeedRateListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	# validatecommand ==> error!…
	# self.feedRate=tk.Spinbox (self.frame2, from_=6, to=100, command=self.refreshSpinBox, validate=tk.ALL, validatecommand=self.refreshSpinBox) ==> error!…
	# ==> no modificationButtonState into spinboxes when content is modified via keyboard
	self.feedRate=tk.Spinbox (self.frame2, from_=c.feedRateMinimumValue, to=c.feedRateMaximumValue, command=self.refreshSpinBox)
	self.feedRate.delete (0,"end")
	self.feedRate.insert (0, self.getSkSetting (c.skSpeedFile, self.skFeedRateSearchString, c.skDefaultFeedRate))
	self.feedRate.config (width=c.menuWidth)
	self.feedRate.pack ()
	self.feedRate.place (x=c.labelMarginLeft, y=c.menuMarginTop)

	self.firstFeedRate = self.feedRate.get ()
	self.newFeedRate = self.feedRate.get ()

	#-----------------------------------------------------

	''' frame containing infill solidity menu '''
	#-----------------------------------------------------
	self.frame4=tk.Frame (self)
	self.frame4.pack ()
	self.newFrametopoffset += c.frameTopOffset
	self.frame4.place (x=c.frameLeftMargin, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)
	print(self.newFrametopoffset)
	self.label=tk.Label (self.frame4, text=c.InfillSolidityListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.infillSolidity=tk.Spinbox (self.frame4, from_=4, to=100, increment=1, command=self.refreshSpinBox)
	self.infillSolidity.delete (0,"end")
	self.infillSolidity.insert (0, self.ratioToPercentage (self.getSkSetting (c.skFillFile, self.skInfillSoliditySearchString, c.skDefaultInfillSolidity)))
	self.infillSolidity.config (width=c.menuWidth)
	self.infillSolidity.pack ()
	self.infillSolidity.place (x=c.labelMarginLeft, y=c.menuMarginTop)

	self.firstInfillSolidity = self.infillSolidity.get ()
	self.newInfillSolidity = self.infillSolidity.get ()

	#-----------------------------------------------------
	''' frame containing multiply rows menu '''
	#-----------------------------------------------------
	self.frame5=tk.Frame (self)
	self.frame5.pack ()
	self.newFrametopoffset += c.frameTopOffset
	self.frame5.place (x=c.frameLeftMargin, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)

	self.label=tk.Label (self.frame5, text=c.multiplyRowListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.multiplyRow=tk.StringVar (self)
	self.multiplyRow.set (self.getSkSetting (c.skMultiplyFile, self.skMultiplyRowSearchString, c.skDefaultMultiplyRow))
	self.menu=tk.OptionMenu (self.frame5, self.multiplyRow, *c.multiplyRowList, command=self.refreshOptionMenu)
	self.menu.config (width=c.menuWidth)
	self.menu.pack ()
	self.menu.place (y=c.menuMarginTop)

	self.firstMultiplyRow = self.multiplyRow.get ()
	self.newMultiplyRow = self.multiplyRow.get ()

	#-----------------------------------------------------
	''' frame containing multiply columns menu '''
	#-----------------------------------------------------
	self.frame6=tk.Frame (self)
	self.frame6.pack ()
	self.newFrametopoffset += c.frameTopOffset*0
	self.frame6.place (x=c.frameLeftMargin + c.frameRightOffset, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)

	self.label=tk.Label (self.frame6, text=c.multiplyColListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.multiplyCol = tk.StringVar (self)
	self.multiplyCol.set (self.getSkSetting (c.skMultiplyFile, self.skMultiplyColSearchString, c.skDefaultMultiplyCol))
	self.menu = tk.OptionMenu (self.frame6, self.multiplyCol, *c.multiplyColList, command=self.refreshOptionMenu)
	self.menu.config (width=c.menuWidth)
	self.menu.pack ()
	self.menu.place (y=c.menuMarginTop)

	self.firstMultiplyCol = self.multiplyCol.get ()
	self.newMultiplyCol = self.multiplyCol.get ()

	#-----------------------------------------------------
	''' frame containing skirt menu '''
	#-----------------------------------------------------
	self.frame7=tk.Frame (self)
	self.frame7.pack ()
	self.newFrametopoffset += c.frameTopOffset
	self.frame7.place (x=c.frameLeftMargin, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight, width=c.frameWidth)

	self.label=tk.Label (self.frame7, text=c.skirtLayersListLabel, fg=c.labelColor)
	self.label.pack ()
	self.label.place (x=c.labelMarginLeft)

	self.skirtLayers = tk.StringVar (self)
	self.skirtLayers.set (self.getSkSetting (c.skSkirtFile, self.skSkirtLayersSearchString, c.skDefaultSkirtLayers))
	self.menu = tk.OptionMenu (self.frame7, self.skirtLayers, *c.skirtLayersList, command=self.refreshOptionMenu)
	self.menu.config (width=c.menuWidth)
	self.menu.pack ()
	self.menu.place (y=c.menuMarginTop)

	self.firstSkirtLayers = self.skirtLayers.get ()
	self.newSkirtLayers = self.skirtLayers.get ()

	#-----------------------------------------------------
	''' last frame of the window: buttons
		(plenty of hard-coded controls display values… ) '''
	#-----------------------------------------------------
	self.frame8=tk.Frame (self)
	self.frame8.pack ()
	self.newFrametopoffset += c.frameTopOffset + 35 # extra separation
	self.frame8.place (x=c.frameLeftMargin, y=c.frameTopMargin + self.newFrametopoffset, height=c.frameHeight+200, width=c.frameWidth + 300)
	self.lastFrametopOffset = self.newFrametopoffset
	self.saveModificationsButton = tk.Button (self.frame8, text=c.saveButtonLabel, command=self.saveChanges, state=tk.DISABLED)
	self.modificationButtonState = "DISABLED"
	self.saveModificationsButton.pack ()
	self.saveModificationsButton.place (x=c.labelMarginLeft)

	self.chooseFileButton = tk.Button (self.frame8, text=c.chooseFileButtonLabel, command=self.chooseFileDialog)
	self.chooseFileButton.pack ()
	self.chooseFileButton.place (x=c.labelMarginLeft, y=40)

	self.fileToSkName = tk.StringVar()
	self.fileToSk = tk.Label (self.frame8, fg=c.fileNameColor, textvariable=self.fileToSkName)
	self.fileToSkName.set (c.noFileSelectedText)
	self.fileToSk.pack ()
	self.fileToSk.place (x=c.labelMarginLeft+155, y=43)

	self.runSkeinforgeButton = tk.Button (self.frame8, text=c.runSkeinforgeButtonLabel, state=tk.DISABLED, command=self.runSkeinforge)
	self.runSkeinforgeButton.pack()
	self.runSkeinforgeButton.place (x=c.labelMarginLeft, y=80)

	self.quitButton = tk.Button (self.frame8, text=c.quitButtonLabel, command=self.quitApplication)
	self.quitButton.pack ()
	self.quitButton.place (x=c.labelMarginLeft + 260, y=80)

	#-----------------------------------------------------
	''' compiling regexs '''
	#-----------------------------------------------------
	self.searchNumberRegex = "\\t([-+]?[0-9]*\\.?,?[0-9]+)"
	self.searchTrueFalseRegex = "\\t(True|False)"
	self.searchTextStringRegex = "\\t(.+)"
	self.layerHeightRE = re.compile (self.skCarveSearchString + self.searchNumberRegex)
	self.edgeWidthRE = re.compile (self.skCarveSearchString + self.searchNumberRegex)
	self.feedRateRE = re.compile (self.skFeedRateSearchString + self.searchNumberRegex)
	self.infillSolidityRE = re.compile (self.skInfillSoliditySearchString + self.searchNumberRegex)
	self.multiplyRowRE = re.compile (self.skMultiplyRowSearchString + self.searchNumberRegex)
	self.multiplyColRE = re.compile (self.skMultiplyColSearchString + self.searchNumberRegex)
	self.skirtLayersRE = re.compile (self.skSkirtLayersSearchString + self.searchNumberRegex)
	self.skirtActivateRE = re.compile (self.skSkirtActivateSearchString + self.searchTrueFalseRegex)
	self.extrusionProfileRE = re.compile (self.skExtrusionProfileSearchString + self.searchTextStringRegex)

	#-----------------------------------------------------
	''' set Skeinforge's extrusion profile name '''
	#-----------------------------------------------------
	self.setSkeinforgeExtrusionProfile ()


	# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
	''' end of application __init__ '''
	# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


  #-----------------------------------------------------
  ''' tracking parameters functions '''
  #-----------------------------------------------------
  def refreshOptionMenu (self, unusedButNecessary):
	self.newLayerHeight = self.layerHeight.get ()
	self.newEdgeWidth = self.edgeWidth.get ()
	self.newMultiplyRow = self.multiplyRow.get ()
	self.newMultiplyCol = self.multiplyCol.get ()
	self.newSkirtLayers = self.skirtLayers.get ()
	self.setSaveModificationButtonState ()

  def refreshSpinBox (self):
	self.newFeedRate = self.feedRate.get ()
	self.newInfillSolidity = self.infillSolidity.get ()
	self.setSaveModificationButtonState ()
	return True

  def setSaveModificationButtonState (self):
	if (
	 self.firstLayerHeight != self.newLayerHeight
	 or self.firstEdgeWidth != self.newEdgeWidth
	 or self.firstFeedRate != self.newFeedRate
	 or self.firstFlowRate != self.newFlowRate
	 or self.firstInfillSolidity != self.newInfillSolidity
	 or self.firstMultiplyRow != self.newMultiplyRow
	 or self.firstMultiplyCol != self.newMultiplyCol
	 or self.firstSkirtLayers != self.newSkirtLayers
	 ):
	  self.saveModificationsButton.config (state=tk.NORMAL)
	  self.modificationButtonState = "NORMAL"
	else:
	  self.saveModificationsButton.config (state=tk.DISABLED)
	  self.modificationButtonState = "DISABLED"

  #-----------------------------------------------------
  ''' getting an sk plugin parameter '''
  #-----------------------------------------------------
  def getSkSetting (self, fileName, searchString, defaultReturnValue):
	try:
	  returnValue = defaultReturnValue
	  p = re.compile (searchString)
	  file = open (os.path.join (c.skProfileDirectory, fileName), "r")
	  lines = file.readlines ()
	  for line in lines:
		if p.match (line):
		  ligne = line.split ('\t')
		  returnValue = ligne[1].rstrip('\n')
		  break
	  file.close ()
	  return returnValue
	except Exception, err:
	  tkMessageBox.showerror (c.titleErrorMsgBox, "%s " % str(err))
	  return returnValue

  #-----------------------------------------------------
  ''' pharenthesis backslash for regex search '''
  #-----------------------------------------------------
  def backslash (self, str):
	str = re.sub (r'\(', '\\(', str)
	str = re.sub (r'\)', '\\)', str)
	return str

  #-----------------------------------------------------
  ''' transforms ratio into percentage (from 0.3 to 30 for ex.)'''
  #-----------------------------------------------------
  def ratioToPercentage (self, n):
	return int (float (n) * 100)

  #-----------------------------------------------------
  ''' transforms percentage into ratio(from 30 to 0.3 for ex.) '''
  #-----------------------------------------------------
  def percentageToRatio (self, n):
	return str (float (n) / 100)

  #-----------------------------------------------------
  ''' choose file to be skeinforged dialog '''
  #-----------------------------------------------------
  def chooseFileDialog (self):
	self.fileToSkeinforge = tkFileDialog.askopenfilename (initialdir=c.STLFilesDefaultDirectory, filetypes=c.openableFilesTypes)
	if self.fileToSkeinforge:
	  self.fileToSkeinforgeName = self.fileToSkeinforge.rsplit ("/", 1)
	  self.fileToSkName.set ("")
	  self.fileToSkName.set (self.fileToSkeinforgeName[1])
	  self.runSkeinforgeButton.config (state=tk.NORMAL)

  #-----------------------------------------------------
  ''' run Skeinforge '''
  #-----------------------------------------------------
  def runSkeinforge (self):
	try:
	  if self.modificationButtonState == "NORMAL":
		if tkMessageBox.askquestion (title=c.unSavedModificationsDialogTitle, message=c.runSkUnSavedModificationsMsg) == "no":
		  return
	  #print "python " + c.skCraftPath + " " + self.fileToSkeinforge
	  os.system ("python " + c.skCraftPath + " " + self.fileToSkeinforge)
	except Exception, err:
	  # the more usual error:
	  tkMessageBox.showerror (c.titleErrorMsgBox, c.unASCIIerrorMessage)
	  # also possible, less explicit but the real error:
	  # tkMessageBox.showerror (c.titleErrorMsgBox, "%s " % str(err))
	  return 1

  #-----------------------------------------------------
  ''' ask or not file save function for profiles files '''
  #-----------------------------------------------------
  def saveChanges (self):
	# carve.csv file: layer height
	if self.firstLayerHeight != self.newLayerHeight:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skCarveFile), self.layerHeightRE, self.newLayerHeight)
	  self.firstLayerHeight = self.newLayerHeight

	if self.firstEdgeWidth != self.newEdgeWidth:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skCarveFile), self.edgeWidthRE, self.newEdgeWidth)
	  self.firstEdgeWidth = self.newEdgeWidth

	# speed.csv file: feed rate
	self.newFeedRate = self.feedRate.get ()
	if self.firstFeedRate != self.newFeedRate:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skSpeedFile), self.feedRateRE, self.newFeedRate)
	  self.firstFeedRate = self.newFeedRate

	# fill.csv file: infill solidity
	self.newInfillSolidity = self.infillSolidity.get ()
	if self.firstInfillSolidity != self.newInfillSolidity:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skFillFile), self.infillSolidityRE, self.percentageToRatio (self.newInfillSolidity))
	  self.firstInfillSolidity = self.newInfillSolidity

	# multiply.csv file: number of rows
	if self.firstMultiplyRow != self.newMultiplyRow:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skMultiplyFile), self.multiplyRowRE, self.newMultiplyRow)
	  self.firstMultiplyRow = self.newMultiplyRow

	# multiply.csv file: number of columns
	if self.firstMultiplyCol != self.newMultiplyCol:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skMultiplyFile), self.multiplyColRE, self.newMultiplyCol)
	  self.firstMultiplyCol = self.newMultiplyCol

	# skirt.csv file: layers to, then activate skirt or not
	if self.firstSkirtLayers != self.newSkirtLayers:
	  self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skSkirtFile), self.skirtLayersRE, self.newSkirtLayers)
	  self.firstSkirtLayers = self.newSkirtLayers
	if self.newSkirtLayers == "0":
	  boolean = "False"
	else:
	  boolean = "True"
	self.saveIntoFile (os.path.join (c.skProfileDirectory, c.skSkirtFile), self.skirtActivateRE, boolean)

	self.saveModificationsButton.config (state=tk.DISABLED)
	self.modificationButtonState = "DISABLED"

  #-----------------------------------------------------
  ''' save changes into file '''
  #-----------------------------------------------------
  def saveIntoFile (self, file, compiledRE, newValue):
	try:
	  with open (file, "r") as source:
		lines = source.readlines ()
	  with open (file, "w") as source:
		for line in lines:
		  matchObject = compiledRE.match (line)
		  if matchObject:
			source.write (re.sub (matchObject.group (1), newValue, line))
		  else:
			source.write (line)
	except Exception, err:
	  tkMessageBox.showerror (c.titleErrorMsgBox, "%s " % str(err))
	  return 1

  #-----------------------------------------------------
  ''' quit '''
  #-----------------------------------------------------
  def quitApplication (self):
	if self.modificationButtonState == "NORMAL":
	  if tkMessageBox.askquestion (title=c.unSavedModificationsDialogTitle, message=c.quitAppUnSavedModificationsMsg) == "no":
		return
	print "ciao!"
	self.destroy ()

  #-----------------------------------------------------
  ''' tell Skeinforge to use profile set into config.py
	  (end of path into skProfileDirectory var) '''
  #-----------------------------------------------------
  def setSkeinforgeExtrusionProfile (self):
	# finding Skeinforge's profiles types directory -not extrusion profiles directory
	(skProfilesTypePath, unused) =  os.path.split (self.path)
	self.saveIntoFile (os.path.join (skProfilesTypePath, c.skExtrusionFile), self.extrusionProfileRE, self.profileName)

#-----------------------------------------------------

if __name__ == "__main__":
  app = SkFrontend ()
  app.mainloop ()

