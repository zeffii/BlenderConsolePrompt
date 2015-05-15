import bpy
from console_python import add_scrollback

from .bc_command_dispatch import (
    in_scene_commands,
    in_search_commands,
    in_sverchok_commands,
    in_core_dev_commands,
    in_modeling_tools,
    in_upgrade_commands)

history_append = bpy.ops.console.history_append
addon_enable = bpy.ops.wm.addon_enable


def print_most_useful():
    content = '''\

for full verbose descriptor use -man

command    |  description
-----------+----------------
tt / tb    |  turntable / trackball nav.
cen        |  centers 3d cursor
cento      |  centers to selected
cen=<  >   |  center to eval , eg: cen = 2,3,2
endswith!  |  copy current console line if ends with exclm.
x?bpy      |  search blender python for x
x?bs       |  search blenderscripting.blogspot for x
x?py       |  search python docs for x
x?(?)se,   |  x??se searches B3D stackexchange, x?se just regular SE
vtx, xl    |  enable or trigger tinyCAD vtx (will download)
ico        |  enables icon addon in texteditor panel (Dev)
123        |  use 1 2 3 to select vert, edge, face
-or2s      |  origin to selected.
-steps     |  download + enable steps script
-dist      |  gives local distance between two selected verts
-gist -o x |  uploads all open text views as x to anon gist.
-debug     |  dl + enable extended mesh index visualiser. it's awesome.'''

    add_scrollback(content, 'OUTPUT')


class TextSyncOps(bpy.types.Operator):

    bl_idname = "text.text_upsync"
    bl_label = "Upsyncs Text from disk changes"

    def execute(self, context):
        text_block = context.edit_text
        bpy.ops.text.resolve_conflict(resolution='RELOAD')
        return{'FINISHED'}


class ConsoleDoAction(bpy.types.Operator):
    bl_label = "ConsoleDoAction"
    bl_idname = "console.do_action"

    def execute(self, context):
        m = bpy.context.space_data.history[-1].body
        m = m.strip()

        DONE = {'FINISHED'}
        if any([
            in_scene_commands(context, m),
            in_search_commands(context, m),
            in_sverchok_commands(context, m),
            in_core_dev_commands(context, m),
            in_modeling_tools(context, m),
            in_upgrade_commands(context, m)
        ]):
            return DONE

        elif m == '-ls':
            print_most_useful()
            return DONE

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
