class Character(object):
	def __init__(self, **data):
		super(Character, self).__init__
		self.data = data
		self.get = lambda *properties:tuple([self.data[name] if name in self.data else None for name in properties])
		self.set = lambda **properties:exec("for i in prop:sp.data[i] = prop[i]", {"prop" : properties,"sp" : sprite})
		self.skillStatus = dict()
	def __str__(self):
		return f'HP:{self.data["HP"]},MP:{self.data["MP"]}'
	def __lt__(self, other):
		self.skillStatus = self.data["skill"][other]
	def __gt__(self, other):
		if "OD" in self.skillStatus["flag"]:other.data["HP"] -= self.readText(other, "damage")
		if "SM" in self.skillStatus["flag"]:self.data["MP"] -= self.readText(self, "MP")
		if "SD" in self.skillStatus["flag"]:self.data["HP"] -= self.readText(self, "HP")
	def readText(self, target, value):
		totalValue = 0
		k = str(value)
		value = self.skillStatus[k].split("+")
		if k == "damage":k = "HP"
		for i in value:
			bonus = (eval(i[1:]) / 100) if i[1:].isdigit() else (self.data["ATK"] * eval(i[2:]) / 100) / 100
			if i[0] == "F":totalValue += bonus
			elif i[0] == "R":totalValue += target.data[k] * bonus
			elif i[0] == "M":totalValue += target.data["Max" + k] * bonus
			elif i[0] == "L":totalValue += (target.data["Max" + k] - target.data[k]) * bonus
			elif i[0] == "A":totalValue += self.data["ATK"] * bonus
		return round(totalValue)
# terms --> L:loss, F:fixed, R:remain, M:max
spriteName = ["MushroomMan", "FatRat"]
heroSkills = {}
for q in spriteName:
	heroSkills[q] = {}
	with open(f"{q}.hero") as file:
		for line in file.readlines():
			line = list(map(lambda i:tuple(i.split(":")), line.split(" ")))
			temp = {}
			for i in line[1:]:temp[i[0]] = i[1]
			heroSkills[q][line[0][1]] = temp
print(heroSkills)


sprite = Character(name = "Mushroom Man", HP = 100, MaxHP = 100, MP = 60, MaxMP = 60, ATK = 10, DEF = 2, AGI = 2, skill = heroSkills["MushroomMan"])
sprite2 = Character(name = "Fat Rat", HP = 200, MaxHP = 200, MP = 100, MaxMP = 100, ATK = 10, DEF = 2, AGI = 2, skill = heroSkills["FatRat"])

sprite < "spur"
sprite > sprite2
sprite2 < "scratch"
sprite2 > sprite

print(sprite2)
print(sprite)