from random import randrange
from functools import reduce
from xrange import xrange
from PrimeSubModule.SelectorOf2 import operate2
from PrimeSubModule.SelectorOf3 import operate3
from PrimeSubModule.SelectorOf5 import operate5
gcd = lambda a, b:gcd_factor(max(a, b), min(a,b))
prod = lambda data, i = 0:(data[i] * prod(data, i + 1)) if (i < len(data) - 1) else (data[i])
gcd_factor = lambda a, b:b if a % b == 0 else gcd_factor(b, a % b)
lcm = lambda a, b:a * b / gcd(a, b)
count_each_char_sort_value = lambda string:sorted(list(set([(c, string.count(c)) if c not in string[:i] else " " for i, c in enumerate(string)])), key = lambda n:n[0])
isPositiveInterger = lambda x:{(i >= 0) and isinstance(i, int) for i in x} == {True}
def miller_rabin(n, k):
	if not isPositiveInterger((n, k)):
		raise AttributeError("Inpuit not valid")
	if n == 0:
		return False
	if n == 1:
		return False
	if n == 2:
		return True
	elif n == 3:
		return True
	if operate2([n]) == []:
		return False
	elif operate3([n]) == []:
		return False
	elif operate5([n]) ==[]:
		return False
	r, s = 0, n - 1
	while s % 2 == 0:
		r += 1
		s //= 2
	for _ in xrange(k):
		a = randrange(2, n - 1)
		x = pow(a, s, n)
		if x == 1 or x == n - 1:
			continue
		for _ in xrange(r - 1):
			x = pow(x, 2, n)
			if x == n - 1:
				break
		else:
			return False
	return True
def prime_factorization(n, mode = "single"):
	if not isPositiveInterger([n]):
		raise AttributeError("Inpuit not valid")
	if n == 0:
		return 0
	if miller_rabin(n, 3):
		return [n]
	result = []
	i = 2
	while n != 1:
		if n % i == 0:
			n //= i
			result.append(i)
			i = 2
		else:i += 1
	return result if mode == "single" else count_each_char_sort_value(result)
def is_coprime(a, b):
	if not isPositiveInterger((a, b)):
		raise AttributeError("Inpuit not valid")
	if a == b:
		return False
	if a % b == 0 or b % a == 0:
		return False
	a_isPrime, b_isPrime = miller_rabin(a, 3), miller_rabin(b, 3)
	if a_isPrime and b_isPrime:
		return True
	if a == 1 or b == 1:
		return True
	discranpacy = abs(a - b)
	if discranpacy == 1:
		return True
	if discranpacy == 2 and a % 2 == 1:
		return True
	if (a > b and a_isPrime) or (b > a and b_isPrime):
		return True
	if not (a_isPrime and b_isPrime):
		big_one, small_one = max(a, b), min(a, b)
		if discranpacy <= 1000:
			if 0 not in list(map(lambda x:big_one % x, set(prime_factorization(big_one - small_one)))):
				return True
		if 1000 < discranpacy <= 100000:
			if 0 not in list(map(lambda x:big_one % x, set(prime_factorization(small_one)))):
				return True
		if 100000 < discranpacy:
			if gcd(a, b) == 1:
				return True
	return set(prime_factorization(a)) & set(prime_factorization(b)) == set()
def modular_multiplicative_inverse(K, m):
	if not isPositiveInterger((K, m)):
		raise AttributeError("Inpuit not valid")
	result = []
	for i in range(m):
		if (K * i) % m == 1:
			result.append(i)
	return result
def chinese_remainder_theorem(remainder_dict, mode = "single"):
	if not isPositiveInterger(list(remainder_dict.keys()) + list(remainder_dict.values())):
		raise AttributeError("Inpuit not valid")
	mods = list(remainder_dict.keys())
	coprime_flag = False
	for i in xrange(len(mods) - 2):
		for m in mods[i:]:
			if is_coprime(mods[i], mods[i + 1]):
				coprime_flag = True
				break
		if coprime_flag:break
	if not coprime_flag:return None
	M = reduce(lambda x, y:x * y, mods)
	Mi = list(map(lambda x:M // x, mods))
	Ti = list(map(lambda x:modular_multiplicative_inverse(x[0], x[1])[0], zip(Mi, mods)))
	solutionSet = lambda k:sum([list(remainder_dict.values())[i] * Ti[i] * Mi[i] for i in range(len(mods))]) % M + k * M
	return solution(0) if mode == "single" else solution
def euler_totient_function(n):
	if not isPositiveInterger([n]):
		raise AttributeError("Inpuit not valid")
	return prod(list(map(lambda x:x[0] ** (x[1] - 1) * (x[0] - 1), prime_factorization(n, "exponential"))))
