import matplotlib.pyplot as plt
from statistics import lnrg, plrg
from mathEquationSolver import quadraticFormula

alpha = [28.4, 22.5, 18, 14, 11, 8, 6, 3.5, 1.5, 0, 0, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5, -0.5]

beta = [-0.0	-0.0	-0.0	0	0.2	0.2	0.3	0.5	0.6	0.8	0.9	1	1.2]
plt.scatter(list(range(13)), beta)
plt.plot(list(range(13)), beta)
plt.show()

'''
regression1 = lnrg([list(range(10, 25))], alpha[10:])
regression2 = plrg(list(range(0, 11)), alpha[:11], 2)

coes = [27.641458944281535 + 2.767619047619047, -1.9582690363029638 + 0.022857142857142878, 0.026590150672464397]

coes.reverse()

print(quadraticFormula(coes)[1].value())
print(regression1["predicter"](quadraticFormula(coes)[1].value()))

intersection = (22.945068732306474, -3.2920777615003383)

for i in range(len(alpha) - 1):
	plt.text(x = i + 1.0, y = alpha[i] + 0.5, s = f'{(i, alpha[i])}', fontdict=dict(color='red',size=7))
plt.plot(list(range(0, 11)), list(map(regression2["predicter"], list(range(0, 11)))), color = "blue")
plt.plot([0] + list(range(10, 25)), list(map(regression1["predicter"], [0] + list(range(10, 25)))), color = "blue")
plt.scatter(list(range(0, 25)), alpha, color = "green")
plt.plot(list(range(0, 25)), alpha, color = "green")
plt.show()
'''