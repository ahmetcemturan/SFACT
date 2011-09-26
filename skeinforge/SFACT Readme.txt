I have modified Skeinforge to be more practical and easier to tune.  features include:


A more up to date version could be found at http://dl.dropbox.com/u/38819298/SFACT%20Readme.txt

Also trying to get the SFACT wiki up and running: https://github.com/ahmetcemturan/SFACT/wiki

SFACT is at home: http://www.reprapfordummies.net




-Will not mess up your old Skeinforge settings as it will use its own sfact_settings directory inside its own folder.

-Deleted unused plugins and unused settings.

-Namings changed to be more understandable.

-Important settings moved to top of Plugin Tab.

-Default values give good prints rightaway.

-Internally used Gcode files use extension .gmc now.

-Most Feedrates are now entered as values (mm/s) and their respective flowrates are 1 so you dont have to enter everything twice.

 CARVE:

-Extrusion width is now entered in mm instead of a ratio to layer height.

CHAMBER:

-Moved Turn Extruder off at shutdown to Chamber.

-Added Turn PrintBed off at shutdown.

CLIP: 

Clip over Perimeter width is now calculated automatically.  The default is 1 and can be tuned from there.

DIMENSION:

-Added feature for calibration.

-Retract can be set conditionally depending on extrusion amount before retract and the travel move in retracted state.  Also retract can be forced to happen if moving over loops.

EXPORT: 

Replaced Export plugin with Gary Hodgson's plugin.  

-Option to export settings as Zip file or a single CSV file for sharing.

-Option to individually name the exported gcode files with description, timestamp and profile used.

FILL:

-Infill width over layerthickness setting is replaced by Extrusion Lines Extra spacing.

-Extrusion Lines Extra spacing is calculated automatically and defaults to 1 for tuning.

-Infill Overlap over Perimeter is also calculated internally and defaults to 1 so it can be easily tweaked.

INSET:

The inset value is now Overlap Removal and is also calculated internally with default 1 for tweaking.

PREFACE:

-Added the option to send Extruder reset (G92 E0) command before print so that the extruder does not spool back after priming. (Even without start.gmc file)

RAFT:

-Ordering, grouping and namings changed to reflect the use of interface settings for the support structures.

-Support feedrate and support flowrate can be set seperately.

-Support extension(s) are now more understandable.

-First Layer feedrates are given in mm/s instead of a ratio to the main feedrate.
-A travel feedrate for the first layer can be specified now.

SPEED:

-Feedrates are entered as values with respective flowrates as 1, instead of entering same value again. (except for Bridge Feedrate).
-Note that Flowrates are always in reference to the respective Feedrate.  (No need to change the flowrate when you change the speed, the ratio is calculated accordingly..)

-Nozzle Lift setting has been changed to "Extra nozzle Lift over object" and defaults to 0.

-Wipe is on by default and is around the 0 point

 

(CAUTION: If you want to use SFACT from within Pronterface, you need to copy the files into a folder called skeinforge within the folder of Pronterface.  Then you will need to manually copy or move the sfact_profiles folder into that directory as otherwise SFACT wont see the default profiles shipped with it.) 

For alterations files to work You need to put the alterations files into: ..\skeinforge_application\alterations\  directory...

 

The latest working version is available here: http://www.reprapfordummies.net/downloads/SFACT.rar

The latest development version is: https://github.com/ahmetcemturan/SFACT

 You need to have Python installed (if you had Skeinforge running before thats sufficent)

1-Extract the contents of the RAR file into a Folder of your choice :)

Go into folder skeinforge_application.

2-Click skeinforge.py

3-Go to DIMENSION tab and enter your "measured" filament diameter.

4-Go to Carve, enter reasonable Layer height and Extrusion width values.(this step is not necessary for the first try)

(Try to have layer height slightly lower than nozzle diameter and Extrusion width slightly wider than nozzle diameter.)

5-Click Skeinforge at the bottom of the tab and choose the STL file to slice.

6-Generated Gcode will be created in the same folder as the STL file.

Enjoy good Prints.

 

CALIBRATION:

If you should feel the need to calibrate:

1-Print a thin walled test object (Single wall)

Measure the width of the wall.

2-Go to Dimension and check the Calibration Checkbox.

3-Enter the Measured value.

4-ReSkein and print the object. (During the Skein the command window will display a packing ratio.  Note it somewhere (the first 4 digits are enough)

5-If satisfied with the print, go to DIMENSION tab uncheck the calibration checkbox and enter that value into the packing density Box.

6-You are done.  Repeat when needed.  Changing extrusion values should not necessarily arise the need for recalibration...


Known Bugs: 
-Skin plugin skips first extra perimeter loop if extra perimeters set to 1.  Works when 0 or >=2.
-will not create correct 


Updated and working versions of SFACT and help are under : www.reprapfordummies.net

and the development is under: https://github.com/ahmetcemturan/SFACT (Master branch)

License is same as Skeinforge (GNU Affero General Public License)


14.9.2011

Main changes:
DIMENSION:Retraction handled differently.
Now the only variable is the Oozerate.  SFACt automatically does retraction based on the duration of the move that it will do in retracted state.
SPEED and INSET 
Bridging:
Bridge settings are calculated automatically so that your extrusion xsection equals the nozzle-orifice x-section..
As it will not change the layer height it will alter the extrusion width to achieve that.
The default bridge feedrate is now referencing the perimeter feedrate.  
Also the settings for bridge spacing in INSET is now calculated according to the newly calculated extrusion width of the bridge extrusion.
You can experiment with values from 1-2 for the spacing that should all give decent results.  ý personally prefer closer to 2 and have set default accordingly.
RAFT:
Raft feed and flowrates are working now.
First layer travel feedrate now controls all travel moves..
EXPORT:
The export archiving commands have moved to the top menu. (>Analyze>Synopsis)
There is also an option for Gen3 users to have small gcode with their Z-commands on a seperate line (for faster Z moves)
If you get memory errors during skein disable skeiniso. (enabled by default)
For being able to open a preview lateron you should enable exporting penultimate gcode.
CARVE:Extra decimals range is now 2-6 with 4 as default. (needed for the finer printing possibilities..)
COOL: You can now specify a minimum feedrate so you dont end up having the printhead move at 2mm/s and ruining your top layer.
SKIN and LEADIN: Is calculating the flow correctly now.  But a bug prevents the inner ring from being extruded when the extra perimeters option in Fill is set to 1. (0 or more than one works without problems..)
Also I found that the option to prefer loops in INSET produces better result hence is set as default.

GENERAL:I also changed most of the broken links that were in the top menu.
A more detailed explanation will be posted at www.reprapfordummies.net 
