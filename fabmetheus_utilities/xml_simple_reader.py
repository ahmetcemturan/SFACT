"""
The xml_simple_reader.py script is an xml parser that can parse a line separated xml text.

This xml parser will read a line seperated xml text and produce a tree of the xml with a root element.  Each element can have an attribute table, childNodes, a class name, parentNode, text and a link to the root element.

This example gets an xml tree for the xml file boolean.xml.  This example is run in a terminal in the folder which contains boolean.xml and xml_simple_reader.py.


> python
Python 2.5.1 (r251:54863, Sep 22 2007, 01:43:31)
[GCC 4.2.1 (SUSE Linux)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> fileName = 'boolean.xml'
>>> file = open(fileName, 'r')
>>> xmlText = file.read()
>>> file.close()
>>> from xml_simple_reader import XMLSimpleReader
>>> xmlParser = XMLSimpleReader(fileName, None, xmlText)
>>> print( xmlParser )
  ?xml, {'version': '1.0'}
  ArtOfIllusion, {'xmlns:bf': '//babelfiche/codec', 'version': '2.0', 'fileversion': '3'}
  Scene, {'bf:id': 'theScene'}
  materials, {'bf:elem-type': 'java.lang.Object', 'bf:list': 'collection', 'bf:id': '1', 'bf:type': 'java.util.Vector'}
..
many more lines of the xml tree
..

"""


from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities.geometry.geometry_utilities import matrix
from fabmetheus_utilities import archive
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import xml_simple_writer
import cStringIO


__author__ = 'Enrique Perez (perez_enrique@yahoo.com)'
__credits__ = 'Nophead <http://hydraraptor.blogspot.com/>\nArt of Illusion <http://www.artofillusion.org/>'
__date__ = '$Date: 2008/21/04 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def addXMLLine(line, xmlLines):
	'Get the all the xml lines of a text.'
	strippedLine = line.strip()
	if strippedLine[ : len('<!--') ] == '<!--':
		endIndex = line.find('-->')
		if endIndex != - 1:
			endIndex += len('-->')
			commentLine = line[: endIndex]
			remainderLine = line[endIndex :].strip()
			if len(remainderLine) > 0:
				xmlLines.append(commentLine)
				xmlLines.append(remainderLine)
				return
	xmlLines.append(line)

def getXMLLines(text):
	'Get the all the xml lines of a text.'
	accumulatedOutput = None
	textLines = archive.getTextLines(text)
	combinedLines = []
	lastWord = '>'
	for textLine in textLines:
		strippedLine = textLine.strip()
		firstCharacter = None
		lastCharacter = None
		if len( strippedLine ) > 1:
			firstCharacter = strippedLine[0]
			lastCharacter = strippedLine[-1]
		if firstCharacter == '<' and lastCharacter != '>' and accumulatedOutput == None:
			accumulatedOutput = cStringIO.StringIO()
			accumulatedOutput.write( textLine )
			if strippedLine[ : len('<!--') ] == '<!--':
				lastWord = '-->'
		else:
			if accumulatedOutput == None:
				addXMLLine( textLine, combinedLines )
			else:
				accumulatedOutput.write('\n' + textLine )
				if strippedLine[ - len( lastWord ) : ] == lastWord:
					addXMLLine( accumulatedOutput.getvalue(), combinedLines )
					accumulatedOutput = None
					lastWord = '>'
	xmlLines = []
	for combinedLine in combinedLines:
		xmlLines += getXMLTagSplitLines(combinedLine)
	return xmlLines

