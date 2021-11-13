from math import log, e
from primes import prime_factorization

typeEq = lambda item, types:isinstance(item, types)

prod = lambda data, i = 0:(data[i] * prod(data, i + 1)) if (i < len(data) - 1) else (data[i])
getSign = lambda x:1 if x >= 0 else -1
gcd = lambda a, b:gcd_factor(max(a, b), min(a,b))
gcd_factor = lambda a, b:b if a % b == 0 else gcd_factor(b, a % b)
lcm = lambda a, b:a * b / gcd(a, b)
class HoldPower(object):
	def __init__(self, base, power):
		super(HoldPower, self)
		self.base = base
		self.power = power
	def __str__(self):
		return f'({self.base})^{self.power}'
	def value(self):
		return (self.base if typeEq(self.base, (int, float, complex)) else self.base.value()) ** (self.power if typeEq(self.power, (int, float, complex)) else self.power.value())	
class HoldAdder(object):
	def __init__(self, *number):
		super(HoldAdder, self)
		self.number = list(number)
	def __str__(self):
		result = f"({'+'.join(list(map(str, self.number)))})"
		return result
	def __add__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(self.number + other.number)
		return HoldAdder(self.number.append(other))
	def __iadd__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(self.number + other.number)
		return HoldAdder(self.number.append(other))
	def __radd__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(self.number + other.number)
		return HoldAdder(self.number.append(other))
	def __sub__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(self.number + list(map(lambda x:x * (-1), other.number)))
		return HoldAdder(self.number.append((-1) * other.number))
	def __isub__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(self.number + list(map(lambda x:x * (-1), other.number)))
		return HoldAdder(self.number.append((-1) * other.number))
	def __rsub__(self, other):
		if typeEq(other, HoldAdder):
			return HoldAdder(other.number + list(map(lambda x:x * (-1), self.number)))
		return HoldAdder(other.number.append((-1) * self.number))
	def __mul__(self, other):
		return HoldMultipler(self, other)
	def __imul__(self, other):
		return HoldMultipler(self, other)
	def __rmul__(self, other):
		return HoldMultipler(self, other)
	def __truediv__(self, other):
		return HoldMultipler(self, Fraction(1, other))
	def __itruediv__(self, other):
		return HoldMultipler(self, Fraction(1, other))
	def __rtruediv__(self, other):
		return HoldMultipler(other, Fraction(1, self))
	def __pow__(self, other):
		return HoldMultipler([self for i in range(other)])
	def append(self, *number):
		self.number += list(number)
	def value(self):
		result = sum([i if isinstance(i, (int, float, complex)) else i.value() for i in self.number])
		return result
class HoldMultipler(object):
	def __init__(self, *number):
		super(HoldMultipler, self)
		self.number = list(number)
	def __str__(self):
		result = f"{'*'.join(list(map(str, self.number)))}"
		return result
	def __sub__(self, other):
		return HoldAdder(self, (-1) * other)
	def __rsub__(self, other):
		return HoldAdder((-1) * self, other)
	def __radd__(self, other):
		return HoldAdder(self.number, other)
	def __mul__(self, other):
		if isinstance(other, HoldMultipler):
			result = self.number.extend(other.number)
		result = self.number.append(other)
		return HoldMultipler(result)
	def __rmul__(self, other):
		result = self * other
		return result
	def __imul__(self, other):
		result = self * other
		return result
	def __truediv__(self, other):
		if isinstance(other, HoldMultipler):
			result = self.number.extend(list(map(lambda x:Fraction(1 / x), other.number)))
		result = self.number.append(1 / other)
		return HoldMultipler(result)
	def __rtruediv__(self, other):
		result = Fraction(other, self)
		return result
	def __itruediv__(self, other):
		result = self / other
		return result
	def append(self, *number):
		self.number += list(number)
	def value(self):
		result = prod([i if isinstance(i, (int, float, complex)) else i.value() for i in self.number])
		return result
