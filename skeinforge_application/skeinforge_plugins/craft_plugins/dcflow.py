#! /usr/bin/env python
"""
This page is in the table of contents.
Dcflow adds Adrian's extruder distance E value to the gcode movement lines, as described at:
http://blog.reprap.org/2009/05/4d-printing.html

and in Erik de Bruijn's conversion script page at:
http://objects.reprap.org/wiki/3D-to-5D-Gcode.php

The dcflow manual page is at:
http://fabmetheus.crsndoo.com/wiki/index.php/Skeinforge_Dcflow

Nophead wrote an excellent article on how to set the filament parameters:
http://hydraraptor.blogspot.com/2011/03/spot-on-flow-rate.html

==Operation==
The default 'Activate Dcflow' checkbox is off.  When it is on, the functions described below will work, when it is off, the functions will not be called.

==Settings==
===Extrusion Distance Format Choice===
Default is 'Absolute Extrusion Distance' because in Adrian's description the distance is absolute.  In future, because the relative distances are smaller than the cumulative absolute distances, hopefully the firmaware will be able to use relative distance.

====Absolute Extrusion Distance====
When selected, the extrusion distance output will be the total extrusion distance to that gcode line.

====Relative Extrusion Distance====
When selected, the extrusion distance output will be the extrusion distance from the last gcode line.

===Extruder Retraction Speed===
Default is 13.3 mm/s.

Defines the extruder retraction feed rate.

===Filament===
====Filament Diameter====
Default is 2.8 millimeters.

Defines the filament diameter.

====Filament Packing Density====
Default is 0.85.  This is for ABS.

Defines the effective filament packing density.

The default value is so low for ABS because ABS is relatively soft and with a pinch wheel extruder the teeth of the pinch dig in farther, so it sees a smaller effective diameter.  With a hard plastic like PLA the teeth of the pinch wheel don't dig in as far, so it sees a larger effective diameter, so feeds faster, so for PLA the value should be around 0.97.  This is with Wade's hobbed bolt.  The effect is less significant with larger pinch wheels.

Overall, you'll have to find the optimal filament packing density by experiment.

===Retraction Distance===
Default is zero.

Defines the retraction distance when the thread ends.

===Restart Extra Distance===
Default is zero.

Defines the restart extra distance when the thread restarts.  The restart distance will be the retraction distance plus the restart extra distance.

==Examples==
The following examples dcflow the file Screw Holder Bottom.stl.  The examples are run in a terminal in the folder which contains Screw Holder Bottom.stl and dcflow.py.

> python dcflow.py
This brings up the dcflow dialog.

> python dcflow.py Screw Holder Bottom.stl
The dcflow tool is parsing the file:
Screw Holder Bottom.stl
..
The dcflow tool has created the file:
.. Screw Holder Bottom_dcflow.gcode

"""

#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from datetime import date
from fabmetheus_utilities.fabmetheus_tools import fabmetheus_interpret
from fabmetheus_utilities.geometry.solids import triangle_mesh
from fabmetheus_utilities import archive
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import gcodec
from fabmetheus_utilities import intercircle
from fabmetheus_utilities import settings
from skeinforge_application.skeinforge_utilities import skeinforge_craft
from skeinforge_application.skeinforge_utilities import skeinforge_polyfile
from skeinforge_application.skeinforge_utilities import skeinforge_profile
import math
import os
import sys


__author__ = 'Enrique Perez (perez_enrique@yahoo.com) modifed as SFACT by Ahmet Cem Turan (ahmetcemturan@gmail.com)'
__date__ = '$Date: 2008/02/05 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def getCraftedText( fileName, gcodeText = '', repository=None):
	'Dcflow a gcode file or text.'
	return getCraftedTextFromText( archive.getTextIfEmpty(fileName, gcodeText), repository )

def getCraftedTextFromText(gcodeText, repository=None):
	'Dcflow a gcode text.'
	if gcodec.isProcedureDoneOrFileIsEmpty( gcodeText, 'dcflow'):
		return gcodeText
	if repository == None:
		repository = settings.getReadRepository( DcflowRepository() )
	if not repository.activateDcflow.value:
		return gcodeText
	return DcflowSkein().getCraftedGcode(gcodeText, repository)