def getXMLTagSplitLines(combinedLine):
	'Get the xml lines split at a tag.'
	characterIndex = 0
	lastWord = None
	splitIndexes = []
	tagEnd = False
	while characterIndex < len(combinedLine):
		character = combinedLine[characterIndex]
		if character == '"' or character == "'":
			lastWord = character
		elif combinedLine[characterIndex : characterIndex + len('<!--')] == '<!--':
			lastWord = '-->'
		elif combinedLine[characterIndex : characterIndex + len('<![CDATA[')] == '<![CDATA[':
			lastWord = ']]>'
		if lastWord != None:
			characterIndex = combinedLine.find(lastWord, characterIndex + 1)
			if characterIndex == -1:
				return [combinedLine]
			character = None
			lastWord = None
		if character == '>':
			tagEnd = True
		elif character == '<':
			if tagEnd:
				if combinedLine[characterIndex : characterIndex + 2] != '</':
					splitIndexes.append(characterIndex)
		characterIndex += 1
	if len(splitIndexes) < 1:
		return [combinedLine]
	xmlTagSplitLines = []
	lastSplitIndex = 0
	for splitIndex in splitIndexes:
		xmlTagSplitLines.append(combinedLine[lastSplitIndex : splitIndex])
		lastSplitIndex = splitIndex
	xmlTagSplitLines.append(combinedLine[lastSplitIndex :])
	return xmlTagSplitLines


