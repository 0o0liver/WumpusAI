#import MalmoAI_DFS_Dijkstra as MalmoAI
#import MalmoAI_DFS as MalmoAI
import MalmoAI_AStar as MalmoAI
#import MalmoAI_AStar_noH as MalmoAI
import worldGenerator

try:
	from malmo import MalmoPython
except:
	import MalmoPython

import os
import sys
import time
import json
import random

'''
world = [
["glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass"],
["glass", "wool", "air", "wool", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "wool", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "obsidian", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "obsidian", "stone", "obsidian", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "obsidian", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "wool", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "wool", "air", "wool", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "wool", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "gold_block", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "stone", "glass"],
["glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass", "glass",]]
'''


class feedback:
	def __init__(self, world):
		self.current_location = [1,1]
		self.start_location = self.current_location.copy()
		self.stench = False
		self.breeze = False
		self.bump = False
		self.gliter = False
		self.map = world
		self.check_current_block()
		self.score = 0

	def check_current_block(self):
		current_stone = self.map[self.current_location[0]][self.current_location[1]]
		if current_stone == "wool":
		    self.stench = False
		    self.breeze = True
		    self.bump = False
		    self.gliter = False
		elif current_stone == "obsidian":
		    self.stench = True
		    self.breeze = False
		    self.bump = False
		    self.gliter = False
		elif current_stone == "glowstone":
		    self.stench = True
		    self.breeze = True
		    self.bump = False
		    self.gliter = False
		elif current_stone == "gold_block":
		    self.stench = False
		    self.breeze = False
		    self.bump = False
		    self.gliter = True
			
	def get_state(self):
		return [self.stench, self.breeze, self.bump, self.gliter]

	def get_current_location(self):
		return self.current_location

	def move_north(self):
		self.current_location[0] += 1

	def move_south(self):
		self.current_location[0] -= 1

	def move_west(self):
		self.current_location[1] -= 1

	def move_east(self):
		self.current_location[1] += 1

	def move(self, direction):
			self.score -= 2
			if direction == MalmoAI.Movement.NORTH:
				self.move_north()
			elif direction == MalmoAI.Movement.SOUTH:
				self.move_south()
			elif direction == MalmoAI.Movement.EAST:
				self.move_east()
			elif direction == MalmoAI.Movement.WEST:
				self.move_west()

	def get_block(self, movement):
		if movement == MalmoAI.Movement.NORTH:
			return self.map[self.current_location[0]+1][self.current_location[1]]
		elif movement == MalmoAI.Movement.SOUTH:
			return self.map[self.current_location[0]-1][self.current_location[1]]
		elif movement == MalmoAI.Movement.WEST:
			return self.map[self.current_location[0]][self.current_location[1]-1]
		elif movement == MalmoAI.Movement.EAST:
			return self.map[self.current_location[0]][self.current_location[1]+1]

	def process(self, direction):
		stone = self.get_block(direction)
		print(stone)
		if stone == "glass":
			self.bump = True
		elif stone == "obsidian":
			self.bump = False
			self.stench = True
			self.breeze = False
			self.gliter = False
			self.move(direction)
		elif stone == "wool":
			self.bump = False
			self.stench = False
			self.breeze = True
			self.gliter = False
			self.move(direction)
		elif stone == "gold_block":
			self.bump = False
			self.stench = False
			self.breeze = False
			self.gliter = True
			self.move(direction)
		elif stone == "stone":
			self.bump = False;
			self.stench = False;
			self.breeze = False;
			self.gliter = False
			self.move(direction)
		elif stone == "glowstone":
			self.bump = False
			self.stench = True
			self.breeze = True
			self.gliter = False
			self.move(direction)
		elif direction == MalmoAI.Movement.GRAB:
			if self.map[self.current_location[0]][self.current_location[1]] == "gold_block":
				self.score += 1000
			else:
				self.score -= 10
		elif direction == MalmoAI.Movement.CLIMB:
			if self.current_location != self.start_location:
			    self.score -= 10
		elif direction == MalmoAI.Movement.STABN:
			self.score -= 10
		elif direction == MalmoAI.Movement.STABS:
			self.score -= 10
		elif direction == MalmoAI.Movement.STABE:
			self.score -= 10
		elif direction == MalmoAI.Movement.STABW:
			self.score -= 10