class Sqrt(object):
	def __init__(self, number, base = 2, multipler = 1):
		super(Sqrt, self)
		self.number = number
		self.base = base
		self.multipler = multipler
		self.outputMode = "simplify"
		self.isComplex = number < 0
		self.simplify()
	def __add__(self, other):
		return HoldAdder(self, other)
	def __radd__(self, other):
		return HoldAdder(other, self)
	def __sub__(self, other):
		return HoldAdder(self, other * (-1))
	def __rsub__(self, other):
		return HoldAdder(other, self * (-1))
	def __mul__(self, other):
		return HoldMultipler(self, other)
	def __rmul__(self, other):
		return HoldMultipler(self, other)
	def __str__(self):
		if self.outputMode == "simplify":
			result = f"{self.multipler}*SQRT{self.base}({self.number})"
		elif self.outputMode == "value":
			result = f"{self.value()}"
		return result
	def __pow__(self, other):
		return Sqrt(self.number ** other, self.base, self.multipler)
	def __lt__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		return self.value() < other
	def __gt__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		return self.value() > other
	def __le__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		return self.value() <= other
	def __ge__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		return self.value() >= other
	def simplify(self):
		if isinstance(self.number, int) and self.number > 0:
			factors = prime_factorization((self.number), "power")
			for i in factors:
				if i[1] >= self.base:
					muls = i[1] // self.base
					self.number //= i[0] ** (muls * self.base)
					self.multipler *= i[0] ** muls
	def value(self):
		if getSign(self.number) == -1:
			return self.multipler * (self.number) ** (1 / self.base) * 1j
		return self.multipler * (self.number) ** (1 / self.base)
class Logarithm(object):
	def __init__(self, number, base = 10, multipler = 1):
		super(Logarithm, self)
		if base <= 0 or base == 1 or isinstance(base, complex):
			raise AttributeError(f"invalid base: {base}")
		if number <= 0 or isinstance(number, complex):
			raise AttributeError(f"invalid number: {number}")
		self.base = base
		self.number = number
		self.multipler = multipler
	def __str__(self):
		if self.base == e:
			result = f"{'' if self.multipler == 1 else self.multipler}LN({self.number})"
			return result
		result = f"{'' if self.multipler == 1 else self.multipler}LOG{'' if self.base == 10 else '_'}{'' if self.base == 10 else self.base}({self.number})"
		return result
	def __add__(self, other):
		if isinstance(other, Logarithm):
			if self.base == other.base:
				return Logarithm(self.number ** self.multipler * other.number ** other.multipler, self.base)
			return self + other.changeBase(self.base)
		return HoldAdder(self, other)
	def __radd__(self, other):
		result = self + other
		return result
	def __iadd__(self, other):
		result = self + other
		return result
	def __mul__(self, other):
		if isinstance(other, Logarithm):
			return HoldMultipler(self, other)
		return Logarithm(self.number ** other, self.base, self.multipler)
	def __rmul__(self, other):
		result = self * other
		return result
	def __imul__(self, other):
		result = self * other
		return result
	def __sub__(self, other):
		result = self + (-1) * other
		return result
	def __rsub__(self, other):
		result = self * (-1) + other
		return result
	def __isub__(self, other):
		result = self + (-1) * other
		return result
	def __div__(self, other):
		if isinstance(other, Logarithm):
			return HoldMultipler(self, Fraction(1, other))
		return Logarithm(self.number ** Fraction(1, other), self.base, self.multipler)
	def __rdiv__(self, other):
		result = other / self.value()
		return result
	def __idiv__(self, other):
		result = self / other
		return result
	def __truediv__(self, other):
		if isinstance(other, Logarithm):
			return HoldMultipler(self, Fraction(1, other))
		return Logarithm(self.number ** Fraction(1, other), self.base, self.multipler)
	def __rtruediv__(self, other):
		result = other / self.value()
		return result
	def __itruediv__(self, other):
		result = self / other
		return result
	def value(self):
		result = log(self.number if isinstance(self.number, (int, float, complex)) else self.number.value(), self.base) * self.multipler
		return result
	def changeBase(self, base = 10):
		if self.base == base:
			return self
		numerator = Logarithm(self.number, base)
		denomenator = Logarithm(self.base, base)
		return Fraction(numerator, denomenator)
