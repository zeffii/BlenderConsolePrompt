This is much cooler than you think.

# BlenderConsolePrompt
A small project to add features to blender's python console. We can use the console to execute commands, instead of key-combos. Sometimes we run out of sane key combos or find that they get complex. At the moment only one-shot commands are implemented, but future implementations will be modal/interactive and possibly a bpm (Blender package manager).

these are the non modal, one shot commands

Command String | Description
-------------- | -------------
cen | centers 3d cursor
cen=some_value | where some value can be evalled, 3d cursor will be placed at it
vtx | sees if tinyCAD is enabled and performs VTX, (or first enables it)
xl (XL) | sees if tinyCAD is enabled and performs XALL, (or first enables it)
ico | sees if developers icons addon is enabled (enables if not)
wipe | un-links and removes objects, and all meshes
tt | turntable
tb | trackball
syntax | sets text editor to syntax highlighting, wrap, linenumber, margin
string! | anything followed by an exclamation mark is copied to buffer
string?se | search blender.stackexchange for everything infront of the ?
string??se | search stackoverflow for everything infront of the ??
string?py | search py docs ..
string?bpy | search blender bpy docs ..
_svc | checking recent sverchok commits (github api) [image](https://github.com/zeffii/BlenderConsolePrompt/issues/3#issuecomment-74256330)

![img](https://cloud.githubusercontent.com/assets/619340/5883599/368909cc-a354-11e4-9a8e-f442ebb8621e.gif)
