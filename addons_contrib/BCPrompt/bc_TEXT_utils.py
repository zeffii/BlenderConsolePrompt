import bpy



def detect_comments(lines):
    for line in lines:
        if len(line.strip()) == 0:
            # just spaces..
            continue
        elif line.strip().startswith("#"):
            # line starts with #
            continue
        else:
            return False
    return True

class TEXT_OT_do_comment(bpy.types.Operator):

    bl_idname = "text.do_comment"
    bl_label = "set or unset comment"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        print(self, context)

        edit_text = bpy.context.edit_text
        strs = edit_text.as_string()

        wm = bpy.context.window_manager

        bpy.ops.text.copy()
        copied_text = wm.clipboard
        copied_lines = copied_text.split('\n')

        # are all lines essentially comments?
        comment_mode = detect_comments(copied_lines)

        if comment_mode:
            ''' lines are all comments '''
            pass

        else:
            ''' lines need to be commented '''        
            # find least indent
            num_spaces = []
            for idx, l in enumerate(copied_lines):
                if '\t' in l:
                    print('mixing tabs..')
                    return {'FINISHED'}
                else:
                    g = l.lstrip()
                    indent_size = len(l) - len(g)
                    num_spaces.append(indent_size)

            min_space = min(num_spaces)
            print('minspace:', min_space)

            indent = ' ' * min_space
            for idx, l in enumerate(copied_lines):
                copied_lines[idx] = indent + "# " + l[min_space:]

            lines_to_paste = '\n'.join(copied_lines)
            wm.clipboard = lines_to_paste
            bpy.ops.text.paste()


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

