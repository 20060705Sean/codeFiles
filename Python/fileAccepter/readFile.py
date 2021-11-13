from os import listdir
from time import time
from os.path import isfile, join
onlyfiles = [f for f in listdir("Assets/") if isfile(join("Assets/", f))]



q = 0
for i in onlyfiles:
	tempSaver = []
	q += 1
	timer = time()
	with open(f"Assets/{i}") as file:
		for L in file.readlines():
			tempSaver.append(L)
	print(f"file {q} read finished:{time() - timer}")
	timer = time()
	with open(f"finished/{i}", "w") as file:
		file.write("".join(tempSaver))
	print(f"file {q} write finished:{time() - timer}")