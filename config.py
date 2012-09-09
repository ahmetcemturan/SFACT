# -*- coding: utf-8 -*-

# config.py - v1.0 - 2012-08-31
# config.py is imported by skFrontend.py
#
# German text strings translation thanks to Markus Hitter
import skFrontend as SFront
import os
#-----------------------------------------------------
''' two mandatory parameters to be adapted
	to your Skeinforge configuration '''
#-----------------------------------------------------

# absolute path to Skeinforge's craft.py:
# Linux sample: "/opt/50_reprap_python_beanshell/skeinforge_application/skeinforge_plugins/craft.py"
# OS X sample: "/Applications/50_reprap_python_beanshell/skeinforge_application/skeinforge_plugins/craft.py"
# Windows: better to double backslashes
# Windows sample: "C:\\50_reprap_python_beanshell\\skeinforge_application\\skeinforge_plugins\\craft.py"

print ("Current working dir : %s\\skeinforge_application\\skeinforge_plugins\\craft.py" % os.getcwdu())
#skCraftPath = os.path.join(os.getcwd(), '\\skeinforge_application\\skeinforge_plugins\\craft.py')
skCraftPath = ("%s\\skeinforge_application\\skeinforge_plugins\\craft.py" % os.getcwdu())
#"%s%s" os.getcwd(),%s (\\skeinforge_application\\)
#skCraftPath = "C:\\Users\\Ahmet\\Documents\\GitHub\\SFACT\\skeinforge_application\\skeinforge_plugins"


# absolute path to Skeinforge's extrusion profile used by skFrontend (no ending slash):
# Linux sample: "/home/userName/.skeinforge/profiles/extrusion/profileName"
# OS X sample: "/Users/userName/.skeinforge/profiles/extrusion/profileName"
# Windows: better to double backslashes
# Windows sample: "C:\\Users\\userName\\.skeinforge\\profiles\\extrusion\\profileName"
# Windows sample: "C:\\Documents and Settings\\userName\\.skeinforge\\profiles\\extrusion\\profileName"
#globalTemporarySettingsPath = os.path.join(os.path.expanduser('~'), '.skeinforge')
#skProfileDirectory = os.path.join(os.getcwd(), '\\sfact_profiles\\profiles\\\extrusion\\Default\\')
skProfileDirectory =  ("%s\\sfact_profiles\\profiles\\extrusion\\Default" % os.getcwdu())
#skProfileDirectory =  ("%s \\.skeinforge\\profiles\\extrusion\\PLA" % os.path.join(os.path.expanduser('~'))

#-----------------------------------------------------
''' controls configuration to be adapted to your usage '''
#-----------------------------------------------------

# default directory where to find STL files to be skeinforged:
STLFilesDefaultDirectory = ""

# interface language
# set to "fr" for french, "en" for english, "de" for german
interfaceLanguage = "en"

# carve plugin: list of layer thicknesses into drop-down menu:
layerHeightList = ("0.2", "0.25", "0.3", "0.4", "0.5")

# carve plugin: list of edge widths into drop-down menu:
edgeWidthList = ("0.2", "0.25", "0.33", "0.4", "0.45", "0.5", "0.55", "0.6", "0.7",0.8)

# speed plugin: feed rate min & max values into spinboxes:
# Skeinforge defaults to 2 & 50
feedRateMinimumValue = 2
feedRateMaximumValue = 50

#  multiply plugin: numbers of rows and columns into drop-down menus:
multiplyRowList = range (1,6)
multiplyColList = range (1,6)

# skirt plugin: number of layers into drop-down menu:
skirtLayersList = range (21)

#-----------------------------------------------------
''' text strings french version '''
#-----------------------------------------------------

if interfaceLanguage == "fr":
  thicknessListLabel = "Hauteur des couches"
  infillFeedRateListLabel = "Vitesse (mm/s)"
  InfillSolidityListLabel = "Remplissage (%)"
  multiplyRowListLabel = "Nb de lignes"
  multiplyColListLabel = "Nb de colonnes"
  skirtLayersListLabel = "Entourage (nb couches)"
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
  noExtrusionProfileErrorMsg = "Le profil d’extrusion déclaré dans config.py n’existe pas… !"

#-----------------------------------------------------
''' text strings english version '''
#-----------------------------------------------------

