import bpy
from console_python import add_scrollback
from BCPrompt.bc_utils import (
    do_text_glam,
    set_keymap,
    vtx_specials,
    remove_obj_and_mesh
)

history_append = bpy.ops.console.history_append


class TextSyncOps(bpy.types.Operator):

    bl_idname = "text.text_upsync"
    bl_label = "Upsyncs Text from disk changes"

    def execute(self, context):
        text_block = context.edit_text
        # print('is modified:', text_block.is_modified)
        # print('is updated:', text_block.is_updated)
        # print('is updated data:', text_block.is_updated_data)
        bpy.ops.text.resolve_conflict(resolution='RELOAD')
        return{'FINISHED'}


class ConsoleDoAction(bpy.types.Operator):
    bl_label = "ConsoleDoAction"
    bl_idname = "console.do_action"

    def execute(self, context):
        m = bpy.context.space_data.history[-1].body
        m = m.strip()
        if m == "cen":
            '''cursor to center'''
            context.scene.cursor_location = (0.0, 0.0, 0.0)

        if m.startswith("cen="):
            '''
            cursor to coordinate
            eg: cen=bpy.data.objects[1].data.verts[1].co

            '''
            right = m.split('=')[1]
            context.scene.cursor_location = eval(right)

        elif m.endswith('!'):
            '''copy current line to clipboard'''
            m = m[:-1]
            context.window_manager.clipboard = m
            add_scrollback('added to clipboard', 'OUTPUT')

        elif m in {'vtx', 'xl'}:
            vtx_specials(self, m)

        elif m == 'ico':
            try:
                bpy.ops.wm.addon_enable(module="development_icon_get")
                add_scrollback('added icons to TextEditor', 'OUTPUT')
            except:
                self.report({'INFO'}, "ico addon not present!")

        elif m == 'wipe':
            remove_obj_and_mesh(context)
            add_scrollback('wiped objects and meshes', 'OUTPUT')
            # history_append(text=m, current_character=0, remove_duplicates=True)
            history_append(text=m, remove_duplicates=True)

        elif m in {'tt', 'tb'}:
            prefs = context.user_preferences
            method = {'tb': 'TRACKBALL', 'tt': 'TURNTABLE'}.get(m)
            prefs.inputs.view_rotate_method = method
            msg = 'set rotation_method to {0} ({1})'.format(method, m)
            add_scrollback(msg, 'OUTPUT')

        elif m == '123':
            set_keymap()

        elif m == 'syntax':
            do_text_glam()

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
