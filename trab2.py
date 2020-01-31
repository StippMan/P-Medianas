import random as rd
import math
from bisect import insort
# rd.seed(379126485)

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

	# def __eq__(self, other):
	# 	return self.coord_x == other.coord_x and self.coord_y == other.coord_y

	def __lt__(self, other):
		return self.distance < other.distance
	
	def __repr__(self):
		return '\nVertex({})'.format((self.coord_x,self.coord_y))

	def reset(self, capacity_max, demand):
		self.capacity_max = capacity_max
		self.capacity_current = demand
		self.demand = demand
		self.isConnected = False
		self.distance = 0

	def copy(self):
		return Vertex(self.coord_x, self.coord_y, self.capacity_max, self.demand)

class Solution():
	def __init__(self, nMedians, nVertices, vertices, medians,fitness):
		self.nMedians = nMedians
		self.nVertices = nVertices
		self.medians = medians
		self.vertices = vertices
		self.fitness = fitness
	
	def __lt__(self, other):
		return self.fitness < other.fitness
	
	def __repr__(self):
		return '\nSolution({})'.format(self.fitness)
	
	def copy(self):
		return Solution(self.nMedians, self.nVertices, self.vertices.copy(), self.medians.copy(),self.fitness)
	
def testPopulation(population):
	fitness= []
	soma = 0
	for x in population:
		print('====================')
		for y in x.medians:
			print(y,x.fitness)
		print(x.fitness)
		soma+=x.fitness
		fitness.append(x.fitness)
	# print(fitness)
	return soma/len(population)

def calcDist(median,vertex):
	x1 = median.coord_x
	y1 = median.coord_y
	x2 = vertex.coord_x
	y2 = vertex.coord_y
	return math.sqrt( (x2-x1)**2 + (y2-y1)**2)

def testMedian(vertex_list, n_medians):
	return vertex_list[0:12]

def selectMedians(vertex_list, n_medians):
	median_list = []
	for i in range(n_medians):
		# median = vertex_list.pop(0)
		median = vertex_list[i]
		median.isConnected = True
		median.capacity_current = median.demand
		median_list.append(median)
	return median_list

def addDist(vec):
	res = 0
	for x in vec:
		res += x.distance
	return res

def connectVertexToMedian(median, vertex, dist):
	median.capacity_current += vertex.demand
	vertex.distance = dist
	vertex.isConnected = True
	median.isConnected = True

def makeGraph(vertex_list, median_list):
	
	for x in vertex_list:
		x.reset(x.capacity_max, x.demand)

	for vertex in vertex_list:
		dist = []
		for median in median_list:
			if(vertex not in median_list):
				
				median.isConnected = True
				insort(dist,(calcDist(median, vertex), median))
		
		for x in dist:
			med = x[1]
			if med.capacity_current + vertex.demand <= med.capacity_max:
				connectVertexToMedian(x[1], vertex, x[0])
				# print(vertex,vertex.demand, med, med.capacity_current)
				break
		
	for x in vertex_list:
		# print(x.distance)
		if not x.isConnected:
			# print('Não deu certo')
			return -1
	return median_list

		


def randomSol(n_vertices, n_medians, original_vertex_list):
	#cria indiviuos (soluções)
	vertex_list = original_vertex_list.copy()
	aux = -1
	while aux == -1:
		rd.shuffle(vertex_list)
		median_list = selectMedians(vertex_list, n_medians)
		aux = makeGraph(vertex_list, median_list)
	
	return Solution(n_medians, n_vertices,vertex_list, median_list, addDist(vertex_list))


def randomPopulation(n_vertices, n_medians, vertex_list):
	solutionList = []
	populationNumber = int(7.5 * math.log(n_vertices))
	# populationNumber = 100
	for i in range(0, populationNumber):
		solution = randomSol(n_vertices, n_medians, vertex_list)
		insort(solutionList, solution)
		# print(solution.fitness)
		# solutionList.append(solution)
	
	return solutionList

def tournament(population):
	# A função retorna uma tupla de soluções
	selection = []
	while len(selection) <= 2:
		winner1 = min(rd.choices(population,k=3), key=lambda x: x.fitness)
		winner2 = min(rd.choices(population,k=3), key=lambda x: x.fitness)
		if winner1 != winner2:
			selection.append(winner1)
			selection.append(winner2)
	return selection

def rank(population):
	selection = []
	weight = [i for i in reversed( range(1, len(population)+1) )]

	while len(selection) <= 2:
		selecteds = rd.choices(population, weights = weight, k=2)
		if(selecteds[0] != selecteds[1]):
			return selecteds


def makeSwapVec(p1,p2):
	swapVec = []
	swapVec2 = []

	# print(p1)
	for x in range(0,len(p1)):
		median = p1[x]
		# print('Pai 1:', median)
		if median not in p2:
			swapVec.append(x)
		median = p2[x]
		# print('Pai 2:', median)
		if median not in p1:
			swapVec2.append(x)
		
	if(len(swapVec) == 0):
		# print('Individuos iguais')
		return -1
	rd.shuffle(swapVec)
	rd.shuffle(swapVec2)
	return swapVec, swapVec2

	

def crossover(p1, p2, swap1, swap2, k):
	# swap sao as listas de trocas, e a func retorna uma tupla de medianas
	
	for x in range(0, k):
		# i1 e i2 sao indices a serem trocados
		i1 = swap1[x]
		i2 = swap2[x]
		# print(i1,i2)
		p1[i1], p2[i2] = p2[i2], p1[i1]



	return p1, p2


