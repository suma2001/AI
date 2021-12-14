from collections import deque
from heapq import heappop, heappush, heapify
from queue import PriorityQueue
import random
import math
def heuristic(state, goal):
	cnt=0
	for i in range(3):
		for j in range(3):
			if state[i][j] != goal[i][j]:
				cnt+=1

	return cnt

def or_search(state, problem, path):
	print("In and or ",state)
	if problem.goal_test(state):
		return []
	if state in path:
		return None
	for action in problem.actions(state):
		lis = [[[0 for k in range(3)] for j in range(3)] for i in range(3)]
		lis = problem.transitionModel(state, action)
		plan = and_search(lis ,problem, path + [state, ])
		if plan is not None:
		   	return [action, plan]

def and_search(states, problem, path):
	print("States: ", states)
	plan={}
	for s in states:
		print("I am s: ",s)
		plan[s] = or_search(s, problem, path)
		if plan[s] is None:
			return None
	return plan

class Problem:

	def __init__(self, initial_state, goal):
		self.initial_state = initial_state
		self.goal = goal

	def actions(self, state):
		for i in range(3):
			for j in range(3):
				if state[i][j]==0:
					ind1 = i
					ind2 = j
					break
		seq = []
		if ind1-1>=0:
			seq.append('U')
		if ind1+1<=2:
			seq.append('D')
		if ind2-1>=0:
			seq.append('L')
		if ind2+1<=2:
			seq.append('R')

		return seq

	def transitionModel(self, state, action):
		for i in range(3):
			for j in range(3):
				if state[i][j]==0:
					ind1 = i
					ind2 = j
					break
		temp = [row[:] for row in state]
		if action=='U':
			temp[ind1][ind2], temp[ind1-1][ind2] = temp[ind1-1][ind2], temp[ind1][ind2]
		if action=='D':
			temp[ind1][ind2], temp[ind1+1][ind2] = temp[ind1+1][ind2], temp[ind1][ind2]
		if action=='L':
			temp[ind1][ind2], temp[ind1][ind2-1] = temp[ind1][ind2-1], temp[ind1][ind2]
		if action=='R':
			temp[ind1][ind2], temp[ind1][ind2+1] = temp[ind1][ind2+1], temp[ind1][ind2]

		return temp 

	def goal_test(self, state):
		if state == self.goal:
			return True
		else:
			return False

	def pathCost(self, state1, cost):
		return state1.path_cost + cost  ## here cost is 1 for BFS

	
		
