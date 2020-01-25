import random
import math
from bisect import insort
random.seed(379126485)

class Vertex():
	def __init__(self ,coord_x, coord_y, capacity_max, demand):
		self.coord_x = coord_x
		self.coord_y = coord_y
		self.capacity_max = capacity_max
		self.capacity_current = demand
		self.demand = demand
		self.isConnected = False
		self.distance = 0
	
	def __str__(self):
		return "Vertice(%d, %d)" % (self.coord_x, self.coord_y)

	def __lt__(self, other):
		self.distance < other.distance

class Solution():
	def __init__(self, nMedians, nVertices, vertices, medians,fitness):
		self.nMedians = nMedians
		self.nVertices = nVertices
		self.vertices = vertices
		self.medians = medians
		self.fitness = fitness
	
	def __lt__(self, other):
		self.fitness < other.fitness

# def printMedians(median_list):
# 	for x in median_list:
# 			print("=========================")
# 			print("Median: ", x)
# 			for y in x.connected_vertices:
# 				print(y)
# 			print("=========================")

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
		median.isConnected = True
		median.capacity_current = median.demand
		median_list.append(median)
	return median_list

def connectVertexToMedian(median, vertex, dist):
	# median.connected_vertices.append(vertex)
	vertex.median = median
	median.capacity_current += vertex.demand
	vertex.distance = dist
	vertex.isConnected = True

def makeGraph(n_vertices, n_medians, vertex_list, median_list):
	for vertex in vertex_list:
		dist = []
		for median in median_list:
			insort(dist,(calcDist(median, vertex), median))

		for x in dist:
			med = x[1]
			if med.capacity_current + vertex.demand <= med.capacity_max:
				connectVertexToMedian(x[1], vertex, x[0])
				break
				
		
		
	for x in vertex_list:
		# print(x.distance)
		if not x.isConnected:
			print('lol')
			return -1
	return median_list

		

def addDist(vec):
	res = 0
	for x in vec:
		res += x.distance
	return res

def randomSol(n_vertices, n_medians, original_vertex_list):
	vertex_list = original_vertex_list.copy()

	random.shuffle(vertex_list)
	median_list = selectMedians(vertex_list, n_medians)
	aux = -1
	while aux == -1:
		aux = makeGraph(n_vertices, n_medians, vertex_list, median_list)
	
	return Solution(n_medians, n_vertices, vertex_list,median_list, addDist(vertex_list))


def randomPopulation(n_vertices, n_medians, vertex_list):
	solutionList = []
	for i in range(0, int(7.5 * math.log(n_medians))):
		solution = randomSol(n_vertices, n_medians, vertex_list)
		# insort(solutionList, (solution.fitness, solution))
		solutionList.append(solution)
	
	return solutionList

def tournament(population):
	num = int(len(population)/2)
	if(num%2 != 0) :
		num+=1
	selection = []
	pairs = []
	
	for i in range(0, num):
		if i%2 == 0 and i != 0:
			# print(pairs)
			selection.append(pairs)
			pairs = []

		winner = min(random.choices(population,k=3), key=lambda x: x.fitness)
		pairs.append(winner.medians)
	return selection

def makeSwapVec(p1,p2):
    swapVec = []
    swapVec2 = []

    for x in range(0,len(p1)):
        median = p1[x]
        if median not in p2:
            swapVec.append(x)
        median = p2[x]
        if median not in p1:
            swapVec2.append(x)
     
    if(len(swapVec) == 0):
        return -1
    
    return swapVec, swapVec2

def crossover(p1, p2):
	# swap sao as listas de trocas, e a func retorna uma tupla de medianas
	aux = makeSwapVec(p1,p2)
	swap1 = aux[0]
	swap2 = aux[1]
	k = random.randint(0, len(swap1))
	for x in range(0, k):
		# i1 e i2 sao indices a serem trocados
		i1 = swap1[x]
		i2 = swap2[x]
		print("Pos troca:", i1,i2)
		p1[i1], p2[i2] = p2[i2], p1[i1]
	return p1, p2

def genetic(n_vertices, n_medians, vertex_list):
	population = randomPopulation(n_vertices, n_medians, vertex_list)
	generations = 0

	selection = tournament(population)
	for x in range(0, len(selection)):
		# p1 e p2 sao listas de medianas (pai1 e pai2)
		p1 = selection[x][0]
		p2 = selection[x][1]
		
		print("Antes troca")
		for i in range(0,12):
			print(p1[i],p2[i])
	
		print("==============================")

		b = crossover(p1, p2)
		print("Depois troca")
		for i in range(0,12):
			print(b[0][i],b[1][i])
		print("==============================")
		

	# while generations != 10:

		



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
	
	genetic(n_vertices, n_medians, vertex_list)
	# randomPopulation(n_vertices, n_medians, vertex_list)
	# randomSol(n_vertices, n_medians, vertex_list)
	# makeGraph(n_vertices, n_medians, vertex_list, )

	


