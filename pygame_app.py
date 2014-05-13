from pygame_runner import *
from motion_planner import *
from graphs import *

# =============================================================================
# Constants
# =============================================================================

#MAP_DATA_FILE = 'data/simple_map.osm'
MAP_DATA_FILE = 'data/medium_map.osm'
#MAP_DATA_FILE = 'data/four_map.osm'
#MAP_DATA_FILE = 'data/one_building.osm'

# Lines
LINE_WIDTH = 3
LINE_COLOR = (0, 50, 255) 

# Polygons 
POLYGON_COLOR = (100, 100, 100)
POLYGOG_WIDTH = 0

# Start and end points
CIRCLE_RADIUS = 10
START_POINT_COLOR = (50,255,50)
END_POINT_COLOR = (255, 100, 0)

# =============================================================================
# Other Classes
# =============================================================================


# =============================================================================
# Pygame App
# =============================================================================
class MyPygameApp(BasePygameApp):
	def setup(self):
		# Init the screen
		self.size(800, 800)

		# Parse the map and init the mtion planner
		self.motion_planner = MotionPlanner(self.WIDTH, self.HEIGHT)
		self.motion_planner.init_map_parser(MAP_DATA_FILE)

		self.init_state()

		if True:
			return
		self.compute_path()

	def init_state(self):
		self.start = None
		self.end = None
		# State variable indicates if we're setting start or end point
		# False = start point
		# True = end point
		self.set_point_state = False

		self.path = list()

	def draw(self):
		# Clear the screen
		self.background(WHITE)

		# Draw the map 
		self.draw_map()

		self.draw_start_end()
		
	def mouse_pressed(self, x, y):
		print 'mouse pressed:', x, ',', y
		self.set_start_end_point(x,y)

	def key_pressed(self, key):
		print 'key pressed', key
		if key == pygame.K_SPACE:
			self.compute_path()
		if key == pygame.K_ESCAPE:
			self.quit()

# =============================================================================
	def set_start_end_point(self, x, y):
		if not self.set_point_state:
			# Set start point
			self.start = Point(x,y)
			print 'Start point set'
		else:
			# Set end point
			self.end = Point(x,y)
			print 'End point set'
		self.set_point_state = not self.set_point_state

	def compute_path(self):
		# Only compute if we have a start and end point
		if not (self.start and self.end):
			print 'ERROR, cannot run without start and end point'
			return
		# Get Polys
		polys = self.motion_planner.map_parser.get_polys()
		start = self.start
		end = self.end
		# Compute the path
		path = shortest_path_visibility_graph(polys, start, end)
		# Print Results
		print 'The shortest path of length:', len(path)
		for point in path:
			print point.x, point.y
		# Save path
		self.path = path 

	def draw_map(self):
		# Draw each poly in the motion planner
		polys = self.motion_planner.map_parser.get_polys()
		for poly in polys:
			pygame.draw.polygon(self.screen, POLYGON_COLOR, poly.points, POLYGOG_WIDTH)

		# Draw the perfect path
		for index in range(len(self.path)-1):
			p1 = self.path[index]
			p2 = self.path[index + 1]
			pygame.draw.line(self.screen, LINE_COLOR, p1, p2, LINE_WIDTH)

	def draw_start_end(self):
		if self.start:
			pygame.draw.circle(self.screen, START_POINT_COLOR, self.start, CIRCLE_RADIUS, 0)
		if self.end:
			pygame.draw.circle(self.screen, END_POINT_COLOR, self.end, CIRCLE_RADIUS, 0)


# =============================================================================
# Runner Methods
# =============================================================================
if __name__ == '__main__':
	pygame_app = MyPygameApp()
	pygame_app.run()
