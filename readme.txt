I have modified Skeinforge to be more prectical and easier to tune.  features include:

-Will not mess up your old Skeinforge settings as it will use its own sfact_settings directory inside its own folder.

-Deleted unused plugins and unused settings.

-Namings changed to be more understandable.

-Important settings moved to top of Plugin Tab.

-Default values give good prints rightaway.

-Internally used Gcode files use extension .gmc now.

-Most Feedrates are now entered as values (mm/s) and their respective flowrates are 1 so you dont have to enter everything twice.

 CARVE:

-Extrusion width is now entered in mm insteda of a ratio to layer height.

CHAMBER:

-Moved Turn Extruder off at shutdown to Chamber.

-Added Turn PrintBed off at shutdown.

CLIP: 

Clip over Perimeter width is now calculated automatically.  The default is 1 and can be tuned from there.

DIMENSION:

-Added feature for calibration.

-Retract can be set conditionally depending on extrusion amount before retract and the travel move in retracted state (SF Beanshell).  Also retract can be forced to happen if moving over loops.

EXPORT: 

Replaced Export plugin with Gary Hodgson's plugin.  

-Option to export settings as Zip file or a single CSV file for sharing.

-Option to individually name the exported gcode files with description, timestamp and profile used.

FILL:

-Infill width over layerthickness setting is replaced by Extrusion Lines Extra spacing.

-Extrusion Lines Extra spacing is calculated automatically and defaults to 1 for tuning.

-Infill Overlap over Perimeter is also calculated internally and defaults to 1 so it can be easily tweaked.

INSET:

The ýnset value is now Overlap Removal and is also calculated internally with default 1 for tweaking.

PREFACE:

-Added the option to send Extruder reset (G92 E0) command before print so that the extruder does not spool back after priming. (Even without start.gmc file)

RAFT:

-Ordering, grouping and namings changed to reflect the use of interface settings for the support structures.

-Support feedrate and support flowrate can be set seperately.

-Support extension(s) are now more understandable.

-First Layer feedrates are given in mm/s instead of a ratio to the main feedrate.

SPEED:

-Feedrates are entered as values with respective flowrates as 1, instead of entering sam value again. (except for Bridge Feedrate).

-Nozzle Lift setting has been changed to Extra nozzle Lift over object and defaults to 0.

-Wipe is on by default and is around the 0 point

 

(CAUTION: If you want to use SFACT from within Pronterface, you need to copy the files into a folder called skeinforge within the folder of Pronterface.  Then you will need to manually copy or move the sfact_settings folder into that directory as otherwise SFACT wont see the default profiles shipped with it.) 

 

The latest working version is available here: http://www.reprapfordummies.net/downloads/SFACT.rar

The latest development version is: https://github.com/ahmetcemturan/SFACT

 You need to have Python installed (if you had Skeinforge running before thats sufficent)

1-Extract the contents of the RAR file into a Folder of your choice :)

Go into folder skeinforge_application.

2-Click skeinforge.py

3-Go to DIMENSION tab and enter your "measured" filament diameter.

4-Go to Carve, enter reasonable Layer height and Extrusion width values.

(Try to have layer height slightly lower than nozzle diameter and Extrusion width slightly wider than nozzle diameter.)

5-Click Skeinforge at bottom of tab and choose the STL file to slice.

6-Generated Gcode will be at the sam folder as the STL file.

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
-In FILL only Line Fill works reliably.
-In SPEED when you set perimeter speed exact same as fill  it will not work.  just make one of them slightly bigger (>1 is enough)



Updated and working versions of SFACT and help are under : www.reprapfordummies.net

and the development is under: https://github.com/ahmetcemturan/SFACT (Master branch)

License is same as Skeinforge (GNU Affero General Public License)