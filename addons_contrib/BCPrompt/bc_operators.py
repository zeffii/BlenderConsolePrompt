import bpy
from console_python import add_scrollback

from BCPrompt.bc_utils import (
    do_text_glam,
    set_keymap,
    vtx_specials,
    remove_obj_and_mesh,
    github_commits,
    get_sv_times, get_sv_times_all,
    bcp_justbrowse,
    throw_manual
)

from BCPrompt.bc_search_utils import (
    search_blenderscripting,
    search_bpydocs,
    search_pydocs,
    search_stack,
)

from BCPrompt.bc_gist_utils import (
    find_filenames, to_gist
)

from BCPrompt.bc_scene_utils import (
    select_starting, select_starting2
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

        # Searches!

        elif m.endswith('?bs'):
            search_blenderscripting(m[:-3])

        elif m.endswith('?se'):
            if m.endswith('??se'):
                site = 'stackoverflow'
                search_str = m[:-4]
            else:
                site = 'blender.stackexchange'
                search_str = m[:-3]
            search_stack(search_str, site)

        elif m.endswith('?py'):
            # no immediate search yet.
            search_pydocs(m[:-3])

        elif m.endswith('?bpy'):
            search_bpydocs(m[:-4])

        elif m.startswith('_svc_'):
            bcp_justbrowse('https://github.com/nortikin/sverchok/commits/master')

        elif m.startswith('_svc'):
            # sv commits
            url = "https://api.github.com/repos/nortikin/sverchok/commits"
            github_commits(url, 5)

        elif m.startswith('times '):
            command, named_group = m.split(' ')
            if not (named_group in bpy.data.node_groups):
                pass
            else:
                get_sv_times(named_group)

        elif m == 'times':
            get_sv_times_all()

        elif m.startswith('-gist '):
            # will not upload duplicates of the same file, placed in Set first.

            if m == '-gist -o':
                # send all visible, unnamed.
                pass

            if m.startswith('-gist -o '):
                # like:  "-gist -o test_gist"
                # send all visible, try naming it.
                gname = m[9:].strip()
                gname = gname.replace(' ', '_')
                file_names = find_filenames()
                to_gist(file_names, project_name=gname, public_switch=True)

        elif m.startswith('-sel -t '):
            # starting2 not implemented yet
            # accepts:
            # '-sel -t CU CurveObj56'
            # '-sel -t CU CurveObj 56'
            # '-sel -t CURVE CurveObj 56'
            _type, *find_str = m[8:].split()
            select_starting2(' '.join(find_str), _type)

        elif m.startswith('-sel '):
            find_str = m[5:]
            select_starting(find_str)

        elif m == "-man":
            throw_manual()

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
