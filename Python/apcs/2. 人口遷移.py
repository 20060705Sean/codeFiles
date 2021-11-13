from copy import deepcopy
class Matrix(object):
	def __init__(self, array2D, k):
		super(Matrix, self).__init__()
		self.matrix = array2D
		self.matrix_copy = deepcopy(self.matrix)
		self.rows = len(array2D)
		self.columns = len(array2D[0])
		self.k = k
	def __str__(self):
		BACKSLASHN = '\n'
		maxima = 0
		minima = 10000000000
		for i in self.matrix:
			for val in i:
				if val > maxima:
					maxima = int(val)
				elif val < minima and val != -1:
					minima = int(val)
		return f"{minima}{BACKSLASHN}{maxima}"
	def getAdjacentBlockData(self, n, m):
		temp = int(self.matrix[n][m] / k); flag = 0
		for i in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			if 0 <= n + i[0] < self.rows and 0 <= m + i[1] < self.columns:
				if self.matrix[n + i[0]][m + i[1]] != -1:
					self.matrix_copy[n + i[0]][m + i[1]] += temp; flag += 1
		self.matrix_copy[n][m] -= temp * flag	

	def update(self):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.matrix[i][j] != -1:
					self.getAdjacentBlockData(i, j)
		self.matrix = deepcopy(self.matrix_copy)
r, c, k, m = list(map(int, input().split()))
u3er_1nput = [list(map(int, input().split())) for i in range(r)]
entity = Matrix(u3er_1nput, k)
for i in range(m):
	entity.update()	
print(entity)