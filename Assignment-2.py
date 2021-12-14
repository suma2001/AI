import pandas as pd
import time
df = pd.read_excel('Indian_capitals.xlsx', header=None)
from collections import deque
from heapq import heappop, heappush, heapify
from locationiq.geocoder import LocationIQ
from math import radians, sin, cos, acos

geocoder = LocationIQ('10db090e679efa')
coordinates={}
def coordinate_values():
	capitals = []
	for i in df[0]:
		if i not in capitals:
			capitals.append(i)
	for i in df[1]:
		if i not in capitals:
			capitals.append(i)
	# print(capitals)
	for a in capitals:
		time.sleep(1)
		pla = geocoder.geocode(a)[0]

		lati = radians(float(pla['lat']))
		longi = radians(float(pla['lon']))
		coordinates[a] = (lati, longi)

	# print(coordinates)

coordinate_values()

def stepcost(state1, state2):
	if not df.where(df[0]==state1).dropna().empty:
		if not df.where(df[1]==state2).dropna().empty: 
			weight = ((df.where(df[0]==state1).dropna())[2])
	if not df.where(df[1]==state2).dropna().empty:
		if not df.where(df[0]==state1).dropna().empty: 
			weight = ((df.where(df[1]==state1).dropna())[2])
	wt=[]
	for i in weight:
		wt.append(i)
	wt = float(wt[0])
	return wt
	# print(wt)


def heuristic(state, goal):
	slat = coordinates[state][0]
	slon = coordinates[state][1]
	elat = coordinates[goal][0]
	elon = coordinates[goal][1]
	dist = 6371.01 * acos(sin(slat)*sin(elat) + cos(slat)*cos(elat)*cos(slon-elon))
	# print(dist)
	return dist

# heuristic()
class Problem:

	def __init__(self, initial_state, goal):
		self.initial_state = initial_state
		self.goal = goal

	def actions(self, node):
		# print("I am in", node, node.state)
		seq = []
		p1 = ((df.where(df[0]==node.state).dropna())[1])
		p2 = ((df.where(df[1]==node.state).dropna())[0])
		for i in p1:
			seq.append(i)
		for i in p2:
			seq.append(i)
		# print("Sequence is :",seq)
		return seq

	def transitionModel(self, state, action):
		return action

	def goal_test(self, state):
		# print("this is inside goal :",str(state).replace(" ",""), self.goal)
		place = str(state).replace(" ","")
		if place == self.goal:
			return True
		else:
			return False

	def pathCost(self, state1, cost):
		# print("Total cost: ", cost + state1.path_cost)
		return state1.path_cost + cost  ## here cost is 1 for BFS

	
		
class Node:
	def __init__(self, state, parent, action, path_cost=0, heuristic=0, tot=0):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.heuristic = heuristic
		self.tot = tot
		# if parent:
		# 	self.path_cost = parent.path_cost + step
		# else:
		# 	self.path_cost=0

	def __lt__(self, other):
		return self.heuristic < other.heuristic

	def child_node(self, problem, action):
		new_state = problem.transitionModel(self.state, action)
		if not df.where(df[0]==self.state).dropna().empty:
			if not df.where(df[1]==new_state).dropna().empty: 
				weight = ((df.where(df[0]==self.state).dropna())[2])
		if not df.where(df[1]==self.state).dropna().empty:
			if not df.where(df[0]==new_state).dropna().empty: 
				weight = ((df.where(df[1]==self.state).dropna())[2])
		wt=[]
		for i in weight:
			wt.append(i)
		wt = float(wt[0])
		# print(wt)
		cost = problem.pathCost(self, wt)
		return Node(new_state, self, action, cost)

	def solution(self):
		path = []
		node = self
		while node:
			path.append(node.action)
			node = node.parent 
		return path


