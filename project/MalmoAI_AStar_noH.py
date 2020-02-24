from __future__ import division
from enum import Enum
from queue import Queue
from priority_dict import priorityDictionary as PQ
import numpy as np
#import MalmoPython

class Movement(Enum):
		NORTH = 1
		SOUTH = 2
		WEST  = 3
		EAST  = 4
		GRAB  = 5
		CLIMB = 6
		STABN = 7
		STABS = 8
		STABW = 9
		STABE = 10

class MalmoAI():
	def __init__(self):
		#self.map = ["unexplored"]*21 #may not need
		self.current = (0,0)
		self.explored = set()
		self.wumpusMap = [0]*21
		self.pitMap = [0]*21
		self.wumpusFound = False
		self.WumpusLocation = None

		self.eastMax = 21
		self.northMax = 21
		self.defaultnMax = 21

		self.safeSpots = []
		self.unsafeSpots = set()

		self.previousAction = None
		self.gettingOut = False
		self.haveGold = False
		self.movementQueue = Queue()

		temp2 = [1]*21
		for i in range(0, 21):
			self.wumpusMap[i] = temp2.copy()
			self.pitMap[i] = temp2.copy()

		self.wumpusMap[0][0] = 0
		self.pitMap[0][0] = 0
		



	def getMovement(self, stench, breeze, glitter, bump):
		#print(self.safeSpots)
		if (glitter and not self.haveGold):
			self.movementQueue = Queue()
			self.movementQueue.put("GRAB")
			self.haveGold = True
			return self.doActions()

		if (self.haveGold):
			self.gettingOut = True
			self.getOut()
			return self.doActions()



		
	
		if (bump):
			if (self.previousAction == "NORTH"):
				self.northMax = self.current[1]
				print("new n max ", self.northMax)
				self.current = (self.current[0], self.current[1] - 1)
			if (self.previousAction == "SOUTH"):
				self.current = (self.current[0], self.current[1] + 1)
			if (self.previousAction == "EAST"):
				self.eastMax = self.current[0]
				print("new e max ", self.eastMax)
				self.current = (self.current[0] - 1, self.current[1])
			if (self.previousAction == "WEST"):
				self.current = (self.current[0] + 1, self.current[1])


		if (self.current not in self.explored):
			print(stench)
			print(breeze)
			self.explored.add(self.current)
			self.handleStenchBreeze(stench, breeze)


		#self.printMap(self.wumpusMap)
		#self.printMap(self.pitMap)

		if (not self.movementQueue.empty()):
			print("going to queue")
			return self.doActions()

		self.handleBump(bump)
		self.movementQueue = self.getNextAction()

		

		
		
		return self.doActions()

	def doActions(self):
		if (self.current not in self.explored):
			print ("adding to explored:************************************************************************************* ", self.current)
			self.explored.add(self.current)

		#print(self.safeSpots)
		if (self.movementQueue.empty()):
			#self.previousAction = direction
			return Movement.CLIMB

		direction = self.movementQueue.get()

		if (direction == "NORTH"):
			print(direction)
			self.previousAction = direction
			self.current = (self.current[0], self.current[1] + 1)
			return Movement.NORTH
		if (direction == "SOUTH"):
			print(direction)
			self.previousAction = direction
			self.current = (self.current[0], self.current[1] - 1)
			return Movement.SOUTH
		if (direction == "EAST"):
			print(direction)
			self.previousAction = direction
			self.current = (self.current[0] + 1, self.current[1])
			return Movement.EAST
		if (direction == "WEST"):
			print(direction)
			self.previousAction = direction
			self.current = (self.current[0] - 1, self.current[1])
			return Movement.WEST
		if (direction == "GRAB"):
			print(direction)
			self.previousAction = direction
			return Movement.GRAB
		if (direction == "CLIMB"):
			print(direction)
			self.previousAction = direction
			return Movement.CLIMB
		if (direction == "STABN"):
			print(direction)

			self.previousAction = direction
			return Movement.STABN
		if (direction == "STABS"):
			print(direction)
			self.previousAction = direction
			return Movement.STABS
		if (direction == "STABE"):
			print(direction)
			self.previousAction = direction
			return Movement.STABE
		if (direction == "STABW"):
			print(direction)
			self.previousAction = direction
			return Movement.STABW


	def getAdjacents(self, location):
		north = (location[0], location[1] + 1)
		east = (location[0] + 1, location[1])
		south = (location[0], location[1] - 1)
		west = (location[0] - 1, location[1])

		return north, east, south, west

	def handleStenchBreeze(self, stench, breeze):
		#at 4 set wumpus to found
		north, east, south, west = self.getAdjacents(self.current)

		if (not stench and not breeze):
			if (north[1] < self.northMax):
				self.wumpusMap[north[0]][north[1]] = 0
				self.pitMap[north[0]][north[1]] = 0
				#if (north not in self.safeSpots):
				self.setSafe(north, True)
			if (east[0] < self.eastMax):
				self.wumpusMap[east[0]][east[1]] = 0
				self.pitMap[east[0]][east[1]]  = 0
				#if (east not in self.safeSpots):
				self.setSafe(east, True)
			if (south[1] >= 0):
				self.wumpusMap[south[0]][south[1]] = 0
				self.pitMap[south[0]][south[1]] = 0
				#if (south not in self.safeSpots):
				self.setSafe(south, True)
			if (west[0] >= 0):
				self.wumpusMap[west[0]][west[1]] = 0
				self.pitMap[west[0]][west[1]] = 0
				#if (west not in self.safeSpots):
				self.setSafe(west, True)
		else:
			if (stench and breeze and not self.wumpusFound):
				print("here")
				if (north[1] < self.northMax):
					if (self.wumpusMap[north[0]][north[1]] != 0 or self.pitMap[north[0]][north[1]] != 0):
						if (self.wumpusMap[north[0]][north[1]] != 0):
							self.wumpusMap[north[0]][north[1]] += 1
							if (self.wumpusMap[north[0]][north[1]] == 4):
								self.WumpusLocation = north
								self.wumpusFound = True
						if (self.pitMap[north[0]][north[1]] != 0):
							self.pitMap[north[0]][north[1]] += 1
						self.unsafeSpots.add(north)	
				if (east[0] < self.eastMax):
					if (self.wumpusMap[east[0]][east[1]] != 0 or self.pitMap[east[0]][east[1]] != 0):	
						if (self.wumpusMap[east[0]][east[1]] != 0):
							self.wumpusMap[east[0]][east[1]] += 1
							if (self.wumpusMap[east[0]][east[1]] == 4):
								self.WumpusLocation = east
								self.wumpusFound = True
						if (self.pitMap[east[0]][east[1]] != 0):
							self.pitMap[east[0]][east[1]] += 1
						self.unsafeSpots.add(east)
				if (south[1] >= 0):
					if (self.wumpusMap[south[0]][south[1]] != 0 or self.pitMap[south[0]][south[1]] != 0):
						if (self.wumpusMap[south[0]][south[1]] != 0):
							self.wumpusMap[south[0]][south[1]] += 1
							if (self.wumpusMap[south[0]][south[1]] == 4):
								self.WumpusLocation = south
								self.wumpusFound = True
						if (self.pitMap[south[0]][south[1]] != 0):
							self.pitMap[south[0]][south[1]] += 1
						self.unsafeSpots.add(south)
				if (west[0] >= 0):
					if (self.wumpusMap[west[0]][west[1]] != 0 or self.pitMap[west[0]][west[1]] != 0):
						if (self.wumpusMap[west[0]][west[1]] != 0):
							self.wumpusMap[west[0]][west[1]] += 1
							if (self.wumpusMap[west[0]][west[1]] == 4):
								self.WumpusLocation = west
								self.wumpusFound = True
						if (self.pitMap[west[0]][west[1]] != 0):
							self.pitMap[west[0]][west[1]] += 1
						self.unsafeSpots.add(west)
					
				if (self.wumpusFound):
					self.wumpusFoundProtocol()
			else:		
				if (stench and not self.wumpusFound):
					if (north[1] < self.northMax and self.wumpusMap[north[0]][north[1]] != 0):
						self.wumpusMap[north[0]][north[1]] += 1
						self.pitMap[north[0]][north[1]] = 0
						self.unsafeSpots.add(north)
						if (self.wumpusMap[north[0]][north[1]] == 4):
							self.WumpusLocation = north
							self.wumpusFound = True
					if (east[0] < self.eastMax and self.wumpusMap[east[0]][east[1]] != 0):
						self.wumpusMap[east[0]][east[1]] += 1
						self.pitMap[east[0]][east[1]] = 0
						self.unsafeSpots.add(east)
						if (self.wumpusMap[east[0]][east[1]] == 4):
							self.WumpusLocation = east
							self.wumpusFound = True
					if (south[1] >= 0 and self.wumpusMap[south[0]][south[1]] != 0):
						self.wumpusMap[south[0]][south[1]] += 1
						self.pitMap[south[0]][south[1]] = 0
						self.unsafeSpots.add(south)
						if (self.wumpusMap[south[0]][south[1]] == 4):
							self.WumpusLocation = south
							self.wumpusFound = True
					if (west[0] >= 0 and self.wumpusMap[west[0]][west[1]] != 0):
						self.wumpusMap[west[0]][west[1]] += 1
						self.pitMap[west[0]][west[1]] = 0
						self.unsafeSpots.add(west)
						if (self.wumpusMap[west[0]][west[1]] == 4):
							self.WumpusLocation = west
							self.wumpusFound = True
					
					if (self.wumpusFound):
						self.wumpusFoundProtocol()

				if (breeze):
					if (north[1] < self.northMax and self.pitMap[north[0]][north[1]] != 0):
						self.pitMap[north[0]][north[1]] += 1
						self.wumpusMap[north[0]][north[1]] = 0
						self.unsafeSpots.add(north)
					if (east[0] < self.eastMax and self.pitMap[east[0]][east[1]] != 0):
						self.pitMap[east[0]][east[1]] += 1
						self.wumpusMap[east[0]][east[1]] = 0
						self.unsafeSpots.add(east)
					if (south[1] >= 0 and self.pitMap[south[0]][south[1]] != 0):
						self.pitMap[south[0]][south[1]] += 1
						self.wumpusMap[south[0]][south[1]] = 0
						self.unsafeSpots.add(south)
					if (west[0] >= 0 and self.pitMap[west[0]][west[1]] != 0):
						self.pitMap[west[0]][west[1]] += 1
						self.wumpusMap[west[0]][west[1]] = 0
						self.unsafeSpots.add(west)

	def handleBump(self, bump):
		#if (bump):
		pass


	def getNextAction(self):
		actionQ = Queue()

		if (not self.safeSpots):
			return self.getOut()
		print("before pick: ", self.safeSpots)

		picked = None
		smallest = 1000

		for x in list(self.safeSpots):
			
			if (x[0] >= self.eastMax or x[1] >= self.northMax):
				self.safeSpots.remove(x)
				continue
			current = len(self.dijkstra(self.current, x))
			print(current)
			if (current < smallest):
				picked = x
				smallest = current
				
		if (picked == None):
			return self.getOut()
		self.safeSpots.remove(picked)



		
		#while(picked[0] >= self.eastMax or picked[1] >= self.northMax):
		#	if (self.safeSpots):
		#		picked = self.safeSpots.pop(0)
		#	else:
		#		return self.getOut()


		print("picked: ", picked)
		print("after pick: ", self.safeSpots)
		coordsToMove = self.dijkstra(self.current, (picked))
		actions = self.convertCoordToAction(coordsToMove)
		print("actions to get there: ", list(actions.queue))
		return actions

	def convertCoordToAction(self, coord):
		# translatedPath = Queue()
		# while(coord):
		# 	current = coord.pop(0)
		# 	for x in coord:
		# 		if ((current[0], current[1] + 1) == x): #north
		# 			translatedPath.put("NORTH")
		# 		if ((current[0], current[1] - 1) == x): #south
		# 			translatedPath.put("SOUTH")
		# 		if ((current[0] + 1, current[1]) == x): #east
		# 			translatedPath.put("EAST")
		# 		if ((current[0] - 1, current[1]) == x): #north
		# 			translatedPath.put("WEST")
		# return translatedPath

		translatedPath = Queue()
		print("coord ", coord)
		while(coord):
			current = coord.pop(0)
			if (not coord):
				break
			if ((current[0], current[1] + 1) == coord[0]): #north
				translatedPath.put("NORTH")
				print("putting NORTH")
			if ((current[0], current[1] - 1) == coord[0]): #south
				translatedPath.put("SOUTH")
				print("putting SOUTH")
			if ((current[0] + 1, current[1]) == coord[0]): #east
				translatedPath.put("EAST")
				print("putting EAST")
			if ((current[0] - 1, current[1]) == coord[0]): #north
				translatedPath.put("WEST")
				print("putting WEST")
		return translatedPath


	def getOut(self):
		self.movementQueue = self.convertCoordToAction(self.dijkstra(self.current, (0,0)))
		self.movementQueue.put("CLIMB")
		return self.movementQueue
		

	def dijkstra(self, start, dest):
		start_dist = 0
		priorityQ = PQ()
		priorityQ.setdefault(start, start_dist)

		trace = dict()
		visited = set()

		trace[start] = [None, start_dist]

		while(True):
			#print("AIHSHDAHDHSIHIDDSDASHDSADSIAHSDAH")
			current = priorityQ.smallest()
			#print(current)
			del priorityQ[current]
			if (current == dest):
				break;
			visited.add(current)

			n, e, s, w = self.getAdjacents(current)


			if (n[1] < self.northMax and self.wumpusMap[n[0]][n[1]] == 0 and self.pitMap[n[0]][n[1]] == 0 and n not in visited):   
				priorityQ.setdefault(n, trace[current][1] + 1)
				trace[n] = [current, trace[current][1] + 1]
			if (s[1] >= 0 and self.wumpusMap[s[0]][s[1]] == 0 and self.pitMap[s[0]][s[1]] == 0 and s not in visited):
				priorityQ.setdefault(s, trace[current][1] + 1)
				trace[s] = [current, trace[current][1] + 1]
			if (e[0] < self.eastMax and self.wumpusMap[e[0]][e[1]] == 0 and self.pitMap[e[0]][e[1]] == 0 and e not in visited):
				priorityQ.setdefault(e, trace[current][1] + 1)
				trace[e] = [current, trace[current][1] + 1]
			if (w[0] >= 0 and self.wumpusMap[w[0]][w[1]] == 0 and self.pitMap[w[0]][w[1]] == 0 and w not in visited):
				priorityQ.setdefault(w, trace[current][1] + 1)
				trace[w] = [current, trace[current][1] + 1]

		path = [dest]
		last = dest
		while(True):
			if (trace[last][0] is None):
				break;
			path.insert(0, trace[last][0])
			last = trace[last][0]

		return path


	def wumpusFoundProtocol(self):
		print("Wumpus Found at ", self.WumpusLocation)
		self.safeSpots.insert(0, self.WumpusLocation)
		for x in range(self.eastMax):
			for y in range(self.northMax):
				if (self.wumpusMap[x][y] != 4 and self.wumpusMap[x][y] != 0):
					self.wumpusMap[x][y] = 0
					self.setSafe((x, y), False)
		north, east, south, west = self.getAdjacents(self.current)

		adjacents = [north, east, south, west]
		for x in adjacents:
			if (x == self.WumpusLocation):
				if (x == north):
					self.wumpusMap[north[0]][north[1]] = 0
					self.movementQueue.put("STABN")
				if (x == south):
					self.wumpusMap[south[0]][south[1]] = 0
					self.movementQueue.put("STABS")
				if (x == east):
					self.wumpusMap[east[0]][east[1]] = 0
					self.movementQueue.put("STABE")
				if (x == west):
					self.wumpusMap[west[0]][west[1]] = 0
					self.movementQueue.put("STABW")
		print("Wumpus map value ", self.wumpusMap[self.WumpusLocation[0]][self.WumpusLocation[1]])
		print("pit map value ", self.pitMap[self.WumpusLocation[0]][self.WumpusLocation[1]])

	def setSafe(self, coord, beginning):
		if (self.wumpusMap[coord[0]][coord[1]] == 0 and self.pitMap[coord[0]][coord[1]] == 0 and coord not in self.explored):
			if (coord in self.unsafeSpots):
				self.unsafeSpots.remove(coord)
			if (beginning):
				if (coord in self.safeSpots):
					self.safeSpots.remove(coord)
				self.safeSpots.insert(0, coord)
			else:
				self.safeSpots.append(coord)

	def printMap(self, map):
		for i in range(self.defaultnMax - self.northMax, self.defaultnMax):
			for x in range(self.eastMax):
				if ((x, i) == (self.current[0], -1*(self.current[1] - (self.defaultnMax - 1)))):
					print("@", end = ' ')
				else:
					#print("i is this: ", i)
					print(map[x][::-1][i], end=' ')
			print()
		print("**********************************************")


# testAI = MalmoAI()

# while(True):
# 	stench = True if (input("stench?: ") == "t") else False
# 	breeze = True if (input("breeze?: ") == "t") else False
# 	glitter = True if (input("glitter?: ") == "t") else False
# 	bump = True if (input("bump?: ") == "t") else False
# 	found = testAI.getMovement(stench, breeze, glitter, bump)
# 	if (found == Movement.CLIMB):
# 		print("climbed")
# 		break
# 	testAI.printMap(testAI.wumpusMap)
# 	testAI.printMap(testAI.pitMap)
# 	print("current movable ", testAI.safeSpots)
# 	print("current coord ", testAI.current)


'''
from enum import Enum
class Movement(Enum):
		NORTH = 1
		SOUTH = 2
		WEST  = 3
		EAST  = 4
		GRAB  = 5
		CLIMB = 6
		
class MalmoAI():
	def getstuff(this):
	    return Movement.NORTH
		
class MalmoAI2():
	def checkit(this):
	    newstuff = MalmoAI()
	    print(newstuff.getstuff() == Movement.NORTH)
	    
thisstuff = MalmoAI2()
thisstuff.checkit()

'''

