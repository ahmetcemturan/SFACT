# skFrontend

A Skeinforge 50 Frontend for 3D Printing

[http://reprapide.fr/skfrontend-a-skeinforge-frontend](http://reprapide.fr/skfrontend-a-skeinforge-frontend)

Version 1.3 november 2012

## Introduction

Once good Skeinforge settings are found and good prints obtained, RepRap ordinary use only leads to modify a few Skeinforge settings.

Without running Skeinforge, skFrontend allows to modify those settings and to run G-code calculation, without being faced to a complex interface. Skeinforge common use becomes easier and, if basic settings are established by an expert, becomes possible for those who don't know this software.

As Skeinforge, skFrontend is written with Python and uses Tkinter, no additional software is needed. skFrontend reads and writes settings into it's dedicated profile configuration files. Once settings are saved and a file selected, skFrontend runs Skeinforge's toolchain by calling craft.py.

Known problem: Save Modifications button state, activated or deactivated, isn't updated if values are edited into the three spinboxes: Speed Rate, Flow Rate and Infill Solidity. It is updated when values are modified with spinboxes arrows. Workaround: first change values with arrows then edit.

## Modifiable Settings

Of course settings are those I often change, perhaps others could be added…

*   **Used Profile**
    Picked among profiles into Skeinforge's extrusion directory.
*   **Layer height**
    Layer Height into Carve plugin.
*   **Print velocity**
    Feed Rate into Speed.
*   **Plastic output**
    Flow Rate into Speed. When Feed Rate is changed Flow Rate is automatically modified to be equal to Feed Rate. It can also be changed independently.
*   **First layer speed** (ratio)
     The for 1st layer parameters into Speed are set together at the same value. They concern feed and flow rates for infill and perimeter, which can be reduced by ratio.
*   **Plastic filling rate**
    Infill Solidity into Infill. Unlike Skeinforge, this rate is expressed as a percentage, not as 0 to 1 value, which I found more easy to understand. skFrontend converts.
*   **Perimeter speed** (ratio)
     The two perimeter parameters into Speed are set together at the same value. They concern feed and flow rates for perimeter, which can be reduced by ratio.
*   **Multiply plugin activation/deactivation**
     Multiply can be activated when printing only one part, to modify print location.
*   **Lines and columns numbers**
    Number of Columns & Number of Rows into Multiply. To print several parts at once.
*   **Surrounding layers number**
    Layers To into Skirt. A large layers number may avoid warping. Skirt is activated by skFrontend if number is greater than 0, deactivated if not.

## Configuration

### 1 - Profile(s)

Be sure to have at least one profile into Skeinforge's extrusion directory. Locations :

*   Linux: `/home/userName/.skeinforge/profiles/extrusion`
*   OS X: `/Users/userName/.skeinforge/profiles/extrusion`
*   Windows: `C:\Users\userName\.skeinforge\profiles\extrusion`
*   Windows: `C:\Documents and Settings\userName\.skeinforge\profiles\extrusion`

### 2 - Three mandatory settings

All parameters are set into **config.py**, skFrontend's configuration file. It contains explanations. Three mandatory parameters must be set:

*   `skDefaultProfileName`, name of the default profile, which must exist
*   `skProfilesDirectory`, absolute path Skeinforge's extrusion profiles directory
*   `skCraftPath`, absolute path to Skeinforge's Craft plugin

Windows: double backslashes into `skCraftPath` and `skProfilesDirectory`.

### 3 - Optional settings

The rest of the setup is optional and concerns user interface, especially values into interface controls:

*   `layerThicknessList` layer thickness dropdown menu, model `("0.25", "0.30", "0.40")`
*   `feedRateMinimumValue` and `feedRateMaximumValue` minimum and maximum Feed Rate values spinboxes
*   `flowRateMinimumValue` and `flowRateMaximumValue` minimum and maximum Flow Rate values spinboxes
*   `multiplyRowList` and `multiplyColList` lines & columns numbers dropdown menus
*   `skirtLayersList` surrounding layers number dropdown menu

Interface langage can also be set…

*   `interfaceLanguage`: `fr` french, `en` english, `de` german.

…and absolute acces path to default STLs directory may be set too:

*   `STLFilesDefaultDirectory`

Name of your Python interpreter:

*   `pythonInterpreter`: `python` (default) or `pypy` or another

## Running

Linux and OS X terminal command:

`python /path/to/skFrontendDirectory/skFrontend.py`

Windows: skFronted or alias can be double-clicked. Path to your Python install directory (<span style="font-family:monospace">C:\Python27</span> for example) must be set into <span style="font-family:monospace">Path</span> environment variable.