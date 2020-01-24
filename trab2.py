import random
import math
from bisect import insort
# random.seed(379126485)

class Vertex():
	def __init__(self ,coord_x, coord_y, capacity_max, demand):
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.capacity_max = capacity_max
		self.demand = demand

		self.isConnected = False
		self.distance = 0
		self.connected_vertices = []
		self.capacity_current = demand
	
	def __str__(self):
		return "Vertice(%d, %d)" % (self.coord_x, self.coord_y)

	def __lt__(self, other):
		self.distance < other.distance

class Solution():
	def __init__(self, nMedians, nVertices, vertices, fitness):
		self.nMedians = nMedians
		self.nVertices = nVertices
		self.vertices = vertices
		self.fitness = fitness
	
	def __lt__(self, other):
		self.fitness < other.fitness

def printMedians(median_list):
	for x in median_list:
			print("=========================")
			print("Median: ", x)
			for y in x.connected_vertices:
				print(y)
			print("=========================")

def calcDist(median,vertex):
	x1 = median.coord_x
	y1 = median.coord_y
	x2 = vertex.coord_x
	y2 = vertex.coord_y
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2)

def selectMedians(vertex_list, n_medians):
	median_list = []
	for i in range(n_medians):
		median = vertex_list.pop(0)
		# median.isConnected = True
		median_list.append(median)
	return median_list

def connectVertexToMedian(median, vertex, dist):
	median.connected_vertices.append(vertex)
	median.capacity_current += vertex.demand
	vertex.distance = dist
	vertex.isConnected = True

def makeGraph(n_vertices, n_medians, vertex_list, median_list):
	for median in median_list:
		distList = []
		for vertex in vertex_list:
			if not vertex.isConnected:
				insort(distList,(calcDist(median, vertex), vertex))
		
		for x in distList:
			if median.capacity_current + x[1].demand <= median.capacity_max:
				connectVertexToMedian(median, x[1], x[0])
		
		
	for x in vertex_list:
		if not vertex.isConnected:
			return -1
	return median_list

		

def addDist(vec):
	res = 0
	for x in vec:
		# print(x.distance)
		res += x.distance
	return res

def randomSol(n_vertices, n_medians, original_vertex_list):
	vertex_list = original_vertex_list.copy()

	random.shuffle(vertex_list)
	median_list = selectMedians(vertex_list, n_medians)
	aux = -1
	while aux == -1:
		aux = makeGraph(n_vertices, n_medians, vertex_list, median_list)
	
	return Solution(n_medians, n_vertices, vertex_list, addDist(vertex_list))


def randomPopulation(n_vertices, n_medians, vertex_list):
	solutionList = []
	for i in range(0, int(7.5 * math.log(n_medians))):
		solution = randomSol(n_vertices, n_medians, vertex_list)
		# print(solution.fitness)
		insort(solutionList, (solution.fitness, solution))
		
	for x in solutionList:
		print(x[0])


if __name__ == "__main__":
	n_vertices, n_medians = input().split()
	n_vertices = int(n_vertices)
	n_medians = int(n_medians)

	vertex_list = []
	for i in range(n_vertices):
		input_aux = input()
		coord_x, coord_y, capacity_max, demand = input_aux.split()
		# print(capacity_max)
		new_vertex = Vertex(int(coord_x), int(coord_y), int(capacity_max), int(demand))
		vertex_list.append(new_vertex)
	
	randomPopulation(n_vertices, n_medians, vertex_list)
	# randomSol(n_vertices, n_medians, vertex_list)
	# makeGraph(n_vertices, n_medians, vertex_list, )

	