class Node:
	def __init__(self, state, parent, action, path_cost=0, heuristic=0, tot=0):
		self.state = state
		self.parent = parent
		self.action = action
		self.path_cost = path_cost
		self.heuristic = heuristic
		self.tot = tot
		if parent:
			self.path_cost = parent.path_cost + 1
		# else:
		# 	self.path_cost=0

	def __lt__(self, other):
		return self.heuristic + self.path_cost< other.heuristic + other.path_cost

	def child_node(self, problem, action):
		new_state = problem.transitionModel(self.state, action)
		return Node(new_state, self, action, problem.pathCost(self, 1))

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
		return goal

	def problem_formulation(self, state, goal):
		return Problem(state, goal)

	def search(self, problem, type):
		# print("Entered")
		if type=="Hill Climbing":	
			current = Node(problem.initial_state, None, None, 0)
			while True:
				neighbors = []
				values=[]
				print("\n\n_____________Iter___________\n")
				for action in problem.actions(current.state):
					child = current.child_node(problem, action)
					neighbors.append(child)
					values.append(heuristic(child.state, goal_state))
				for i in neighbors:
					print(i.state, end="  ")
				print(values)
				if not neighbors:
					break
				value = min(values)
				ind = values.index(value)
				print("Max is:", value)
				print("Ind is:", ind)
				if heuristic(current.state, goal_state) <= heuristic(neighbors[ind].state, goal_state):
					break
				current = neighbors[ind]
			return current.state
		elif type=="Simulated Annealing":
		 	current = Node(problem.initial_state, None, None, 0, heuristic(problem.initial_state, self.formulate_goal()))
		 	print(random.random())
		 	T = 10000
		 	tmp = 0.0001
		 	while(T>1):
			 	neighbors=[]
		 		for action in problem.actions(current.state):
		 			child = current.child_node(problem, action)
		 			if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							print("Output: ",child.state)
							# return child.solution()
							return child.state
		 			neighbors.append(child)
		 		if not neighbors:
		 			return current.state
		 		randomneighbor = random.choice(neighbors)
		 		delta = current.heuristic - randomneighbor.heuristic
		 		prob = math.exp(delta/T)
		 		if delta>0 or prob>random.uniform(0,1):
		 			current = randomneighbor
		 			T=T-tmp
		 	print("Output:",current.state)
		 	return current.state
		 	# return current.solution()

		elif type=="AND-OR":
			return or_search(problem.initial_state, problem, [])


		elif type=="BFS":
			## BFS Code
			# print("ji")
			ini_node = Node(problem.initial_state, None, None, 0)
			if problem.goal_test(ini_node.state):
				print(ini_node.solution())
				return ini_node.solution()

			queue = deque([ini_node])
			# queue.append(ini_node)
			explored_set = set()
			while queue:
				# print(queue)
				# print("ioioio")
				node = queue.popleft()
					#print(node.state)
					# print(queue)
				explored_set.add(node)
				for action in problem.actions(node.state):
					child = node.child_node(problem, action)
					if child not in queue and child not in explored_set:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						queue.append(child)


		elif type=="DFS":
			## DFS Code
			ini_node = Node(problem.initial_state, None, None, 0)
			

			stack = deque([ini_node])
			# queue.append(ini_node)
			explored_set = set()
			while stack:
				# print("Hi")
				node = stack.pop()
					#print(node.state)
					# print(queue)
				explored_set.add(node)

				for action in problem.actions(node.state):
					child = node.child_node(problem, action)
					if child not in explored_set and child not in stack:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						stack.append(child)
		elif type=="GBFS":
			# print(problem.heuristic(problem.initial_state))
			ini_node = Node(problem.initial_state, None, None, 0, heuristic(problem.initial_state, self.formulate_goal()))
			
			heap = []
			heappush(heap, (ini_node.heuristic, ini_node))			# queue.append(ini_node)
			explored_set = set()
			while heap:
				node = heappop(heap)
				if node in heap:
					heap.remove(node)
					heapify(heap)
				explored_set.add(node)
				if problem.goal_test(node[1].state):
					print("Sequence of actions are: ")
					return node[1].solution()

				for action in problem.actions(node[1].state):
					child = node[1].child_node(problem, action)
					child.heuristic = heuristic(child.state, self.formulate_goal())
					if child not in explored_set and child not in heap:
						heappush(heap, (child.heuristic, child))
					elif child in heap:
						index = heap.index(child)
						if heuristic(heap[index], self.formulate_goal()) < heuristic(child, self.formulate_goal()):
							heap[index] = child
							heapify(heap)

		elif type=="A*":
			ini_node = Node(problem.initial_state, None, None, 0, heuristic(problem.initial_state, self.formulate_goal()))
			
			heap = []
			ini_node.tot = ini_node.heuristic + ini_node.path_cost
			heappush(heap, (ini_node.tot, ini_node))			# queue.append(ini_node)
			explored_set = set()
			while heap:
				node = heappop(heap)
				if node in heap:
					heap.remove(node)
					heapify(heap)
				explored_set.add(node)
				if problem.goal_test(node[1].state):
					print("Sequence of actions are: ")
					return node[1].solution()

				for action in problem.actions(node[1].state):
					child = node[1].child_node(problem, action)
					child.heuristic = heuristic(child.state, self.formulate_goal())
					child.tot = child.heuristic + child.path_cost
					if child not in explored_set:
						if problem.goal_test(child.state):
							print("Sequence of actions are: ")
							return child.solution()
						heappush(heap, (child.tot, child))

print("Enter start state: ")
# start_state = []
# for i in range(3):
# 	a=[]
# 	for j in range(3):
# 		a.append(int(input()))
# 	start_state.append(a)


print("Enter goal state: ")
# goal_state = []
# for i in range(3):
# 	a=[]
# 	for j in range(3):
# 		a.append(int(input()))
# 	goal_state.append(a)
# start_state = [[7,2,4],[5,0,6],[8,3,1]]
start_state=[[3,4,5],[6,7,8],[0,1,2]]
# start_state=[[1,2,3],[0,4,8],[6,7,5]]
goal_state=[[0,1,2],[3,4,5],[6,7,8]]
print("Enter one of these:   BFS    DFS    Bidir    A*")
# typ = input()
typ="AND-OR"
obj = ProblemSolvingAgent(start_state)
ans = obj.call_agent(start_state, typ)
# ans.remove(None)
# ans = ans[::-1]
print(ans)

