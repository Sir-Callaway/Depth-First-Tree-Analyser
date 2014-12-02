import csv
from operator import itemgetter

class DepthFirstTreeAnalyser:
	"""A class that analyses a CSV file containing raw unorganized data containing the header/
	first row as (id, heading, parent, level, position, status) in any order and forms a tree data structure
	using lists:

		id - the row/data item's identifier

		header - the name or description of the data

		parent - the identifier of the data item in the same CSV which is the parent of this rows data item

		level - depth of this data item in the tree

		position - position of this data item amongst the other data items of same parent and level

		status - determines whether this data item is to be considered (1) or not (0) 

	NOTE: the tree structure formed will be in order of positions in the different levels 
		(multileveled list formed at the end will have length [len(self.data)] equal to number of active items
		which have level equal to 0 - root level)"""

	#stores the raw data from the source
	raw_data = []
	#stores the raw data from the source and gets refined to become the final data of the class; the Navigation in order
	data = []
	#stores the highest level of the data]
	level_loops = 0

	def __init__(self, file_name = 'pages.csv', file_dir_url = ''):
		"""retrives and reads - into the data list of the class - the CSV file into a List"""
		with open(file_dir_url+file_name, 'rb') as csvfile:
			record_reader = csv.reader(csvfile, delimiter=',')
			record_count = 0

			for row in record_reader:
				if record_count == 0:
					self.data.append(row)
				else:
					row[self.get_header_index('id')] = int(row[self.get_header_index('id')])
					row[self.get_header_index('parent')] = int(row[self.get_header_index('parent')])
					row[self.get_header_index('position')] = int(row[self.get_header_index('position')])
					row[self.get_header_index('level')] = int(row[self.get_header_index('level')])
					row[self.get_header_index('status')] = int(row[self.get_header_index('status')])
					self.data.append(row)
				record_count += 1

		results = self.get_active_data_items()
		self.level_loops = int(results[0])
		self.raw_data = results[1]
		self.set_data(results[1])
		self.arrange_data()


	def get_active_data_items(self):
		"""retrives only the data items that are active and
		 counts the number of levels that the tree has"""

		status = self.get_header_index('status')
		level = self.get_header_index('level')
		level_count = 0
		temp = []

		for page in self.data:
			if page[status] == 'status': 
				page.append('children')
				temp.append(page)
			if page[status] == 1:
				page.append(None)
				temp.append(page)
				if page[level] > level_count:
					level_count = page[level]
		temp[1:] = sorted(temp[1:], key = itemgetter(self.get_header_index('level')), reverse = True)
		
		return [level_count, temp]


	def set_data(self, dat = []):
		"""sets the class level variable data to dat list that has been passed"""
		self.data = dat


	def get_results(self):
		"""returns the final analysed data of the class in it's arrange form """
		return self.data


	def get_header_index(self, index = 'id'):
		"""checks for header title and returns the index number"""
		return self.data[0].index(index)


	def arrange_data(self):
		"""Arranges the Items in the data list of the class in order of level >> parent"""		
		#stores the class level data variable without the headers row; the final data product for this function
		temp = self.get_results()[1:]
		
		#creates a dummy slot in the temp list for level [0] analysis
		dummy_data = [-1,-1,-1,-1,-1,-1,-1]
		dummy_data[self.get_header_index('id')] = 0
		temp.append(dummy_data)
		
		#loops through the levels of the data list from the highest recorded to the lowest which is 0
		while self.level_loops >= 0:
			item_counter = int(len(self.data))
			
			#loops through the items of the temp list which is the class' data list without the headers
			while item_counter>0:
				#holds full list of a parent and child items at the current level beign analysed
				temp = self.get_single_item_pack(temp, item_counter)
				item_counter = item_counter - 1
			while item_counter==0:
				temp = self.get_single_item_pack(temp, item_counter)
				item_counter = item_counter - 1

			self.level_loops = self.level_loops - 1

		#sets the final analyzed list of data items in a tree structure an organized in positions of level 0
		temp = temp[0][self.get_header_index('children')]
		self.set_data(temp)


	def get_single_item_pack(self, dat, parent = 0):
		"""arrages dat list finding list items which are children to the item whose identifier is equal to parent,
		merged the children list to the parent item in the column created called Children, and removes the children
		data item entirely from the final product of this analysis; returns the final data list of this analysis"""
		parent_index = self.get_header_index('parent')
		id_index = self.get_header_index('id')
		level_index = self.get_header_index('level')

		parent_data = []
		children_data = []

		for row in dat:			
			#checks for the parent data and returns the data of the row if its id = parent
			if row[id_index] == parent:
				parent_data = row

			#checks whether the level of the parent is the same level that the class is analysing
			try:
				if row[level_index] == self.level_loops:
					#checks and gives a list of the children for the parent
					if row[parent_index] == parent:
						children_data.append(row)	

			except IndexError:
				continue


		#returns a list with [0] as the parent item's data and [1] as the children of the parent if children_data has items
		if children_data != []:
			children_data = sorted(children_data, key=itemgetter(self.get_header_index('position')))
			for child in children_data:
				#pops out the data in dat corresponding to the children
				dat.remove(child)
				#pops out the data corresponding to level, position, status, and parent for the children
				index_of_child = children_data.index(child)
				child_children = children_data[index_of_child][self.get_header_index('children')]
				child_heading = children_data[index_of_child][self.get_header_index('heading')]
				child_id = children_data[index_of_child][self.get_header_index('id')]
				if child_children == None:
					children_data[index_of_child] = [child_id, child_heading]
				else:
					children_data[index_of_child] = [child_id, child_heading, child_children]
				
			#replaces the parent item's children in the final_data list with replacement of children
			dat[dat.index(parent_data)][self.get_header_index('children')] = children_data


		return dat
