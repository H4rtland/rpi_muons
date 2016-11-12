from collections import namedtuple

import mathutils.geometry
from mathutils import Vector


Path = namedtuple("Path", ["xi", "yi", "zi", "xf", "yf", "zf"])


def path_passes_through_plane(path, x, y, z, w, d, h, direction):
    line_start = Vector((path.xi, path.yi, path.zi))
    line_end = Vector((path.xf, path.yf, path.zf))

    plane_point = Vector((x, y, z))
    plane_direction = direction

    # Don't ask.
    w = -w
    h = -h
    d = -d

    intersection = mathutils.geometry.intersect_line_plane(line_start, line_end, plane_point, plane_direction)
    if intersection is None:
        return False
    if direction.x == 0:
        if not (intersection.x-0.01 <= x <= intersection.x+w+0.01):
            return False
    if direction.y == 0:
        if not (intersection.y-0.01 <= y <= intersection.y+d+0.01):
            return False
    if direction.z == 0:
        if not (intersection.z-0.01 <= z <= intersection.z+h+0.01):
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
    #path = Path(1, 1, 1, 0, 0, 0)
    #print(path_passes_through_cube(path, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1))
    failed_num = 0
    for y in range(0, 10):
        for x in range(0, 10):
            p = Path(x/10, y/10, 1, 1-x/10, 1-y/10, 0)
            if not path_passes_through_cube(p, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1):
                print("1FAILED", x/10, y/10, 1, 1-x/10, 1-y/10, 0)
                failed_num += 1
            p = Path(x/10, y/10, 0, 1-x/10, 1-y/10, 1)
            if not path_passes_through_cube(p, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1):
                print("2FAILED", x/10, y/10, 0, 1-x/10, 1-y/10, 1)
                failed_num += 1
        for z in range(0, 10):
            p = Path(0, y/10, z/10, 1, 1-y/10, 1-z/10)
            if not path_passes_through_cube(p, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1):
                print("3FAILED", 0, y/10, z/10, 1, 1-y/10, 1-z/10)
                failed_num += 1
            p = Path(1, y/10, z/10, 0, 1-y/10, 1-z/10)
            if not path_passes_through_cube(p, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1):
                print("4FAILED", 1, y/10, z/10, 0, 1-y/10, 1-z/10)
                failed_num += 1
    print(failed_num)