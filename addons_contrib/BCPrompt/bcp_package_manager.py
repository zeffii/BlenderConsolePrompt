import bpy
from console_python import add_scrollback


def in_bpm_commands(context, m):
    if m.startswith("bpm "):
        add_scrollback(m, 'INFO')
    else:
        return False

    return True
