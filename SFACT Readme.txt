I have modified Skeinforge to be more practical and easier to tune.  features include:


A more up to date version could be found at http://titanpad.com/XTUJXiNHmd

Also trying to get the SFACT wiki up and running: https://github.com/ahmetcemturan/SFACT/wiki

SFACT is at home: http://www.reprapfordummies.net






Main FAQ link: http://doiop.com/FAQMain


Sfact FAQ


Below answers are based on default SFACT settings.  If you have messed them up you can revert to the defaults by closing SFACT and deleting the sfact_profiles directory afte rwards.

This will delete all profiles and SFACt will recreate one with defaults on restart.


Plugin Names are Printed CAPS


Q:        How do you open SFACT (or skeinforge)? Also, how do you load a .STL file in order to create the .GCode file?

A:   

?Open the file skeinforge.py inside the skeinforge_application directory.  Click the "skeinforge" button to get an open dialog for the stl you want to skein.


Q:    Why do my Prints come out crappy.  Is something wrong with SFACT?

A:    

?First of all please consider that SFACT was created/is maintained by someone who has no Programming background.  He sled into this while wanting to write documentation for setting up Skeinforge, found that it would be easier to make a spreadsheet for calculating the many Skeinforge settings and finally found that it would be wisest to enter the formulas directly into Skeinforge. 

? That resulted in SF by ACTion68 (ACT being his Initials) >> SFACT.  So it is possible that there are faults and we welcome it if you inform us about them.  BUT if you have never had a successful print before and are printing with the default settings of SFACT, you can be sure (about 99%...   yeah I measured..:P) that it is some other problem than SFACT.

?Too many people had slam-dunk success with their first prints.  Just forget  everything you know about Skeinforge settings. (feed=flow and things like that).

?Make your first print with default settings of SFACT.   They will be created when you first run SFACT.  Only change Filament diameter to the diameter of your filament.

?The default settings assume you are printing with a 0.5 nozzle. (And you should better be if you are just beginning).

?Possible faults for just inconsistent prints are under: Where do I look for possible hardware problems?

?Look here for some hints on common print problems: http://richrap.blogspot.com/2011/10/art-of-failure-when-3d-prints-go-wrong.html


Q:    Where do I look for possible hardware problems?

A:    

?Sloppiness of anything. the belts, bolts, smooth-rods, gears, motors.... anything will unavoidably worsen you print quality.  And they dont add up but they multiply....

?Bad hotend: You might have self sourced most of the parts but stay with the experienced folks for the hot end.  For recommendations visit IRC channel or look up in reprap.org.

?Bad filament feed system.. I could also have said hobbed bolt but You could also have some other system.  Inconsistent feeding will give you very very bad prints.  You will not be able to calibrate.  Quick way to test this is when you extrude a long piece say 50mm of filament  mark the filament with stripes and then let it slip through your fingers.  It should have one continuous move...  Other methods are to do the calibration of 100mm several times.  The filament should be pulled in the same distance every time. While doing this calibration extrude at no more than 100mm/min, anything faster and your hotend might not be able to hold a high enough temperature.  It is not too bad if its say 98mm, as long as it is 98mm every time.  You can correct for that during SFACT calibration later.

?A quick check for the   health of the filament feeding system is to make a reference mark on the filament, extrude a certain distance (not too much as you dont want to come the filament loose from the extruder later)  then retract the same amount and see whether the mark arrives at the same point.  20-30mm should be a safe distance for most extruders.  It is no use trying to calibrate/get good prints if your feed is not consistent.

?Filament that has soaked up humidity.  Most plastics love to soak up the environments humidity.   So does your filament.  But H20 becomes a gas at 100oC.  So the humidity/water in your filament becomes a gas that pushes your filament out 

?in bursts or less severe case you have a very runny nozzle..   No way You will be able to stop that ooze and still get a decent print.   You need to dry that filament.  For PLA it is recommended to dry in an oven at 60oC.  You need to have some fan circulation during the drying process.  PLA will start to soften at that temperature so keep that in mind when you put it in the oven.  It will get soft and take the shape of the material it sits on.  Best is to try small amounts first to make sure the oven shows tha right temperature.    About 2-4hrs the drying will take.  And reseal the filament after use.  It will soak humidity again...

.

