# bc_scene_utils.py
import bpy


def enumerate_objects_starting_with(find_term):
    return (c for c in bpy.data.objects if c.name.startswith(find_term))


def select_starting(find_term):
    objs = enumerate_objects_starting_with(find_term)
    for o in objs:
        o.select = True


def select_starting2(find_term, type_object):
    objs = enumerate_objects_starting_with(find_term)
    for o in objs:
        if not o.type == type_object:
            continue
        o.select = True
