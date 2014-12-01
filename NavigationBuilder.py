from DepthFirstTreeAnalyser import *

class NavigationBuilder:
	pages = []
	#number of [open, close] brackets
	last_bracket_type = [0, 0] 
	#holds the count of the number of quotes that are encountered
	quote_count = 2
	#holds the final navigation string
	final = str()
	#holds the name of the page and user friendly url derived from the name of the string
	href = [str(),str()]
	#object of the DepthFirstTreeAnalyser class
	page = None

	def __init__(self, file_name = 'pages.csv', file_url = ''):
		self.page = DepthFirstTreeAnalyser(file_name, file_url)
		self.pages = self.page.get_results()
		self.analyse_pages()


	def analyse_pages(self):
		"""loops through the arranged array of pages and calls the function responsible for building the navigation """
		#converts the pages array to string and removes all the commas ',' from the raw data string created
		navigation = str(self.pages).translate(None,',')
		for count in range(len(navigation)):
			self.build_navigation(navigation[count])
		
	def indent(self):	
		"""calculates the indentation that is required in the navigation string for structuring within the <nav></nav> tags"""
		indent = '\t'
		for i in range(self.last_bracket_type[0]-self.last_bracket_type[1]):
			indent += "\t"
		return indent


	def get_navigation(self):
		"""returns the final navigation string"""
		return '<nav>\n'+self.final+'</nav>'


	def build_navigation(self, popped = ''):
		indent = self.indent()
		if popped == '[':
			self.last_bracket_type[0] += 1
			if (self.last_bracket_type[0]-self.last_bracket_type[1])%2 == 0 :
				self.final += indent + '<li id = "page-'
			elif (self.last_bracket_type[0]-self.last_bracket_type[1])%2 == 1:
				self.final += indent + '<ul>\n'

		elif popped == ']':
			self.last_bracket_type[1] += 1
			indent = self.indent()
			if (self.last_bracket_type[0]-self.last_bracket_type[1])%2 == 0:
				self.final += indent + '</ul>\n'
			elif (self.last_bracket_type[0]-self.last_bracket_type[1])%2 == 1:
				self.final += indent + '</li>\n'

		elif popped == '\'':
			self.quote_count += 1		
			if self.quote_count%2 == 0:
				self.final += '">\n' + indent + '<a href="' + self.href[0] + '">' + self.href[1] + '</a>\n'
				self.href = [str(), str()]
		
		else:
			try:
				integers = [0,1,2,3,4,5,6,7,8,9]
				if integers.index(int(popped)) >= 0:
					self.final += popped
			except ValueError:
				if self.quote_count%2 != 0:
					self.href[1] += popped
					if popped != ' ':
						self.href[0] += popped
					else:
						self.href[0] += '-'  
					

			

nav = NavigationBuilder()
print nav.get_navigation()