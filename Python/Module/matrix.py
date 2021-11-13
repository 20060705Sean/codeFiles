createZeroMatrix = lambda r, c:[[0 for i in range(c)]for i in range(r)]
createIdentityMatrix = lambda n:[[int(i == j) for j in range(n)] for i in range(n)]
def DET_method(array):
	if (length :=len(array)) == 1 == len(array[0]):return array[0][0]
	elif length == 2 == len(array[0]):return array[0][0] * array[1][1] - array[1][0] * array[0][1]
	elif length == len(array[0]):
		while array[0][0] == 0:
			if (k := [[i[0] for i in array]]) == createZeroMatrix(1, len(k[0])):return 0
			array = array[1:] + array[:1]
		return DET_method([[DET_method([[array[0][0], array[0][j]], [array[i][0], array[i][j]]]) for j in range(1, length)]for i in range(1, length)]) / array[0][0]
	else:
		print("Not computable yet")



class Matrix(object):
	"""
	Matrix include functions and variable below:
		vars:
			.matrix : an array of elements    <list>
			.rows : the rows of the matrix    <int>
			.columns : the columns of the matrix    <int>
			.isSquareMatrix : bool value     <bool>
			.trace : the trace of the matrix    <number>
		funcs:
			.getRow(n) : get elements of n-th row    <list>
			.getColumn(n) : get elements of n-th column    <list>
			.getTransposedMatrix() : Get the transposed matrix   <Matrix>
			.T() : is equivalent to func getTransposedMatrix()
			.moveElement(pos1 ,pos2, action) : action could be "swap" or "replace"
			@static
			.getDirectProduct(a, b) : get the direct product of two elements
	"""
	def __init__(self, array2D):
		super(Matrix, self).__init__()
		self.matrix = array2D
		
		# Checking Vars
		self.rows = len(array2D)
		self.columns = len(array2D[0])
		self.isSquareMatrix = (self.rows == self.columns)
		self.isRowMatrix, self.isColumnMatrix = (self.rows == 1), (self.columns == 1)
		self.isZeroMatrix = False not in {False not in {arg == 0 for arg in row} for row in self.matrix}
		self.isIndentityMatrix = False not in {False not in {(arg == 1) if i == j else (arg == 0) for j, arg in enumerate(row)} for i, row in enumerate(self.matrix)}
		self.trace = sum([self.matrix[i][i] for i in range(self.rows)]) if self.isSquareMatrix else None

		# Functions with one line
		self.getPos = lambda i, j:self.matrix[i][j]
		self.getRow = lambda n:self.matrix[n]
		self.timesRow = lambda n, k: [i * k for i in self.matrix[n]]
		self.getColumn = lambda n:[i[n] for i in self.matrix]
		self.getRatio = lambda A, B:self.getPos(B[0], B[1]) / self.getPos(A[0], A[1])
	def rowPlus(self, n, v):self.matrix[n] = [self.matrix[n][i] + v[i] for i in range(len(self.matrix[n]))]
	def getInverseMatrix(self):
		if self.isSquareMatrix:
			if DET_method(self.matrix) != 0:
				matrixCopy = Matrix(list(self.matrix))
				inversedMatrix = Matrix(createIdentityMatrix(self.rows))
				def rewriteByRatio(row1, A, row2):
					ratio = -matrixCopy.getRatio(A, (row2, A[1]))
					matrixCopy.rowPlus(row2, matrixCopy.timesRow(row1, ratio))
					inversedMatrix.rowPlus(row2, inversedMatrix.timesRow(row1, ratio))
				for i in range(self.rows):
					if (k := matrixCopy.getPos(i, i)) != 1:
						matrixCopy.matrix[i] = list(map(lambda n:n / k, matrixCopy.matrix[i]))
						inversedMatrix.matrix[i] = list(map(lambda n:n / k, inversedMatrix.matrix[i]))
					for j in range(self.rows):
						if i != j:rewriteByRatio(i, (i, i), j)
				return inversedMatrix
			return None
	def I(self):return self.getInverseMatrix()
	def getTransposedMatrix(self):
		newArray = createZeroMatrix(self.columns, self.rows)
		for i in range(self.rows):
			for j in range(self.columns):
				newArray[j][i] = self.matrix[i][j]
		return Matrix(newArray)
	def T(self):return self.getTransposedMatrix()
	def moveElement(self, position1, position2, action):
		# Get two positions' element
		elements = (
			self.matrix[position1[0]][position1[1]], 
			self.matrix[position2[0]][position2[1]]
		)
		# Execute the action
		if action == "swap":
			self.matrix[position1[0]][position1[1]] = elements[1]
			self.matrix[position2[0]][position2[1]] = elements[0]
		elif action == "replace":
			self.matrix[position1[0]][position1[1]] = 0
			self.matrix[position2[0]][position2[1]] = elements[0]
		else:
			raise AttributeError("action not recognizable")
	@staticmethod
	def getDirectProduct(a, b):
		if len(a) == len(b):
			return sum([b[i] * a[i] for i in range(len(a))])
	def det(self, array):
		# useless : Laplas
		if (length := len(array)) == 2 == len(array[0]):
			return array[0][0] * array[1][1] - array[1][0] * array[0][1]
		elif length == len(array[0]):
			summary = 0
			for i, n in enumerate(array[0]):
				smallArray = [(l[:i] if i == (length - 1) else l[:i] + l[i + 1:])for l in array[1:]]
				summary += self.det(smallArray) * n * ((i % 2 - 0.5) / abs((i % 2 - 0.5)))
			return summary
		else:
			return "Not computable yet"
	def __str__(self):
		NEXT_LINE = "\n"
		return f"{NEXT_LINE.join(list(map(str, self.matrix)))}"
	def __mul__(self, other):
		if isinstance(other, (int, float)):
			matrix = [list(map(lambda j:other * j, i)) for i in self.matrix]
		elif type(self) == type(other):
			if self.columns != other.rows:
				return "matrix not multiable"
			newMatrix = [[
					self.getDirectProduct(self.getRow(i), other.getColumn(j))
					for j in range(other.columns)
				]
				for i in range(self.rows)
			]
			return Matrix(newMatrix)
	def __rmul__(self, other):return Matrix(self.matrix) * other
	def __imul__(self, other):return Matrix(self.matrix) * other
	def __add__(self, other):
		if type(self) != type(other):
			return "unaddable"
		if self.rows != other.rows or self.columns != other.columns:
			return "unaddable"
		return Matrix([[self.matrix[i][j] + other.matrix[i][j] for j in range(self.columns)]for i in range(self.rows)])
	def __radd__(self, other):return Matrix(self.matrix) + other
	def __abs__(self):DET_method(self.matrix)
	def __eq__(self, other):
		for m, n in zip(self.matrix, other.matrix):
			if m != n:
				return False
		return True