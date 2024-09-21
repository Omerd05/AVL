"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor
	@type key: int or None
	@type value: any
	@param value: data of your node
	O(1) time complexity
	"""

	def __init__(self, key=None, value=None):
		self.key = key
		self.value = value
		self.left = None
		self.right = None
		self.parent = None
		self.height = -1
		if self.key != None:
			self.height = 0
		if self.key != None:
			self.set_left(AVLNode(None,None))
			self.set_right(AVLNode(None,None))
		

	"""returns the left child
	@rtype: AVLNode
	@returns: the left child of self, None if there is no left child (if self is virtual)
	O(1) time complexity
	"""

	def get_left(self):
		return self.left



	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	O(1) time complexity
	"""

	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	O(1) time complexity
	"""
	def get_parent(self):
		return self.parent


	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	O(1) time complexity
	"""
	def get_key(self):
		return self.key


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	O(1) time complexity
	"""
	def get_value(self):
		return self.value


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	O(1) time complexity
	"""
	def get_height(self):
		return self.height



	"""sets left child

	@type node: AVLNode
	@param node: a node
	O(1) time complexity
	"""

	# Creates 2 edges - (u->v) AND (v->u)
	def set_left(self, node):
		self.left = node
		#self.height = max(self.height,self.left.height+1)
		node.parent = self


	"""sets right child

	@type node: AVLNode
	@param node: a node
	O(1) time complexity
	"""

	#Creates 2 edges - (u->v) AND (v->u)
	def set_right(self, node):
		self.right = node
		node.parent = self


	#Private method
	#Choosing correct position for node, just a simplification for later.
	#Working in O(1) time complexity
	def set_child(self, node, direction = -1):
		if node.is_real_node():
			if self.key > node.key:
				self.set_left(node)
			else:
				self.set_right(node)
		elif direction != -1: #0-left,1-right
			if direction == 0:
				self.set_left(node)
			else:
				self.set_right(node)


	"""sets parent

	@type node: AVLNode
	@param node: a node
	O(1) time complexity
	"""
	def set_parent(self, node,direction = -1):
		self.parent = node
		if node != None :
			node.set_child(self,direction)


	"""sets key

	@type key: int or None
	@param key: key
	O(1) time complexity
	"""
	def set_key(self, key):
		self.key = key


	"""sets value

	@type value: any
	@param value: data
	O(1) time complexity
	"""
	def set_value(self, value):
		self.value = value


	"""sets the height of the node

	@type h: int
	@param h: the height
	O(1) time complexity
	"""

	def BF(self):
		if not self.is_real_node():
			return 0
		return self.left.height - self.right.height

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	O(1) time complexity
	"""
	def is_real_node(self):
		if self.value == None:
			return False
		return True

	#Private method
	#Adjusting the node's height to its correct value
	#O(1) time complexity
	def fixHeight(self):
		if self.key == None:
			return
		self.height = max(self.left.height,self.right.height)+1

	#Rotating a vertex to the left, implementing the same algorithm as shown in the lecture.
	#O(1) - just playing with <= 4 pointers.
	def RotateLeft(self):
		A = self.right
		B = self
		B.right = A.left
		B.right.parent = B
		A.left = B
		A.parent = B.parent
		if A.parent != None:
			if A.parent.right.key == B.key:
				A.parent.right = A
			else:
				A.parent.left = A
		B.parent = A
		A.fixHeight()
		B.fixHeight()

	#Rotating a vertex to the right, implementing the same algorithm as shown in the lecture.
	#O(1) - just playing with <= 4 pointers.
	def RotateRight(self):
		A = self.left
		B = self
		B.left = A.right
		B.left.parent = B
		A.right = B
		A.parent = B.parent
		if A.parent != None:
			if A.parent.left.key == B.key:
				A.parent.left = A
			else:
				A.parent.right = A
		B.parent = A
		A.fixHeight()
		B.fixHeight()

"""
A class implementing the ADT Dictionary, using an AVL tree.
"""

class AVLTree(object):

	"""
	Constructor
	O(1)
	"""
	def __init__(self, head = AVLNode(None,None)):
		self.root = head
		self.sz = 0
		# add your fields here

	#Private method used for deletion.
	#O(h) as in worst case scenario we are descending all way down/up to a leaf/root, and as we are in AVL then O(h)=O(logn)
	def Successor(self, node):
		if self.root.get_left().get_key() == None and self.root.get_right().get_key() == None:
			return None
		if node.get_right().is_real_node():
			succ = node.get_right()
			while succ.get_left().is_real_node():
				succ = succ.get_left()
			return succ
		else:
			succ = node.get_parent()
			prev = node
			while succ.get_parent() != None and succ.get_right() == node:
				succ = succ.get_parent()
				prev = succ
			if succ.get_key() > node.get_key():
				return succ
		return None

	#Private method used to prevent creating 2 different searches, as the cilent seeks none when key isn't in the AVL
	#O(h) as we are descending all way down to a leaf, therefore O(logn)
	def searchCand(self,key,node = None): #Finds the sole candidate for position of key
		if node == None:
			node = self.root
		if node.get_key()==key:
			return node
		if node.get_key() > key:
			if node.get_left().is_real_node():
				return self.searchCand(key, node.get_left())
			else:
				node
		else:
			if node.get_right().is_real_node():
				return self.searchCand(key, node.get_right())
			else:
				return node
		return node

	"""searches for a AVLNode in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	O(logn) - a call to searchCand - O(logn), other actions are O(1).
	"""

	def search(self, key):
		if(self.root.get_key() == None):
			return None
		cand = self.searchCand(key)
		if cand.get_key() == key:
			return cand
		else:
			return None


	#Gets a node in tree and balancing the tree all the way up from it
	#Returning the number of needed rotations to balance.
	#Also updates heights

	#Time complexity - per insertionMode it's O(1) because we are rotating only once/twice, while for other cases it's O(h) = O(logn)
	#because in the worst case scenario we are bubbling all the way up to the root, executing max 2 rotations, each of O(1) complexity,
	#and due to the fact it's avl tree O(h) = O(logn)
	def balancing(self,node, insertionMode = False):
		runner = node  # As the name indicates it's running on all ancestors.
		result = runner.get_height()
		runner.fixHeight()
		result = 0 if result == runner.get_height() else 1
		runner = runner.get_parent()

		while runner != None:
			flag = runner.get_parent() == None
			last = runner.get_height()
			runner.fixHeight()

			if runner.get_height() != last:
				result += 1
			elif insertionMode: #Only needs 1/2 rotations for insertion, proven in lecture.
				break

			if runner.BF() == -2:
				if runner.right.BF() == 1:
					runner.get_right().RotateRight()
					result += 1
				runner.RotateLeft()
				if flag:
					self.root = self.root.get_parent()

			elif runner.BF() == 2:
				if runner.get_left().BF() == -1:
					runner.get_left().RotateLeft()
					result += 1
				runner.RotateRight()
				if flag:
					self.root = self.root.get_parent()
			runner = runner.get_parent()
		return result

	"""inserts val at position i in the dictionary
	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	O(logn) - O(logn) for the search, O(1) for the balancing, and O(1) for the rest. 
	"""
	def insert(self, key, val):
		#Edge case
		if self.root.get_key() == None:
			self.root = AVLNode(key, val)
			self.sz += 1
			return 0

		self.sz += 1
		par = self.searchCand(key)
		vertex = AVLNode(key,val)
		vertex.set_parent(par) # New edge (vertex,par) in the graph
		return self.balancing(par,True)


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	O(logn) - O(logn) for balancing, O(1) for the rest.
	"""
	def delete(self, node):
		self.sz -= 1
		runner = AVLNode(None,None)

		if node.get_right().is_real_node():
			succ = self.Successor(node)
			if node.get_right().get_key() == succ.get_key(): #Meaning right son has no left child\node.right=succ
				runner = succ
				if node.get_parent() != None:
					node.get_parent().set_child(succ)
				node.get_left().set_parent(succ,0)
			else:
				runner = succ.get_parent()
				succ.get_parent().set_left(succ.get_right())
				if node.get_parent() != None:
					node.get_parent().set_child(succ)
				else:
					succ.set_parent(None)
				succ.set_child(node.get_left(),0)
				succ.set_child(node.get_right(),1)

		else:
			if node.get_parent() != None:
				runner = node.get_parent()
				node.get_parent().set_child(node.get_left(),0 if node.get_key() == node.get_parent().get_left().get_key() else 1)
				# ^ simply removing the edge from node to its parent

		if node.get_key() == self.root.get_key():
			self.root = self.root.get_left().get_parent()

		result = self.balancing(runner.get_left())
		return result


	#Private method
	#Building sorted array from the tree, by implementing in-order search on the tree.
	#Time complexity: a quick observation is that we run on each edge twice - once for entering and once for leaving.
	#As we have N-1 edges for a tree of size N (known fact, discussed in Discreate Math) and the time spent per node is O(1)
	#Overall time complexity is O(n)

	def daq(self, node, lst):
		if node.get_key()==None:
			return
		self.daq(node.get_left(),lst)
		lst.append((node.get_key(),node.get_value()))
		self.daq(node.get_right(),lst)
		#result = []
		#if node.get_left().is_real_node():
		#	result += self.daq(node.get_left())
		#result += [(node.get_key(),node.get_value())]
		#if node.get_right().is_real_node():
		#	result += self.daq(node.get_right())
		#return result

	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

	def avl_to_array(self):
		result = []
		self.daq(self.root,result)
		return result


	"""returns the number of items in dictionary 

	@rtype: int
	@returns: the number of items in dictionary 
	"""
	def size(self):
		return self.sz

	
	"""splits the dictionary at the i'th index

	@type node: AVLNode
	@pre: node is in self
	@param node: The intended node in the dictionary according to whom we split
	@rtype: list
	@returns: a list [left, right], where left is an AVLTree representing the keys in the 
	dictionary smaller than node.key, right is an AVLTree representing the keys in the 
	dictionary larger than node.key.
	"""
	def split(self, node):
		if node == self.root:
			return AVLTree(node.get_left()),AVLNode(node.get_right())

		small = AVLTree(node.get_left())
		node.get_left().set_parent(None)
		big = AVLTree(node.get_right())
		node.get_right().set_parent(None)

		curr = node
		father = curr.get_parent()
		gfather = father.get_parent()

		#We are climbing the tree with 3 pointers, similar to reversing linked list as when we remove the edge between father to its
		#parent in order to join the trees correctly and prevent errors, we still need access to its parent, i.e. g(rand)father.

		while father != None:
			if father.get_right() == curr: #i.e. the root and the left subtree are smaller
				father.set_parent(None)
				father.get_left().set_parent(None)
				# due to the bst structure the current small tree is bigger then the subtree we joining, so we need to swap them momentary.
				T = AVLTree(father.get_left())
				T.join(small,father.get_key(),father.get_value())
				small = T
				father.set_left(AVLNode())

			else: #i.e. the root and the right subtree are bigger
				father.set_parent(None)
				father.get_right().set_parent(None)
				big.join(AVLTree(father.get_right()),father.get_key(),father.get_value())
				father.set_right(AVLNode())

			curr = father
			father = gfather
			if gfather != None:
				gfather = gfather.get_parent()

		return [small,big]

	"""joins self with key and another AVLTree

	@type tree2: AVLTree 
	@param tree2: a dictionary to be joined with self
	@type key: int 
	@param key: The key separting self with tree2
	@type val: any 
	@param val: The value attached to key
	@pre: all keys in self are smaller than key and all keys in tree2 are larger than key
	@rtype: int
	@returns: the absolute value of the difference between the height of the AVL trees joined
	"""

	def join(self, tree2, key, val):
		#We implementing the same algorithm as the one shown in class - join the shorter tree to the most similar in height subtree in the
		#other tree.

		result = abs(self.root.get_height()-tree2.root.get_height()) + 1
		#Edge cases
		if self.root.get_key() == None and tree2.root.get_key() == None: #i.e. both trees are empty
			self.insert(key,val)
			return 1
		if self.root.get_key() == None: #we are empty
			tree2.insert(key,val)
			self.root = tree2.root
			self.sz = tree2.sz
			return result
		if tree2.root.get_key() == None: #they are empty
			self.insert(key,val)
			return result

		#Regular cases
		self.sz += tree2.sz + 1
		merged = AVLNode(key, val)

		if self.get_root().get_height() == tree2.get_root().get_height():
			merged.set_left(self.get_root())
			merged.set_right(tree2.get_root())
			self.root = merged
		elif self.get_root().get_height() < tree2.get_root().get_height(): #We are being joined to them
			cand = tree2.root
			while cand.get_left().is_real_node() and cand.get_height() > self.root.get_height():
				cand = cand.get_left()
			merged.set_parent(cand.get_parent())
			merged.set_left(self.root)
			merged.set_right(cand)
			self.root = tree2.root
		else: #They are joined to us
			cand = self.root
			while cand.get_right().is_real_node() and cand.get_height() > tree2.root.get_height():
				cand = cand.get_right()
			merged.set_parent(cand.get_parent())
			merged.set_left(cand)
			merged.set_right(tree2.root)


		self.balancing(merged)
		return result




	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		if self.root.get_key() == None:
			return None
		return self.root
