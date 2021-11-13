from mathSymbols import *
from math import asin, acos, sin, cos
from statistics import lnrg
from matrix import Matrix

const = {
	"omega" : Fraction(-1 + Sqrt(3) * 1j, 2)
}

def solve2yuan1time(a, b, c, d, e, f):
	A = Matrix([[a, b], [d, e]])
	B = Matrix([[c, f]])
	X = B * A.I()
	return X.matrix[0]

# Quadratic Equations Solver
def quadraticFormula(coefficents):
	discriminant = coefficents[1] ** 2 - 4 * coefficents[0] * coefficents[2]
	return (Fraction((-1) * coefficents[1] + Sqrt(discriminant) , (2 * coefficents[0])), Fraction((-1) * coefficents[1] - Sqrt(discriminant) , (2 * coefficents[0])))
'''
# Cubic Equations Solver
def cardanoFormula(coefficents):
	coes = list(map(lambda c:Fraction(c, coefficents[0]), coefficents))
	p = coes[2] - Fraction(coes[1] ** 2, 3)
	q = Fraction(2 * coes[1] ** 3, 27) - Fraction(coes[1] * coes[2], 3) + coes[3]
	U, V = quadraticFormula([1, q, Fraction(p ** 3, 27)])
	print(U, V)
	u, v = Sqrt(U, base = 3), Sqrt(V, base = 3)
	bPrimeDivideBy3 = Fraction(coes[1], 3)
	x = (
		u + v - bPrimeDivideBy3, 
		u * omega + v * omega - bPrimeDivideBy3, 
		u * omega ** 2 + v * omega ** 2 - bPrimeDivideBy3
	)
	return x
print(cardanoFormula([1, 0, 0, -1]))
'''