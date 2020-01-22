import random
import math
import bisect
# random.seed(379126485)

class Vertex():
	def __init__(self, coord_x, coord_y, capacity_max, demand):
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.capacity_max = capacity_max
		self.demand = demand

		self.distance = 0
		self.connected_vertices = []
		self.capacity_current = demand

class Solution():
	def __init__(self, nMedians, nVertices, vertices, fitness):
		self.nMedians = nMedians
		self.nVertices = nVertices
		self.vertices = vertices
		self.fitness = fitness

	def __lt__(self, other):
		self.fitness < other.fitness


def calcDist(x1,y1,x2,y2):
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2)

def shuffleList(lista):
	random.shuffle(lista)

def selectMedians(vertex_list, n_medians):
	median_list = [vertex_list[x] for x in range(n_medians)]
	return median_list

def connectVertex(n_vertices, n_medians, median_list, vertex_list):
	for i in range(n_medians, n_vertices):
		vertex = vertex_list[i]
		dist_min = -1
		min_dist_median = None
		for median in median_list:
			if vertex.demand + median.capacity_current <= median.capacity_max:
				curr_dist = calcDist(vertex.coord_x, vertex.coord_y, median.coord_x, median.coord_y)
				if dist_min < 0:
					dist_min = curr_dist
					min_dist_median = median
				elif dist_min > curr_dist:
					dist_min = curr_dist
					min_dist_median = median
		if dist_min == -1:
			print("Não foi possivel alocar vertice")
			return -1

		vertex.distance = dist_min
		# print(vertex.distance)
		min_dist_median.connected_vertices.append(vertex)
		min_dist_median.capacity_current += vertex.demand

	return median_list

def addDist(vec):
	res = 0
	for x in vec:
		# print(x.distance)
		res += x.distance
	return res

def randomSol(n_vertices, n_medians, vertex_list):
	
		# print(coord_x, coord_y, capacity_max, demand)
	shuffleList(vertex_list)
	median_list = selectMedians(vertex_list, n_medians)

	aux = -1
	while aux == -1:
		aux = connectVertex(n_vertices, n_medians, median_list, vertex_list)

	return Solution(n_medians, n_vertices, vertex_list, addDist(vertex_list))


def randomPopulation(n_vertices, n_medians, vertex_list):
	solutionList = []
	for i in range(0, 7.5 * math.log(n_medians)):
		temp = randomSol(n_vertices, n_medians, vertex_list)
		bisect.insort(solutionList, temp)


if __name__ == "__main__":

	n_vertices, n_medians = input().split()
	n_vertices = int(n_vertices)
	n_medians = int(n_medians)

	vertex_list = []
	for i in range(n_vertices):
		input_aux = input()
		coord_x, coord_y, capacity_max, demand = input_aux.split()
		new_vertex = Vertex(int(coord_x), int(coord_y), int(capacity_max), int(demand))
		vertex_list.append(new_vertex)
	
	randomPopulation(n_vertices, n_medians, vertex_list)


