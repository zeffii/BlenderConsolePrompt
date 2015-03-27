import bpy


class TEXT_OT_do_comment(bpy.types.Operator):

    bl_idname = "text.do_comment"
    bl_label = "set or unset comment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        print(self, context)

        edit_text = bpy.context.edit_text
        strs = edit_text.as_string()
        print(strs)

        return {'FINISHED'}


def add_keymap2():
    wm = bpy.context.window_manager

    TE = wm.keyconfigs.default.keymaps.get('Text')
    if TE:
        keymaps = TE.keymap_items
        if not ('text.do_comment' in keymaps):
            keymaps.new('text.do_comment', 'SLASH', 'PRESS', ctrl=True)
    else:
        kc = wm.keyconfigs.addon
        print(' nope, TEXT will not work, adding:..')
        km = kc.keymaps.new(name='Text', space_type="TEXT_EDITOR")
        km.keymap_items.new('text.do_comment', 'SLASH', 'PRESS', ctrl=True)


add_keymap2()

# def register():
#     bpy.utils.register_class(TEXT_OT_do_comment)
#     add_keymap2()


# def unregister():
#     bpy.utils.unregister_class(TEXT_OT_do_comment)

