import matplotlib.pyplot as plt


lnrg = linearRegression = lambda data_independent, data_response:{"slope" : (slope := var(data_independent + [data_response]) / prod([var(i) for i in data_independent])), "intercept" : (intercept := mean(data_response) - slope * mean([mean(i) for i in data_independent])), "coefficents" : (intercept, slope), "SSE" : (SSE := sum([(i[1] - (slope * (i[0]) + intercept)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SSR" : (SSR := sum([((slope * (i[0]) + intercept) - mean(data_response)) ** 2 for i in zip([sum([j[i] for j in data_independent]) for i in range(len(data_independent[0]))], data_response)])), "SST" : (SST := SSE + SSR), "R-square" : (R2 := SSR/SST), "R" : getSign(slope) * (R2 ** 0.5), "R-adjusted" : (SSR * (len(data_independent[0]) - 1)) / (SST * (len(data_independent[0]) - len(data_independent) - 1)), "predicter" : lambda x:sum([slope * x[i] for i in range(len(x))]) + intercept if not isinstance(x, (int, float)) else slope * x + intercept}
var = variance = lambda data, isSample = False:(isMultiple := {isinstance(term, list) for term in data} == {True}, (True if {(length := len(term)) == len(data[0]) for term in data} == {True} else exec("raise AttributeError('data amount not suited')"))if isMultiple else None, mu:=list(map(mean, data)) if isMultiple else mean(data), (sum([prod([lst[i] - mu[n] for n, lst in enumerate(data)]) for i in range(length)])/ (len(data[0]) - (0 if isSample else 1)) if isMultiple else sum([(term - mu) ** 2 for term in data]))/ (len(data) - (0 if isSample else 1)))[-1]
mean = lambda data:sum(data) / len(data)
prod = lambda data, i = 0:data[i] * prod(data, i + 1) if i < len(data) - 1 else data[i]
getSign = lambda x:1 if x >= 0 else -1



data_points = [ 
	#[6.85, 6.25, 5.6, 4.9, 4.25, 3.6], 
	#[7.5, 6.75, 6.05, 5.25, 4.5, 3.9], 
	#[12.95, 10.3, 8.95, 7.35, 5.7, 4.35],
	#[15.95, 14.95, 13.1, 11.15, 9.3, 5.85], 
	#[5.4, 4.95, 4.5, 4, 3.6, 3.1], 
	[9.5, 8.7, 7.85, 7.1, 6.25, 5.45], 
	[9, 8.25, 7.5, 6.75, 6, 5.25], 
	[8.65, 7.85, 7.15, 6.35, 5.7, 4.9], 
	[10.12, 9.3, 8.45, 7.55, 6.5, 5.7]
]
derivate = lambda x:round(x*12, 1)
data_points = [list(map(derivate, d)) for d in data_points]
data_points = [list(reversed([round(q[i] - q[i+1], 3) for i in range(len(q) - 1)])) for q in data_points]
data_points = [list(map(derivate, d)) for d in data_points]
data_points = [round(mean(d), 1) for d in data_points]
print(data_points)
F = [0.682, 0.822, 0.583, 1.035]
for f, a in zip(data_points, F):
	plt.scatter(f, a, color = "black")
f = lnrg([data_points], F)["predicter"]
plt.plot(data_points, list(map(f, data_points)), color = "black")
plt.title("a to mass-reciprocal graphing and regression", size = 16)
plt.xlabel('Acceleration(cm/s^2)', size = 13)
plt.ylabel('Mass-reciprocal(kg^-1)', size = 13)
plt.show()