Q:    How do I calibrate Sfact?

A: 

?DIMENSION:  Measure your filament width and enter it (measure across multiple places and enter the average to 2 sig figs (3.1 or 1.7 respectfully)

?Inset: Enter your nozzle diameter (no need to measure, just enter the number you bought it as. Nozzle diameter only affects bridging.

?Set your Filament Packing Density ratio to 1 before beginning this process

?Print the _40x10.STL file included with Sfact. The default extrusion width in SFACT is 0.6

?Using Calipers measure the wall thickness of all 4 sides of the thin wall cube.  Throw out the largest value, and average the other 3. (Be sure you measure from the top of the box, not the bottom, the bottom might be flared out because of the 1st layer not being perfectly level.  Also if you have big variations it is a good idea to measure the side that is extruded last as the extrusion will have mostly stabilise'''d by then (after the Z-move).  Try to measure the smallest number of layers possible from top as the slightest vertical misalignment of your layers will increase the measured value.  Ideally a single layer would be best but very difficult with regular calipers. (Make sure the measuring device is not biting into the filament during measurement.)

?Go Back in Sfact to DIMENSION and click the "Calibrating" radio dial and enter the measurement into "Measured Width of Extrusion".  Reskein the _40x10.STL file.

?At the end of the skeining process you will see (on the command window) a new packing density ratio, it should be somewhere between 1.2 and .8 .  Enter it into the filament packing density ratio box(called "E-steps Corrector" in later versions of SFACT). (If it's more off than that you very likely have a badly calibrated Estep on 1 of your axis�s.  This is not too much of a problem when you want to get to printing rightaway but be aware that bad precision does not add up but multiplies...  So go back later and fix it by re-calibrating E-steps)

?Do not print the G-code that is output with the "Are You Calibrating" checkbox on.   Untick the checkbox and skein again.

?Print the created Gcode.

?Remeasure.  

�If the measured wall width is now equal to your extrusion width set in the "Carve" tab, you're done.

�If not, just enter the newly measured value into the measured width in DIMENSION.  repeat until you are happy with the result. (remember to tick the checkbox "Are You Calibrating" to calculate new values based on the new "Measured With Of Extrusion" value)

?Note:  You can interrupt and measure the print as soon as you feel the extrusion has stabilised.

?Tip:  To avoid extruder related inconsistencies it might be a good idea to turn heat up, to a level that really reduces backpressure.  I have calibrated with 250c for PLA as my bolt was bad and slipping.  BUT BE CAREFUL!!!  TOO HIGH EXTRUSION TEMPERATURES CAN DAMAGE YOUR EXTRUDER/PRINTER.


Q:    The Thin walled print comes out dead on, but my top and bottom layers are overfilled, how do I correct this?

A:

?In the FILL plugin in Sfact you can change the distance between the parallel lines as well as the concentric rings (extra perimeters).  They are controlled by Extrusion lines extra spacing variable.  The default value is 1.  It adjusts itself automatically according to your other settings and this varibale is just for tuning.  Increasing it will make the spaces between these lines bigger.  (with "these" I mean all the layers that have parallel lines as well as the lines in the line fill.  If you reduce the number .95 they will move closer and you will have a more "packed layer".  So if you need to have say a watertight bottom you might need to decrease the spacing (0.95).

?Another way to reduce the full layers density is to turn down the main flow rate.  This has the unfortunate drawback of also reducing the density of your infill.  Always remember that reducing the flowrate means (as the height is given by the space between the already printed piece and the nozzle) that you are changing the extrusion width. This can fix the issue, but should NOT be a 1st choice. 


Q:    What Do I need to change to make SFACT work on my specific printer?

A:

?In SFACT Settings need to be customized only according to your nozzle size (under INSET set nozzle diameter - 0.5mm by default)  and filament diameter (under  DIMENSION set filament diameter - 2.8mm by default).

?The nozzle diameter dictates also your setings in CARVE: it would be very wrong to expect an orifice of 0.5mm diameter to put out extrusion of 0.5x1mm.  That would be more than twice the amount it is capable to extrude. 

�A good rule of thumb is to set layer height slightly lower than the nozzle diameter and extrusion width a bit above the nozzle diameter. ( LayerHeight + ExtrusionWidth = slight bit more than 2xNozzleDiameter)

?Limitations on speed are only set by the capability of your extruders heater, slippage of the filament, mechanical friction/binding etc., and weight of moving parts (acceleration needs to be set slower resulting in lower topspeeds..)


Q:    What does COOL do?

A:

?Cool will slow down your speed to allow the layer to cool before you move to the next layer.  

?In cool you define a minimum layer duration and a minimum feedrate.. (It wont go slower than that as otherwise it will also spoil your print.)


Q:    Why do I need to calibrate in SFACT.  Doesnt calibrating E-steps in FW do that already?

A:

?In theory yes.  If you are 100% sure that you have set the E-steps right you could skip SFACT Calibration.  

?On the other hand, calibrating the E-steps in Firmware is only one step beyond calculating your E-steps based on Motor step angle, microstepping ratio and gearing. Whereas the SFACT calibration allows you to calibrate based on actual extruded material, compensating for all possible errors inbetween.


Q:    What the heck is SKIN?

A:

?When SKIN is enabled SFACT will slice your model regularly with a layer thickness as is set in CARVE.  

?Then it will split your perimeter extrusion into 4. (e.g, a 0.4x0.6 extrusion will become 2x0.2x0.3 extrusions stacked onto each other.  

?This will NOT improve resolution but it will effect your finish as instead of having 0.4mm (half layer height) ridges you will have 0.2mm  (quarter layer height) ridges.

?Possible problems:

� If your layer height and extrusion width is already low, trying to extrude 1/4th of the previous cross-section will probably result in very inconsistent flow.

�Another problem is the decimals.  You might find that the output code does not increase as the increment is so little that it gets lost during rounding.

�The situation is even worse with relative E-steps.


Q:    Why are the width setting in SFACT absolute and not a ratio as in SF?

A:

?The reason the width settings in SF are ratios to the layer height is to decrease the amount of settings that you need to adjust when you change layer height,  In SFACT these settings are already interconnected (in the background).  So you can set height and width of extrusion freely.


Q:    Can I set width and height of extrusion at will or are there any guidelines?

A:

?Regarding the calculation and the generated G-code the answer is yes. BUT the real world has limitations:

�Your hot-end has a limit.  It is imposed by the nozzle diameter, shape and internal details, as well as the capacity of your heater/heating system and how good it can transfer the heat to the filament.  An upper as well as a lower limit.  

�If you go below the lower limit, you will have inconsistent extrusion. (Just imagine a water hose that fows only little water. The flow will wander and be inconsistent.)  This effect becomes worse when your filament has soaked up humidity as it will create steam pockets that will cause small jets of filament during print.

�If you go higher than the limit you will have lots of pressure in the nozzle.

?This can cause excessive stringing as plastic will still flow when the extruder motor stops, as it will try to get the pressure down.  Retraction helps here a bit but it will never release the pressure instantly.  This is the best case...

?If all parts of your Extruder are sound and the extruder just cant handle that much flow, you will strip filament.  Stripped filament can cause less grip, and therefore even more stripping.  It also could cause inconsistent flow if the teeth are partly jammed with plastic as it will alter the "hob diameter".  

?Worst case You could have leaks in your hotend.  In such a case try to d isassemble the hot-end before letting it cool,  otherwise it might become impossible to seperate the parts.

�UTMOST CARE IS NEEDED AS YOU WILL BURN YOURSELF. (Not otherwise but be prepared to have burns..) I am using Latex covered textile working gloves when working with the hot parts of my printer.

�Plastic parts might have become soft,  try to reinstate their original shape/state before they cool down.

�Filament gets to a rubbery state at some temperature (PLA about 120-130c)  Thats the best time to clean it off.  (with some experience you can take off the whole contents of the nozzle in one piece)

?I found that it is a good value to have the layer height the same or slightly less than the nozzle diameter.

?The width of extrusion should be chosen so that you stick to the formula:  Layer height + Extrusion Width  is slightly bigger (110-125%) than double the nozzle diameter 


Q:    What exactly does the Infill Extra Spacing in FILL do?

A:

?The main indicator for wrong settings here is too sparse or too thick top layer.

?If this happens you probably have wrong calibaration (as in your extrusion is not coming out the same as the setting in Carve.)

?It is the setting that adjusts the spacing of the parallel or concentric extrusion lines (Top and bottom fill, regular line fill and extra perimeters).

?A similar setting is also in Inset.  That one only will affect bridge layers.


Q:    What are bridge/bridge layers? 

A:

?Bridge layers are layers that have areas that have no material underneath.

�Bridges that span between two filled areas.

�These can be extreme overhangs.

?SFACT will try to print these areas wit a 100%fill and in the direction of the shortest distance of the bridge.

?You can set the feed/flowrate for bridges under SPEED.  It is a relative setting that is calculated by multiplying the perimeter feed/flow values.  

?Settings under INSET let you adjust the spacing of these 100% fill lines and also the nozzle diameter setting is needed here to be able to calculate a "natural flow" for the nozzle.

?The default settings will result in an extrusion that has obviously same layer height as the rest of the print, the extrusion width will be set to a value that I call "natural flow" or "native flow".  That is the extrusion X-section is the same as the nozzle diameter X-section.

?The bridge settings will only kick in if Infill in direction of bridges is checked.  This setting will cause for some fully filled layers if you are printing shapes with all-around overhangs (especially organic shapes or statue like things).  They might appear random to you but this is the reason for that.


Q:    Why is TEMPERATURE disabled by default.  

A:

?The SFACT defaults are set the way that they provide failsafe defaults for beginners.  

?SFACT is as tuneable as SF.

?Setting the temperatures in SFACT would cause the G-code that is generated to include Temperature codes.

?They would be issued every time the print type changes. (You dont notice it but it happens more often than you think..)

?Temperature settings are very different for every configuration.  (plastic type, color, humidity, thermistor, thermistor placement, nozzle diameter, print speed, extrusion diameter)

?A wrong setting is ver difficult to correct during print as it will try to go back to the G-Code settings every time the print type changes.

?Instead of that we advise to set the temperature in the host program and adjust if necessary..

?If you are really sure that you are able to choose correct temperatures go ahead and enable it..



Q:    My alterations and start.gmc, end.gmc files are not working.   What am I doing wrong?

A:

?You have to place them into the skeinforge_application\alterations folder.  Unfortunately there are other folders with the name alterations around but this would be the correct one!


Q:    What is the penultimate gcode file I am getting?

A:

?It is the G-code file that SFACT uses to carry data from plugin to plugin.  It has lots of extra information inside.

�At the start of the file there are most of your settings.

�Each section is marked whether it is fill, loop, perimeter etc.

�You can reopen a penultimate file with skeinforge to have a preview in SKEINLAYER or SKEINISO

�It is a great source of information if you need help.


Q:    Why are there now two dimension plugins (DIMENSION and OLDDIMENSION)?

A:

?DIMENSION Plugin has a new method to calculate Retraction.  It calculates the duration of the upcoming travel move and retracts accordingly. 

?OLDDIMENSION is the OLD-DIMENSION Plugin.  It behaves the way You probably are used to.

?

Q:    What happened to the old retraction settings?  What the hell is oozerate?

A:

?Oozerate is abandoned in recent versions of SFACT

?The old retraction is still available under the OLDDIMENSION tab.

?The current DIMENSION calculates retraction differently.

?It assumes that you are having either a drippy or very tight nozzle that oozes not at all... (Or anything inbetween).

?The oozerate is what you are estimateing when you extrude filament and then stop, it is about the amount of filament that oozes from your nozzle in standby in one minute.(in mm)

?SFACT will then calculate how long the travel move in retracted state will take and retract accordingly.  So if the next move is very short it will hardly retract (You can boost this with the minimum value..) or if it is a long move it will make a big retraction.(the max value is there to avoid any mishaps if somehow you have a very slow travel move or similar, otherwise the filament will pop out of the extruder..)

?


Q:    What is CLIP.  What does it do?

A:

?CLIP adjusts the gap between the start and the end of the perimeter (outermost) extrusion.  If there was no clip the halves of the extrusions would overlap, causing overfill at the join.  Too much clip will cause open perimeters.

?Clip is to create a distance between the start and endpoint of a loop.  Be it a perimeter or inner loop..

?The default of 1 in sfact will create a space (space is only there fort he extrusion path.) that is just enough apart to have a joined perimeter according to your extrusion settings.  It is calculated similarly to how top layer extrusion spacing is calculated..

?

