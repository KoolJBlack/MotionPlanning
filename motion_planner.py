from osm_parser import *

class Robot:
	def __init__(self):
		position = Point(-1,-1)
		theta = 0.0

	def set_body(self, poly):
		self.body = poly

	def translate(self, delta_position):
		self.position += delta_position

	def rotate(self, delta_theta):
		self.theta += delta_theta


class MotionPlanner:
	def __init__(self, screen_width, screen_height):
		self.map_parser = None
		self.WIDTH = screen_width
		self.HEIGHT = screen_height

		# The robots information 
		self.robot = None
	
	def init_map_parser(self, map_filename):
		self.map_parser = MapParser(map_filename)
		self.map_parser.parse_map()
		self.map_parser.convert_points((self.WIDTH, self.HEIGHT))

	def calc_configuration_space(self, robot):
		''' Uses MINKOWSKISUM intandom with robot '''
		self.robot = robot