def getNewRepository():
	'Get new repository.'
	return DcflowRepository()

def writeOutput(fileName, shouldAnalyze=True):
	'Dcflow a gcode file.'
	skeinforge_craft.writeChainTextWithNounMessage(fileName, 'dcflow', shouldAnalyze)

class DcflowRepository:
	'A class to handle the dcflow settings.'
	def __init__(self):
		'Set the default settings, execute title & settings fileName.'
		skeinforge_profile.addListsToCraftTypeRepository('skeinforge_application.skeinforge_plugins.craft_plugins.dcflow.html', self )
		self.fileNameInput = settings.FileNameInput().getFromFileName( fabmetheus_interpret.getGNUTranslatorGcodeFileTypeTuples(), 'Open File for Dcflow', self, '')
		self.openWikiManualHelpPage = settings.HelpPage().getOpenFromAbsolute('http://fabmetheus.crsndoo.com/wiki/index.php/Skeinforge_Dcflow')
		self.activateDcflow = settings.BooleanSetting().getFromValue('Activate Dcflow', self, False )
		self.activateDCExtruderFlowScale = settings.BooleanSetting().getFromValue('Activate DC Extruder Flow scaling (DC Extruders)', self, True )
		settings.LabelSeparator().getFromRepository(self)
		self.filamentDiameter = settings.FloatSpin().getFromValue(1.5, 'Filament Diameter (mm):', self, 3.5, 2.8)
		self.filamentPackingDensity = settings.FloatSpin().getFromValue(0.7, 'Extruder Flow Correction (ratio) lower=more extrusion:', self, 1.0, 1.00)
		self.activateCalibration = settings.BooleanSetting().getFromValue('Are You Calibrating?', self, False )
		self.MeasuredXSection = settings.FloatSpin().getFromValue(0.20, 'Measured Width of Extrusion:', self, 2.0, 0.5)
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- Fighting Oooze -', self )
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- Filament Retraction Settings -', self )
		self.retractionDistance = settings.FloatSpin().getFromValue( 0.00, 'Retraction Distance (millimeters):', self, 3.00, 1.00 )
		self.restartExtraDistance = settings.FloatSpin().getFromValue( -0.50, 'Restart Extra Distance (millimeters):', self, 0.50, 0.00 )
		self.extruderRetractionSpeed = settings.FloatSpin().getFromValue( 5.0, 'Extruder Retraction Speed (mm/s):', self, 50.0, 15.0 )
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- When to retract ? -', self )
		self.retractWhenCrossing = settings.BooleanSetting().getFromValue('Force to retract when crossing over spaces', self, True)
		self.minimumExtrusionForRetraction = settings.FloatSpin().getFromValue(0.0, 'Minimum Extrusion before Retraction (millimeters):', self, 2.0, 1.0)
		self.minimumTravelForRetraction = settings.FloatSpin().getFromValue(0.0, 'Minimum Travelmove after Retraction (millimeters):', self, 2.0, 1.0)
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- Firmware Related Stuff -', self )
		extrusionDistanceFormatLatentStringVar = settings.LatentStringVar()
		self.extrusionDistanceFormatChoiceLabel = settings.LabelDisplay().getFromName('Extrusion Values should be: ', self )
		settings.Radio().getFromRadio( extrusionDistanceFormatLatentStringVar, 'in Absolute units', self, True )
		self.relativeExtrusionDistance = settings.Radio().getFromRadio( extrusionDistanceFormatLatentStringVar, 'in Relative units', self, False )
		settings.LabelSeparator().getFromRepository(self)
		self.executeTitle = 'Dcflow'

	def execute(self):
		'Dcflow button has been clicked.'
		fileNames = skeinforge_polyfile.getFileOrDirectoryTypesUnmodifiedGcode(self.fileNameInput.value, fabmetheus_interpret.getImportPluginFileNames(), self.fileNameInput.wasCancelled)
		for fileName in fileNames:
			writeOutput(fileName)


