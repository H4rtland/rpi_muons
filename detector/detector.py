from collections import namedtuple

import mathutils.geometry
from mathutils import Vector

Path = namedtuple("Path", ["xi", "yi", "zi", "xf", "yf", "zf"])

def path_passes_through_plane(path, x, y, z, w, d, h, direction):
    line_start = Vector((path.xi, path.yi, path.zi))
    line_end = Vector((path.xf, path.yf, path.zf))

    plane_point = Vector((x, y, z))
    plane_direction = direction

    w = -w
    h = -h
    d = -d

    intersection = mathutils.geometry.intersect_line_plane(line_start, line_end, plane_point, plane_direction)
    if intersection is None:
        return False
    if direction.x == 0:
        if not (intersection.x < x < intersection.x+w):
            return False
    if direction.y == 0:
        if not (intersection.y < y < intersection.y+d):
            return False
    if direction.z == 0:
        if not (intersection.z < z < intersection.z+h):
            return False
    return True

def path_passes_through_cube(path, x, y, z, w, d, h):
    near_corner = (x, y, z)
    far_corner = (x+w, y+d, z+h)
    anchor_points = (near_corner, near_corner, near_corner,
                     far_corner, far_corner, far_corner)
    directions = (
        Vector((0, 0, -1)), # -z
        Vector((0, -1, 0)), # -y
        Vector((-1, 0, 0)), # -x
        Vector((0, 0, 1)), # +z
        Vector((0, 1, 0)), # +y
        Vector((1, 0, 0)), # +x
    )
    dimensions = (
        (w, d, 0),
        (w, 0, h),
        (0, d, h),
        (-w, -d, 0),
        (-w, 0, -h),
        (0, -d, -h),
    )
    # todo: convert direction vectors to dimensions automagically

    # normal brackets are a generator comprehension, as opposed to a list comprehension
    # any returns true on the first true item in a generator comprehension
    # but evaluates all terms in a list comprehension before returning
    # this had no effect on performance but it's a nice thing to know
    return any((path_passes_through_plane(path, *anchor_points[i], *dimensions[i], directions[i]) for i in range(0, len(anchor_points))))



if __name__ == "__main__":
    path = Path(1, 1, 1, 0, 0, 0)
    print(path_passes_through_cube(path, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1))