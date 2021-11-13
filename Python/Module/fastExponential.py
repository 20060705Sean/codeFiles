from primes import miller_rabin
# exponential by square
def EBS(x, p):
	result = 1
	b = bin(p)[2:]
	for i, power in enumerate(reversed(b)):
		result *= x ** (int(power) * 2 ** i)
	return result
#(Fermat's little theorem)
#a^b = a^(p-1) * a^(b-p+1) (mod P)
def FLT(a, b, P):
	if b <= 10000:
		return a ** b % P
	elif miller_rabin(P, 2):
		return RE(a, b - P + 1, P)
	else:
		print("SE-1102:P not prime")
# reduction exponential 
def RE(a, b, N):
	factors = []
	i = 2
	while b >= 50000 and not miller_rabin(b, 2):
		if a <= 2:
			return a ** b % N
		if b % i == 0:
			b //= i
			a **= i
			a %= N
			print(a, b)
		else:
			i+=1
	if miller_rabin(N, 2):
		return FLT(a, b, N)
	return a ** b % N
#a ^ b === k(mod N)
def modmodmod(a, b, N):
	if a >= N:
		a %= N
	if b <= 50000 or a == 1 or a == 0:
		return a ** b % N
	temp1 = 1 * a
	temp2 = 1
	while temp1 <= N:
		temp1 *= temp1
		temp2 += 1
	a %= N
	return (modmodmod(a, b % temp2, N) * modmodmod((temp1 % N), b // temp2, N)) % N