class DcflowSkein:
	'A class to dcflow a skein of extrusions.'
	def __init__(self):
		'Initialize.'
		self.absoluteDistanceMode = True
		self.boundaryLayers = []
		self.distanceFeedRate = gcodec.DistanceFeedRate()
		self.feedRateMinute = None
		self.isExtruderActive = False
		self.layerIndex = -1
		self.lineIndex = 0
		self.maximumZTravelFeedRatePerSecond = None
		self.oldLocation = None
		self.operatingFlowRate = None
		self.retractionRatio = 1.0
		self.totalExtrusionDistance = 0.0
		self.travelFeedRatePerSecond = None
		self.zDistanceRatio = 5.0
		self.oldFlowRateString = None

	def addLinearMoveExtrusionDistanceLine( self, extrusionDistance ):
		'Get the extrusion distance string from the extrusion distance.'
		self.distanceFeedRate.output.write('G1 F%s\n' % self.extruderRetractionSpeedMinuteString )
		self.distanceFeedRate.output.write('G1%s\n' % self.getExtrusionDistanceStringFromExtrusionDistance( extrusionDistance ) )
		self.distanceFeedRate.output.write('G1 F%s\n' % self.distanceFeedRate.getRounded( self.feedRateMinute ) )

	def getCraftedGcode(self, gcodeText, repository):
		'Parse gcode text and store the dcflow gcode.'
		self.repository = repository
		filamentRadius = 0.5 * repository.filamentDiameter.value
		xSectionCorrector = repository.MeasuredXSection.value
		filamentPackingArea = math.pi * filamentRadius * filamentRadius * repository.filamentPackingDensity.value
		self.minimumExtrusionForRetraction = self.repository.minimumExtrusionForRetraction.value
		self.minimumTravelForRetraction = self.repository.minimumTravelForRetraction.value
		self.doubleMinimumTravelForRetraction = self.minimumTravelForRetraction + self.minimumTravelForRetraction
		self.lines = archive.getTextLines(gcodeText)
		self.parseInitialization()
		if self.repository.retractWhenCrossing.value:
			self.parseBoundaries()
		self.calibrationFactor = 1
		if repository.activateCalibration.value:
			self.calibrationFactor = (((self.layerThickness**2/4)*math.pi)+self.layerThickness*(xSectionCorrector -self.layerThickness))/(((self.layerThickness**2/4)*math.pi)+self.layerThickness *(self.perimeterWidth-self.layerThickness))
		self.newfilamentPackingDensity = repository.filamentPackingDensity.value * self.calibrationFactor
		print('****************Filament Packing Density (For Calibration)**********************:')
		print( 'Filament Packing Density (For Calibration) STEPPER EXTRUDERS ONLY :', self.newfilamentPackingDensity )
		print('****************Filament Packing Density (For Calibration)**********************:')
		self.flowScaleSixty = 60.0 * ((((self.layerThickness+self.perimeterWidth)/4) ** 2 * math.pi )/filamentPackingArea) / self.calibrationFactor
		if self.calibrationFactor is None:
			print('Mesaured extrusion width cant be 0, either un-check calibration or set measured width to what you have measured!')			
		if self.operatingFlowRate == None:
			print('There is no operatingFlowRate so dcflow will do nothing.')
			return gcodeText
		self.restartDistance = self.repository.retractionDistance.value + self.repository.restartExtraDistance.value
		self.extruderRetractionSpeedMinuteString = self.distanceFeedRate.getRounded(60.0 * self.repository.extruderRetractionSpeed.value)
		if self.maximumZTravelFeedRatePerSecond != None and self.travelFeedRatePerSecond != None:
			self.zDistanceRatio = self.travelFeedRatePerSecond / self.maximumZTravelFeedRatePerSecond
		for lineIndex in xrange(self.lineIndex, len(self.lines)):
			self.parseLine( lineIndex )
		return self.distanceFeedRate.output.getvalue()

	def getDcflowedArcMovement(self, line, splitLine):
		'Get a dcflowed arc movement.'
		if self.oldLocation == None:
			return line
		relativeLocation = gcodec.getLocationFromSplitLine(self.oldLocation, splitLine)
		self.oldLocation += relativeLocation
		distance = gcodec.getArcDistance(relativeLocation, splitLine)
		return line + self.getExtrusionDistanceString(distance, splitLine)

	def getDcflowedLinearMovement( self, line, splitLine ):
		'Get a dcflowed linear movement.'
		distance = 0.0
		if self.absoluteDistanceMode:
			location = gcodec.getLocationFromSplitLine(self.oldLocation, splitLine)
			if self.oldLocation != None:
				distance = abs( location - self.oldLocation )
			self.oldLocation = location
		else:
			if self.oldLocation == None:
				print('Warning: There was no absolute location when the G91 command was parsed, so the absolute location will be set to the origin.')
				self.oldLocation = Vector3()
			location = gcodec.getLocationFromSplitLine(None, splitLine)
			distance = abs( location )
			self.oldLocation += location
		return line + self.getExtrusionDistanceString( distance, splitLine )

	def getDistanceToNextThread(self, lineIndex):
		'Get the travel distance to the next thread.'
		if self.oldLocation == None:
			return None
		isActive = False
		location = self.oldLocation
		for afterIndex in xrange(lineIndex + 1, len(self.lines)):
			line = self.lines[afterIndex]
			splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
			firstWord = gcodec.getFirstWord(splitLine)
			if firstWord == 'G1':
				if isActive:
					location = gcodec.getLocationFromSplitLine(location, splitLine)
					if self.repository.retractWhenCrossing.value:
						locationEnclosureIndex = self.getSmallestEnclosureIndex(location.dropAxis())
						if locationEnclosureIndex != self.getSmallestEnclosureIndex(self.oldLocation.dropAxis()):
							return None
					locationMinusOld = location - self.oldLocation
					xyTravel = abs(locationMinusOld.dropAxis())
					zTravelMultiplied = locationMinusOld.z * self.zDistanceRatio
					return math.sqrt(xyTravel * xyTravel + zTravelMultiplied * zTravelMultiplied)
			elif firstWord == 'M101':
				isActive = True
			elif firstWord == 'M103':
				isActive = False
		return None

	def getExtrusionDistanceString( self, distance, splitLine ):
		'Get the extrusion distance string.'
		self.feedRateMinute = gcodec.getFeedRateMinute( self.feedRateMinute, splitLine )
		if not self.isExtruderActive:
			return ''
		if distance <= 0.0:
			return ''
		scaledFlowRate = self.flowRate * self.flowScaleSixty
		return '' #self.getExtrusionDistanceStringFromExtrusionDistance(scaledFlowRate / self.feedRateMinute * distance)

	def getExtrusionDistanceStringFromExtrusionDistance( self, extrusionDistance ):
		'Get the extrusion distance string from the extrusion distance.'
		if self.repository.relativeExtrusionDistance.value:
			return ' E' + self.distanceFeedRate.getRounded( extrusionDistance )
		self.totalExtrusionDistance += extrusionDistance
		return ' E' + self.distanceFeedRate.getRounded( self.totalExtrusionDistance )


	def getRetractionRatio(self, lineIndex):
		'Get the retraction ratio.'
		distanceToNextThread = self.getDistanceToNextThread(lineIndex)
		#print ('distanceToNextThread',distanceToNextThread)
		#print ('totalExtrusionDistance',self.totalExtrusionDistance)
		if distanceToNextThread == None or distanceToNextThread <= self.minimumTravelForRetraction:
			return 0.0
		elif  self.totalExtrusionDistance <= self.minimumExtrusionForRetraction:
			return self.totalExtrusionDistance/self.minimumExtrusionForRetraction
		elif distanceToNextThread >= self.doubleMinimumTravelForRetraction:
			return 1.0
		return (distanceToNextThread - self.minimumTravelForRetraction) / self.minimumTravelForRetraction


	def getSmallestEnclosureIndex(self, point):
		'Get the index of the smallest boundary loop which encloses the point.'
		boundaryLayer = self.boundaryLayers[self.layerIndex]
		for loopIndex, loop in enumerate(boundaryLayer.loops):
			if euclidean.isPointInsideLoop(loop, point):
				return loopIndex
		return None
	def addFlowRateLineIfNecessary(self):
		"Add flow rate line."
		self.newFlowrate = str (round(self.flowRate * self.flowScaleSixty,0) )
		flowRateString = self.newFlowrate
		if flowRateString != self.oldFlowRateString:
			self.distanceFeedRate.addLine('M108 S' + self.newFlowrate )
		self.oldFlowRateString = flowRateString


	def parseBoundaries(self):
		'Parse the boundaries and add them to the boundary layers.'
		boundaryLoop = None
		boundaryLayer = None
		for line in self.lines[self.lineIndex :]:
			splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
			firstWord = gcodec.getFirstWord(splitLine)
			if firstWord == '(</boundaryPerimeter>)':
				boundaryLoop = None
			elif firstWord == '(<boundaryPoint>':
				location = gcodec.getLocationFromSplitLine(None, splitLine)
				if boundaryLoop == None:
					boundaryLoop = []
					boundaryLayer.loops.append(boundaryLoop)
				boundaryLoop.append(location.dropAxis())
			elif firstWord == '(<layer>':
				boundaryLayer = euclidean.LoopLayer(float(splitLine[1]))
				self.boundaryLayers.append(boundaryLayer)
		for boundaryLayer in self.boundaryLayers:
			triangle_mesh.sortLoopsInOrderOfArea(False, boundaryLayer.loops)

	def parseInitialization(self):
		'Parse gcode initialization and store the parameters.'
		for self.lineIndex in xrange(len(self.lines)):
			line = self.lines[self.lineIndex]
			splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
			firstWord = gcodec.getFirstWord(splitLine)
			self.distanceFeedRate.parseSplitLine(firstWord, splitLine)
			if firstWord == '(</extruderInitialization>)':
				self.distanceFeedRate.addLine('(<procedureName> dcflow </procedureName>)')
				return
			elif firstWord == '(<layerThickness>':
				self.layerThickness = float(splitLine[1])
			elif firstWord == '(<maximumZDrillFeedRatePerSecond>':
				self.maximumZTravelFeedRatePerSecond = float(splitLine[1])
			elif firstWord == '(<maximumZTravelFeedRatePerSecond>':
				self.maximumZTravelFeedRatePerSecond = float(splitLine[1])
			elif firstWord == '(<operatingFeedRatePerSecond>':
				self.feedRateMinute = 60.0 * float(splitLine[1])
			elif firstWord == '(<operatingFlowRate>':
				self.operatingFlowRate = float(splitLine[1])
				self.flowRate = self.operatingFlowRate
			elif firstWord == '(<perimeterWidth>':
				self.perimeterWidth = float(splitLine[1])
			elif firstWord == '(<travelFeedRatePerSecond>':
				self.travelFeedRatePerSecond = float(splitLine[1])
			self.distanceFeedRate.addLine(line)

	def parseLine( self, lineIndex ):
		'Parse a gcode line and add it to the dcflow skein.'
		line = self.lines[lineIndex].lstrip()
		splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
		if len(splitLine) < 1:
			return
		firstWord = splitLine[0]
		if firstWord == 'G2' or firstWord == 'G3':
			line = self.getDcflowedArcMovement( line, splitLine )
		if firstWord == 'G1':
			line = self.getDcflowedLinearMovement( line, splitLine )
		if firstWord == 'G90':
			self.absoluteDistanceMode = True
		elif firstWord == 'G91':
			self.absoluteDistanceMode = False
		elif firstWord == '(<layer>':
			self.layerIndex += 1
		elif firstWord == 'M101':
			self.addLinearMoveExtrusionDistanceLine(self.restartDistance * self.retractionRatio)
			if not self.repository.relativeExtrusionDistance.value:
				self.distanceFeedRate.addLine('G92 E0')
				self.totalExtrusionDistance = 0.0
			self.isExtruderActive = True
		elif firstWord == 'M103':
			self.retractionRatio = self.getRetractionRatio(lineIndex)
			self.addLinearMoveExtrusionDistanceLine(-self.repository.retractionDistance.value * self.retractionRatio)
			self.isExtruderActive = False
			#print ('self.retractionRatio', self.retractionRatio)
		elif firstWord == 'M108':
			self.flowRate = float( splitLine[1][1 :] )
		self.addFlowRateLineIfNecessary()
		self.distanceFeedRate.addLine(line)


def main():
	'Display the dcflow dialog.'
	if len(sys.argv) > 1:
		writeOutput(' '.join(sys.argv[1 :]))
	else:
		settings.startMainLoopFromConstructor(getNewRepository())

if __name__ == '__main__':
	main()
