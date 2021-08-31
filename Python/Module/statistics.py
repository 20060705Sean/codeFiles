from matrix import Matrix
prod = lambda data, i = 0:data[i] * prod(data, i + 1) if i < len(data) - 1 else data[i]
getSign = lambda x:1 if x >= 0 else -1
rounder = lambda data, place = 2:list(map(lambda x:round(x, place), data))
mean = lambda data:sum(data) / len(data)
median = lambda data:list(sorted(data))[int(l)] if (l := len(data) / 2) == l // 2 else mean(list(sorted(data))[int(l) - 1:int(l) + 1])
mode = lambda data:(count := {term : data.count(term) for term in set(data)}, key := list(count.keys()), value := list(count.values()), key[value.index(max(value))])[-1]
var = variance = lambda data, isSample = False:(isMultiple := {isinstance(term, list) for term in data} == {True}, (True if {(length := len(term)) == len(data[0]) for term in data} == {True} else exec("raise AttributeError('data amount not suited')"))if isMultiple else None, mu:=list(map(mean, data)) if isMultiple else mean(data), (sum([prod([lst[i] - mu[n] for n, lst in enumerate(data)]) for i in range(length)])/ (len(data[0]) - (0 if isSample else 1)) if isMultiple else sum([(term - mu) ** 2 for term in data]))/ (len(data) - (0 if isSample else 1)))[-1]
std = standardDeviation = lambda data:variance(data) ** 0.5
percentile = lambda data, percent:data[mean([data[a - 1], data[a]]) if int(a := len(data) * percent / 100) == a else int(a) + 1]
zpoint = lambda data:list(map(lambda x:(x - mean(data) / standardDeviation(data)), data))
lnrg = linearRegression = lambda data_independent, data_response:{"slope" : (slope := var(data_independent + [data_response]) / prod([var(i) for i in data_independent])), "intercept" : (intercept := mean(data_response) - slope * mean([mean(i) for i in data_independent])), "coefficents" : (intercept, slope), "SSE" : (SSE := sum([(i[1] - (slope * (i[0]) + intercept)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SSR" : (SSR := sum([((slope * (i[0]) + intercept) - mean(data_response)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : getSign(slope) * (R2 ** 0.5), "R-adjusted" : (SSR * (len(data_independent[0]) - 1)) / (SST * (len(data_independent[0]) - len(data_independent) - 1)), "predicter" : lambda x:sum([slope * x[i] for i in range(len(x))]) + intercept if not isinstance(x, (int, float)) else slope * x + intercept}
plrg = polynomialRegression = lambda data_independent, data_response, nTimes:{"X" : (X := Matrix([[i ** j for j in range(nTimes + 1)]for i in data_independent])), "y" : (y := Matrix([[i] for i in data_response])), "coefficents" : (coe := list(map(lambda x:x[0], (w := (X.T()*X).I() * X.T() * y).matrix))), "SSE" : (SSE := sum([(data_response[i] - sum([w.matrix[j][0] * x ** j for j in range(len(w.matrix))])) ** 2 for i, x in enumerate(data_independent)])), "SSR" : (SSR := sum([(mean(data_response) - sum([w.matrix[j][0] * x ** j for j in range(len(w.matrix))])) ** 2 for i, x in enumerate(data_independent)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : R2 ** 0.5, "R-adjusted" : (SSR * (len(data_independent) - 1)) / (SST * (len(data_independent) - 2)), "predicter" : lambda x:sum([c*(x** i) for i, c in enumerate(coe)])}
#mllnrg = multipleLinearRegression = lambda data_independent, data_response:{"means" : (means := [mean(i)for i in data_independent]), "numerator" : (nomen := lambda main_character:var(main_character, data_response) * (length := len(data_independent[0])) * prod([var(i) * length for i in data_independent.remove(main_character)]) -  * prod([var(data_independent[i], data_independent[i - 1]) for i in range(length + 1)])) , "denomenator" : (denom := prod([var(i) * length for i in data_independent]) - (var(data_independent) * length)** 2)}
if __name__ == "__main__":
	import matplotlib.pyplot as plt
	dt = [[[1, 2, 3, 4, 5, 6], [3, 5, 7, 9, 11, 13]], [4, 7, 10, 13, 16, 19]]
	x = dt[0]
	y = dt[1]
	a = lnrg(x, y)
	print(a)
	zippe = lambda u:[[j[i] for j in u] for i in range(len(u[0]))]
	print(zippe(x))
	mymodel = list(map(a["predicter"], zippe(x)))
	plt.scatter([i[0]+ i[1] for i in zippe(x)], y)
	plt.plot([i[0]+ i[1] for i in zippe(x)], mymodel)
	plt.show()
	"""
	[[2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99], [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.9973, 0.0, 0.0, 1.0073, 0.988, 0.0, 0.9968, 0.9975, 0.9973, 0.9971, 0.9973, 0.9975, 1.9946, 1.9946, 2.9933, 4.9868, 5.9841, 3.9878, 3.999, 3.9797, 4.9868, 4.9865, 5.9841, 5.9841, 5.985, 7.0243, 13.9201, 9.9719, 9.9735, 18.9497, 10.9704, 19.9926, 11.9665, 15.9135, 14.9965, 14.9658, 18.9507, 17.3237, 19.948, 19.9463, 21.8978, 23.3397, 23.9372, 25.9295, 28.9681, 31.0991, 38.9278, 31.9271, 34.3783, 35.8987, 37.8973, 39.3252, 43.8678, 45.1887, 48.8818, 54.2591, 50.8652, 54.198, 56.8309, 60.2527, 61.8412, 69.8073, 77.7938, 84.7716, 74.2133, 75.7732, 76.2959, 94.9676, 94.6934, 91.7563, 100.2765, 100.7392, 102.7248, 103.7459, 108.6864, 114.6853, 119.6992, 123.6162, 139.2744, 130.6398, 135.6585, 141.0124, 145.6621, 158.5433, 169.518, 172.5731, 171.536, 184.5386, 205.4043, 232.7163, 201.3359, 214.5]] [[2, 3, 4, 5, 6, 7, 8, 9], [0.0, 0.0, 0.0, 1.0002, 0.0, 5.0042, 39.9024, 365.962]]
	"""