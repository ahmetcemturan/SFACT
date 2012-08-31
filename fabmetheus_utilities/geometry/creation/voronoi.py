"""
Grid path points.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.creation import lineation
from fabmetheus_utilities.geometry.geometry_tools import path
from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities.vector3 import Vector3
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import intercircle
import math
import random


__author__ = 'Enrique Perez (perez_enrique@yahoo.com)'
__credits__ = 'Art of Illusion <http://www.artofillusion.org/>'
__date__ = '$Date: 2008/02/05 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def addVoronoiPoint(begin, end, midX, loop, rotatedBegin, rotatedEnd):
	'Add voronoi point to loop.'
	if rotatedBegin.real >= midX:
		loop.append(begin)
		if rotatedEnd.real < midX:
			beginMinusEnd = begin - end
			rotatedBeginMinusEnd = rotatedBegin - rotatedEnd
			loop.append(end + beginMinusEnd * (midX - rotatedEnd.real) / rotatedBeginMinusEnd.real)
		return
	if rotatedEnd.real <= midX:
		return
	endMinusBegin = end - begin
	rotatedEndMinusBegin = rotatedEnd - rotatedBegin
	loop.append(begin + endMinusBegin * (midX - rotatedBegin.real) / rotatedEndMinusBegin.real)

def getGeometryOutput(elementNode):
	'Get vector3 vertexes from attribute dictionary.'
	derivation = VoronoiDerivation(elementNode)
	complexPath = euclidean.getConcatenatedList(euclidean.getComplexPaths(derivation.target))
	geometryOutput = []
	topRight = derivation.inradius
	squareLoop = euclidean.getSquareLoopWiddershins(-topRight, topRight)
	loopComplexes = []
	for pointIndex, point in enumerate(complexPath):
		outsides = complexPath[: pointIndex] + complexPath[pointIndex + 1 :]
		loopComplex = getVoronoiLoopByPoints(point, squareLoop, outsides)
		loopComplex = intercircle.getLargestInsetLoopFromLoop(loopComplex, derivation.radius)
		loopComplexes.append(loopComplex)
	elementNode.attributes['closed'] = 'true'
	for loopComplex in loopComplexes:
		vector3Path = euclidean.getVector3Path(loopComplex)
		geometryOutput += lineation.SideLoop(vector3Path).getManipulationPluginLoops(elementNode)
	return geometryOutput

def getGeometryOutputByArguments(arguments, elementNode):
	'Get vector3 vertexes from attribute dictionary by arguments.'
	return getGeometryOutput(None, elementNode)

def getNewDerivation(elementNode):
	'Get new derivation.'
	return VoronoiDerivation(elementNode)

def getVoronoiLoopByPoint(inside, loop, outside):
	'Get voronoi loop enclosing the inside.'
	insideMinusOutside = inside - outside
	insideMinusOutside /= abs(insideMinusOutside)
	rotation = complex(insideMinusOutside.real, -insideMinusOutside.imag)
	rotatedInside = inside * rotation
	rotatedLoop = euclidean.getRotatedComplexes(rotation, loop)
	rotatedOutside = outside * rotation
	midX = 0.5 * (rotatedInside.real + rotatedOutside.real)
	voronoiLoop = []
	for pointIndex, point in enumerate(loop):
		nextIndex = (pointIndex + 1) % len(loop)
		addVoronoiPoint(point, loop[nextIndex], midX, voronoiLoop, rotatedLoop[pointIndex], rotatedLoop[nextIndex])
	return voronoiLoop

def getVoronoiLoopByPoints(inside, loop, outsides):
	'Get voronoi loop enclosing the inside.'
	for outside in outsides:
		loop = getVoronoiLoopByPoint(inside, loop, outside)
	return loop

def processElementNode(elementNode):
	'Process the xml element.'
	path.convertElementNode(elementNode, getGeometryOutput(elementNode))


class VoronoiDerivation:
	'Class to hold voronoi variables.'
	def __init__(self, elementNode):
		self.inradius = lineation.getInradiusFirstByHeightWidth(complex(10.0, 10.0), elementNode)
		self.radius = evaluate.getEvaluatedFloat(1.0, elementNode, 'radius')
		self.target = evaluate.getTransformedPathsByKey([], elementNode, 'target')
