from pygame_runner import *
from motion_planner import *
from graphs import *

# =============================================================================
# Constants
# =============================================================================
#MAP_DATA_FILE = 'data/simple_map.osm'
#MAP_DATA_FILE = 'data/medium_map.osm'
#MAP_DATA_FILE = 'data/four_map.osm'
MAP_DATA_FILE = 'data/one_building.osm'



LINE_WIDTH = 3

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

		if False:
			return

		# Test Visibility Graphs

		# Get Polys
		polys = self.motion_planner.map_parser.get_polys()
		#start = polys[0].points[0]
		#end = polys[-1].points[-1]
		start = Point(0,0)
		end = Point(self.WIDTH, self.HEIGHT)
		# Compute the path
		path = shortest_path_visibility_graph(polys, start, end)
                #self.path = []
                #return
		print 'The shortest path of length:', len(path)
		for point in path:
			print point.x, point.y

		self.path = path 


	def draw(self):
		# Clear the screen
		self.background(WHITE)

		# Draw the map 
		self.draw_map()
		
	def mouse_pressed(self, x, y):
		print 'mouse pressed:', x, ',', y

	def key_pressed(self, key):
		if key == pygame.K_ESCAPE:
			self.quit()

	def draw_map(self):
		# Draw each poly in the motion planner
		polys = self.motion_planner.map_parser.get_polys()
		for poly in polys:
			pygame.draw.polygon(self.screen, BLACK, poly.points, LINE_WIDTH)

		# Draw the perfect path
		for index in range(len(self.path)-1):
			p1 = self.path[index]
			p2 = self.path[index + 1]
			pygame.draw.line(self.screen, (0, 50, 255), p1, p2, LINE_WIDTH)

# =============================================================================
# Runner Methods
# =============================================================================
if __name__ == '__main__':
	pygame_app = MyPygameApp()
	pygame_app.run()
