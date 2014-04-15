from pygame_runner import *
from osm_parser import *

# =============================================================================
# Constants
# =============================================================================
#MAP_DATA_FILE = 'data/simple_map.osm'
MAP_DATA_FILE = 'data/medium_map.osm'

LINE_WIDTH = 0

# =============================================================================
# Other Classes
# =============================================================================
class MotionPlanner:
	def __init__(self):
		self.map_parser = None

# =============================================================================
# Pygame App
# =============================================================================
class MyPygameApp(BasePygameApp):

	def setup(self):
		# Init the screen
		self.size(800, 800)

		# Parse the map and init the mtion planner
		parser = MapParser(MAP_DATA_FILE)
		parser.parse_map()
		parser.convert_points((self.WIDTH, self.HEIGHT))

		self.motion_planner = MotionPlanner()
		self.motion_planner.map_parser = parser
		#self.motion_planner.polys = parser.get_polys()
		#self.motion_planner.bounds = parser.get_bounds()

	def draw(self):
		# Clear the screen
		self.background(WHITE)

		# Draw each poly in the motion planner
		polys = self.motion_planner.map_parser.get_polys()
		for poly in polys:
			pygame.draw.polygon(self.screen, BLACK, poly.points, LINE_WIDTH)

		
	def mouse_pressed(self, x, y):
		print 'mouse pressed:', x, ',', y

	def key_pressed(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()

# =============================================================================
# Runner Methods
# =============================================================================
if __name__ == '__main__':
	pygame_app = MyPygameApp()
	pygame_app.run()