class XMLElement:
	'An xml element.'
	def __init__(self):
		'Add empty lists.'
		self.attributeDictionary = {}
		self.childNodes = []
		self.idDictionary = {}
		self.importName = ''
		self.localName = ''
		self.nameDictionary = {}
		self.parentNode = None
		self.tagDictionary = {}
		self.text = ''
		self.xmlObject = None

	def __repr__(self):
		'Get the string representation of this XML element.'
		return '%s\n%s\n%s' % ( self.localName, self.attributeDictionary, self.text )

	def _getAccessibleAttribute(self, attributeName):
		'Get the accessible attribute.'
		global globalGetAccessibleAttributeSet
		if attributeName in globalGetAccessibleAttributeSet:
			return getattr(self, attributeName, None)
		return None

	def addAttribute( self, beforeQuote, withinQuote ):
		'Add the attribute to the dictionary.'
		beforeQuote = beforeQuote.strip()
		lastEqualIndex = beforeQuote.rfind('=')
		if lastEqualIndex < 0:
			return
		key = beforeQuote[ : lastEqualIndex ].strip()
		self.attributeDictionary[key] = withinQuote

	def addSuffixToID(self, idSuffix):
		'Add the suffix to the id.'
		if 'id' in self.attributeDictionary:
			self.attributeDictionary['id'] += idSuffix

	def addToIdentifierDictionaryIFIdentifierExists(self):
		'Add to the id dictionary if the id key exists in the attribute dictionary.'
		if 'id' in self.attributeDictionary:
			idKey = self.getImportNameWithDot() + self.attributeDictionary['id']
			self.getRoot().idDictionary[idKey] = self
		if 'name' in self.attributeDictionary:
			nameKey = self.getImportNameWithDot() + self.attributeDictionary['name']
			euclidean.addElementToListDictionaryIfNotThere(self, nameKey, self.getRoot().nameDictionary)
		for tagKey in self.getTagKeys():
			euclidean.addElementToListDictionaryIfNotThere(self, tagKey, self.getRoot().tagDictionary)

	def addXML(self, depth, output):
		'Add xml for this xmlElement.'
		if self.localName == 'comment':
			output.write( self.text )
			return
		innerOutput = cStringIO.StringIO()
		xml_simple_writer.addXMLFromObjects(depth + 1, self.childNodes, innerOutput)
		innerText = innerOutput.getvalue()
		xml_simple_writer.addBeginEndInnerXMLTag(self.attributeDictionary, depth, innerText, self.localName, output, self.text)

	def copyXMLChildNodes( self, idSuffix, parentNode ):
		'Copy the xml childNodes.'
		for childNode in self.childNodes:
			childNode.getCopy( idSuffix, parentNode )

	def getCascadeFloat(self, defaultFloat, key):
		'Get the cascade float.'
		if key in self.attributeDictionary:
			value = evaluate.getEvaluatedFloat(None, key, self)
			if value != None:
				return value
		if self.parentNode == None:
			return defaultFloat
		return self.parentNode.getCascadeFloat(defaultFloat, key)

	def getChildNodesByLocalName(self, localName):
		'Get the childNodes which have the given class name.'
		childNodesByLocalName = []
		for childNode in self.childNodes:
			if localName == childNode.localName:
				childNodesByLocalName.append(childNode)
		return childNodesByLocalName

	def getChildNodesByLocalNameRecursively(self, localName):
		'Get the childNodes which have the given class name recursively.'
		childNodesByLocalName = self.getChildNodesByLocalName(localName)
		for childNode in self.childNodes:
			childNodesByLocalName += childNode.getChildNodesByLocalNameRecursively(localName)
		return childNodesByLocalName

	def getCopy(self, idSuffix, parentNode):
		'Copy the xml element, set its dictionary and add it to the parentNode.'
		matrix4X4 = matrix.getBranchMatrixSetXMLElement(self)
		attributeDictionaryCopy = self.attributeDictionary.copy()
		attributeDictionaryCopy.update(matrix4X4.getAttributeDictionary('matrix.'))
		copy = self.getCopyShallow(attributeDictionaryCopy)
		copy.setParentAddToChildNodes(parentNode)
		copy.addSuffixToID(idSuffix)
		copy.text = self.text
		copy.addToIdentifierDictionaryIFIdentifierExists()
		self.copyXMLChildNodes(idSuffix, copy)
		return copy

	def getCopyShallow(self, attributeDictionary=None):
		'Copy the xml element and set its dictionary and parentNode.'
		if attributeDictionary == None: # to evade default initialization bug where a dictionary is initialized to the last dictionary
			attributeDictionary = {}
		copyShallow = XMLElement()
		copyShallow.attributeDictionary = attributeDictionary
		copyShallow.localName = self.localName
		copyShallow.importName = self.importName
		copyShallow.parentNode = self.parentNode
		return copyShallow

	def getFirstChildByLocalName(self, localName):
		'Get the first childNode which has the given class name.'
		for childNode in self.childNodes:
			if localName == childNode.localName:
				return childNode
		return None

	def getIDSuffix(self, elementIndex=None):
		'Get the id suffix from the dictionary.'
		suffix = self.localName
		if 'id' in self.attributeDictionary:
			suffix = self.attributeDictionary['id']
		if elementIndex == None:
			return '_%s' % suffix
		return '_%s_%s' % (suffix, elementIndex)

	def getImportNameWithDot(self):
		'Get import name with dot.'
		if self.importName == '':
			return ''
		return self.importName + '.'

	def getParentParseReplacedLine(self, line, lineStripped, parentNode):
		'Parse replaced line and return the parentNode.'
		if lineStripped[: len('<!--')] == '<!--':
			self.localName = 'comment'
			self.text = line + '\n'
			self.setParentAddToChildNodes(parentNode)
			return parentNode
		if lineStripped[: len('</')] == '</':
			if parentNode == None:
				return parentNode
			return parentNode.parentNode
		self.setParentAddToChildNodes(parentNode)
		cdataBeginIndex = lineStripped.find('<![CDATA[')
		if cdataBeginIndex != - 1:
			cdataEndIndex = lineStripped.rfind(']]>')
			if cdataEndIndex != - 1:
				cdataEndIndex += len(']]>')
				self.text = lineStripped[cdataBeginIndex : cdataEndIndex]
				lineStripped = lineStripped[: cdataBeginIndex] + lineStripped[cdataEndIndex :]
		self.localName = lineStripped[1 : lineStripped.replace('/>', ' ').replace('>', ' ').replace('\n', ' ').find(' ')]
		lastWord = lineStripped[-2 :]
		lineAfterLocalName = lineStripped[2 + len(self.localName) : -1]
		beforeQuote = ''
		lastQuoteCharacter = None
		withinQuote = ''
		for characterIndex in xrange(len(lineAfterLocalName)):
			character = lineAfterLocalName[characterIndex]
			if lastQuoteCharacter == None:
				if character == '"' or character == "'":
					lastQuoteCharacter = character
					character = ''
			if character == lastQuoteCharacter:
				self.addAttribute(beforeQuote, withinQuote)
				beforeQuote = ''
				lastQuoteCharacter = None
				withinQuote = ''
				character = ''
			if lastQuoteCharacter == None:
				beforeQuote += character
			else:
				withinQuote += character
		self.addToIdentifierDictionaryIFIdentifierExists()
		if lastWord == '/>':
			return parentNode
		tagEnd = '</%s>' % self.localName
		if lineStripped[-len(tagEnd) :] == tagEnd:
			untilTagEnd = lineStripped[: -len(tagEnd)]
			lastGreaterThanIndex = untilTagEnd.rfind('>')
			self.text += untilTagEnd[ lastGreaterThanIndex + 1 : ]
			return parentNode
		return self

	def getParser(self):
		'Get the parser.'
		return self.getRoot().parser

	def getPaths(self):
		'Get all paths.'
		if self.xmlObject == None:
			return []
		return self.xmlObject.getPaths()

	def getPreviousVertex(self, defaultVector3=None):
		'Get previous vertex if it exists.'
		if self.parentNode == None:
			return defaultVector3
		if self.parentNode.xmlObject == None:
			return defaultVector3
		if len(self.parentNode.xmlObject.vertexes) < 1:
			return defaultVector3
		return self.parentNode.xmlObject.vertexes[-1]

	def getPreviousXMLElement(self):
		'Get previous XMLElement if it exists.'
		if self.parentNode == None:
			return None
		previousXMLElementIndex = self.parentNode.childNodes.index(self) - 1
		if previousXMLElementIndex < 0:
			return None
		return self.parentNode.childNodes[previousXMLElementIndex]

	def getRoot(self):
		'Get the root element.'
		if self.parentNode == None:
			return self
		return self.parentNode.getRoot()

	def getSubChildWithID( self, idReference ):
		'Get the childNode which has the idReference.'
		for childNode in self.childNodes:
			if 'bf:id' in childNode.attributeDictionary:
				if childNode.attributeDictionary['bf:id'] == idReference:
					return childNode
			subChildWithID = childNode.getSubChildWithID( idReference )
			if subChildWithID != None:
				return subChildWithID
		return None

	def getTagKeys(self):
		'Get stripped tag keys.'
		if 'tags' not in self.attributeDictionary:
			return []
		tagKeys = []
		tagString = self.attributeDictionary['tags']
		if tagString.startswith('='):
			tagString = tagString[1 :]
		if tagString.startswith('['):
			tagString = tagString[1 :]
		if tagString.endswith(']'):
			tagString = tagString[: -1]
		for tagWord in tagString.split(','):
			tagKey = tagWord.strip()
			if tagKey != '':
				tagKeys.append(tagKey)
		return tagKeys

	def getValueByKey( self, key ):
		'Get value by the key.'
		if key in evaluate.globalElementValueDictionary:
			return evaluate.globalElementValueDictionary[key](self)
		if key in self.attributeDictionary:
			return evaluate.getEvaluatedLinkValue( self.attributeDictionary[key], self )
		return None

	def getVertexes(self):
		'Get the vertexes.'
		if self.xmlObject == None:
			return []
		return self.xmlObject.getVertexes()

	def getXMLElementByID(self, idKey):
		'Get the xml element by id.'
		idDictionary = self.getRoot().idDictionary
		if idKey in idDictionary:
			return idDictionary[idKey]
		return None

	def getXMLElementByImportID(self, idKey):
		'Get the xml element by import file name and id.'
		return self.getXMLElementByID( self.getImportNameWithDot() + idKey )

	def getXMLElementsByImportName(self, name):
		'Get the xml element by import file name and name.'
		return self.getXMLElementsByName( self.getImportNameWithDot() + name )

	def getXMLElementsByName(self, name):
		'Get the xml elements by name.'
		nameDictionary = self.getRoot().nameDictionary
		if name in nameDictionary:
			return nameDictionary[name]
		return None

	def getXMLElementsByTag(self, tag):
		'Get the xml elements by tag.'
		tagDictionary = self.getRoot().tagDictionary
		if tag in tagDictionary:
			return tagDictionary[tag]
		return None

	def getXMLProcessor(self):
		'Get the xmlProcessor.'
		return self.getRoot().xmlProcessor

	def linkObject(self, xmlObject):
		'Link self to xmlObject and add xmlObject to archivableObjects.'
		self.xmlObject = xmlObject
		self.xmlObject.xmlElement = self
		self.parentNode.xmlObject.archivableObjects.append(self.xmlObject)

	def printAllVariables(self):
		'Print all variables.'
		print('attributeDictionary')
		print(self.attributeDictionary)
		print('childNodes')
		print(self.childNodes)
		print('idDictionary')
		print(self.idDictionary)
		print('importName')
		print(self.importName)
		print('localName')
		print(self.localName)
		print('nameDictionary')
		print(self.nameDictionary)
		print('parentNode')
		print(self.parentNode)
		print('tagDictionary')
		print(self.tagDictionary)
		print('text')
		print(self.text)
		print('xmlObject')
		print(self.xmlObject)
		print('')

	def printAllVariablesRoot(self):
		'Print all variables and the root variables.'
		self.printAllVariables()
		root = self.getRoot()
		if root != None and root != self:
			print('')
			print('Root variables:')
			root.printAllVariables()

	def removeChildNodesFromIDNameParent(self):
		'Remove the childNodes from the id and name dictionaries and the childNodes.'
		childNodesCopy = self.childNodes[:]
		for childNode in childNodesCopy:
			childNode.removeFromIDNameParent()

	def removeFromIDNameParent(self):
		'Remove this from the id and name dictionaries and the childNodes of the parentNode.'
		self.removeChildNodesFromIDNameParent()
		if 'id' in self.attributeDictionary:
			idDictionary = self.getRoot().idDictionary
			idKey = self.getImportNameWithDot() + self.attributeDictionary['id']
			if idKey in idDictionary:
				del idDictionary[idKey]
		if 'name' in self.attributeDictionary:
			nameDictionary = self.getRoot().nameDictionary
			nameKey = self.getImportNameWithDot() + self.attributeDictionary['name']
			euclidean.removeElementFromListTable(self, nameKey, nameDictionary)
		for tagKey in self.getTagKeys():
			euclidean.removeElementFromListTable(self, tagKey, self.getRoot().tagDictionary)
		if self.parentNode != None:
			self.parentNode.childNodes.remove(self)

	def setParentAddToChildNodes(self, parentNode):
		'Set the parentNode and add this to its childNodes.'
		self.parentNode = parentNode
		if self.parentNode != None:
			self.parentNode.childNodes.append(self)


