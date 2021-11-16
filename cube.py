from lib import *
from plane import *
from sphere import *

class Cube(object):
  def __init__(self, position, size, material):
    midWay = size / 2
    self.position = position
    self.size = size
    self.material = material
    self.structure = [
      Plane(sum(position, V3(midWay,0,0)), V3(1,0,0), material),
      Plane(sum(position, V3(-midWay,0,0)), V3(-1,0,0), material),
      Plane(sum(position, V3(0,midWay,0)), V3(0,1,0), material),
      Plane(sum(position, V3(0,-midWay,0)), V3(0,-1,0), material),
      Plane(sum(position, V3(0,0,midWay)), V3(0,0,1), material),
      Plane(sum(position, V3(0,0,-midWay)), V3(0,0,-1), material),
      ]

  def ray_intersect(self, origin, direction):
    epsilon = 0.001
    minn = [0, 0, 0]
    maxx = [0, 0, 0]

    for i in range(3):
      minn[i] = self.position[i] - (epsilon + self.size / 2)
      maxx[i] = self.position[i] + (epsilon + self.size / 2)

    t = float('inf')
    intersect = None

    for plane in self.structure:
      plane_intersect = plane.ray_intersect(origin, direction)

      if plane_intersect is not None:
        if plane_intersect.point[0] >= minn[0] and plane_intersect.point[0] <= maxx[0]:
          if plane_intersect.point[1] >= minn[1] and plane_intersect.point[1] <= maxx[1]:
            if plane_intersect.point[2] >= minn[2] and plane_intersect.point[2] <= maxx[2]:
              if plane_intersect.distance < t:
                t = plane_intersect.distance
                intersect = plane_intersect

    if intersect is None:
      return None

    return Intersect(
      distance = intersect.distance,
      point = intersect.point,
      normal = intersect.normal
    )
