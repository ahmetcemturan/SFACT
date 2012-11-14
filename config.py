# -*- coding: utf-8 -*-

# config.py - v1.3 - 2012-11-09
# config.py is imported by skFrontend.py
# 
# German text strings translation thanks to Markus Hitter

#-----------------------------------------------------
''' three *mandatory* parameters to be adapted 
    to your Skeinforge configuration '''
#-----------------------------------------------------

# absolute path to Skeinforge's craft.py:
#   Linux sample: "/opt/50_reprap_python_beanshell/skeinforge_application/skeinforge_plugins/craft.py"
#   OS X sample: "/Applications/50_reprap_python_beanshell/skeinforge_application/skeinforge_plugins/craft.py"
#   Windows: better to double backslashes
#   Windows sample: "C:\\50_reprap_python_beanshell\\skeinforge_application\\skeinforge_plugins\\craft.py"
skCraftPath = "/xxx/skeinforge_application/skeinforge_plugins/craft.py"

# absolute path to Skeinforge's extrusion profile directory:
# (profiles used by Skeinforge and then skFrontend are into this directory)
#   Linux sample: "/home/userName/.skeinforge/profiles/extrusion"
#   OS X sample: "/Users/userName/.skeinforge/profiles/extrusion"
#   Windows: better to double backslashes
#   Windows sample: "C:\\Users\\userName\\.skeinforge\\profiles\\extrusion"
#   Windows sample: "C:\\Documents and Settings\\userName\\.skeinforge\\profiles\\extrusion"
skProfilesDirectory = "/xxx/.skeinforge/profiles/extrusion"

# name of the default profile used by skFrontend
# this profile must exists as a directory into your skProfilesDirectory
skDefaultProfileName = ""

#-----------------------------------------------------
''' controls configuration to be adapted to your usage,
    not mandatory  '''
#-----------------------------------------------------

# interface language
# set to "fr" for french, "en" for english, "de" for german
interfaceLanguage = "en"

# name of your Python interpreter, defaults to "python"
# set to "pypy" or another interpreter if needed
pythonInterpreter = "python"

# default directory where to find STL files to be skeinforged:
STLFilesDefaultDirectory = ""

# carve plugin: list of layer thicknesses into drop-down menu: 
layerThicknessList = ("0.10", "0.15", "0.20", "0.25", "0.30", "0.35", "0.40", "0.45", "0.50")

# speed plugin: feed rate min & max values into spinboxes:
# Skeinforge defaults to 2 & 50
feedRateMinimumValue = 2
feedRateMaximumValue = 50

# speed plugin: 1st layer speed value into drop-down menu:
firstLayerSpeedList = ("0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0")

# speed plugin: perimeter speed value into drop-down menu:
perimeterSpeedList = ("0.1", "0.2", "0.3", "0.4", "0.5", "0.6", "0.7", "0.8", "0.9", "1.0")

# speed plugin: flow rate min & max values into spinboxes:
# Skeinforge defaults to 50 & 250
flowRateMinimumValue = 1.0
flowRateMaximumValue = 250.0

#  multiply plugin: numbers of rows and columns into drop-down menus:
multiplyRowList = range (1,6)
multiplyColList = range (1,6)

# skirt plugin: number of layers into drop-down menu:
skirtLayersList = range (21)

#-----------------------------------------------------
''' text strings french version '''
#-----------------------------------------------------

