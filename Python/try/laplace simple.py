import matplotlib.pyplot as plt
from matplotlib.font_manager import *
from math import log, e

resolution = 250 #(m)

myfont = FontProperties(fname='msjh.ttc')
plt.rcParams['axes.unicode_minus']=False

P_sea = 1013.25 #hpa
a = 1 / 273

calculate_height = lambda p, t:log(P_sea / p, 10) * 18400 * (1 + a * (t + 20) / 2)
lnrg = linearRegression = lambda data_independent, data_response:{"slope" : (slope := var(data_independent + [data_response]) / prod([var(i) for i in data_independent])), "intercept" : (intercept := mean(data_response) - slope * mean([mean(i) for i in data_independent])), "coefficents" : (intercept, slope), "SSE" : (SSE := sum([(i[1] - (slope * (i[0]) + intercept)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SSR" : (SSR := sum([((slope * (i[0]) + intercept) - mean(data_response)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : getSign(slope) * (R2 ** 0.5), "R-adjusted" : (SSR * (len(data_independent[0]) - 1)) / (SST * (len(data_independent[0]) - len(data_independent) - 1)), "predicter" : lambda x:sum([slope * x[i] for i in range(len(x))]) + intercept if not isinstance(x, (int, float)) else slope * x + intercept}
var = variance = lambda data, isSample = False:(isMultiple := {isinstance(term, list) for term in data} == {True}, (True if {(length := len(term)) == len(data[0]) for term in data} == {True} else exec("raise AttributeError('data amount not suited')"))if isMultiple else None, mu:=list(map(mean, data)) if isMultiple else mean(data), (sum([prod([lst[i] - mu[n] for n, lst in enumerate(data)]) for i in range(length)])/ (len(data[0]) - (0 if isSample else 1)) if isMultiple else sum([(term - mu) ** 2 for term in data]))/ (len(data) - (0 if isSample else 1)))[-1]
mean = lambda data:sum(data) / len(data)
prod = lambda data, i = 0:data[i] * prod(data, i + 1) if i < len(data) - 1 else data[i]
getSign = lambda x:1 if x >= 0 else -1
data = {"06":[], "12":[]}
for month in ("06", "12"):
	with open(f"2020{month}_upair.txt") as file:
		i = 1
		date = -1
		previous_temperature = -273
		for line in file.readlines():
			if i <= 13:
				i += 1
				continue
			i += 1
			line = line.replace("  ", " ").replace("   ", " ").replace("   ", " ")
			line = list(map(lambda x:float(x), line.split()))
			pressure, temperature = line[3], line[5]
			height = calculate_height(pressure, temperature)
			if abs(previous_temperature - temperature) < 15:
				data[month][date].append((height, temperature))
			else:
				date += 1
				data[month].append([(height, temperature)])
			previous_temperature = float(temperature)
def linear_interpolation(lst):
	result = []
	height = 0
	for i in range(1, len(lst) - 1):
		prev = lst[i - 1]
		now = lst[i]
		nxt = lst[i + 1]
		if not(prev[1] == now[1] == nxt[1]):
			f = lnrg([[prev[0], now[0], nxt[0]]], [prev[1], now[1], nxt[1]])["predicter"]
		else:
			f = lambda x:prev[1]
		while prev[0] - 100 < height < nxt[0] + 100:
			result.append((height, f(height)))
			height += resolution
	return result
data = {i:list(map(linear_interpolation, data[i])) for i in data}
for m in ["06", "12"]:
	i = 0
	h = 0
	result_h = []
	result_t = []
	for q in range(data[m].count([])):
		data[m].remove([])
	k = list(map(len, data[m]))
	maximum = max(k)
	while i < maximum - 1:
		added = 0
		count = 0
		for j, obj in enumerate(data[m]):
			if k[j] > i:
				h = obj[i][0]
				count += 1
				added += obj[i][1]
		i += 1
		added /= count
		h /= 1000
		result_h.append(h)
		result_t.append(added)
		plt.scatter(added, h, color = ("red" if m == "06" else "blue"), s = 4)
	plt.plot(result_t, result_h, label = "June" if m == "06" else "December", color = ("red" if m == "06" else "blue"))
plt.title(f'對流層、平流層高度－氣溫圖(線性內插{resolution}公尺)', size = 16, fontproperties=myfont)
plt.legend(loc='upper right')
plt.xlabel('溫度(°C)',fontproperties=myfont, size = 13)
plt.ylabel('高度(km)',fontproperties=myfont, size = 13)
plt.xticks(range(-80, 40, 10))
plt.grid(True,linestyle = "--",color = 'gray' ,linewidth = '0.5',axis='both')
plt.show()