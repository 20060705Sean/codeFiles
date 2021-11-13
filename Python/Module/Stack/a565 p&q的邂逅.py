from sys import stdin

def main():
	inLine = stdin.readline
	for t in range(int(inLine())):
		waitingLine = []
		waitingLine_pop = waitingLine.pop
		waitingLine_append = waitingLine.append
		situation = inLine()
		pairs = 0
		situation = situation.replace(".", "")
		for c in situation:
			if c == "p":
				waitingLine_append("p")
			elif c == "q" and waitingLine != []:
				waitingLine_pop()
				pairs += 1
		print(pairs)
main()