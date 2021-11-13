from random import randint
sign = lambda x:1 if x > 0 else (0 if x == 0 else -1)
def greedy(element : list):
	maximum = 0; temp1 = 0;temp2 = 0
	for elem in element:
		if elem >= 0:
			temp2 += elem
			temp1 = int(temp2)
		else:
			temp2 += elem
			if temp2 <= 0:
				if maximum < temp1:
					maximum = float(temp1)
				temp1 = 0
				temp2 = 0
		if maximum < temp1:
			maximum = float(temp1)
	return maximum

x = [1, 2, 3, -7, 8, 6, 2, 5, -1, -2, -6, -8, 7]
print(greedy(x))