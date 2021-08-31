line = []
with open("EnglishWords.txt", encoding='UTF-8') as file:
	line = file.read().split("     ")
word = []
for data in line:
	data = data.split('  ')
	temp = data[0].split('=') if '=' in data[0] else None
	if isinstance(temp, list):
		for w in temp:
			data.append((w, data[1]))
	else:
		word.append((data[0], data[1]))
print(word)
with open("EnglishWords.csv", "w", encoding="UTF-8") as file:
	flag = 0
	NEXTLINE="\n"
	for i in word:
		if flag < 14:
			file.write(f'{i[0]},{i[1]},')
			flag += 1
		else:
			file.write(f'{i[0]},{i[1]}{NEXTLINE}')
			flag = 0