import bpy
from console_python import add_scrollback

from BCPrompt.bc_utils import (
    do_text_glam,
    set_keymap,
    vtx_specials,
    test_dl_run,
    remove_obj_and_mesh,
    github_commits,
    get_sv_times, get_sv_times_all,
    bcp_justbrowse,
    throw_manual,
    center_to_selected
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
    select_starting,
    select_starting2,
    distance_check
)

from BCPrompt.bc_update_utils import (
    peek_builder_org, process_zip
)

from BCPrompt.bc_CAD_utils import perform_face_intersection


history_append = bpy.ops.console.history_append
addon_enable = bpy.ops.wm.addon_enable

# use this for one shot - function calls

lazy_dict = {
    '-imgp': [addon_enable, "io_import_images_as_planes"]
}


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
-steps     |  download + enable steps script
-dist      |  gives local distance between two selected verts
-gist -o x |  uploads all open text views as x to anon gist.
-debug     |  dl + enable extended mesh index visualiser. it's awesome.

    '''
    add_scrollback(content, 'OUTPUT')


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

        if m == 'cento':
            center_to_selected(context)

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

        elif m.startswith("-theme "):
            # UNFINISHED WORK.
            result = m.strip().split(' ')
            if len(result) == 2:
                if result[1] == 'loc':
                    # "C:\\blender_trunk\\2.73\\scripts\\presets
                    # \\interface_theme\\back_to_black.xml"
                    pass  # print local location of theme
                if result[1] == 'togist':
                    pass  # uploads current xml to gist

        elif m.startswith("-up "):
            # inputs            | argument result
            # ------------------+-------------------
            # -up win32         | option = ['win32']
            # -up win64 berry   | option = ['win64', 'berry']
            cmd, *option = m.split(' ')
            res = peek_builder_org(option)
            if res:
                for line in res:
                    add_scrollback(line, 'OUTPUT')
                add_scrollback('', 'OUTPUT')

            if len(res) == 1:
                process_zip(res[0])
            else:
                msg = 'too many zips, narrow down!'
                add_scrollback(msg, 'INFO')

        elif m == '-dist':
            msg = distance_check()
            add_scrollback(msg, 'INFO')

        elif m == '-steps':
            registers_operator = [bpy.ops.mesh, 'steps_add']
            module_to_enable = 'mesh_add_steps'
            url_prefix = 'https://raw.githubusercontent.com/zeffii/'
            url_repo = 'rawr/master/blender/scripts/addons_contrib/'
            file_name = 'mesh_add_steps.py'
            dl_url = url_prefix + url_repo + file_name

            packaged = dict(
                operator=registers_operator,
                module_to_enable=module_to_enable,
                url=dl_url
            )

            test_dl_run(packaged)

        elif m == '-debug':  # formerly -debug_mesh
            registers_operator = [bpy.ops.view3d, 'index_visualiser']
            module_to_enable = 'view3d_idx_view'
            url_prefix = 'https://gist.githubusercontent.com/zeffii/9451340/raw'
            hasher = '/205610d27968305dfd88b0a521fe35aced83db32/'
            file_name = 'view3d_idx_view.py'
            dl_url = url_prefix + hasher + file_name

            packaged = dict(
                operator=registers_operator,
                module_to_enable=module_to_enable,
                url=dl_url
            )

            test_dl_run(packaged)

        elif m == '-snaps':
            # https://raw.githubusercontent.com/Mano-Wii/Snap-Utilities-Line/master/mesh_snap_utilities_line.py
            url_prefix = "https://raw.githubusercontent.com/Mano-Wii/Snap-Utilities-Line/master/"
            module_to_enable = "mesh_snap_utilities_line"
            dl_url = url_prefix + (module_to_enable + '.py')

            registers_operator = [bpy.ops.mesh, 'snap_utilities_line']

            packaged = dict(
                operator=registers_operator,
                module_to_enable=module_to_enable,
                url=dl_url
            )

            test_dl_run(packaged)

        elif m == '-gh':
            import os
            import subprocess
            _root = os.path.dirname(__file__)
            f = [os.path.join(_root, 'tmp', 'github_start.bat')]
            subprocess.call(f)

        elif m == '-itx':
            perform_face_intersection()

        elif m == '-ls':
            print_most_useful()

        elif m in lazy_dict:
            try:
                f, cmd = lazy_dict[m]
                f(module=cmd)
                msg = 'enabled: ' + cmd
                add_scrollback(msg, 'OUTPUT')
            except:
                rt = 'failed to do: ' + str(lazy_dict[m])

        return {'FINISHED'}


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
