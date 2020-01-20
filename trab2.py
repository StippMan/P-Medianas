import math

class Vertex():
	def __init__(self, coord_x, coord_y, capacity_max, demand):
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.capacity_max = capacity_max
		self.demand = demand

		self.connected_vertices = []
		self.capacity_current = 0


def inicializar():
	n_vertices, n_medians = input().split()
	n_vertices = int(n_vertices)
	n_medians = int(n_medians)

	vertex_list = []
	for i in range(n_vertices):
		input_aux = input()
		coord_x, coord_y, capacity_max, demand = input_aux.split()
		new_vertex = Vertex(int(coord_x), int(coord_y), int(capacity_max), int(demand))
		vertex_list.append(new_vertex)
		# print(coord_x, coord_y, capacity_max, demand)

def caclDist(x1,y1,x2,y2):
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2)
if __name__ == "__main__":
	inicializar()
	assert caclDist(2,4,6,4) == 4
