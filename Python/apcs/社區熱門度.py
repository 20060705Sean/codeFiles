from copy import deepcopy
class Matrix(object):
	def __init__(self, array2D):
		super(Matrix, self).__init__()
		self.matrix = array2D
		self.matrix_copy = deepcopy(self.matrix)

		self.rows = len(array2D)
		self.columns = len(array2D[0])

	def __str__(self):
		BACKSLASHN = '\n'
		return f"{BACKSLASHN.join(map(lambda i:' '.join(list(map(str, i))), self.matrix_copy))}"

	def getAdjacentBlockData(self, n, m):
		flag = 0; summary = 0; temp = 0
		for i in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
			if 0 <= n + i[0] < self.rows and 0 <= m + i[1] < self.columns:
				temp = self.matrix[n + i[0]][m + i[1]]
				if temp == 0:continue
				flag += 1;summary += temp
		return 0 if flag == 0 else int(summary / flag)

	def update(self):
		for i in range(self.rows):
			for j in range(self.columns):
				if self.matrix[i][j] == 0:
					self.matrix_copy[i][j] = self.getAdjacentBlockData(i, j)

r, c = list(map(int, input().split()))
u3er_1nput = [list(map(int, input().split())) for i in range(r)]
entity = Matrix(u3er_1nput)
entity.update()
print(entity)