if interfaceLanguage == "fr":
  profilesListLabel = "Profil"
  thicknessListLabel = "Couches (mm)"
  feedRateListLabel = "Vitesse (mm/s)"
  flowRateListLabel = "Débit"
  firstLayerLabel = "1re couche"
  InfillSolidityListLabel = "Remplissage (%)"
  perimeterLabel = "Périmètre"
  multiplyRowListLabel = "Lignes"
  multiplyColListLabel = "Colonnes"
  multiplyActivityLabel = "Multiply"
  skirtListLabel = "Entourage"
  saveButtonLabel = "Enregistrer les modifications"
  chooseFileButtonLabel = "Skeinforger quoi ?"
  noFileSelectedText = "Pas de fichier choisi"
  runSkeinforgeButtonLabel = "Générer le G-code"
  quitButtonLabel = "Quitter"
  titleErrorMsgBox = "Erreur"
  unASCIIerrorMessage = "Attention, pas de caractère non-ASCII dans le chemin et le nom du fichier !"
  unSavedModificationsDialogTitle = "Modifications non enregistrées"
  runSkUnSavedModificationsMsg = "Des modifications ne sont pas enregistrées, lancer Skeinforge tout de même ?"
  quitAppUnSavedModificationsMsg = "Des modifications ne sont pas enregistrées, quitter skFrontend tout de même ?"
  changeProfileUnSavedModificationsMsg = "Des modifications ne sont pas enregistrées, changer de profil tout de même ?"
  noProfilesDirectoryErrorMsg = "config.py : mauvais paramètre \" skProfilesDirectory \""
  noExtrusionProfileErrorMsg = "config.py : mauvais paramètre \" skDefaultProfileName \""
  noPathToCraftPyErrorMsg = "config.py : mauvais paramètre \" skCraftPath \""
  noPreferencesFileErrorMsg = "Fichier de préférences non trouvé"

#-----------------------------------------------------
''' text strings english version '''
#-----------------------------------------------------

if interfaceLanguage == "en":
  profilesListLabel = "Profile"
  thicknessListLabel = "Layer Height"
  feedRateListLabel = "Speed Rate"
  flowRateListLabel = "Flow Rate"
  firstLayerLabel = "1st Layer"
  InfillSolidityListLabel = "Infill Solidity (%)"
  perimeterLabel = "Perimeter"
  multiplyRowListLabel = "Lines"
  multiplyColListLabel = "Columns"
  multiplyActivityLabel = "Multiply"
  skirtListLabel = "Skirt Layers"
  saveButtonLabel = "Save Modifications"
  chooseFileButtonLabel = "What to Skeinforge?"
  noFileSelectedText = "No File Selected"
  runSkeinforgeButtonLabel = "Generate G-code"
  quitButtonLabel = "Quit"
  titleErrorMsgBox = "Error"
  unASCIIerrorMessage = "Warning, no non-ASCII symbol into path or file name!"
  unSavedModificationsDialogTitle = "Unsaved Modifications"
  runSkUnSavedModificationsMsg = "Some modifications aren't saved, run Skeinforge anyway?"
  quitAppUnSavedModificationsMsg = "Some modifications aren't saved, quit skFrontend anyway?"
  changeProfileUnSavedModificationsMsg = "Some modifications aren't saved, change profile anyway?"
  noProfilesDirectoryErrorMsg = "config.py: bad parameter \"skProfilesDirectory\""
  noExtrusionProfileErrorMsg = "config.py: bad parameter \"skDefaultProfileName\""
  noPathToCraftPyErrorMsg = "config.py: bad parameter \"skCraftPath\""
  noPreferencesFileErrorMsg = "Preferences file not found"

#-----------------------------------------------------
''' text strings german version '''
#-----------------------------------------------------

if interfaceLanguage == "de":
  profilesListLabel = "Profil"
  thicknessListLabel = "Layerdicke"
  feedRateListLabel = "Geschwindigkeit"
  flowRateListLabel = "Materialfluss"
  firstLayerLabel = "Erste Schicht"
  InfillSolidityListLabel = "Füllgrad (%)"
  perimeterLabel = "Umfang"
  multiplyRowListLabel = "Zeilen"
  multiplyColListLabel = "Spalten"
  multiplyActivityLabel = "Multiply"
  skirtListLabel = "Vorhang-Schichten"
  saveButtonLabel = "Änderungen speichern"
  chooseFileButtonLabel = "Bauteil laden"
  noFileSelectedText = "Keine Datei"
  runSkeinforgeButtonLabel = "G-code generieren"
  quitButtonLabel = "Beenden"
  titleErrorMsgBox = "Fehler"
  unASCIIerrorMessage = "Warnung, nicht-ASCII-Zeichen sind im Pfad nicht erlaubt."
  unSavedModificationsDialogTitle = "Ungespeicherte Änderungen"
  runSkUnSavedModificationsMsg = "Änderungen wurden noch nicht gespeichert, Skeinforge trotzdem starten?"
  quitAppUnSavedModificationsMsg = "Änderungen wurden noch nicht gespeichert, skFrontend trotzdem beenden?"
  changeProfileUnSavedModificationsMsg = "Änderungen wurden noch nicht gespeichert, Profil ändern sowieso?"
  noProfilesDirectoryErrorMsg = "config.py: Falscher Parameter \"skProfilesDirectory\""
  noExtrusionProfileErrorMsg = "config.py: Falscher Parameter \"skDefaultProfileName\""
  noPathToCraftPyErrorMsg = "config.py: Falscher Parameter \"skCraftPath\""
  noPreferencesFileErrorMsg = "Preferences Datei nicht gefunden"