if interfaceLanguage == "en":
  thicknessListLabel = "Layer Height"
  edgeWidthListLabel = "Edge Width"
  infillFeedRateListLabel = "Infill Speed (mm/sec)"
  perimeterFeedRateListLabel = "Edge Speed (mm/sec)"
  InfillSolidityListLabel = "Infill Solidity (%)"
  EdgeShellsListLabel = "Number of Shells "
  BottomsListLabel = "Number of Tops/bottoms "
  multiplyRowListLabel = "Lines Nb"
  multiplyColListLabel = "Columns Nb"
  skirtLayersListLabel = "Number of Skirt Layers"
  skirtRingsListLabel = "Number of Skirt Rings"
  saveButtonLabel = "Save Modifications"
  chooseFileButtonLabel = "What to Skeinforge?"
  noFileSelectedText = "No File Selected"
  runSkeinforgeButtonLabel = " >> G-code via Python"
  runPyPyButtonLabel = " >> G-code via PyPy"
  quitButtonLabel = "Quit"
  titleErrorMsgBox = "Error"
  unASCIIerrorMessage = "Warning, no non-ASCII symbol into path or file name!"
  unSavedModificationsDialogTitle = "Unsaved Modifications"
  runSkUnSavedModificationsMsg = "Some modifications aren't saved,\nrun Skeinforge anyway?"
  quitAppUnSavedModificationsMsg = "Some modifications aren't saved,\nquit skFrontend anyway?"
  noExtrusionProfileErrorMsg = "Extrusion profile set into config.py don't exists… !"


#-----------------------------------------------------
''' text strings german version '''
#-----------------------------------------------------

if interfaceLanguage == "de":
  thicknessListLabel = "Layerdicke"
  infillFeedRateListLabel = "Geschwindigkeit"
  InfillSolidityListLabel = "Füllgrad (%)"
  multiplyRowListLabel = "Zeilen"
  multiplyColListLabel = "Spalten"
  skirtLayersListLabel = "Vorhang-Schichten"
  saveButtonLabel = "Änderungen speichern"
  chooseFileButtonLabel = "Bauteil laden"
  noFileSelectedText = "Keine Datei"
  runSkeinforgeButtonLabel = "G-code generieren"
  quitButtonLabel = "Beenden"
  titleErrorMsgBox = "Fehler"
  unASCIIerrorMessage = "Warnung, nicht-ASCII-Zeichen sind im Pfad nicht erlaubt."
  unSavedModificationsDialogTitle = "Ungespeicherte Änderungen"
  runSkUnSavedModificationsMsg = "Änderungen wurden noch nicht gespeichert,\nSkeinforge trotzdem starten?"
  quitAppUnSavedModificationsMsg = "Änderungen wurden noch nicht gespeichert,\nskFrontend trotzdem beenden?"
  noExtrusionProfileErrorMsg = "Das in config.py deklarierte Profil existiert nicht."

#-----------------------------------------------------
''' skeinforge parameters to be only modified if
	Skeinforge changes (names of files, search strings values…)
	Currently Skeinforge 50 '''
#-----------------------------------------------------

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

skFillFile = "fill.csv"
skInfillSoliditySearchString = "Infill Solidity (ratio):"

skMultiplyFile = "multiply.csv"
skMultiplyRowSearchString = "Number of Rows (integer):"
skMultiplyColSearchString = "Number of Columns (integer):"

skSkirtFile = "skirt.csv"
skSkirtLayersSearchString = "Layers To (index):"
skSkirtActivateSearchString = "Activate Skirt"

#-----------------------------------------------------
''' default values below are only used if no valid values
	are found into plugins configuration files '''
#-----------------------------------------------------

# default layer height for carve plugin:
skDefaultLayerHeight = "0.4"
# default edge Width for carve plugin:
skDefaultEdgeWidth = "0.45"
# default feed rates for speed plugin:
skDefaultFeedRate = "16.0"

# default infill solidity for fill plugin:
skDefaultInfillSolidity = "0.35"

# default columns & rows numbers for multiply plugin:
skDefaultMultiplyCol = 1
skDefaultMultiplyRow = 1

# default layers number for skirt plugin:
skDefaultSkirtLayers = 1

#-----------------------------------------------------
''' files types to be opened '''
#-----------------------------------------------------

openableFilesTypes = [("Stereolithography", ".stl"), ("GNU Triangulated Surface", ".gts"), ("Wavefront 3D Object", ".obj"), ("Scalable Vector Graphics", ".svg"), ("Extensible Markup Language", ".xml")]

#-----------------------------------------------------
''' display configuration '''
#-----------------------------------------------------

windowWidth = "380"
windowHeight= "600"
frameLeftMargin = 25
frameTopMargin = 15
frameHeight = 50
frameWidth = 200
frameTopOffset = 60
frameRightOffset = 130
labelMarginLeft = 2
labelColor = "blue"
fileNameColor = "#EC9808"
menuMarginTop = 20
menuWidth = 8

  