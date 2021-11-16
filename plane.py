from lib import *
from sphere import *
from math import pi, acos, atan2

class Plane(object):
  def __init__(self, position, normal, material):
    self.position = position
    self.normal = norm(normal)
    self.material = material
  def ray_intersect(self, orig, direction):
    denom = dot(direction, self.normal)

    if abs(denom) > 0.0001:
      d = dot(self.normal, sub(self.position, orig)) / denom
      if d > 0:
        pt = sum(orig, mul(direction, d))

        
        return Intersect(
          distance = d,
          point = pt,
          normal = self.normal
        )

    return None
  
import mmap
import numpy

class Envmap(object):
    def __init__(self, path):
        self.path = path
        self.read()

    def read(self):
        img = open(self.path, "rb")
        m = mmap.mmap(img.fileno(), 0, access=mmap.ACCESS_READ)
        ba = bytearray(m)
        header_size = struct.unpack("=l", ba[10:14])[0]
        self.width = struct.unpack("=l", ba[18:22])[0]
        self.height = struct.unpack("=l", ba[18:22])[0]
        all_bytes = ba[header_size::]
        self.pixels = numpy.frombuffer(all_bytes, dtype='uint8')
        img.close()

    def get_color(self, direction):
      width = 2000
      height = 1000
      direction = norm(direction)

      x = int((atan2(direction.z, direction.x) / (2 * pi) + 0.5) * width)
      y = int(acos(-direction.y) / pi * height)
      index = (y * self.width + x) * 3 % len(self.pixels)

      processed = self.pixels[index:index+3].astype(numpy.uint8)
      return color(processed[2], processed[1], processed[0])
