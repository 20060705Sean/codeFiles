methodExists = lambda instance, method:hasattr(instance, method)

class StoreSpace(object):
	def __init__(self):
		self.value = None
	def write(self, value):
		self.value = value
	def read(self):
		return self.value

class EzStack(object):
	def __init__(self, *args):
		super(EzStack, self).__init__()
		self.args = list(args)
		self.index = len(args)
	def push(self, arg):
		self.args[self.index] = arg
		self.index += 1
	def pop(slef):
		self.index -= 1
		return self.args[self.index]		

class Stack(object):
	def __init__(self, length):
		super(Stack, self)
		self.errorRaise = "raise"
		self.__storage = [StoreSpace() for i in range(length)]
		self.__index = 0
		self.length = length
	def __next__(self):
		self.__index -= 1
		return self.__storage[self.__index]
	def __iter__(self):
		while self.__index > 0:
			self.__index -= 1
			yield self.__storage[self.__index].read()
		self.clear()
	def __repr__(self):
		return f"-->{[obj.read() for obj in self.__storage]}-->"
	def clear(self):
		self.__storage = [StoreSpace() for i in range(self.length)]
	def push(self, value):
		if self.__index == self.length:
			if self.errorRaise == "raise":
				raise MemoryError("Stack Overflow")
			return "error"
		self.__storage[self.__index].write(value)
		self.__index += 1
	def pushIterable(self, value):
		if not methodExists(value, "__iter__"):
			if self.errorRaise == "raise":
				raise AttributeError(f"Object <{value}> has no method __iter__")
			return "error"
		if len(value) + self.__index > self.length:
			if self.errorRaise == "raise":
				raise MemoryError("Stack Overflow")
			return "error"
		for obj in value:
			self.push(obj)
	def pop(self):
		if self.__index == 0:
			if self.errorRaise == "raise":
				raise MemoryError("Stack Unextractable")
			return "error"
		object_now = self.__storage[self.__index].read()
		self.__index -= 1
		return object_now

def wordInverse(word):
	newword = ""
	reverseStack = Stack(len(word))
	reverseStack.pushIterable(word)
	for char in reverseStack:
		newword += char
	return word