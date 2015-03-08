import bpy
import bmesh
from mathutils.geometry import intersect_ray_tri
from mathutils.geometry import tessellate_polygon as tessellate


def perform_face_intersection():

    def rays_from_active_face(face):
        '''
        for every edge returns bidirectional (v1,v2), (v2,v1)
        - in case the face intersection happens on the origin of the ray
        '''
        indices = [v.index for v in face.verts]
        indices.append(indices[0])  # makes cyclic
        edges_f = [[indices[i], indices[i+1]] for i in range(len(indices)-1)]  # forward
        edges_b = [[indices[i+1], indices[i]] for i in range(len(indices)-1)]  # backward
        return edges_f + edges_b

    def triangulated(face):
        return tessellate([[v.co for v in face.verts]])

    def get_selected_minus_active(bm_faces):
        return [f for f in bm_faces if f.select and not (f.index == active.index)]

    # Get the active mesh
    obj = bpy.context.edit_object
    me = obj.data

    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()  # get 2.73+
    bm_verts = bm.verts
    bm_faces = bm.faces
    active = bm_faces.active

    test_rays = rays_from_active_face(active)
    faces_to_intersect = get_selected_minus_active(bm_faces)

    vert_set = set()
    for f in faces_to_intersect:
        print('intersect test')
        for tri in triangulated(f):
            idx1, idx2, idx3 = tri
            v1, v2, v3 = bm_verts[idx1].co, bm_verts[idx2].co, bm_verts[idx3].co
            for ray_idx, orig_idx in test_rays:
                orig = bm_verts[orig_idx].co
                ray = bm_verts[ray_idx].co - orig
                res = intersect_ray_tri(v1, v2, v3, ray.normalized(), orig)
                if res:
                    vert_set.add(res[:])

    print('found {0} unique verts'.format(vert_set))

    for v in vert_set:
        bm.verts.new(v)
    bm.verts.ensure_lookup_table()  # get 2.73+

    bmesh.update_edit_mesh(me, True)
