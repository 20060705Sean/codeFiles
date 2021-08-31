from subprocess import Popen, PIPE, STDOUT
def run(fileName, inputString):
	p = Popen(f"{fileName}.exe", stdout=PIPE, stdin=PIPE, stderr=STDOUT)    
	grep_stdout = p.communicate(input=inputString.encode())[0]
	return grep_stdout.decode()