class Fraction(object):
	def __init__(self, numerator, denomenator):
		super(Fraction, self)
		self.numerator = numerator
		self.denomenator = denomenator
		if self.denomenator == 0:
			raise ZeroDivisionError("denomenator cannot be zero.")
		if isinstance(self.denomenator, complex):
			conjugate = self.denomenator.conjugate()
			self.denomenator *= conjugate
			self.numerator *= conjugate
		self.isComplex = isinstance(self.numerator, complex)
	def __int__(self):
		result = int(self.value())
		return result
	def __str__(self):
		result = f"frac{'{'}{self.numerator}; {self.denomenator}{'}'}"
		return result
	def __lt__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		if isinstance(other, Fraction):
			return self.numerator * other.denomenator < other.numerator * self.denomenator
		return self.value() < other
	def __gt__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		if isinstance(other, Fraction):
			return self.numerator * other.denomenator > other.numerator * self.denomenator
		return self.value() > other
	def __le__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		if isinstance(other, Fraction):
			return self.numerator * other.denomenator <= other.numerator * self.denomenator
		return self.value() <= other
	def __ge__(self, other):
		if self.isComplex or isinstance(other, complex):
			raise TypeError("<complex> type is not comparable")
		if isinstance(other, Fraction):
			return self.numerator * other.denomenator >= other.numerator * self.denomenator
		return self.value() >= other
	def __abs__(self, other):
		new = Fraction(abs(self.numerator), abs(self.denomenator))
		return new
	def __add__(self, other):
		if isinstance(other, Fraction):
			return Fraction(self.numerator * other.denomenator + other.numerator * self.denomenator, self.denomenator * other.denomenator)
		return Fraction(self.numerator + other * self.denomenator, self.denomenator)
	def __radd__(self, other):
		result = self + other
		return result
	def __iadd__(self, other):
		result = self + other
		return result
	def __mul__(self, other):
		if isinstance(other, Fraction):
			return Fraction(self.numerator * other.numerator, self.denomenator * other.denomenator)
		return Fraction(self.numerator * other, self.denomenator)
	def __rmul__(self, other):
		result = self * other
		return result
	def __imul__(self, other):
		result = self * other
		return result
	def __sub__(self, other):
		result = self + (-1) * other
		return result
	def __rsub__(self, other):
		result = self * (-1) + other
		return result
	def __isub__(self, other):
		result = self + (-1) * other
		return result
	def __div__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __rdiv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __idiv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __truediv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __rtruediv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __itruediv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return Fraction(self.numerator, self.denomenator * other)
	def __floordiv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return int(Fraction(self.numerator, self.denomenator * other))
	def __rfloordiv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return int(Fraction(self.numerator, self.denomenator * other))
	def __ifloordiv__(self, other):
		if isinstance(other, Fraction):
			return self * other ** (-1)
		return int(Fraction(self.numerator, self.denomenator * other))
	def __pow__(self, other):
		numerator = self.numerator
		denomenator = self.denomenator
		if isinstance(other, complex):
			# https://www.math.toronto.edu/mathnet/questionCorner/complexexp.html
			return None
		if getSign(other) == -1:
			numerator, denomenator = self.denomenator, self.numerator
		if isinstance(other, Fraction):
			numerator **= abs(other.numerator)
			denomenator **= abs(other.numerator)
			numerator **= 1 / abs(other.denomenator)
			denomenator **= 1 / abs(other.denomenator)
			return Fraction(numerator, denomenator)
		numerator **= other
		denomenator **= other
		return Fraction(numerator, denomenator)
	def __rpow__(self, other):
		if self.isComplex:
			# https://www.math.toronto.edu/mathnet/questionCorner/complexexp.html
			return None
		return other ** self.numerator ** (1 / self.denomenator)
	def __ipow__(self, other):
		result = self ** other
		return result
	def value(self):
		val = (self.numerator if isinstance(self.numerator, (int, float, complex)) else self.numerator.value()) / (self.denomenator if isinstance(self.denomenator, (int, float, complex)) else self.denomenator.value())
		return val

if __name__ == "__main__":
	import matplotlib.pyplot as plt
	f = lambda n, b:Logarithm(Fraction(n, b), b).value()
	def exe(rg , scale, base):
		x, y = [], []
		rg, sc = rg, scale
		i = rg[0]
		while i <= rg[1]:
			x.append(i)
			y.append(f(i, base))
			i += sc
			print()
		plt.plot(x, y)
	rg = (0.1, 2)
	plt.show()