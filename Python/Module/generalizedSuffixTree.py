class Node(object):
	def __init__(self, arg):
		super(Node, self).__init__()
		self.arg = arg
		self.parent = None
		self.children = list()
		# command
		self.getPosition = lambda spliter = "", string = "":f"${string}" if self.arg == "master" else self.parent.getPosition(spliter, f"{self.arg}{spliter}{string}")
	def __gt__(self, other):
		self.children.append(other)
		other.parent = self
	def __str__(self):
		return f'"{self.arg}":{sorted(map(str, self.children))}'.replace("\\", "").replace("\'", "").replace("[", "{").replace("]", "}")
	def getChildrenArg(self):
		return [i.arg for i in self.children]
class GST_strict(object):
	def __init__(self, strings):
		super(GST_strict, self).__init__()
		if len(strings) > 10:raise AttributeError("too many strings to process")
		self.specials = "!@#$%^&_~`"
		self.stringAmount = len(strings)
		self.stringsProcess = [[word[i:] for i in range(len(word) - 1, -1, -1)] for word in strings]
		self.maxRecord = [0]
		self.masterNode = Node("master")
		for n, wordSet in enumerate(self.stringsProcess):
			for word in wordSet:
				nowNode = self.masterNode
				for i, char in enumerate(word + self.specials[n]):
					if not char in nowNode.getChildrenArg():nowNode > Node(char)
					nowNode = nowNode.children[nowNode.getChildrenArg().index(char)]
		self.getResult(self.masterNode, 0, set())
	def getResult(self, nowNode, layer, nowChars):
		oriChar = set(nowChars)
		if nowNode.getChildrenArg() != []:
			for i, nd in enumerate(nowNode.children):
				nowChars |= self.getResult(nd, layer + 1, set(oriChar))
		for i in self.specials:
			if i in nowNode.getChildrenArg():
				nowChars.add(str(i))
		if {self.specials[i] in nowChars for i in range(len(self.stringsProcess))} == {True}:
			if self.maxRecord[0] < layer:
				self.maxRecord.clear()
				self.maxRecord.append(int(layer))
				self.maxRecord.append(nowNode.getPosition()[1:])
			elif self.maxRecord[0] == layer:
				self.maxRecord.append(nowNode.getPosition()[1:])
		return nowChars
a = GST_strict(["abcdadd", "abcfdadd", "pldaddabc"])
print(a.maxRecord)

'''
a1b2c3d4e
zz1yy2xx3ww4vv
abcdgh
aedfhr
abcdefghijklmnopqrstuvwxyz
a0b0c0d0e0f0g0h0i0j0k0l0m0n0o0p0q0r0s0t0u0v0w0x0y0z0
abcdefghijklmnzyxwvutsrqpo
opqrstuvwxyzabcdefghijklmn'''