class XMLSimpleReader:
	'A simple xml parser.'
	def __init__(self, fileName, parentNode, xmlText):
		'Add empty lists.'
		self.beforeRoot = ''
		self.fileName = fileName
		self.isXML = False
		self.numberOfWarnings = 0
		self.parentNode = parentNode
		self.root = None
		if parentNode != None:
			self.root = parentNode.getRoot()
		self.lines = getXMLLines(xmlText)
		for self.lineIndex, line in enumerate(self.lines):
			self.parseLine(line)
		self.xmlText = xmlText
	
	def __repr__(self):
		'Get the string representation of this parser.'
		return str( self.root )

	def getOriginalRoot(self):
		'Get the original reparsed root element.'
		if evaluate.getEvaluatedBoolean(True, 'getOriginalRoot', self.root):
			return XMLSimpleReader(self.fileName, self.parentNode, self.xmlText).root
		return None

	def getRoot(self):
		'Get the root element.'
		return self.root

	def parseLine(self, line):
		'Parse an xml line and add it to the xml tree.'
		lineStripped = line.strip()
		if len( lineStripped ) < 1:
			return
		if lineStripped.startswith('<?xml'):
			self.isXML = True
			return
		if not self.isXML:
			if self.numberOfWarnings < 1:
				print('Warning, xml file should start with <?xml.')
				print('Until it does, parseLine in XMLSimpleReader will do nothing for:')
				print(self.fileName)
				self.numberOfWarnings += 1
			return
		xmlElement = XMLElement()
		self.parentNode = xmlElement.getParentParseReplacedLine( line, lineStripped, self.parentNode )
		if self.root != None:
			return
		lowerLocalName = xmlElement.localName.lower()
		if lowerLocalName == 'comment' or lowerLocalName == '!doctype':
			return
		self.root = xmlElement
		self.root.parser = self
		for line in self.lines[ : self.lineIndex ]:
			self.beforeRoot += line + '\n'


globalGetAccessibleAttributeSet = set('getPaths getPreviousVertex getPreviousXMLElement getVertexes parent'.split())
