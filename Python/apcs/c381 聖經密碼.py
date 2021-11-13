from time import sleep
while True:
	n, m = list(map(int, input().split()))
	if n == 0 and m == 0:
		break
	words = ''.join([input() for i in range(n)])
	print(''.join([words[i - 1] for i in list(map(int, input().split()))]))