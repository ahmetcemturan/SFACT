"""
This page is in the table of contents.
The xml.py script is an import translator plugin to get a carving from an Art of Illusion xml file.

An import plugin is a script in the interpret_plugins folder which has the function getCarving.  It is meant to be run from the interpret tool.  To ensure that the plugin works on platforms which do not handle file capitalization properly, give the plugin a lower case name.

The getCarving function takes the file name of an xml file and returns the carving.

An xml file can be exported from Art of Illusion by going to the "File" menu, then going into the "Export" menu item, then picking the XML choice.  This will bring up the XML file chooser window, choose a place to save the file then click "OK".  Leave the "compressFile" checkbox unchecked.  All the objects from the scene will be exported, this plugin will ignore the light and camera.  If you want to fabricate more than one object at a time, you can have multiple objects in the Art of Illusion scene and they will all be carved, then fabricated together.

"""


from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.geometry_utilities import boolean_geometry
from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities import archive
from fabmetheus_utilities import gcodec
from fabmetheus_utilities import settings
from fabmetheus_utilities import xml_simple_reader
import os
import sys
import traceback


__author__ = 'Enrique Perez (perez_enrique@yahoo.com)'
__credits__ = 'Nophead <http://hydraraptor.blogspot.com/>\nArt of Illusion <http://www.artofillusion.org/>'
__date__ = '$Date: 2008/21/04 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def getCarvingFromParser(xmlParser):
	"Get the carving for the parser."
	booleanGeometryElement = xmlParser.getRoot()
	booleanGeometryElement.xmlObject = boolean_geometry.BooleanGeometry()
	booleanGeometryElement.xmlProcessor = XMLBooleanGeometryProcessor()
	booleanGeometryElement.xmlProcessor.processChildNodes(booleanGeometryElement)
	return booleanGeometryElement.xmlObject


class XMLBooleanGeometryProcessor():
	"A class to process xml boolean geometry elements."
	def __init__(self):
		"Initialize processor."
		self.functions = []
		self.manipulationMatrixDictionary = archive.getGeometryDictionary('manipulation_matrix')
		self.manipulationPathDictionary = archive.getGeometryDictionary('manipulation_paths')
		self.manipulationShapeDictionary = archive.getGeometryDictionary('manipulation_shapes')
		self.namePathDictionary = {}
		self.namePathDictionary.update(evaluate.globalCreationDictionary)
		self.namePathDictionary.update(archive.getGeometryDictionary('manipulation_meta'))
		self.namePathDictionary.update(self.manipulationMatrixDictionary)
		self.namePathDictionary.update(self.manipulationPathDictionary)
		self.namePathDictionary.update(self.manipulationShapeDictionary)
		archive.addToNamePathDictionary(archive.getGeometryToolsPath(), self.namePathDictionary)
		archive.addToNamePathDictionary(archive.getGeometryToolsPath('path_elements'), self.namePathDictionary)
		archive.addToNamePathDictionary(archive.getGeometryPath('solids'), self.namePathDictionary)
		archive.addToNamePathDictionary(archive.getGeometryPath('statements'), self.namePathDictionary)

	def __repr__(self):
		'Get the string representation of this XMLBooleanGeometryProcessor.'
		return 'XMLBooleanGeometryProcessor with %s functions.' % len(self.functions)

	def convertXMLElement( self, geometryOutput, xmlElement ):
		"Convert the xml element."
		geometryOutputKeys = geometryOutput.keys()
		if len( geometryOutputKeys ) < 1:
			return None
		firstKey = geometryOutputKeys[0]
		lowerLocalName = firstKey.lower()
		if lowerLocalName not in self.namePathDictionary:
			return None
		pluginModule = archive.getModuleWithPath( self.namePathDictionary[ lowerLocalName ] )
		if pluginModule == None:
			return None
		xmlElement.localName = lowerLocalName
		return pluginModule.convertXMLElement(geometryOutput[ firstKey ], xmlElement)

	def createChildNodes( self, geometryOutput, parentNode ):
		"Create childNodes for the parentNode."
		for geometryOutputChild in geometryOutput:
			childNode = xml_simple_reader.XMLElement()
			childNode.setParentAddToChildNodes( parentNode )
			self.convertXMLElement(geometryOutputChild, childNode)

	def processChildNodes(self, xmlElement):
		"Process the childNodes of the xml element."
		for childNode in xmlElement.childNodes:
			self.processXMLElement(childNode)

	def processXMLElement(self, xmlElement):
		'Process the xml element.'
		lowerLocalName = xmlElement.localName.lower()
		if lowerLocalName not in self.namePathDictionary:
			return None
		pluginModule = archive.getModuleWithPath(self.namePathDictionary[lowerLocalName])
		if pluginModule == None:
			return None
		try:
			return pluginModule.processXMLElement(xmlElement)
		except:
			print('Warning, could not processXMLElement in fabmetheus for:')
			print(pluginModule)
			print(xmlElement)
			traceback.print_exc(file=sys.stdout)
		return None
