#username - complete info
#id1      - complete info 
#name1    - complete info 
#id2      - complete info
#name2    - complete info  



"""A class represnting a node in an AVL tree"""

class AVLNode(object):
	"""Constructor, you are allowed to add more fields. 

	@type key: int or None
	@type value: any
	@param value: data of your node
	"""
	def __init__(self, key, value):
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
	"""
	def get_left(self):
		return self.left



	"""returns the right child

	@rtype: AVLNode
	@returns: the right child of self, None if there is no right child (if self is virtual)
	"""
	def get_right(self):
		return self.right


	"""returns the parent 

	@rtype: AVLNode
	@returns: the parent of self, None if there is no parent
	"""
	def get_parent(self):
		return self.parent


	"""returns the key

	@rtype: int or None
	@returns: the key of self, None if the node is virtual
	"""
	def get_key(self):
		return self.key


	"""returns the value

	@rtype: any
	@returns: the value of self, None if the node is virtual
	"""
	def get_value(self):
		return self.value


	"""returns the height

	@rtype: int
	@returns: the height of self, -1 if the node is virtual
	"""
	def get_height(self):
		return self.height


	"""sets left child

	@type node: AVLNode
	@param node: a node
	"""
	def set_left(self, node):
		self.left = node
		self.height = max(self.height,self.left.height+1)
		node.parent = self


	"""sets right child

	@type node: AVLNode
	@param node: a node
	"""
	def set_right(self, node):
		self.right = node
		node.parent = self
		self.height = max(self.height,self.right.height+1)


	def set_child(self, node):
		if self.key > node.key:
			self.set_left(node)
		else:
			self.set_right(node)

	"""sets parent

	@type node: AVLNode
	@param node: a node
	"""
	def set_parent(self, node):
		self.parent = node
		node.set_child(self)


	"""sets key

	@type key: int or None
	@param key: key
	"""
	def set_key(self, key):
		self.key = key


	"""sets value

	@type value: any
	@param value: data
	"""
	def set_value(self, value):
		self.value = value


	"""sets the height of the node

	@type h: int
	@param h: the height
	"""

	def BF(self):
		if not self.is_real_node():
			return 0
		return self.left.height - self.right.height

	"""returns whether self is not a virtual node 

	@rtype: bool
	@returns: False if self is a virtual node, True otherwise.
	"""
	def is_real_node(self):
		if self.value == None:
			return False
		return True

	def fixHeight(self):
		self.height = max(self.left.height,self.right.height)+1

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
	Constructor, you are allowed to add more fields.

	"""
	def __init__(self, head = AVLNode(None,None)):
		self.root = head
		self.sz = 0
		# add your fields here

	def Successor(self, node):
		if self.sz == 1:
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

	"""searches for a AVLNode in the dictionary corresponding to the key

	@type key: int
	@param key: a key to be searched
	@rtype: AVLNode
	@returns: the AVLNode corresponding to key or None if key is not found.
	"""

	def searchCand(self,key,node = None): #Finds the sole candidate for position of key
		if node == None:
			node = self.root
		if node.get_key()==key:
			return node
		if node.get_left().is_real_node() and node.get_key() > key:
			return self.searchCand(key,node.get_left())
		elif node.get_right().is_real_node():
			return self.searchCand(key,node.get_right())
		return node

	def search(self, key):
		if(self.sz == 0):
			return None
		cand = self.searchCand(key)
		if cand.get_key() == key:
			return cand
		else:
			return None


	"""inserts val at position i in the dictionary

	@type key: int
	@pre: key currently does not appear in the dictionary
	@param key: key of item that is to be inserted to self
	@type val: any
	@param val: the value of the item
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def insert(self, key, val):
		if self.sz == 0:
			self.root = AVLNode(key, val)
			self.sz += 1
			return 0
		self.sz += 1
		par = self.searchCand(key)
		vertex = AVLNode(key,val)
		vertex.set_parent(par) # New edge (vertex,par) in the graph

		runner = par # As the name indicates, running on all ancestors.
		runner = runner.get_parent()
		result = 0
		while runner != None:
			flag = runner.get_parent() == None
			last = runner.get_height()
			runner.fixHeight()
			if runner.get_height() == last:
				break

			if runner.BF() == -2:
				if runner.right.BF() == 1:
					runner.get_right().RotateRight()
					result += 1
				runner.RotateLeft()
				if flag:
					self.root = self.root.get_parent()
				result += 1

			elif runner.BF() == 2:
				if runner.right.BF() == -1:
					runner.get_left().RotateLeft()
					result += 1
				runner.RotateRight()
				if flag:
					self.root = self.root.get_parent()
				result += 1
			runner = runner.get_parent()
		return result


	"""deletes node from the dictionary

	@type node: AVLNode
	@pre: node is a real pointer to a node in self
	@rtype: int
	@returns: the number of rebalancing operation due to AVL rebalancing
	"""
	def delete(self, node):
		sz -= 1
		return -1


	"""returns an array representing dictionary 

	@rtype: list
	@returns: a sorted list according to key of touples (key, value) representing the data structure
	"""

	def daq(self, node): # Divide and conquer strat
		return daq(self,node.get_left()) + [self.root] + daq(self,node.get_right())

	def avl_to_array(self):
		return daq(self,self.root)


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
		return None

	
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
		return None


	"""returns the root of the tree representing the dictionary

	@rtype: AVLNode
	@returns: the root, None if the dictionary is empty
	"""
	def get_root(self):
		return self.root