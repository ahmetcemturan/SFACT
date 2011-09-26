"""
Help has buttons and menu items to open help, blog and forum pages in your primary browser.

"""

from __future__ import absolute_import
#Init has to be imported first because it has code to workaround the python bug where relative imports don't work if the module is imported as a main module.
import __init__

from fabmetheus_utilities import settings
from skeinforge_application.skeinforge_utilities import skeinforge_profile


__author__ = 'Enrique Perez (perez_enrique@yahoo.com) modifed as SFACT by Ahmet Cem Turan (ahmetcemturan@gmail.com)'
__date__ = '$Date: 2008/21/04 $'
__license__ = 'GNU Affero General Public License http://www.gnu.org/licenses/agpl.html'


def getNewRepository():
	'Get new repository.'
	return HelpRepository()


class HelpRepository:
	"A class to handle the help settings."
	def __init__(self):
		"Set the default settings, execute title & settings fileName."
		skeinforge_profile.addListsToCraftTypeRepository('skeinforge_application.skeinforge_utilities.skeinforge_help.html', self)
		settings.LabelDisplay().getFromName('- Announcements -', self )
		settings.LabelDisplay().getFromName('Fabmetheus Blog, Skeinforge Announcements & Questions:', self )
		settings.HelpPage().getFromNameAfterHTTP('fabmetheus.blogspot.com/', 'Fabmetheus Blog', self )
		settings.LabelDisplay().getFromName('RepRap for Dummies website:', self )
		settings.HelpPage().getFromNameAfterHTTP('www.reprapfordummies.net/', 'reprapfordummies.net', self )
		settings.LabelSeparator().getFromRepository(self)
		
		settings.LabelDisplay().getFromName('- Documentation -', self )
		settings.LabelDisplay().getFromName('Local Documentation Table of Contents: ', self )
		settings.HelpPage().getFromNameSubName('Contents', self, 'contents.html')
		settings.LabelDisplay().getFromName('Wiki Manual with Pictures & Charts: ', self )
		settings.HelpPage().getFromNameAfterHTTP('fabmetheus.crsndoo.com/wiki/index.php/Skeinforge', 'Wiki Manual', self )
		settings.LabelDisplay().getFromName('Skeinforge Overview: ', self )
		settings.HelpPage().getFromNameSubName('Skeinforge Overview', self, 'skeinforge_application.skeinforge.html')
		settings.LabelSeparator().getFromRepository(self)
		settings.LabelDisplay().getFromName('- Forums -', self )
		settings.LabelDisplay().getFromName('Skeinforge/SFACT Forum:', self )
		settings.HelpPage().getFromNameAfterWWW('forums.reprap.org/list.php?154', 'Skeinforge/SFACT', self )
		settings.LabelDisplay().getFromName('Getting Started with the RepRap:', self )
		settings.HelpPage().getFromNameAfterHTTP('oreilly.com/catalog/0636920021537', 'RepRap Book', self )
		settings.LabelDisplay().getFromName('moving to Skeinforge 40 and later:', self )
		settings.HelpPage().getFromNameAfterHTTP('forums.reprap.org/read.php?154,75635,77156#msg-77156', 'Skeinforge 40 and over', self )


		
		settings.LabelDisplay().getFromName('Extruder Calibration:', self )
		settings.HelpPage().getFromNameAfterHTTP('www.reprapfordummies.net/index.php/anything-that-can-not-be-downloaded-or-sent-by-email/34-introduction/54-volumetriccalibration', 'Extruder Calibration', self )
		settings.LabelDisplay().getFromName('Skeinforge Settings Thread:', self )
		settings.HelpPage().getFromNameAfterHTTP('dev.forums.reprap.org/read.php?12,27434', 'Skeinforge Settings Thread', self )
		settings.LabelSeparator().getFromRepository(self)
		self.wikiManualPrimary = settings.BooleanSetting().getFromValue('Wiki Manual Primary', self, True )
		self.wikiManualPrimary.setUpdateFunction( self.save )



	def save(self):
		"Write the entities."
		settings.writeSettingsPrintMessage(self)
