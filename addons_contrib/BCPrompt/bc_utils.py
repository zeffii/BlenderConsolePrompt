import bpy

import json
from urllib.request import urlopen


def github_commits(url, num_items):
    found_json = urlopen(url).readall().decode()

    wfile = json.JSONDecoder()
    wjson = wfile.decode(found_json)
    for idx, i in enumerate(wjson):
        commit = i['commit']

        print(commit['committer']['name'])
        for line in commit['message'].split('\n'):
            if not line:
                continue
            print('  ' + line)
        print()
        if idx > num_items:
            break


def do_text_glam():

    def set_props(s):
        # s = context.space_data
        s.show_line_numbers = True
        s.show_word_wrap = True
        s.show_syntax_highlight = True
        s.show_margin = True

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:

            if not area.type == 'TEXT_EDITOR':
                continue

            for s in area.spaces:
                if s.type == 'TEXT_EDITOR':
                    set_props(s)


def set_keymap():

    # script to map 1, 2, 3 to vertex, edge, face selection for 3dview
    wm = bpy.context.window_manager

    if True:
        deactivate_list = ['ONE', 'TWO', 'THREE']
        view3d_km_items = wm.keyconfigs.default.keymaps['3D View'].keymap_items
        for j in view3d_km_items:
            if j.type in deactivate_list and j.name == 'Layers':
                j.active = False

    if True:
        my_keymap = {
            'ONE': "True, False, False",
            'TWO': "False, True, False",
            'THREE': "False, False, True"
        }

        km = wm.keyconfigs.default.keymaps['Mesh']
        for k, v in my_keymap.items():
            new_shortcut = km.keymap_items.new('wm.context_set_value', k, 'PRESS')
            new_shortcut.properties.data_path = 'tool_settings.mesh_select_mode'
            new_shortcut.properties.value = v

    print('complete')


def vtx_specials(self, m):
    '''
    [1] checks if the addon is enabled by testing a known operator
    [2] if operator is not present, tries to enable the addon.
    [3] If it fails to enable the addon the function returns early.
        [ arguably this should suggest download + install + enable ]
    [4] If the function is found, it calls the specified function.
    '''
    addon_enabled = hasattr(bpy.ops.view3d, 'autovtx')
    if not addon_enabled:
        try:
            bpy.ops.wm.addon_enable(module="mesh_tinyCAD")
        except:
            print('tinyCAD addon not found.')
            return

    if m == 'vtx':
        bpy.ops.view3d.autovtx()
    elif m == 'xl':
        bpy.ops.mesh.intersectall()


def remove_obj_and_mesh(context):
    scene = context.scene
    objs = bpy.data.objects
    meshes = bpy.data.meshes
    for obj in objs:
        if obj.type == 'MESH':
            scene.objects.unlink(obj)
            objs.remove(obj)
    for mesh in meshes:
        meshes.remove(mesh)


def register():
    bpy.utils.register_module(__name__)


def unregister():
    bpy.utils.unregister_module(__name__)
