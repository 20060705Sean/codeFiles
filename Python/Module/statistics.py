from matrix import Matrix
prod = lambda data, i = 0:data[i] * prod(data, i + 1) if i < len(data) - 1 else data[i]
getSign = lambda x:1 if x >= 0 else -1
rounder = lambda data, place = 2:list(map(lambda x:round(x, place), data))
mean = lambda data:sum(data) / len(data)
median = lambda data:list(sorted(data))[int(l)] if (l := len(data) / 2) == l // 2 else mean(list(sorted(data))[int(l) - 1:int(l) + 1])
mode = lambda data:(count := {term : data.count(term) for term in set(data)}, key := list(count.keys()), value := list(count.values()), key[value.index(max(value))])[-1]
var = variance = lambda data, isSample = False:(isMultiple := {isinstance(term, list) for term in data} == {True}, (True if {(length := len(term)) == len(data[0]) for term in data} == {True} else exec("raise AttributeError('data amount not suited')"))if isMultiple else None, mu:=list(map(mean, data)) if isMultiple else mean(data), (sum([prod([lst[i] - mu[n] for n, lst in enumerate(data)]) for i in range(length)])/ (len(data[0]) - (0 if isSample else 1)) if isMultiple else sum([(term - mu) ** 2 for term in data]))/ (len(data) - (0 if isSample else 1)))[-1]
std = standardDeviation = lambda data:variance(data) ** 0.5
unaccuracy = lambda data:std(data) / (len(data) ** 0.5)
percentile = lambda data, percent:data[mean([data[a - 1], data[a]]) if int(a := len(data) * percent / 100) == a else int(a) + 1]
zpoint = lambda data:list(map(lambda x:(x - mean(data) / standardDeviation(data)), data))
lnrg = linearRegression = lambda data_independent, data_response:{"slope" : (slope := var(data_independent + [data_response]) / prod([var(i) for i in data_independent])), "intercept" : (intercept := mean(data_response) - slope * mean([mean(i) for i in data_independent])), "coefficents" : (intercept, slope), "SSE" : (SSE := sum([(i[1] - (slope * (i[0]) + intercept)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SSR" : (SSR := sum([((slope * (i[0]) + intercept) - mean(data_response)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : getSign(slope) * (R2 ** 0.5), "R-adjusted" : (SSR * (len(data_independent[0]) - 1)) / (SST * (len(data_independent[0]) - len(data_independent) - 1)), "predicter" : lambda x:sum([slope * x[i] for i in range(len(x))]) + intercept if not isinstance(x, (int, float)) else slope * x + intercept}
plrg = polynomialRegression = lambda data_independent, data_response, nTimes:{"X" : (X := Matrix([[i ** j for j in range(nTimes + 1)]for i in data_independent])), "y" : (y := Matrix([[i] for i in data_response])), "coefficents" : (coe := list(map(lambda x:x[0], (w := (X.T()*X).I() * X.T() * y).matrix))), "SSE" : (SSE := sum([(data_response[i] - sum([w.matrix[j][0] * x ** j for j in range(len(w.matrix))])) ** 2 for i, x in enumerate(data_independent)])), "SSR" : (SSR := sum([(mean(data_response) - sum([w.matrix[j][0] * x ** j for j in range(len(w.matrix))])) ** 2 for i, x in enumerate(data_independent)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : R2 ** 0.5, "R-adjusted" : (SSR * (len(data_independent) - 1)) / (SST * (len(data_independent) - 2)), "predicter" : lambda x:sum([c*(x** i) for i, c in enumerate(coe)])}
#mllnrg = multipleLinearRegression = lambda data_independent, data_response:{"means" : (means := [mean(i)for i in data_independent]), "numerator" : (nomen := lambda main_character:var(main_character, data_response) * (length := len(data_independent[0])) * prod([var(i) * length for i in data_independent.remove(main_character)]) -  * prod([var(data_independent[i], data_independent[i - 1]) for i in range(length + 1)])) , "denomenator" : (denom := prod([var(i) * length for i in data_independent]) - (var(data_independent) * length)** 2)}
if __name__ == "__main__":
	l, w = [64.5, 64.0, 65.1, 64.9], [46.0, 45.7, 45.0, 46.1]
	print(mean(l), mean(w))
	print(std(l), std(w))
	print(unaccuracy(l), unaccuracy(w))
	print((0.37**2*45.67**2 + 64.63**2*0.38**2) ** 0.5)
	'''import matplotlib.pyplot as plt
	dt = [list(range(-15, 16)), list(map(lambda x:(x-2)**2, list(range(-15, 16))))]
	x = list(sorted(dt[0]))
	y = list(sorted(dt[1]))
	a = plrg(x, y, 2)
	mymodel = list(map(a["predicter"], x))
	plt.scatter(x, y
)	plt.plot(x, mymodel)
	plt.show()'''