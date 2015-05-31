import bpy
from console_python import add_scrollback

import os
import sys
import subprocess


def make_animated_gif(m):
    if not os.path.exists(m):
        add_scrollback('{0} does not exist'.format(m), 'ERROR')

    initial_location = os.getcwd()
    try:
        os.chdir(m)
        f = "convert -delay 20 -loop 0 *png animated.gif"
        subprocess.Popen(f.split())
    except:
        add_scrollback('failed.. - with errors', 'ERROR')

    os.chdir(initial_location)
