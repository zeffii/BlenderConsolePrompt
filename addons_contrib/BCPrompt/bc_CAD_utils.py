import bpy
import bmesh
from mathutils.geometry import intersect_ray_tri
from mathutils.geometry import intersect_point_line
from mathutils.geometry import tessellate_polygon as tessellate


def perform_face_intersection():
    
    '''
    (currently) only points that are found on the face that is active, are accepted
    - In practice this means the last selected face will be used to receive
      intersection points.
    '''

    def rays_from_face(face):
        '''
        per edge (v1, v2) this returns the reverse edge too (v2, v1)
        in case the face intersection happens on the origin of the ray
        '''
        indices = [v.index for v in face.verts]
        indices.append(indices[0])  # makes cyclic
        edges_f = [(indices[i], indices[i+1]) for i in range(len(indices)-1)]  # forward
        edges_b = [(indices[i+1], indices[i]) for i in range(len(indices)-1)]  # backward
        return edges_f + edges_b

    def triangulated(face):
        return tessellate([[v.co for v in face.verts]])

    def get_selected_minus_active(bm_faces, active_idx):
        return [f for f in bm_faces if f.select and not (f.index == active_idx)]

    # Get the active mesh
    obj = bpy.context.edit_object
    me = obj.data

    bm = bmesh.from_edit_mesh(me)
    bm.verts.ensure_lookup_table()  # get 2.73+
    bm_verts = bm.verts
    bm_faces = bm.faces

    # Prime Face
    active = bm_faces.active

    # triangulate face to intersect
    tris_to_intersect = triangulated(active)  # list of collections of 3 coordinates
    av = active.verts
    tris = [[av[idx1].co, av[idx2].co, av[idx3].co] for idx1, idx2, idx3 in tris_to_intersect]

    # this will hold the set of edges used to raycast, using set will avoid many duplicates of touching
    # faces that share edges.
    test_rays = set()

    # check intersection with bidirectional of all edges of all faces that are selected but not active

    # Non Prime Faces
    faces_to_intersect_with = get_selected_minus_active(bm_faces, active.index)
    for face in faces_to_intersect_with:
        rays = rays_from_face(face)
        for ray in rays:
            test_rays.add(ray)

    vert_set = set()

    for v1, v2, v3 in tris:

        for ray_idx, orig_idx in test_rays:
            orig = bm_verts[orig_idx].co
            ray_original = bm_verts[ray_idx].co
            ray = (bm_verts[ray_idx].co - orig).normalized()
            pt = intersect_ray_tri(v1, v2, v3, ray, orig)
            if pt:
                # filter new verts,
                # they must lie on the line described by (origin, ray_original) then add.
                itx_res = intersect_point_line(pt, ray_original, orig)
                if itx_res:
                    v, dist = itx_res
                    if (0.0 < dist < 1.0):
                        vert_set.add(pt[:])

    print('found {0} unique new verts'.format(len(vert_set)))

    for v in vert_set:
        bm.verts.new(v)

    bmesh.update_edit_mesh(me, True)