#-----------------------------------------------------
''' skeinforge parameters to be only modified if
    Skeinforge changes (names of files, search strings values…)
    Currently Skeinforge 50 '''
#-----------------------------------------------------

# name of craft file
skCraftFileName = "craft.py"

# name of Skeinforge's extrusion profile setup file:
skExtrusionFile = "extrusion.csv"
# string to search to identify profile's name:
skExtrusionProfileSearchString = "Profile Selection:"

# name of carve plugin configuration file:
skCarveFile = "carve.csv"
# text to be searched into "skCarveFile" to identify layer height:
skCarveSearchString = "Layer Height (mm):"

# idem for others plugins files:
skSpeedFile = "speed.csv"
skFeedRateSearchString = "Feed Rate (mm/s):"
skFlowRateSearchString = "Flow Rate Setting (float):"
skFirstLayerSearchString0 = "Object First Layer Feed Rate Infill Multiplier (ratio):"
skFirstLayerSearchString1 = "Object First Layer Feed Rate Perimeter Multiplier (ratio):"
skFirstLayerSearchString2 = "Object First Layer Flow Rate Infill Multiplier (ratio):"
skFirstLayerSearchString3 = "Object First Layer Flow Rate Perimeter Multiplier (ratio):"
skPerimeterSpeedSearchString0 = "Perimeter Feed Rate Multiplier (ratio):"
skPerimeterSpeedSearchString1 = "Perimeter Flow Rate Multiplier (ratio):"

skFillFile = "fill.csv"
skInfillSoliditySearchString = "Infill Solidity (ratio):"

skMultiplyFile = "multiply.csv"
skMultiplyActivateSearchString = "Activate Multiply"
skMultiplyRowSearchString = "Number of Rows (integer):"
skMultiplyColSearchString = "Number of Columns (integer):"

skSkirtFile = "skirt.csv"
skSkirtActivateSearchString = "Activate Skirt"
skSkirtLayersSearchString = "Layers To (index):"

#-----------------------------------------------------
''' default values below are only used if no valid values
    are found into plugins configuration files '''
#-----------------------------------------------------

# default layer height for carve plugin:
skDefaultLayerHeight = "0.4"

# default 1st layer speed for speed plugin:
skDefaultFirstLayerSpeed = "1"

# default perimeter speed for speed plugin:
skDefaultPerimeterSpeed = "1"

# default feed & flow rates for speed plugin:
skDefaultFeedRate = "16.0"
skDefaultFlowRate = "16.0"

# default infill solidity for fill plugin:
skDefaultInfillSolidity = "0.35"

# default columns & rows numbers for multiply plugin:
skDefaultMultiplyCol = 1
skDefaultMultiplyRow = 1
skDefaultMultiplyActivate = 0

# default layers number for skirt plugin:
skDefaultSkirtLayers = 1

#-----------------------------------------------------
''' files types to be opened '''
#-----------------------------------------------------

openableFilesTypes = [("Stereolithography", ".stl"), ("GNU Triangulated Surface", ".gts"), ("Wavefront 3D Object", ".obj"), ("Scalable Vector Graphics", ".svg"), ("Extensible Markup Language", ".xml")]

#-----------------------------------------------------
''' names of files '''
#-----------------------------------------------------

preferencesFileName = "preferences"

#-----------------------------------------------------
''' display configuration '''
#-----------------------------------------------------

windowWidth = "380"
windowHeight= "450"
frameLeftMargin = 25
frameTopMargin = 15
frameHeight = 50
frameWidth = 200
frameTopOffset = 60
frameRightOffset = 120
labelMarginLeft = 2
labelColor = "blue"
fileNameColor = "#EC9808"
menuMarginTop = 20
menuWidth = 5
mediumMenuWidth = 6
largeMenuWidth = 8
superLargeMenuWidth = 20
