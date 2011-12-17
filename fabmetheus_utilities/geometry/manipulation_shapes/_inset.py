"""
Create inset.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities.geometry.creation import lineation
from fabmetheus_utilities.geometry.creation import solid
from fabmetheus_utilities.geometry.geometry_utilities.evaluate_elements import setting
from fabmetheus_utilities.geometry.geometry_utilities import boolean_geometry
from fabmetheus_utilities.geometry.geometry_utilities import boolean_solid
from fabmetheus_utilities.geometry.geometry_utilities import evaluate
from fabmetheus_utilities.geometry.geometry_utilities import matrix
from fabmetheus_utilities.geometry.solids import triangle_mesh
from fabmetheus_utilities.vector3index import Vector3Index
from fabmetheus_utilities import euclidean
from fabmetheus_utilities import intercircle
import math


__author__ = 'Enrique Perez (perez_enrique@yahoo.com)'
__credits__ = 'Art of Illusion <http://www.artofillusion.org/>'
__date__ = '$Date: 2008/02/05 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


globalExecutionOrder = 80


def getLoopOrEmpty(loopIndex, loops):
	'Get the loop, or if the loopIndex is out of range, get an empty list.'
	if loopIndex < 0 or loopIndex >= len(loops):
		return []
	return loops[loopIndex]

def getManipulatedPaths(close, elementNode, loop, prefix, sideLength):
	"Get inset path."
	radius = lineation.getStrokeRadiusByPrefix(elementNode, prefix)
	return intercircle.getInsetLoopsFromVector3Loop(loop, radius)

def getManipulatedGeometryOutput(elementNode, geometryOutput, prefix):
	'Get inset geometryOutput.'
	derivation = InsetDerivation(elementNode, prefix)
	if derivation.radius == 0.0:
		return geometryOutput
	copyShallow = elementNode.getCopyShallow()
	solid.processElementNodeByGeometry(copyShallow, geometryOutput)
	targetMatrix = matrix.getBranchMatrixSetElementNode(elementNode)
	matrix.setElementNodeDictionaryMatrix(copyShallow, targetMatrix)
	transformedVertexes = copyShallow.xmlObject.getTransformedVertexes()
	minimumZ = boolean_geometry.getMinimumZ(copyShallow.xmlObject)
	maximumZ = euclidean.getTopPath(transformedVertexes)
	layerThickness = setting.getLayerThickness(elementNode)
	importRadius = setting.getImportRadius(elementNode)
	zoneArrangement = triangle_mesh.ZoneArrangement(layerThickness, transformedVertexes)
	copyShallow.attributes['visible'] = True
	copyShallowObjects = [copyShallow.xmlObject]
	bottomLoopLayer = euclidean.LoopLayer(minimumZ)
	z = minimumZ + 0.1 * layerThickness
	bottomLoopLayer.loops = boolean_geometry.getEmptyZLoops(copyShallowObjects, importRadius, False, z, zoneArrangement)
	loopLayers = [bottomLoopLayer]
	z = minimumZ + layerThickness
	loopLayers += boolean_geometry.getLoopLayers(copyShallowObjects, importRadius, layerThickness, maximumZ, False, z, zoneArrangement)
	copyShallow.parentNode.xmlObject.archivableObjects.remove(copyShallow.xmlObject)
	belowLoop = []
	diagonalRadius = math.sqrt(0.5) * derivation.radius
	insetDiagonalLoops = []
	loops = []
	vertexes = []
	for loopLayer in loopLayers:
		insetDiagonalLoops.append(intercircle.getLargestInsetLoopFromLoop(loopLayer.loops[0], diagonalRadius))
	for loopLayerIndex, loopLayer in enumerate(loopLayers):
		vector3Loop = []
		insetLoop = intercircle.getLargestInsetLoopFromLoop(loopLayer.loops[0], derivation.radius)
		loopLists = [[getLoopOrEmpty(loopLayerIndex - 1, insetDiagonalLoops)], [insetLoop]]
		largestLoop = euclidean.getLargestLoop(boolean_solid.getLoopsIntersection(importRadius, loopLists))
		if evaluate.getEvaluatedBoolean(True, elementNode, prefix + 'insetTop'):
			loopLists = [[getLoopOrEmpty(loopLayerIndex + 1, insetDiagonalLoops)], [largestLoop]]
			largestLoop = euclidean.getLargestLoop(boolean_solid.getLoopsIntersection(importRadius, loopLists))
		for point in largestLoop:
			vector3Index = Vector3Index(len(vertexes), point.real, point.imag, loopLayer.z)
			vector3Loop.append(vector3Index)
			vertexes.append(vector3Index)
		if len(vector3Loop) > 0:
			loops.append(vector3Loop)
	if evaluate.getEvaluatedBoolean(False, elementNode, prefix + 'addExtraTopLayer') and len(loops) > 0:
		topLoop = loops[-1]
		vector3Loop = []
		loops.append(vector3Loop)
		z = topLoop[0].z + layerThickness
		for point in topLoop:
			vector3Index = Vector3Index(len(vertexes), point.x, point.y, z)
			vector3Loop.append(vector3Index)
			vertexes.append(vector3Index)
	geometryOutput = triangle_mesh.getMeldedPillarOutput(loops)
	return geometryOutput

def getNewDerivation(elementNode, prefix, sideLength):
	'Get new derivation.'
	return OutsetDerivation(elementNode, prefix)

def processElementNode(elementNode):
	"Process the xml element."
	solid.processElementNodeByFunctionPair(elementNode, getManipulatedGeometryOutput, getManipulatedPaths)


class InsetDerivation:
	"Class to hold inset variables."
	def __init__(self, elementNode, prefix):
		'Set defaults.'
		self.radius = evaluate.getEvaluatedFloat(2.0 * setting.getPerimeterWidth(elementNode), elementNode, prefix + 'radius')
