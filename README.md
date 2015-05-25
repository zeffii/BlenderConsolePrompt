This is much cooler than you think. Read on!

# BlenderConsolePrompt

[![Join the chat at https://gitter.im/zeffii/BlenderConsolePrompt](https://badges.gitter.im/Join%20Chat.svg)](https://gitter.im/zeffii/BlenderConsolePrompt?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)


BCP is an addon that allows me to run various scripts from Blender's Python console (REPL). I have many useful code snippets that are too short to warrent all the bloat that comes with writing addon-boilerplate, but that are useful enough that I do want to be able to trigger at will. Instead of writing addons for short snippets I now add them to various snippet files and givem them a short trigger name. This helps maintain workflow and the simple `-ls` command shows the list of most common commands, the `-man` command shows an exhaustive list of stored commands.

At the moment only one-shot commands are implemented, but future implementations will be modal/interactive and possibly a bpm (Blender package manager).

these are some of the non modal, one shot commands

Command String | Description
-------------- | -------------
cen | centers 3d cursor
cenv | centers 3d cursor and aligns all 3d views to it.
cen=some_value | where some value can be evalled, 3d cursor will be placed at it
vtx | sees if tinyCAD is enabled and performs VTX, (or first enables it)
xl (XL) | sees if tinyCAD is enabled and performs XALL, (or first enables it)
ico | sees if developers icons addon is enabled (enables if not) [image](https://cloud.githubusercontent.com/assets/619340/5883599/368909cc-a354-11e4-9a8e-f442ebb8621e.gif)
wipe | un-links and removes objects, and all meshes
tt / tb | turntable, trackball
-debug | downloads / enables index visualizer with polygon bg
syntax | sets text editor to syntax highlighting, wrap, linenumber, margin
string! | anything followed by an exclamation mark is copied to buffer
string?se | search blender.stackexchange for everything infront of the ?
string??se | search stackoverflow for everything infront of the ??
string?py | search py docs ..
string?bpy | search blender bpy docs ..
_svc | checking recent sverchok commits (github api) [image](https://github.com/zeffii/BlenderConsolePrompt/issues/3#issuecomment-74256330)
-gist -o somename | uploads all visible text blocks as a unified github anonymous public gist, then it will open the url in a browser. `-gist -o somename`
-sel somename | is select=True for all data.objects where `.name.startswith(somename)`
-psel | make a parent empty for selected objects
-man | opens github readme.md for the addon





