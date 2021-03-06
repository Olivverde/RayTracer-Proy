from lib import *
from sphere import *
from plane import *
from math import pi, tan
from cube import *

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
MAX_RECURSION_DEPTH = 3

class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = color(0, 0, 0)
    self.scene = []
    self.light = None
    self.clear()

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def cast_ray(self, orig, direction, recursion = 0):
    material, intersect = self.scene_intersect(orig, direction)

    if material is None or recursion >= MAX_RECURSION_DEPTH:  
      if self.envmap:
        return self.envmap.get_color(direction)
      return self.background_color
      

    offset_normal = mul(intersect.normal, 1.1)

    if material.albedo[2] > 0:
      reverse_direction = mul(direction, -1)
      reflect_dir = reflect(reverse_direction, intersect.normal)
      reflect_orig = sub(intersect.point, offset_normal) if dot(reflect_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
      reflect_color = self.cast_ray(reflect_orig, reflect_dir, recursion + 1)
    else:
      reflect_color = color(0, 0, 0)

    if material.albedo[3] > 0:
      refract_dir = refract(direction, intersect.normal, material.refractive_index)
      refract_orig = sub(intersect.point, offset_normal) if dot(refract_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
      refract_color = self.cast_ray(refract_orig, refract_dir, recursion + 1)
    else:
      refract_color = color(0, 0, 0)

    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
        shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = material.diffuse * intensity * material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
    reflection = reflect_color * material.albedo[2]
    refraction = refract_color * material.albedo[3]

    return diffuse + specular + reflection + refraction

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    intersect = None

    for obj in self.scene:
      hit = obj.ray_intersect(orig, direction)
      if hit is not None:
        if hit.distance < zbuffer:
          zbuffer = hit.distance
          material = obj.material
          intersect = hit

    return material, intersect

  def render(self):
    fov = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1) * tan(fov/2) * self.width/self.height
        j =  (2*(y + 0.5)/self.height - 1) * tan(fov/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)

water = Material(diffuse=color(35, 177, 209), albedo=(0.6, 0.3, 0.1, 0), spec=50, refractive_index=1.5)
grass = Material(diffuse=color(83, 140, 27), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
trunk = Material(diffuse=color(197, 178, 146), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
leaves = Material(diffuse=color(60, 107, 19), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
leaves_2 = Material(diffuse=color(24, 38, 19), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
cloud = Material(diffuse=color(255, 255, 255), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
mirror = Material(diffuse=color(255, 255, 255), albedo=(0, 10, 0.8, 0), spec=1425)
sand = Material(diffuse=color(241, 230, 158), albedo=(0.9, 0.1, 0, 0, 0), spec=50)
trunk_2 = Material(diffuse=color(71, 49, 41), albedo=(0.9, 0.1, 0, 0, 0), spec=50)


r = Raytracer(1000, 600)

r.light = Light(
  position=V3(-15, 10, 20),
  intensity=2
)


r.background_color = color(95, 167, 244)
# lado, altura, atr??s
"""
"""
r.scene = [
  Cube(V3(1.5, -2.1, -11), 3, sand),
  Cube(V3(4.5, -2.1, -11), 3, sand),
  Cube(V3(1.5, -0.5, -12), 0.35, trunk_2),
  Cube(V3(1.5, -0.2, -12), 0.35, trunk_2),
  Cube(V3(1.5, 0.1, -12), 0.35, trunk_2),
  Cube(V3(1.7, 0.7, -12), 1, leaves),
  Cube(V3(1.45, 0.7, -12.3), 1, leaves_2),
  Cube(V3(1.5, 1.3, -12), 0.5, leaves),
  Cube(V3(-0.5, -2.1, -1), 3, grass), #OK
  Cube(V3(-1.5, -2.1, -2), 3, grass), #OK
  Cube(V3(-2, -2.1, -5), 3, grass), #OK
  Cube(V3(-5, -2.1, -5), 3, grass), #OK
  Cube(V3(-1.3, -0.5, -5), 0.35, trunk_2),
  Cube(V3(-1.3, -0.2, -5), 0.35, trunk_2),
  Cube(V3(-1.3, 0.1, -5), 0.35, trunk_2),
  Cube(V3(-1.5, 0.7, -5), 1, leaves),
  Cube(V3(-1.25, 0.7, -5.3), 1, leaves_2),
  Cube(V3(-1.3, 1.3, -5), 0.5, leaves),
  Cube(V3(-4.5, -2.1, -8), 3, grass),
  Cube(V3(-7.5, -2.1, -8), 3, grass),
  Cube(V3(-1.5, -2.1, -11), 3, grass),
  Cube(V3(-4.5, -2.1, -11), 3, grass),
  Cube(V3(-7.5, -2.1, -11), 3, grass),
  Cube(V3(-1.5, -0.5, -11), 0.35, trunk),
  Cube(V3(-1.5, -0.2, -11), 0.35, trunk),
  Cube(V3(-1.5, 0.1, -11), 0.35, trunk),
  Cube(V3(-1.75, 0.7, -11), 1, leaves),
  Cube(V3(-1, 0.7, -11), 1, leaves),
  Cube(V3(-1.5, 0.9, -11.5), 1, leaves),
  Cube(V3(2,-4.8,-7),8, water), #OK
  Cube(V3(3, 1.5, -5), 0.5, cloud),
  Cube(V3(0.6, -0.5, -2), 0.35, trunk), #OK
  Cube(V3(0.6, -0.2, -2), 0.35, trunk), #OK
  Cube(V3(0.6, 0.1, -2), 0.35, trunk), #OK
  Cube(V3(0.45, 0.7, -2), 1, leaves), #OK
  Cube(V3(0.65, 0.7, -2.2), 1, leaves_2),
  Sphere(V3(-2, 1, -4), 0.85, mirror)
  
]


r.envmap = Envmap('./envmap.bmp')
r.render()
r.write('output.bmp')