import bpy
from console_python import add_scrollback

from .bc_utils import (
    set_keymap,
    vtx_specials,
    test_dl_run,
    remove_obj_and_mesh,
    github_commits,
    get_sv_times, get_sv_times_all,
    bcp_justbrowse,
    throw_manual,
    center_to_selected,
    write_keys_textfile
)

from .bc_text_repr_utils import (
    do_text_glam,
    do_text_synthax)

from .bc_search_utils import (
    search_blenderscripting,
    search_bpydocs,
    search_pydocs,
    search_stack,
)

from .bc_gist_utils import (
    find_filenames, to_gist
)

from .bc_scene_utils import (
    select_starting,
    select_starting2,
    distance_check
)

from .bc_update_utils import (
    peek_builder_org, process_zip
)

from .bc_CAD_utils import perform_face_intersection


history_append = bpy.ops.console.history_append
addon_enable = bpy.ops.wm.addon_enable


# this to be used for addons which are definitely present..
lazy_dict = {
    '-imgp': [addon_enable, "io_import_images_as_planes"],
    '-bb2': [addon_enable, "BioBlender"]
}


def lazy_power_download(mod, dl_url, op_path, op_name, invoke_type=None):
    registers_operator = [op_path, op_name]

    packaged = dict(
        operator=registers_operator,
        module_to_enable=mod,
        url=dl_url
    )

    if invoke_type:
        test_dl_run(packaged)
    else:
        test_dl_run(packaged, invoke_type=invoke_type)


def in_scene_commands(context, m):
    if m == "cen":
        '''cursor to center'''
        context.scene.cursor_location = (0.0, 0.0, 0.0)

    elif m == 'cento':
        center_to_selected(context)

    elif m.startswith("cen="):
        '''
        cursor to coordinate, anything that can be evalled..
        eg: cen=bpy.data.objects[1].data.verts[1].co

        '''
        right = m.split('=')[1]
        context.scene.cursor_location = eval(right)

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
        add_scrollback('enabled: 1=VERT_SEL, 2=EDGE_SEL, 3=FACE_SEL', 'OUTPUT')

    elif m.startswith('v2rdim'):
        SCN = bpy.context.scene
        SE = SCN.sequence_editor

        if m == 'v2rdim':
            sequence = SE.active_strip
        elif m.startswith('v2rdim '):
            vidname = m[7:]
            sequence = SE.sequences.get(vidname)
            if not sequence:
                print(vidname, 'is not a sequence - check the spelling')
                return True

        def get_size(sequence):
            clips = bpy.data.movieclips
            fp = sequence.filepath
            mv = clips.load(fp)
            x, y = mv.size[:]
            clips.remove(mv)
            return x, y

        x, y = get_size(sequence)
        SCN.render.resolution_x = x
        SCN.render.resolution_y = y
        SCN.render.resolution_percentage = 100

    else:
        return False

    return True


def in_search_commands(context, m):
    if m.endswith('?bs'):
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
    else:
        return False

    return True


def in_sverchok_commands(context, m):
    if m.startswith('_svc_'):
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

    else:
        return False

    return True


def in_core_dev_commands(context, m):
    if m.endswith('!'):
        '''copy current line to clipboard'''
        m = m[:-1]
        context.window_manager.clipboard = m
        add_scrollback('added to clipboard', 'OUTPUT')

    elif m == 'ico':
        try:
            bpy.ops.wm.addon_enable(module="development_icon_get")
            add_scrollback('added icons to TextEditor', 'OUTPUT')
        except:
            self.report({'INFO'}, "ico addon not present!")

    elif m == '-keys':
        write_keys_textfile()

    elif m == 'syntax':
        do_text_glam()

    elif m in {'syntax lt', 'syntax dk'}:
        do_text_glam()
        theme = m.split()[1]
        print('theme', theme)
        do_text_synthax(theme)

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

    elif m == '-gh':
        import os
        import subprocess
        _root = os.path.dirname(__file__)
        f = [os.path.join(_root, 'tmp', 'github_start.bat')]
        subprocess.call(f)

    else:
        return False

    return True


def in_modeling_tools(context, m):
    if m in {'vtx', 'xl'}:
        vtx_specials(self, m)

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

    elif m == '-or2s':
        url_prefix = "https://gist.githubusercontent.com/zeffii/"
        burp = "5844379/raw/01515bbf679f3f7a7c965d732004086dd40e64c0/"
        mod = "space_view3d_move_origin"
        dl_url = url_prefix + burp + mod + '.py'
        lazy_power_download(mod, dl_url, bpy.ops.object, 'origin_to_selected')

        msg = 'start with space-> Origin Move To Selected'
        add_scrollback(msg, 'INFO')

    elif m in lazy_dict:
        try:
            f, cmd = lazy_dict[m]
            f(module=cmd)
            msg = 'enabled: ' + cmd
            add_scrollback(msg, 'OUTPUT')
        except:
            rt = 'failed to do: ' + str(lazy_dict[m])

    elif m == '-itx':
        perform_face_intersection()

    elif m.startswith('enable '):
        command, addon = m.split()
        bpy.ops.wm.addon_enable(module=addon)

    else:
        return False

    return True


def in_upgrade_commands(context, m):
    if m.startswith("-up "):
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
    else:
        return False

    return True
