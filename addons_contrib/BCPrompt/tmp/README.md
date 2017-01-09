# BlenderConsolePrompt (BCP)

BCP is an addon that allows scripts to execute from Blender's Python console (REPL). I have many snippets that don't need a full addon status, but are useful enough that I do want to be able to have fast access to them. The simple `-ls` command shows a list of most common commands, the `-man` command shows a more exhaustive list of stored commands.

The following commands can be executed straight for the Blender Python console by pressing ctrl+enter after entering the command. You can alter the execute keyboard shortcut by changing it yourself in UserPreferences (or more permanently in the code.. tho I should probably add addonpreferences for this)

At the moment only one-shot commands are implemented, but future implementations will be modal/interactive and possibly a bpm (Blender package manager).

these are some of the non modal, one shot commands

Command String | Description
-------------- | -------------
cen | centers 3d cursor
cenv | centers 3d cursor and aligns all 3d views to it.
cen=some_value | where some value can be evalled, 3d cursor will be placed at it
ico | sees if developers icons addon is enabled (enables if not) [image](https://cloud.githubusercontent.com/assets/619340/5883599/368909cc-a354-11e4-9a8e-f442ebb8621e.gif)
wipe | un-links and removes objects, and all meshes
tt / tb | turntable, trackball
string! | anything followed by an exclamation mark is copied to buffer
string?se | search blender.stackexchange for everything infront of the ?
string??se | search stackoverflow for everything infront of the ??
string?py | search py docs ..
string?bpy | search blender bpy docs ..
psel | make a parent empty for selected objects
-sel somename | is select=True for all data.objects where `.name.startswith(somename)`
-gist -o somename | uploads all visible text blocks as a unified github anonymous public gist, then it will open the url in a browser. `-gist -o somename`
_svc | checking recent sverchok commits (github api) [image](https://github.com/zeffii/BlenderConsolePrompt/issues/3#issuecomment-74256330)
-man | opens github readme.md for the addon





