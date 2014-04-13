import xml.etree.ElementTree as ET

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


class Poly:
	"""A poly is a list of points"""
	def __init__(self):
		self.points = []
		self.buildings = []


class MapParser:
	def __init__(self, target_file):
		self.polys = []
		self.target = target_file

	def parse_map(self):
		"""Reference: http://wiki.openstreetmap.org/wiki/OSM_XML"""
		tree = ET.parse(self.target)
		root = tree.getroot()

		# Read the bounds of the map
		map_bounds = root[0].attrib

		# Read all of the nodes
		nodes = dict()
		for child in root.iter('node'):
			# Formamt of points is id: [x (lon), y(lat)}
			id = child.attrib['id']
			lon = child.attrib['lon']
			lat = child.attrib['lat']
			nodes[id] = [lon, lat]

		# Create a building for each way that describes a building
		buildings = []
		for way in root.iter('way'):
			# We only care about those tagged buildings
			tag = way.find('tag')
			if tag.attrib['k'] == 'building' and tag.attrib['v'] == 'yes':
				building = []
				for nd in way.iter('nd'):
					building.append(nodes[nd.attrib['ref']])
				print 'building', building
				buildings.append(building)
		self.buildings  =buildings

		return root

	def normalize_points(self):
		"""Converts lon/lat points to x,y"""
		pass

	def get_polys(self):
		return self.points

def main():
	pass

if __name__ == "__main__":
    main()

# For testing

parser = MapParser('data/map.osm')
root = parser.parse_map()

