try:
	while True:
		x, y = tuple(map(int, input().split()))
		if x == y:
			print(x)
		else:
			print(y+1)
except:
	pass