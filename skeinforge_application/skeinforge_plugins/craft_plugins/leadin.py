"""
This page is in the table of contents.
Leadin is a script to smooth the surface leadin of an object by replacing the perimeter surface with a surface printed at half the carve
height. This gives the impression that the object was carved at a much thinner height giving a high-quality finish, but still prints
in a relatively short time. The process is described at:
http://adventuresin3-dprinting.blogspot.com/2011/05/leadinning.html

The leadin manual page is at:
http://fabmetheus.crsndoo.com/wiki/index.php/Skeinforge_Leadin


==Operation==
The default 'Activate Leadin' checkbox is off.  When it is on, the functions described below will work, when it is off, the functions will not be called.

==Settings==
====Clip Over Perimeter Width====
Default is 0.1.

Defines the ratio of the amount each end of the loop is clipped over the perimeter width.  The total gap will therefore be twice the clip.  If the ratio is too high loops will have a gap, if the ratio is too low there will be a bulge at the loop ends.

====Layer From====
Default is one.

Defines which layer of the print the leadinning process starts from. It is not wise to set this to zero, leadinning the bottom layer is likely to cause the bottom perimeter not to adhere well to the print surface.

====Tips====
Due to the very small Z-axis moves leadinning can generate as it prints the perimeter, it can cause the Z-axis speed to be limited by the Limit plug-in, if you have it enabled. This can cause some printers to pause excessively during each layer change. To overcome this, ensure that the Z-axis max speed in the Limit tool is set to an appropriate value for your printer, e.g. 10mm/s

Since Leadin prints two half-height perimeter layers for each layer, printing the perimeter last causes the print head to travel down from the current print height. Depending on the shape of your extruder nozzle, you may get higher quality prints if you print the perimeters first, so the print head always travels up.  This is set via the Thread Sequence Choice setting in the Fill tool.


==Examples==
The following examples leadin the file Screw Holder Bottom.stl.  The examples are run in a terminal in the folder which contains Screw Holder Bottom.stl and leadin.py.

> python leadin.py
This brings up the leadin dialog.

> python leadin.py Screw Holder Bottom.stl
The leadin tool is parsing the file:
Screw Holder Bottom.stl
..
The leadin tool has created the file:
.. Screw Holder Bottom_leadin.gcode

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.fabmetheus_tools import fabmetheus_interpret
from fabmetheus_utilities.vector3 import Vector3
from fabmetheus_utilities import archive
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import gcodec
from fabmetheus_utilities import intercircle
from fabmetheus_utilities import settings
from skeinforge_application.skeinforge_utilities import skeinforge_craft
from skeinforge_application.skeinforge_utilities import skeinforge_polyfile
from skeinforge_application.skeinforge_utilities import skeinforge_profile
import sys
import math

__author__ = 'Enrique Perez (perez_enrique aht yahoo.com) & James Blackwell (jim_blag ahht hotmail.com)'
__date__ = '$Date: 2008/21/04 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def getCraftedText(fileName, gcodeText, repository=None):
	'Leadin a gcode linear move text.'
	return getCraftedTextFromText(archive.getTextIfEmpty(fileName, gcodeText), repository)

def getCraftedTextFromText(gcodeText, repository=None):
	'Leadin a gcode linear move text.'
	if gcodec.isProcedureDoneOrFileIsEmpty(gcodeText, 'leadin'):
		return gcodeText
	if repository == None:
		repository = settings.getReadRepository(LeadinRepository())
	if not repository.activateLeadin.value:
		return gcodeText
	return LeadinSkein().getCraftedGcode(gcodeText, repository)

def getNewRepository():
	'Get new repository.'
	return LeadinRepository()

def writeOutput(fileName, shouldAnalyze=True):
	'Leadin a gcode linear move file.  Chain leadin the gcode if it is not already leadinned.'
	skeinforge_craft.writeChainTextWithNounMessage(fileName, 'leadin', shouldAnalyze)


class LeadinRepository:
	'A class to handle the leadin settings.'
	def __init__(self):
		'Set the default settings, execute title & settings fileName.'
		skeinforge_profile.addListsToCraftTypeRepository('skeinforge_application.skeinforge_plugins.craft_plugins.leadin.html', self )
		self.fileNameInput = settings.FileNameInput().getFromFileName( fabmetheus_interpret.getGNUTranslatorGcodeFileTypeTuples(), 'Open File for Leadin', self, '')
		self.openWikiManualHelpPage = settings.HelpPage().getOpenFromAbsolute('http://fabmetheus.crsndoo.com/wiki/index.php/Skeinforge_Leadin')
		self.activateLeadin = settings.BooleanSetting().getFromValue('Activate Leadin', self, False )
		self.clipOverPerimeterWidth = settings.FloatSpin().getFromValue(0.5, 'Clip Over Perimeter Width (ratio):', self,1.5, 1.0)
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- Infill -', self )
		self.infillBottomFeedRate = settings.FloatSpin().getFromValue(0.2, 'Infill Bottom Feed Rate Multiplier (ratio):', self, 2.0, 1.0)
		self.infillBottomFlowRate = settings.FloatSpin().getFromValue(0.2, 'Infill Bottom Flow Rate Multiplier (ratio):', self, 2.0, 1.0)
		self.infillTopFeedRate = settings.FloatSpin().getFromValue(0.2, 'Infill Top Feed Rate Multiplier (ratio):', self, 2.0, 1.0)
		self.infillTopFlowRate = settings.FloatSpin().getFromValue(0.2, 'Infill Top Flow Rate Multiplier (ratio):', self, 2.0, 1.0)
		settings.LabelSeparator().getFromRepository(self)
		self.layersFrom = settings.IntSpin().getSingleIncrementFromValue(0, 'Layers From (index):', self, 912345678, 1)
		self.executeTitle = 'Leadin'

	def execute(self):
		'Leadin button has been clicked.'
		fileNames = skeinforge_polyfile.getFileOrDirectoryTypesUnmodifiedGcode(self.fileNameInput.value, fabmetheus_interpret.getImportPluginFileNames(), self.fileNameInput.wasCancelled)
		for fileName in fileNames:
			writeOutput(fileName)


class LeadinSkein:
	'A class to leadin a skein of extrusions.'
	def __init__(self):
		'Initialize.'
		self.distanceFeedRate = gcodec.DistanceFeedRate()
		self.feedRateMinute = 959.0
		self.infill = None
		self.layerCount = settings.LayerCount()
		self.layerIndex = -1
		self.lineIndex = 0
		self.lines = None
		self.oldFlowRate = None
		self.oldLocation = None
		self.perimeter = None
		self.travelFeedRateMinute = 957.0

	def addFlowRateLine(self, flowRate):
		'Add a flow rate line.'
		self.distanceFeedRate.addLine('M108 S' + euclidean.getFourSignificantFigures(flowRate))

	def addInfillOutlines(self, feedRate, infillOutlines, z):
		'Add the infill outlines to the gcode.'
		for infillOutline in infillOutlines:
			infillPath = infillOutline + [infillOutline[0]]
			self.distanceFeedRate.addGcodeFromFeedRateThreadZ(feedRate, infillPath, self.travelFeedRateMinute, z)

	def addPerimeterLoop(self, thread, z):
		'Add the perimeter loop to the gcode.'
		self.distanceFeedRate.addGcodeFromFeedRateThreadZ(self.feedRateMinute, thread, self.travelFeedRateMinute, z)

	def addLeadinnedInfill(self):
		'Add leadinned infill.'
		if self.infill == None:
			return
		if len(self.infill) < 2:
			return
		infillOutlines = intercircle.getAroundsFromPath(self.infill, self.quarterInfillWidth)
		lowerZ = self.oldLocation.z - self.halfLayerThickness
		self.addFlowRateLine(0.25 * self.repository.infillBottomFlowRate.value * self.oldFlowRate* (self.repository.infillBottomFeedRate.value))
		self.addInfillOutlines(self.repository.infillBottomFeedRate.value * self.feedRateMinute, infillOutlines, lowerZ)
		self.addFlowRateLine(0.25 * self.repository.infillTopFlowRate.value * self.oldFlowRate * self.repository.infillTopFeedRate.value)
		self.addInfillOutlines(self.repository.infillTopFeedRate.value * self.feedRateMinute, infillOutlines, self.oldLocation.z)
		self.addFlowRateLine(self.oldFlowRate)

	def addLeadinnedPerimeter(self):
		'Add leadinned perimeter.'
		if self.perimeter == None:
			return
		self.perimeter = self.perimeter[: -1]
		innerPerimeter = intercircle.getLargestInsetLoopFromLoop(self.perimeter, self.quarterPerimeterWidth)
		innerPerimeter = self.getClippedSimplifiedLoopPathByLoop(innerPerimeter)
		outerPerimeter = intercircle.getLargestInsetLoopFromLoop(self.perimeter, -self.quarterPerimeterWidth*0.7853)#		outerPerimeter = intercircle.getLargestInsetLoopFromLoop(self.perimeter, -self.quarterPerimeterWidth)
		outerPerimeter = self.getClippedSimplifiedLoopPathByLoop(outerPerimeter)
		lowerZ = self.oldLocation.z - self.halfLayerThickness
		self.addFlowRateLine(0.5 * self.oldFlowRate)
		#self.addPerimeterLoop(innerPerimeter, lowerZ)
		#self.addPerimeterLoop(outerPerimeter, lowerZ)
		self.addPerimeterLoop(innerPerimeter, self.oldLocation.z)
		self.addPerimeterLoop(outerPerimeter, self.oldLocation.z)
		self.addFlowRateLine(self.oldFlowRate)

	def getClippedSimplifiedLoopPathByLoop(self, loop):
		'Get clipped and simplified loop path from a loop.'
		loopPath = loop + [loop[0]]
		return euclidean.getClippedSimplifiedLoopPath(self.clipLength, loopPath, self.halfPerimeterWidth)

	def getCraftedGcode( self, gcodeText, repository ):
		'Parse gcode text and store the leadin gcode.'
		self.lines = archive.getTextLines(gcodeText)
		self.repository = repository
		self.layersFromBottom = self.repository.layersFrom.value
		self.parseInitialization()
		self.parseBoundaries()
		for self.lineIndex in xrange(self.lineIndex, len(self.lines)):
			line = self.lines[self.lineIndex]
			self.parseLine(line)
		return self.distanceFeedRate.output.getvalue()

	def parseBoundaries(self):
		'Parse the boundaries and add them to the boundary layers.'
		self.boundaryLayers = []
		self.layerIndexTop = -1
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
				self.layerIndexTop += 1
		for boundaryLayerIndex, boundaryLayer in enumerate(self.boundaryLayers):
			if len(boundaryLayer.loops) > 0:
				self.layersFromBottom += boundaryLayerIndex
				return

	def parseInitialization(self):
		'Parse gcode initialization and store the parameters.'
		for self.lineIndex in xrange(len(self.lines)):
			line = self.lines[self.lineIndex]
			splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
			firstWord = gcodec.getFirstWord(splitLine)
			self.distanceFeedRate.parseSplitLine(firstWord, splitLine)
			if firstWord == '(</extruderInitialization>)':
				self.distanceFeedRate.addLine('(<procedureName> leadin </procedureName>)')
				return
			elif firstWord == '(<infillWidth>':
				self.quarterInfillWidth = 0.25 * float(splitLine[1])
			elif firstWord == '(<layerThickness>':
				self.LayerThickness = float(splitLine[1])
				self.halfLayerThickness = 0.5 * float(splitLine[1])
			elif firstWord == '(<operatingFlowRate>':
				self.oldFlowRate = float(splitLine[1])
			elif firstWord == '(<perimeterWidth>':
				perimeterWidth = float(splitLine[1])
				self.PerimeterWidth = perimeterWidth
				self.halfPerimeterWidth = 0.5 * perimeterWidth
				self.quarterPerimeterWidth = 0.25 * perimeterWidth
				self.clipLength = (self.repository.clipOverPerimeterWidth.value * self.halfLayerThickness * (0.7853))/2
			elif firstWord == '(<travelFeedRatePerSecond>':
				self.travelFeedRateMinute = 60.0 * float(splitLine[1])
			self.distanceFeedRate.addLine(line)

	def parseLine(self, line):
		'Parse a gcode line and add it to the leadin skein.'
		splitLine = gcodec.getSplitLineBeforeBracketSemicolon(line)
		if len(splitLine) < 1:
			return
		firstWord = splitLine[0]
		if firstWord == 'G1':
			self.feedRateMinute = gcodec.getFeedRateMinute(self.feedRateMinute, splitLine)
			location = gcodec.getLocationFromSplitLine(self.oldLocation, splitLine)
			self.oldLocation = location
			if self.infill != None:
				self.infill.append(location.dropAxis())
				return
			if self.perimeter != None:
				self.perimeter.append(location.dropAxis())
				return
		elif firstWord == '(<layer>':
			self.layerCount.printProgressIncrement('leadin')
			self.layerIndex += 1
			self.setInfill()
		elif firstWord == '(<loop>':
			self.infill = None
		elif firstWord == '(</loop>)':
			self.setInfill()
		elif firstWord == 'M108':
			self.oldFlowRate = gcodec.getDoubleAfterFirstLetter(splitLine[1])
		elif firstWord == '(<perimeter>':
			self.infill = None
			if self.layerIndex >= self.layersFromBottom:
				self.perimeter = []
		elif firstWord == '(</perimeter>)':
			self.addLeadinnedPerimeter()
			self.setInfill()
			self.perimeter = None
		if firstWord == 'M103':
			if self.infill != None:
				self.addLeadinnedInfill()
				self.setInfill()
				return
		if firstWord == 'M101' or firstWord == 'M103':
			if self.infill != None:
				return
			if self.perimeter != None:
				return
		self.distanceFeedRate.addLine(line)

	def setInfill(self):
		'Set the infill to an empty list if the layerIndex is above layersFromBottom and there is nothing above.'
		if self.layerIndex >= self.layersFromBottom and self.layerIndex == self.layerIndexTop:
			self.infill = []


def main():
	'Display the leadin dialog.'
	if len(sys.argv) > 1:
		writeOutput(' '.join(sys.argv[1 :]))
	else:
		settings.startMainLoopFromConstructor(getNewRepository())

if __name__ == '__main__':
	main()
 