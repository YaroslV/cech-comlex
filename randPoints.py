import matplotlib.pyplot as plt
import random
import math
import itertools


#TODO plt is global variable entry point for display is it good or bad

class Cell:
	def __init__(self,x,y,r,index):
		self.x = x
		self.y = y
		self.r = r
		self.index = index
	
	def draw_cell(self):
		circle1 = plt.Circle((self.x,self.y),self.r,color='b', alpha =.2)
		plt.gcf().gca().add_artist(circle1)
		
	def is_intersects_with_cell(self, c):
		dist = calculateDistance(self.x,c.x,self.y,c.y)
		if dist > self.r + c.r :
			return False
		return True
	
	def get_intersection_points(self,c):
		if self.is_intersects_with_cell(c) == False:
			return None
		d = calculateDistance(self.x,self.y,c.x,c.y)
		a = d /2
		h = math.sqrt((self.r)**2 - a**2)
		Pm_0 = self.x + (a*(c.x - self.x))/d
		Pm_1 = self.x + (a*(c.y - self.y))/d
		ip1_0 = Pm_0 + (h*(c.y - self.y))/d
		ip1_1 = Pm_1 - (h*(c.x - self.x))/d
		ip2_0 = Pm_0 - (h*(c.y - self.y))/d	
		ip2_1 = Pm_1 + (h*(c.x - self.x))/d
		return [(ip1_0,ip1_1),(ip2_0, ip2_1)]
	def is_contains_point(self,p):
		d = calculateDistance(self.x, self.y, p[0],p[1])
		return d <= self.r

def showRandomPoints(n,r):	
	data = get_list_of_random_cells_with_length_n(n,r)
	xs = [x.x for x in data]
	ys = [y.y for y in data]
	
	labels = ['{0}'.format(i) for i in range(n)]
	
	plt.scatter(xs,ys)	
	
	for i in range(n):		
		plt.annotate(labels[i],(data[i].x, data[i].y))	
	
	for p in data:
		p.draw_cell()
		
	plt.gca().set_aspect('equal')
	
	S1 = construct_1_simplices(data, r)
	Sset = construct_cech_complex(data,S1)
	
	drawLinesForCertainsIndexes(data, S1)
	print(S1)		
	print(get_neigbors_dict(S1))
	print(Sset)
	plt.show()

def getIntersectionPoints(p1,p2,r):
	if (isIntersect(p1,p2,r) == False):
		return None
	
	d = calculateDistance(p1[0],p1[1], p2[0],p2[1])
	a = d / 2 
	h = math.sqrt(r**2 - a**2)
	Pm_0 = p1[0] + (a*(p2[0] - p1[0]))/d
	Pm_1 = p1[0] + (a*(p2[1] - p1[1]))/d
	
	ip1_0 = Pm_0 + (h*(p2[1] - p1[1]))/d
	ip1_1 = Pm_1 - (h*(p2[0] - p1[0]))/d
	
	ip2_0 = Pm_0 - (h*(p2[1] - p1[1]))/d	
	ip2_1 = Pm_1 + (h*(p2[0] - p1[0]))/d
	return [(ip1_0,ip1_1),(ip2_0, ip2_1)]
		
def drawLine(p1,p2):
	plt.plot([p1.x,p2.x],[p1.y,p2.y])
	
def drawLinesForCertainsIndexes(data,indexes):
	for idx in indexes:
		drawLine(data[idx[0]],data[idx[1]])
	
def drawCircle(p,r):
	circle1 = plt.Circle((p[0],p[1]),r,color='b', alpha =.2)
	plt.gcf().gca().add_artist(circle1)

def calculateDistance(x1,y1,x2,y2):
	d = math.sqrt((x1 - y1)**2 + (x2 - y2)**2)
	return d

	#hard-coded range
def get_list_of_random_cells_with_length_n(n,r):
	list = []
	for i in range(n):
		rx = random.randint(0,21)
		ry = random.randint(0,21)
		list.append(Cell(rx,ry,r,i))
	return list

def isIntersect(p1,p2,r):
	dist = calculateDistance(p1[0],p2[0],p1[1],p2[1])
	if dist > 2 * r :
		return False	
	return True
	
def is_intersect_cells(c1,c2):
	dist = calculateDistance(c1.x,c2.x,c1.y,c2.y)
	if dist > c1.r + c2.r :
		return False
	return True
		
	
def construct_1_simplices(cells, r):	
	S1 = []
	N = len(cells)
	for i in range(N - 1):
		for j in range(i + 1, N):
			if is_intersect_cells(cells[i],cells[j]) == True:
				s = (i,j)
				S1.append(s)
	return S1
	

	

#candidates are cells
def verify_candidate(candidates):
	X = []
	k = len(candidates)
	for i in range(k):
		for j in range(i+1, k+1) :
			intersectionPoints = candidates[i].get_intersection_points(candidates[j])
			if intersectionPoints is not None:
				X.append((i,j,intersectionPoints))
	for x in X:
		i = x[0]
		j = x[1]
		restCellsIndexList = range(k)
		restCellsIndexList.remove(i)
		restCellsÌndexList.remove(j)
		numberOfXijExistsInRestCells = 0
		for t in restCells:
			anotherCell = candidates[t]
			if anotherCell.is_contains_point(x[2][0]) or anotherCell.is_contains_point(x[2][1]) :
				numberOfXijExistsInRestCells = numberOfXijExistsInRestCells + 1
		
		if numberOfXijExistsInRestCells == len(restCellsIndexList) :
			return True		
	return False
	
def construct_cech_complex(S0, S1):
	k = 2
	S = []
	neighDict = get_neigbors_dict(S1)
	S.append(0)
	S.append(1)	
	while (True) :
		S.append([])
		Sstar = get_set_of_candidate(neighDict,k,S0)
		for u in Sstar :
			verification = verify_candidate(u)
			if verification :
				S[k].append(u)
		if len(S[k]) != 0 :
			k = k + 1
		else: 
			break
		return S[2:]
		
def get_neigbors_dict(S1):	

	neigboursDict = dict()
	for j in S1:
			if neigboursDict.get(j[0],0) == 0:
				neigboursDict[j[0]] = []
			neigboursDict[j[0]].append(j[1])
			if neigboursDict.get(j[1],0) == 0:
				neigboursDict[j[1]] = []
				neigboursDict[j[1]].append(j[0])

	return neigboursDict


def get_set_of_candidate(neighDict, kSimplexNo,cells):
	candidateCellsList = []
	for i in neighDict : 
		if len(neighDict[i]) >=kSimplexNo :
			comb = [ list(c) for c in itertools.combinations(neighDict[i],kSimplexNo)]
			for c in comb:									
				c.append(i)
				cellsC = [cells[i] for i in c]
				candidateCellsList.append(cellsC)
	return candidateCellsList

	



if __name__ == "__main__":    
	import sys
	showRandomPoints(int(sys.argv[1]), int(sys.argv[2]))