def mutate(solution):
	sol = solution.copy()
	chance = rd.random()
	if chance <= 0.2:
		medPos = rd.randrange(0, len(sol.medians))
		verPos = rd.randrange(0, len(sol.vertices))
		# print(sol.vertices, verPos)
		while sol.vertices[verPos] in sol.medians:
			verPos = rd.randrange(0, len(sol.vertices))
		sol.medians[medPos] = sol.vertices[verPos]
		makeGraph(sol.vertices,sol.medians)
		sol.fitness = addDist(sol.vertices)
		if sol.fitness < solution.fitness:
			return sol
	return solution



def findclosest(solution,median,memo):
	strcoords = str(median.coord_x) + "-" + str(median.coord_y)
	if memo.get(strcoords,None) == None:
		closest = []
		for vertex in solution.vertices:
			if vertex not in solution.medians:
				dist = calcDist(median,vertex)
				insort(closest,(dist,vertex))
				if len(closest) > 3:
					closest.pop()
		closestV = []
		for c in closest:
			closestV.append(c[1])
		memo[strcoords] = closestV
	return memo[strcoords]

# def findclosest(solution,median,banlist,memo):
	# banlist.append(median)
	# closest = []
	# for vertex in solution.vertices:
	# 	if vertex not in solution.medians and vertex not in banlist:
	# 		dist = calcDist(median,vertex)
	# 		insort(closest,(dist,vertex))
	# 		if len(closest) > 3:
	# 			closest.pop()
	# return [closest[0][1],closest[1][1],closest[2][1]]


def localSearch(parent, median = None, memo = {}):

	closestmemo = {}
	strcoords = str(parent.medians)
	if memo.get(strcoords,None) == None:
		memo[strcoords] = parent	
		if median == None:
			median = parent.medians[rd.randrange(0,parent.nMedians)]
		closestlist = findclosest(parent,median,closestmemo)
		for closest in closestlist:
			sol = parent.copy()
			sol.medians.remove(median)
			sol.medians.append(closest)
			makeGraph(sol.vertices, sol.medians)
			sol.fitness = addDist(sol.vertices)
			if sol.fitness < parent.fitness:
				strcoords = str(parent.medians)
				memo[strcoords] = localSearch(sol,closest,memo=memo)
	return memo[strcoords]


def genetic(n_vertices, n_medians, vertices):
	vertex_list = vertices.copy()
	population = randomPopulation(n_vertices, n_medians, vertex_list)
	# testPopulation(population)
	generations = 0
	# media1 = testPopulation(population)
	
	while generations != 6000:
		# selection = rank(population)
		selection = tournament(population)
		
		# p1 e p2 sao listas de medianas (pai1 e pai2)

		parent1 = selection[0]
		parent2 = selection[1]
		p1 = parent1.medians.copy()
		p2 = parent2.medians.copy()
		# makeSwapVec retorna uma tuplas de vetores de posições q n são iguais
		aux = makeSwapVec(p1,p2)
		if(aux == -1):
			parents = [parent1, parent2]
			rd.shuffle(parents)
			i = population.index(parents[0])
			population.pop(i)
			generations+=1
			continue
		swap1 = aux[0]
		swap2 = aux[1]
		# As funções chamadas alteram os seus parametros
		

		crossover(p1, p2, swap1, swap2, rd.randint(0, len(swap1)-1))
		makeGraph(vertices, p1)
		fitness1 = addDist(vertices)


		worstSolution = population[-1]
		offspring1 = Solution(n_medians, n_vertices, vertices, p1, fitness1)
		offspring = mutate(offspring1)
		if(fitness1 < worstSolution.fitness):
			# insort(population, localSearch(offspring))
			insort(population, offspring)


		makeGraph(vertices, p2)
		fitness2 = addDist(vertices)
		worstSolution = population[-1]
		offspring2 = Solution(n_medians, n_vertices, vertices, p2, fitness2)
		offspring = mutate(offspring2)
		if(fitness2 < worstSolution.fitness):
			# insort(population, localSearch(offspring))
			insort(population, offspring)

		for i in range(5):
			localSearch(population[i])
			
		if generations%100 == 0:
			print(generations, population[0].fitness)

		generations+=1

	print(generations, population[0].fitness)
	return population[0].fitness

def runTest():
	# assert selectMedians(vertex_list, n_medians) == testMedian(vertex_list, n_medians)
	p1 = [24, 12, 9, 26, 18, 40]
	p2 = [8, 13, 18, 36, 24, 20]
	swap1 = [1,2,3,5]
	swap2 = [0,1,3,5]
	assert makeSwapVec(p1, p2) ==  (swap1, swap2)
	assert crossover(p1, p2, swap1, swap2, 2) == ([24, 8, 13 , 26,18, 40], [12, 9, 18, 36, 24, 20])
	# assert b[0].fitness == 1581.6422311800602
	# assert b[1].fitness == 2264.0906003051387

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
	
	bestSol = genetic(n_vertices, n_medians, vertex_list)
	# n = 0
	# while(n != 5):
	# 	print()
	# 	sol = genetic(n_vertices, n_medians, vertex_list)
	# 	if(sol < bestSol):
	# 		bestSol = sol
	# 	n+=1
	# print(bestSol)

"""
python3 trab2.py < SJC1.dat > outSJC1.txt
python3 trab2.py < SJC2.dat > outSJC2.txt
python3 trab2.py < SJC3a.dat > outSJC3a.txt
python3 trab2.py < SJC3b.dat > outSJC3b.txt
python3 trab2.py < SJC4a.dat > outSJC4a.txt
python3 trab2.py < SJC4b.dat > outSJC4b.txt


"""
	



	