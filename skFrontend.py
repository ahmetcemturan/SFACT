# -*- coding: utf-8 -*-

# skFrontend.py - v1.3 - 2012-11-09
# 
# A Skeinforge Frontend for 3D Printing
# Copyright 2012 François Delègue
#
# http://reprapide.fr/skfrontend-un-frontal-pour-skeinforge
# http://reprapide.fr/skfrontend-a-skeinforge-frontend
#
# skFrontend.py can't run without config.py and preferences file into it's directory
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
#
# Changes from v1.0 to v1.1:
# -Flow Rate set to Feed Rate when Feed Rate is modified
# Changes from v1.1 to v1.2:
# -radio buttons for Multiply activation/deactivation
# -first layer speed setting
# -perimeter speed setting
# Changes from v1.2 to v1.3:
# -several profiles can be managed
# -last file to be skeinforged is remembered
# -Python interpreter can be defined
#

import Tkinter as tk, tkFileDialog, tkMessageBox, os, re, sys
import config as c

class SkFrontend (tk.Tk):
  def __init__(self, *args, **kwargs):
    tk.Tk.__init__(self, *args, **kwargs)

    # test of config.py settings
    self.configPyTests ()

    # window settings
    self.resizable (width=False, height=False)    
    self.geometry (c.windowWidth + "x" + c.windowHeight)
    self.protocol ('WM_DELETE_WINDOW', self.quitApplication)

    # where is skFrontend?
    self.pathToSkFrontend = os.path.abspath (os.path.dirname (sys.argv[0]))

    # preferences file name
    self.preferencesFile = os.path.join (self.pathToSkFrontend, c.preferencesFileName)

    # preferences file exists?
    self.preferencesFileTest ()

    # compiling regex for research into preferences file
    self.lastUsedProfileRE = re.compile ("lastUsedProfile=(.+)")
    self.lastFileToCraftRE = re.compile ("lastFileToCraft=(.+)")

    # get last used profile name from preferences file
    self.profileName = self.getLastSettings (self.preferencesFile, self.lastUsedProfileRE)

    # profile 1st choice from preferences file, 2nd choice from config.py
    if (self.profileName):
      self.profileFullName = os.path.join (c.skProfilesDirectory, self.profileName, "")
      if not (os.path.isdir (self.profileFullName)):
        self.profileFullName = os.path.join (c.skProfilesDirectory, c.skDefaultProfileName, "")
        self.profileName = c.skDefaultProfileName
        self.saveIntoFile (self.preferencesFile, self.lastUsedProfileRE, self.profileName)

    # preparing regexs
    self.parenthesiBackslash ()
    self.regexCompile ()

    # tell Skeinforge to use the profile we just found
    self.setSkeinforgeExtrusionProfile ()

    # get last used STL file path from preferences file
    self.lastFileToCraftFullPath =  self.getLastSettings (self.preferencesFile, self.lastFileToCraftRE)

    # we don't use last STL file if it no longer exists
    if (not os.path.exists (self.lastFileToCraftFullPath)):
      self.lastFileToCraftFullPath = ""

    # find last used STL file name    
    if (self.lastFileToCraftFullPath):
      (unused, self.lastFileToCraft) = os.path.split (self.lastFileToCraftFullPath)

    # profile name into title bar
    self.title ("skFrontend :: " + self.profileName)

    # find profile's names into profiles directory
    self.profilesList = list()
    for file in os.listdir (c.skProfilesDirectory):
      if (os.path.isdir (os.path.join (c.skProfilesDirectory, file))):
        self.profilesList.append(file)

    # running for the 1st time flag
    self.firstRun = 1

    # setting user interface
    self.makeInterface ()
    self.setInterface ()

    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    # end of application __init__
    # @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


  #-----------------------------------------------------
  # user interface
  #-----------------------------------------------------
  def makeInterface (self):
  # here we draw interface controls
  # profiles menu
    self.frame0=tk.Frame (self)
    self.frame0.pack ()
    self.frame0.place (x=c.frameLeftMargin, y=c.frameTopMargin, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame0, text=c.profilesListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.profile=tk.StringVar (self)
    self.profiles=tk.OptionMenu (self.frame0, self.profile, *self.profilesList, command=self.changingProfile)
    self.profiles.config (width=c.superLargeMenuWidth)
    self.profiles.pack ()
    self.profiles.place (y=c.menuMarginTop)

  # layer thickness menu
    self.frame1=tk.Frame (self)
    self.frame1.pack ()
    self.frame1.place (x=c.frameLeftMargin + c.frameRightOffset * 2, y=c.frameTopMargin, height=c.frameHeight, width=c.frameWidth) 
    self.label=tk.Label (self.frame1, text=c.thicknessListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)  
    self.layerThickness=tk.StringVar (self)
    self.layerThicknesses=tk.OptionMenu (self.frame1, self.layerThickness, *c.layerThicknessList, command=self.refreshOptionMenus)
    self.layerThicknesses.config (width=c.largeMenuWidth)
    self.layerThicknesses.pack ()
    self.layerThicknesses.place (y=c.menuMarginTop)  

  # feed rate menu
    self.frame2=tk.Frame (self)
    self.frame2.pack ()
    self.frame2.place (x=c.frameLeftMargin, y=c.frameTopMargin + c.frameTopOffset, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame2, text=c.feedRateListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    # validatecommand ==> error!…
    # self.feedRate=tk.Spinbox (self.frame2, from_=6, to=100, command=self.refreshSpinBoxes, validate=tk.ALL, validatecommand=self.refreshSpinBoxes) ==> error!…
    # ==> no modificationButtonState into spinboxes when content is modified via keyboard
    self.feedRate=tk.Spinbox (self.frame2, from_=c.feedRateMinimumValue, to=c.feedRateMaximumValue, command=self.refreshFeedAndFlowRates, width=c.menuWidth)
    self.feedRate.pack ()
    self.feedRate.place (x=c.labelMarginLeft, y=c.menuMarginTop)  

  # flow rate menu
    self.frame3=tk.Frame (self)
    self.frame3.pack ()
    self.frame3.place (x=c.frameLeftMargin + c.frameRightOffset, y=c.frameTopMargin + c.frameTopOffset, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame3, text=c.flowRateListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.flowRate=tk.Spinbox (self.frame3, from_=c.flowRateMinimumValue, to=c.flowRateMaximumValue, command=self.refreshSpinBoxes, width=c.menuWidth)
    self.flowRate.pack ()
    self.flowRate.place (x=c.labelMarginLeft, y=c.menuMarginTop)

  # first layer menu
    self.frame31=tk.Frame (self)
    self.frame31.pack ()
    self.frame31.place (x=c.frameLeftMargin + c.frameRightOffset * 2, y=c.frameTopMargin + c.frameTopOffset, height=c.frameHeight, width=c.frameWidth)  
    self.label=tk.Label (self.frame31, text=c.firstLayerLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)  
    self.firstLayerSpeed=tk.StringVar (self)
    self.firstLayer=tk.OptionMenu (self.frame31, self.firstLayerSpeed, *c.firstLayerSpeedList, command=self.refreshOptionMenus)
    self.firstLayer.config (width=c.largeMenuWidth)
    self.firstLayer.pack ()
    self.firstLayer.place (y=c.menuMarginTop)  

  # infill solidity menu
    self.frame4=tk.Frame (self)
    self.frame4.pack ()
    self.frame4.place (x=c.frameLeftMargin, y=c.frameTopMargin + c.frameTopOffset * 2, height=c.frameHeight, width=c.frameWidth) 
    self.label=tk.Label (self.frame4, text=c.InfillSolidityListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.infillSolidity=tk.Spinbox (self.frame4, from_=4, to=100, increment=1, command=self.refreshSpinBoxes, width=c.menuWidth)
    self.infillSolidity.pack ()
    self.infillSolidity.place (x=c.labelMarginLeft, y=c.menuMarginTop)

  # perimeter menu
    self.frame40=tk.Frame (self)
    self.frame40.pack ()
    self.frame40.place (x=c.frameLeftMargin + c.frameRightOffset, y=c.frameTopMargin + c.frameTopOffset * 2, height=c.frameHeight, width=c.frameWidth)  
    self.label=tk.Label (self.frame40, text=c.perimeterLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)  
    self.perimeterSpeed=tk.StringVar (self)
    self.perimeterMenu=tk.OptionMenu (self.frame40, self.perimeterSpeed, *c.perimeterSpeedList, command=self.refreshOptionMenus)
    self.perimeterMenu.config (width=c.largeMenuWidth)
    self.perimeterMenu.pack ()
    self.perimeterMenu.place (y=c.menuMarginTop)

  # multiply on/off radiobuttons
    self.frame41=tk.Frame (self)
    self.frame41.pack ()
    self.frame41.place (x=c.frameLeftMargin, y=c.frameTopMargin + c.frameTopOffset * 3, height=c.frameHeight, width=c.frameWidth)  
    self.label=tk.Label (self.frame41, text=c.multiplyActivityLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)  
    self.multiplyActivity = tk.BooleanVar (self)
    self.radio1 = tk.Radiobutton (self.frame41, text="On", variable=self.multiplyActivity, value=True, command=self.refreshRadioButtons)
    self.radio1.pack ()
    self.radio1.place (y=c.menuMarginTop)
    self.radio2 = tk.Radiobutton (self.frame41, text="Off", variable=self.multiplyActivity, value=False, command=self.refreshRadioButtons)
    self.radio2.pack ()
    self.radio2.place (y=c.menuMarginTop, x=50)  
    
  # multiply rows menu
    self.frame5=tk.Frame (self)
    self.frame5.pack ()
    self.frame5.place (x=c.frameLeftMargin + c.frameRightOffset, y=c.frameTopMargin + c.frameTopOffset * 3, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame5, text=c.multiplyRowListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.multiplyRow=tk.StringVar (self)
    self.menu=tk.OptionMenu (self.frame5, self.multiplyRow, *c.multiplyRowList, command=self.refreshOptionMenus)
    self.menu.config (width=c.menuWidth)
    self.menu.pack ()
    self.menu.place (y=c.menuMarginTop)

 # multiply columns menu
    self.frame6=tk.Frame (self)
    self.frame6.pack ()
    self.frame6.place (x=c.frameLeftMargin + c.frameRightOffset * 2, y=c.frameTopMargin + c.frameTopOffset * 3, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame6, text=c.multiplyColListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.multiplyCol = tk.StringVar (self)
    self.menu = tk.OptionMenu (self.frame6, self.multiplyCol, *c.multiplyColList, command=self.refreshOptionMenus)
    self.menu.config (width=c.menuWidth)
    self.menu.pack ()
    self.menu.place (y=c.menuMarginTop)

 # skirt menu
    self.frame7=tk.Frame (self)
    self.frame7.pack ()
    self.frame7.place (x=c.frameLeftMargin, y=c.frameTopMargin + c.frameTopOffset * 4, height=c.frameHeight, width=c.frameWidth)
    self.label=tk.Label (self.frame7, text=c.skirtListLabel, fg=c.labelColor)
    self.label.pack ()
    self.label.place (x=c.labelMarginLeft)
    self.skirtLayers = tk.StringVar (self)
    self.menu = tk.OptionMenu (self.frame7, self.skirtLayers, *c.skirtLayersList, command=self.refreshOptionMenus)
    self.menu.config (width=c.mediumMenuWidth)
    self.menu.pack ()
    self.menu.place (y=c.menuMarginTop)

  # several buttons (plenty of hard-coded controls display values…
    self.frame8=tk.Frame (self)
    self.frame8.pack ()
    self.frame8.place (x=c.frameLeftMargin, y=c.frameTopMargin + c.frameTopOffset * 5, height=c.frameHeight+200, width=c.frameWidth + 300)

    self.saveModificationsButton = tk.Button (self.frame8, text=c.saveButtonLabel, command=self.saveChanges, state=tk.DISABLED)
    self.modificationButtonState = "DISABLED"
    self.saveModificationsButton.pack ()
    self.saveModificationsButton.place (x=c.labelMarginLeft)

    self.chooseFileButton = tk.Button (self.frame8, text=c.chooseFileButtonLabel, command=self.chooseFileDialog)
    self.chooseFileButton.pack ()
    self.chooseFileButton.place (x=c.labelMarginLeft, y=40)

    self.fileToSkName = tk.StringVar()
    self.fileToSk = tk.Label (self.frame8, fg=c.fileNameColor, textvariable=self.fileToSkName)
    if (self.lastFileToCraftFullPath):
      self.fileToSkName.set (self.lastFileToCraft)
      self.fileToSkeinforgePath = self.lastFileToCraftFullPath
    else:
      self.fileToSkName.set (c.noFileSelectedText)
    self.fileToSk.pack ()
    self.fileToSk.place (x=c.labelMarginLeft+155, y=43)

    self.runSkeinforgeButton = tk.Button (self.frame8, text=c.runSkeinforgeButtonLabel, state=tk.DISABLED, command=self.runSkeinforge)
    if (self.lastFileToCraftFullPath):
      self.runSkeinforgeButton.config (state=tk.NORMAL)
    self.runSkeinforgeButton.pack()
    self.runSkeinforgeButton.place (x=c.labelMarginLeft, y=80)

    self.quitButton = tk.Button (self.frame8, text=c.quitButtonLabel, command=self.quitApplication)
    self.quitButton.pack ()
    self.quitButton.place (x=c.labelMarginLeft + 260, y=80)
  def setInterface (self):
  # set user interface controls values
  # Profile
    self.profile.set (self.profileName)
    
  # Layer Thickness
    self.layerThickness.set (self.getSkSetting (os.path.join (self.profileFullName, c.skCarveFile), self.skCarveSearchString, c.skDefaultLayerHeight))
    self.firstLayerHeight = self.layerThickness.get ()
    self.newLayerHeight = self.firstLayerHeight

  # Feed Rate
    self.feedRate.delete (0,"end")
    self.feedRate.insert (0, self.getSkSetting (os.path.join (self.profileFullName, c.skSpeedFile), self.skFeedRateSearchString, c.skDefaultFeedRate))
    self.firstFeedRate = self.feedRate.get ()
    self.newFeedRate = self.firstFeedRate

  # Flow Rate
    self.flowRate.delete (0,"end")
    self.flowRate.insert (0,self.getSkSetting (os.path.join (self.profileFullName, c.skSpeedFile), self.skFlowRateSearchString, c.skDefaultFlowRate))
    self.firstFlowRate = self.flowRate.get ()
    self.newFlowRate = self.firstFlowRate

  # First Layer
    self.firstLayerSpeed.set (self.getSkSetting (os.path.join (self.profileFullName, c.skSpeedFile), self.skFirstLayerSearchString0, c.skDefaultFirstLayerSpeed))
    self.firstFirstLayerSpeed = self.firstLayerSpeed.get ()
    self.newFirstLayerSpeed = self.firstFirstLayerSpeed    

  # Infill Solidity
    self.infillSolidity.delete (0,"end")
    self.infillSolidity.insert (0, self.ratioToPercentage (self.getSkSetting (os.path.join (self.profileFullName, c.skFillFile), self.skInfillSoliditySearchString, c.skDefaultInfillSolidity)))
    self.firstInfillSolidity = self.infillSolidity.get ()
    self.newInfillSolidity = self.firstInfillSolidity

  # Perimeter
    self.perimeterSpeed.set (self.getSkSetting (os.path.join (self.profileFullName, c.skSpeedFile), self.skPerimeterSpeedSearchString0, c.skDefaultPerimeterSpeed))
    self.firstPerimeterSpeed = self.perimeterSpeed.get ()
    self.newPerimeterSpeed = self.firstPerimeterSpeed    
    
  # Multiply on/off
    self.multiplyActivity.set (self.getSkSetting (os.path.join (self.profileFullName, c.skMultiplyFile), self.skMultiplyActivateSearchString, c.skDefaultMultiplyActivate))  
    if (self.multiplyActivity.get () == True):
      self.radio1.select ()
    else:
      self.radio2.select ()
    self.firstMultiplyActivity = self.multiplyActivity.get ()
    self.newMultiplyActivity = self.firstMultiplyActivity

  # Multiply Lines
    self.multiplyRow.set (self.getSkSetting (os.path.join (self.profileFullName, c.skMultiplyFile), self.skMultiplyRowSearchString, c.skDefaultMultiplyRow))
    self.firstMultiplyRow = self.multiplyRow.get ()
    self.newMultiplyRow = self.firstMultiplyRow

  # Multiply Columns
    self.multiplyCol.set (self.getSkSetting (os.path.join (self.profileFullName, c.skMultiplyFile), self.skMultiplyColSearchString, c.skDefaultMultiplyCol))
    self.firstMultiplyCol = self.multiplyCol.get ()
    self.newMultiplyCol = self.firstMultiplyCol

  # Skirt
    self.skirtLayers.set (self.getSkSetting (os.path.join (self.profileFullName, c.skSkirtFile), self.skSkirtLayersSearchString, c.skDefaultSkirtLayers))
    self.firstSkirtLayers = self.skirtLayers.get ()
    self.newSkirtLayers = self.firstSkirtLayers
    
  # changing first run flag
    self.firstRun = 0
  def changingProfile (self, event):
  # set controls new values when profile is changed  
    if (not self.firstRun):
      if self.modificationButtonState == "NORMAL":
        if tkMessageBox.askquestion (title=c.unSavedModificationsDialogTitle, message=c.changeProfileUnSavedModificationsMsg) == "no":
          self.profile.set (self.profileName)
          return
      self.profileName = self.profile.get()
      self.profileFullName = os.path.join (c.skProfilesDirectory, self.profileName, "")
      self.setInterface ()
      self.title ("skFrontend :: " + self.profileName)
      self.refreshOptionMenus (event)
      self.refreshSpinBoxes ()
      self.refreshFeedAndFlowRates ()
      self.refreshRadioButtons ()
      # tel Skeinforge to use new profile
      self.setSkeinforgeExtrusionProfile ()
      # save profile name into preferences file
      self.saveIntoFile (self.preferencesFile, self.lastUsedProfileRE, self.profileName)

  #-----------------------------------------------------
  # regex
  #-----------------------------------------------------
  def parenthesiBackslash (self):
  # parenthesis backslah into search expressions
  # for example parenthesis into "Infill Solidity (ratio):"
  # must be backslahed for this expression to be found by regex
    self.skCarveSearchString = self.backslash (c.skCarveSearchString)
    self.skFeedRateSearchString = self.backslash (c.skFeedRateSearchString)
    self.skFlowRateSearchString = self.backslash (c.skFlowRateSearchString)
    self.skInfillSoliditySearchString = self.backslash (c.skInfillSoliditySearchString)
    self.skMultiplyRowSearchString = self.backslash (c.skMultiplyRowSearchString)
    self.skMultiplyColSearchString = self.backslash (c.skMultiplyColSearchString)
    self.skSkirtLayersSearchString = self.backslash (c.skSkirtLayersSearchString)
    self.skSkirtActivateSearchString = self.backslash (c.skSkirtActivateSearchString)
    self.skExtrusionProfileSearchString = self.backslash (c.skExtrusionProfileSearchString)
    self.skMultiplyActivateSearchString = self.backslash (c.skMultiplyActivateSearchString)
    self.skFirstLayerSearchString0 = self.backslash (c.skFirstLayerSearchString0)
    self.skFirstLayerSearchString1 = self.backslash (c.skFirstLayerSearchString1)
    self.skFirstLayerSearchString2 = self.backslash (c.skFirstLayerSearchString2)
    self.skFirstLayerSearchString3 = self.backslash (c.skFirstLayerSearchString3)
    self.skPerimeterSpeedSearchString0 = self.backslash (c.skPerimeterSpeedSearchString0)
    self.skPerimeterSpeedSearchString1 = self.backslash (c.skPerimeterSpeedSearchString1)
  def backslash (self, str):
  # parenthesis backslash
    str = re.sub (r'\(', '\\(', str)
    str = re.sub (r'\)', '\\)', str)
    return str
  def regexCompile (self):
  #compiling regexs for skeinforge settings
    self.searchNumberRegex = "\\t([-+]?[0-9]*\\.?,?[0-9]+)"
    self.searchTrueFalseRegex = "\\t(True|False)"
    self.searchTextStringRegex = "\\t(.+)"
    self.extrusionProfileRE = re.compile (self.skExtrusionProfileSearchString + self.searchTextStringRegex)
    self.layerHeightRE = re.compile (self.skCarveSearchString + self.searchNumberRegex)
    self.feedRateRE = re.compile (self.skFeedRateSearchString + self.searchNumberRegex)
    self.flowRateRE = re.compile (self.skFlowRateSearchString + self.searchNumberRegex)
    self.infillSolidityRE = re.compile (self.skInfillSoliditySearchString + self.searchNumberRegex)
    self.multiplyRowRE = re.compile (self.skMultiplyRowSearchString + self.searchNumberRegex)
    self.multiplyColRE = re.compile (self.skMultiplyColSearchString + self.searchNumberRegex)
    self.skirtLayersRE = re.compile (self.skSkirtLayersSearchString + self.searchNumberRegex)
    self.skirtActivateRE = re.compile (self.skSkirtActivateSearchString + self.searchTrueFalseRegex)
    self.multiplyActivateRE = re.compile (self.skMultiplyActivateSearchString + self.searchTrueFalseRegex)
    self.firstLayerFeedRateInfillRE = re.compile (self.skFirstLayerSearchString0 + self.searchNumberRegex)
    self.firstLayerFeedRatePerimeterRE = re.compile (self.skFirstLayerSearchString1 + self.searchNumberRegex)
    self.firstLayerFlowRateInfillRE = re.compile (self.skFirstLayerSearchString2 + self.searchNumberRegex)
    self.firstLayerFlowRatePerimeterRE = re.compile (self.skFirstLayerSearchString3 + self.searchNumberRegex)
    self.perimeterFeedRateRE = re.compile (self.skPerimeterSpeedSearchString0 + self.searchNumberRegex)
    self.perimeterFlowRateRE = re.compile (self.skPerimeterSpeedSearchString1 + self.searchNumberRegex)

  #-----------------------------------------------------
  # tracking parameters
  #-----------------------------------------------------
  def refreshOptionMenus (self, event):
    self.newLayerHeight = self.layerThickness.get ()
    self.newMultiplyRow = self.multiplyRow.get ()
    self.newMultiplyCol = self.multiplyCol.get ()
    self.newSkirtLayers = self.skirtLayers.get ()
    self.newFirstLayerSpeed = self.firstLayerSpeed.get ()
    self.newPerimeterSpeed = self.perimeterSpeed.get ()
    self.setSaveModificationButtonState ()
  def refreshSpinBoxes (self):
    self.newFeedRate = self.feedRate.get ()
    self.newFlowRate = self.flowRate.get ()
    self.newInfillSolidity = self.infillSolidity.get ()
    self.setSaveModificationButtonState ()
    return True
  def refreshFeedAndFlowRates (self):
    self.newFeedRate = self.feedRate.get ()
    self.flowRate.delete (0,"end")
    self.flowRate.insert (0, self.newFeedRate)
    self.newFlowRate = self.flowRate.get ()
    self.setSaveModificationButtonState ()
    return True
  def refreshRadioButtons (self):
    self.newMultiplyActivity = self.multiplyActivity.get ()
    self.setSaveModificationButtonState ()
    return True
  def setSaveModificationButtonState (self):
  # we compare original with current settings values
  # self.modificationButtonState is DISABLED if no modifications.
  # its value is evaluated by quitApplication ()
  # and changingProfile ()
    if (
     self.firstLayerHeight != self.newLayerHeight
     or self.firstFeedRate != self.newFeedRate
     or self.firstFlowRate != self.newFlowRate
     or self.firstInfillSolidity != self.newInfillSolidity
     or self.firstMultiplyRow != self.newMultiplyRow
     or self.firstMultiplyCol != self.newMultiplyCol
     or self.firstSkirtLayers != self.newSkirtLayers
     or self.firstMultiplyActivity != self.newMultiplyActivity
     or self.firstFirstLayerSpeed !=  self.newFirstLayerSpeed
     or self.firstPerimeterSpeed != self.newPerimeterSpeed
     ):
      self.saveModificationsButton.config (state=tk.NORMAL)
      self.modificationButtonState = "NORMAL"
    else:
      self.saveModificationsButton.config (state=tk.DISABLED)
      self.modificationButtonState = "DISABLED"

  #-----------------------------------------------------
  # get settings
  #-----------------------------------------------------
  def getSkSetting (self, fileName, searchString, defaultReturnValue):
  # getting a skeinforge plugin parameter
    try:
      returnValue = defaultReturnValue
      p = re.compile (searchString)
      file = open (os.path.join (fileName), "r")
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
  def getLastSettings (self, fileName, compiledRE):
  # getting skFrontend preferences parameter
    returnValue = ""
    try:
      file = open (fileName, "r")
      lines = file.readlines ()
      for line in lines:
        matchObject = compiledRE.match (line)
        if matchObject:
          ligne = line.split ('=')
          returnValue = ligne[1].rstrip('\n')
          break
      file.close ()
      return returnValue
    except Exception, err:
      tkMessageBox.showerror (c.titleErrorMsgBox, "%s " % str(err))
      return 1

  #-----------------------------------------------------
  # ratio / percentage
  #-----------------------------------------------------
  def ratioToPercentage (self, n):
  # transforms ratio into percentage (ex. from 0.3 to 30)
    return int (float (n) * 100)
  def percentageToRatio (self, n):  
  # transforms percentage into ratio(ex. from 30 to 0.3)
    return str (float (n) / 100)

  #-----------------------------------------------------
  # choose file to be skeinforged dialog
  #-----------------------------------------------------
  def chooseFileDialog (self):
    self.fileToSkeinforgePath = tkFileDialog.askopenfilename (initialfile=self.lastFileToCraftFullPath, filetypes=c.openableFilesTypes)
    if self.fileToSkeinforgePath:
      (unused, self.fileToSkeinforgePathName) = os.path.split (self.fileToSkeinforgePath)
      # setting file name into label
      self.fileToSkName.set ("")
      self.fileToSkName.set (self.fileToSkeinforgePathName)
      self.runSkeinforgeButton.config (state=tk.NORMAL)
      # new file name into preferences file
      self.saveIntoFile (self.preferencesFile, self.lastFileToCraftRE, self.fileToSkeinforgePath)

  #-----------------------------------------------------
  # run Skeinforge
  #-----------------------------------------------------
  def runSkeinforge (self):
    try:
      if self.modificationButtonState == "NORMAL":
        if tkMessageBox.askquestion (title=c.unSavedModificationsDialogTitle, message=c.runSkUnSavedModificationsMsg) == "no":
          return
      os.system (c.pythonInterpreter + " " + c.skCraftPath + " " + self.fileToSkeinforgePath)
    except Exception, err:
      # the more usual error:
      tkMessageBox.showerror (c.titleErrorMsgBox, c.unASCIIerrorMessage)
      # also possible, less explicit but the real error:
      # tkMessageBox.showerror (c.titleErrorMsgBox, "%s " % str(err))
      return 1

  #-----------------------------------------------------
  # ask or not file save function for profile files '''
  #-----------------------------------------------------
  def saveChanges (self):
    # carve.csv: layer height
    if self.firstLayerHeight != self.newLayerHeight:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skCarveFile), self.layerHeightRE, self.newLayerHeight)
      self.firstLayerHeight = self.newLayerHeight

    # speed.csv: feed rate
    self.newFeedRate = self.feedRate.get ()
    if self.firstFeedRate != self.newFeedRate:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.feedRateRE, self.newFeedRate)
      self.firstFeedRate = self.newFeedRate

    # speed.csv: flow rate
    self.newFlowRate = self.flowRate.get ()
    if self.firstFlowRate != self.newFlowRate:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.flowRateRE, self.newFlowRate)
      self.firstFlowRate = self.newFlowRate

    # speed.csv: 1st layer (infill & perimeter feed & flow rates are set to the same value)
    self.newFirstLayerSpeed = self.firstLayerSpeed.get ()
    if self.firstFirstLayerSpeed != self.newFirstLayerSpeed:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.firstLayerFeedRateInfillRE, self.newFirstLayerSpeed)
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.firstLayerFeedRatePerimeterRE, self.newFirstLayerSpeed)
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.firstLayerFlowRateInfillRE, self.newFirstLayerSpeed)
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.firstLayerFlowRatePerimeterRE, self.newFirstLayerSpeed)
      self.firstFirstLayerSpeed = self.newFirstLayerSpeed

    # speed.csv: perimeter speed (perimeter feed & flow rates are set to the same value)
    self.newPerimeterSpeed = self.perimeterSpeed.get ()
    if self.firstPerimeterSpeed != self.newPerimeterSpeed:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.perimeterFeedRateRE, self.newPerimeterSpeed)
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSpeedFile), self.perimeterFlowRateRE, self.newPerimeterSpeed)
      self.firstPerimeterSpeed = self.newPerimeterSpeed

    # fill.csv: infill solidity
    self.newInfillSolidity = self.infillSolidity.get ()
    if self.firstInfillSolidity != self.newInfillSolidity:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skFillFile), self.infillSolidityRE, self.percentageToRatio (self.newInfillSolidity))
      self.firstInfillSolidity = self.newInfillSolidity

    # multiply.csv: number of rows
    if self.firstMultiplyRow != self.newMultiplyRow:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skMultiplyFile), self.multiplyRowRE, self.newMultiplyRow)
      self.firstMultiplyRow = self.newMultiplyRow

    # multiply.csv: number of columns
    if self.firstMultiplyCol != self.newMultiplyCol:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skMultiplyFile), self.multiplyColRE, self.newMultiplyCol)
      self.firstMultiplyCol = self.newMultiplyCol
      
    # multiply.csv: activate
    if self.firstMultiplyActivity != self.newMultiplyActivity:
      if self.newMultiplyActivity == 0:
        boolean = "False"
      else:
        boolean = "True"
      self.saveIntoFile (os.path.join (self.profileFullName, c.skMultiplyFile), self.multiplyActivateRE, boolean)
      self.firstMultiplyActivity = self.newMultiplyActivity

    # skirt.csv: layers to, then activate skirt or not
    if self.firstSkirtLayers != self.newSkirtLayers:
      self.saveIntoFile (os.path.join (self.profileFullName, c.skSkirtFile), self.skirtLayersRE, self.newSkirtLayers)
      self.firstSkirtLayers = self.newSkirtLayers
    if self.newSkirtLayers == "0":
      boolean = "False"
    else:
      boolean = "True"
    self.saveIntoFile (os.path.join (self.profileFullName, c.skSkirtFile), self.skirtActivateRE, boolean)
    
    self.saveModificationsButton.config (state=tk.DISABLED)
    self.modificationButtonState = "DISABLED"

  #-----------------------------------------------------
  # save changes into file
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
  # quit
  #-----------------------------------------------------
  def quitApplication (self):
    if self.modificationButtonState == "NORMAL":
      if tkMessageBox.askquestion (title=c.unSavedModificationsDialogTitle, message=c.quitAppUnSavedModificationsMsg) == "no":
        return
    print "ciao!"
    self.destroy ()

  #-----------------------------------------------------
  # tell Skeinforge to use choosen profile
  #-----------------------------------------------------
  def setSkeinforgeExtrusionProfile (self):
    # finding Skeinforge's profiles types directory (not extrusion profiles directory)
    (skProfilesTypePath, tail) =  os.path.split (c.skProfilesDirectory)
    if (not tail):   # tail is empty if c.skProfilesDirectory ends with a path separator
      (skProfilesTypePath, tail) =  os.path.split (skProfilesTypePath)
    
    self.saveIntoFile (os.path.join (skProfilesTypePath, c.skExtrusionFile), self.extrusionProfileRE, self.profileName)

  #-----------------------------------------------------
  # test of config.py mandatory settings
  #-----------------------------------------------------
  def configPyTests (self):
  # tests of config.py settings

    errorMsg = ""    

    # no valid path to craft.py
    (unused, tail) =  os.path.split (c.skCraftPath)
    if (not os.path.isfile (c.skCraftPath) or tail != c.skCraftFileName):
      errorMsg = c.noPathToCraftPyErrorMsg

    # no valid default profile
    if not (os.path.isdir (os.path.join (c.skProfilesDirectory, c.skDefaultProfileName))):
      errorMsg = c.noExtrusionProfileErrorMsg
      
    # no valid path to profiles
    if (not os.path.isdir (c.skProfilesDirectory)):
      errorMsg = c.noProfilesDirectoryErrorMsg

    if (errorMsg):
      tkMessageBox.showerror (sys.argv[0], errorMsg)
      self.destroy ()

  #-----------------------------------------------------
  # test preferences file existence
  #-----------------------------------------------------
  def preferencesFileTest (self):
    if (not os.path.isfile (self.preferencesFile)):
      tkMessageBox.showerror (sys.argv[0], c.noPreferencesFileErrorMsg)
      self.destroy ()

#-----------------------------------------------------
#-----------------------------------------------------
#-----------------------------------------------------

if __name__ == "__main__":
  app = SkFrontend ()
  app.mainloop ()
