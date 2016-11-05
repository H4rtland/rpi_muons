from collections import namedtuple

import mathutils.geometry
from mathutils import Vector

Path = namedtuple("Path", ["xi", "yi", "zi", "xf", "yf", "zf"])

def path_passes_through_cube(path, x, y, z, w, d, h):
    line_start = Vector((path.xi, path.yi, path.zi))
    line_end = Vector((path.xf, path.yf, path.zf))

    plane_point = Vector((x, y, z))
    plane_direction = Vector((0, 0, 1))

    intersection = mathutils.geometry.intersect_line_plane(line_start, line_end, plane_point, plane_direction)
    if x < intersection.x < x+w and y < intersection.y < y+h:
        return True
    return False



if __name__ == "__main__":
    path = Path(1, 1, 1, 0, 0, 0)
    print(path_passes_through_cube(path, 0.45, 0.45, 0.45, 0.1, 0.1, 0.1))