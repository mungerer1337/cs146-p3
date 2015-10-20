import sys
import random
import pickle
import traceback
import Tkinter



def find_path(source_point, destination_point, mesh):
	#runs in O(n) time, searching each box in the picture
	path = []
	visited_nodes = []
	for node in mesh['boxes']:
		if ( source_point [0] > node[0] and  source_point [0] < node[1] and source_point [1] > node[2] and source_point [1] < node[3]):
			# node contains [x,y]
			# path contians a list of [xy] pairs
			visited_nodes.append(((node)))
		if ( destination_point [0] > node[0] and  destination_point [0] < node[1] and destination_point [1] > node[2] and destination_point [1] < node[3]):
			visited_nodes.append(((node)))

	visited_nodes = BFS(visited_nodes, mesh)
	#print visited_nodes
	#print "*************"
	#print visited_nodes[0][0]
	#print visited_nodes [1]
	return path, visited_nodes






from collections import deque

def BFS(visited_nodes, mesh):
	start = visited_nodes[0]
	end = visited_nodes [1]
	q = deque()
	seen = []
	q.append(((start)))
	seen.append(((start)))
	if start == end:
		return start
	while q:
		node = q.popleft()
		for edge in mesh['adj'][node]:
			#print edge
			if edge not in seen:
				q.append(((edge)))
				seen.append(((edge)))
				if edge == end:
				#	print "we found the end!"
				#	print edge
				#	print "----------"
					#print seen
					return seen
	print "cannot reach this node"
	#print seen, dont do this it is huge
	return 



