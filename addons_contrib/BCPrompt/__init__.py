# ***** BEGIN GPL LICENSE BLOCK *****
#
# This program is free software; you may redistribute it, and/or
# modify it, under the terms of the GNU General Public License
# as published by the Free Software Foundation - either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, write to:
#
#   the Free Software Foundation Inc.
#   51 Franklin Street, Fifth Floor
#   Boston, MA 02110-1301, USA
#
# or go online at: http://www.gnu.org/licenses/ to view license options.
#
# ***** END GPL LICENCE BLOCK *****

bl_info = {
    "name": "Console Prompt",
    "author": "Dealga McArdle",
    "version": (0, 1, 3),
    "blender": (2, 7, 4),
    "location": "Console - keystrokes",
    "description": "Adds feature to intercept console input and parse accordingly.",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Console"}

import bpy

'''
console.do_action can be added to:
  UserPreferences/input/Console/
using the ' + new ', i find ctrl+Enter a convenient key combo.
Possible blender bug when adding keycombos for console specifically.

https://github.com/zeffii/BlenderConsolePrompt/issues/1

'''


class ConsoleDoAction(bpy.types.Operator):
    bl_label = "ConsoleDoAction"
    bl_idname = "console.do_action"

    def execute(self, context):
        m = bpy.context.space_data.history[-1].body
        m = m.strip()
        if m == "cen":
            '''cursor to center'''
            context.scene.cursor_location = (0.0, 0.0, 0.0)

        elif m.endswith('!'):
            '''copy current line to clipboard'''
            m = m[:-1]
            context.window_manager.clipboard = m
            print('copied: "{0}"'.format(m))

        elif m == 'vtx':
            if hasattr(bpy.ops.view3d, 'autovtx'):
                bpy.ops.view3d.autovtx()

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == "__main__":
    register()
