import xml.etree.ElementTree as ET
import math

def merc_x(lon):
	r_major=6378137.000
	return r_major*math.radians(lon)
 
def merc_y(lat):
	if lat>89.5:lat=89.5
	if lat<-89.5:lat=-89.5
	r_major=6378137.000
	r_minor=6356752.3142
	temp=r_minor/r_major
	eccent=math.sqrt(1-temp**2)
	phi=math.radians(lat)
	sinphi=math.sin(phi)
	con=eccent*sinphi
	com=eccent/2
	con=((1.0-con)/(1.0+con))**com
	ts=math.tan((math.pi/2-phi)/2)/con
	y=0-r_major*math.log(ts)
	return y

class Point:
	"""2D class representaiton of a point"""
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.items = [x,y]

	def __getitem__(self, index):
		return self.items[index]

	def __len__(self):
		return 2

	def __str__(self):
		return str(self.x) + ', ' + str(self.y) 


class Poly:
	"""A poly is a list of points"""
	def __init__(self):
		self.points = []


class MapParser:
	def __init__(self, target_file):
		self.target = target_file
		self.buildings = []
		self.map_bounds = None
		self.bounds = None
		self.polys = []

	def parse_map(self):
		"""Reference: http://wiki.openstreetmap.org/wiki/OSM_XML"""
		tree = ET.parse(self.target)
		root = tree.getroot()

		# Read the bounds of the map
		map_bounds = root[0].attrib
		self.map_bounds = map_bounds
		self.bounds = dict()
		self.bounds['minx'] = merc_x(float(map_bounds['minlon']))
		self.bounds['maxx'] = merc_x(float(map_bounds['maxlon']))
		self.bounds['miny'] = merc_y(float(map_bounds['minlat']))
		self.bounds['maxy'] = merc_y(float(map_bounds['maxlat']))
		#print self.map_bounds

		# Read all of the nodes
		nodes = dict()
		for child in root.iter('node'):
			# Formamt of points is id: [x (lon), y(lat)}
			id = child.attrib['id']
			lon = child.attrib['lon']
			lat = child.attrib['lat']
			nodes[id] = [float(lon), float(lat)]

		# Create a building for each way that describes a building
		buildings = []
		for way in root.iter('way'):
			# We only care about those tagged buildings
			tag = way.find('tag')
			if tag.attrib['k'] == 'building' and tag.attrib['v'] == 'yes':
				building = []
				for nd in way.iter('nd'):
					building.append(nodes[nd.attrib['ref']])
				#print 'building', building
				buildings.append(building)
		self.buildings  =buildings

		# Convert lon/lat to cartisan coordinates
		self.transform_points()

	def transform_points(self):
		"""Converts lon/lat points to x,y"""
		# Populates the polys list using the buildings input
		self.polys = []
		for building in self.buildings:
			points = []
			for coord in building:
				lon = coord[0]
				lat = coord[1]
				point = Point(merc_x(lon), merc_y(lat))
				points.append(point)
			poly = Poly()
			poly.points = points
			self.polys.append(points) 

	def get_polys(self):
		return self.points

	def get_bounds(self):
		return self.bounds

def main():
	pass

if __name__ == "__main__":
    main()

# For testing

parser = MapParser('data/map.osm')
root = parser.parse_map()

