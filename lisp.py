class lisp:
	def parse(char):
		return char

	
	def tokenize(char):
		return char.replace('(', ' ( ').replace(')', ' ) ').strip()