class ProblemSolvingAgent:

	def __init__(self, initial_state):
		self.initial_state = initial_state
		self.seq = []

	def call_agent(self, percept, mode):
		goal = self.formulate_goal()
		problem = self.problem_formulation(self.initial_state, goal)
		self.seq.append(self.search(problem, mode))
		if not self.seq:
			return None

		return self.seq.pop(0)

	def update_state(self, state, percept):
		return percept

	def formulate_goal(self):
		goal = goal_state
		if goal=="Bengaluru":
			goal = "Bangalore"
		return goal

	def problem_formulation(self, state, goal):
		return Problem(state, goal)

	def search(self, problem, type):
		node = Node(problem.initial_state, None, None, 0)
		if type=="BFS":
			ini_node = Node(problem.initial_state, None, None, 0)
			if problem.goal_test(ini_node.state):
				print(ini_node.solution())
				return ini_node.solution()

			queue = deque([ini_node])
			explored_set = set()
			while queue:
				node = queue.popleft()
				explored_set.add(node)
				for action in problem.actions(node):
					child = node.child_node(problem, action)
					if child not in queue and child not in explored_set:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						queue.append(child)
		elif type=="DFS":
			ini_node = Node(problem.initial_state, None, None, 0)
			stack = deque([ini_node])
			explored_set = set()
			while stack:
				node = stack.pop()
				explored_set.add(node)
				print(problem.actions(node))
				for action in problem.actions(node):
					print(action)
					child = node.child_node(problem, action)
					print(child.state)
					if child not in explored_set and child not in stack:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						stack.append(child)
		elif type=="Bidir":
			problem1 = Problem(problem.initial_state, self.formulate_goal())
			problem2 = Problem(self.formulate_goal(), problem.initial_state)
			ini_node = Node(problem.initial_state, None, None, 0)
			fin_node = Node(self.formulate_goal(), None, None, 0)
			start_frontier = deque([ini_node])
			start_explored = set()
			l=[]
			l1=[]
			l2=[]
			end_frontier = deque([fin_node])
			end_explored = set()
			while start_frontier and end_frontier and len([i.state for i in start_frontier for j in end_frontier if i.state==j.state] )==0:
				node = start_frontier.popleft()
				start_explored.add(node)
				for action in problem1.actions(node):
					child = node.child_node(problem1, action)
					if child not in start_frontier and child not in start_explored:
						if problem1.goal_test(child.state):
							print("Sequence of actions are: ")
							l1.append(child.solution())
							print(child.solution())
							break
						start_frontier.append(child)

				node = end_frontier.popleft()
				end_explored.add(node)
				for action in problem2.actions(node):
					child = node.child_node(problem2, action)
					if child not in end_frontier and child not in end_explored:
						if problem2.goal_test(child.state):
							print("Sequence of actions are: ")
							l2.append(child.solution())
							print(child.solution())
							break
						end_frontier.append(child)

			print([i.state for i in start_frontier for j in end_frontier if i.state==j.state])
			# print([i.state for i in start_frontier])
			# print([j.state for j in end_frontier])
			p=[i.state for i in start_frontier for j in end_frontier if i.state==j.state]
			if not l1 or not l2:
				# print("First if")
				l=l1+l2
			else:
				# print("next if")
				x=[]
				y=[]
				for i in start_frontier:
					for j in end_frontier:
						if i.state==j.state:
							l=i.solution()[::-1]+j.solution()[1:]
							break
			print(l)
			return l

		elif type=="A*":
			ini_node = Node(problem.initial_state, None, None, 0, heuristic(problem.initial_state, self.formulate_goal()))
			
			heap = []
			ini_node.tot = ini_node.heuristic + ini_node.path_cost
			heappush(heap, (ini_node.tot, ini_node))			# queue.append(ini_node)
			explored_set = set()
			while heap:
				node = heappop(heap)
				print("Node with highest priority: ", node[1].state)
				if node in heap:
					heap.remove(node)
					heapify(heap)
				explored_set.add(node)
				if problem.goal_test(node[1].state):
					print("Sequence of actions are: ")
					return node[1].solution()

				for action in problem.actions(node[1]):
					child = node[1].child_node(problem, action)
					child.heuristic = heuristic(child.state, self.formulate_goal())
					child.tot = child.heuristic + child.path_cost
					if child not in explored_set:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						heappush(heap, (child.tot, child))

print("Enter input state: ")
start_state = input()
if start_state=="Bengaluru":
	start_state = "Bangalore"

print("Enter goal state: ")
goal_state = input()

print("Enter one of these:   BFS    DFS    GBFS    A*")
typ = input()
obj = ProblemSolvingAgent(start_state)
ans = obj.call_agent(start_state, typ)
# if None in ans:
# 	ans.remove(None)
ans = ans[::-1]
print(ans)