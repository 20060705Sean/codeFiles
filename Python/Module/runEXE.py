'''from subprocess import Popen, PIPE, STDOUT
def run(fileName, inputString):
	p = Popen(f"{fileName}.exe", stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
	grep_stdout = p.communicate(input=inputString.encode())[0]
	return grep_stdout.decode()
'''
while True:
	try:
		input()
		x = list(sorted(map(int, input().split()), key = lambda x:x % 10))
	except EOFError:
		break
	result = []
	privious = [x[0] % 10, []]
	for i in x:
		if i % 10 == privious[0]:
			privious[1].append(i)
		else:
			result += reversed(sorted(privious[1]))
			privious[1] = [i]
			privious[0] = i % 10
	result += reversed(sorted(privious[1]))
	print(' '.join(result))