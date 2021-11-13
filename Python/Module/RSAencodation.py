from primes import miller_rabin, gcd, prime_factorization, is_coprime
from random import randint, shuffle
from math import sqrt
from fastExponential import RE, modmodmod
from hashes.SHA256 import SHA256 
import sys
sys.setrecursionlimit(10000)
chars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZαβγδεζηθικλμνξοπρστυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ'
class Base110():
	@staticmethod
	def changeToBase110(x, base = 110):
		final = []
		while x > 0:
			final.append(chars[x % base])
			x //= base
		return ''.join(final)
	@staticmethod
	def base110ChangeToInterger(x, base = 110):
		result = 0
		for i, c in enumerate(x):
			result += chars.index(c) * base ** i
		return result
class RSA(object):
	def __init__(self, mode = 'old', secure = 'safe'):
		super(RSA)
		self.secure = 'big' if secure == 'safe' else 'small'
		self.p, self.q = self.find_primes() if mode == "new" else self.find_old_primes()		
		self.N = self.p * self.q
		self.r = (self.p - 1) * (self.q - 1)
		self.e = self.r
		print("Finding Coprime e......")
		while not (gcd(self.e, self.r) == 1):self.e -= randint(15 ** 10, 27 ** 17)
		print("Calculating public key (N, e)")
		print((Base110.changeToBase110(self.N), Base110.changeToBase110(self.e)))
		print('Calculating private key (N, d)')
		self.d = self.modinv(self.e, self.r)
		print((Base110.changeToBase110(self.N), Base110.changeToBase110(self.d)))
	@staticmethod
	def encode(message, N, e, mode = 110):
		e = Base110.base110ChangeToInterger(e) if mode == 110 else e
		N = Base110.base110ChangeToInterger(N) if mode == 110 else N
		print('encoding...')
		adjust_length = lambda s, c, l:f'{c * (l - len(s))}{s}'
		encodationLayer1 = [int(adjust_length(bin(ord(i))[2:], '0', 16), 2) for i in message]
		result = []
		for i in encodationLayer1:
			result.append(Base110.changeToBase110(modmodmod(i, e, N)))
		return result
	@staticmethod
	def decode(message, N, d, mode = 110):
		d = Base110.base110ChangeToInterger(d) if mode == 110 else d
		N = Base110.base110ChangeToInterger(N) if mode == 110 else N
		print('decoding...')
		decodation = bin(modmodmod(Base110.base110ChangeToInterger(message), d, N))[2:]
		decodation = '0' * (16 - len(decodation) % 16) + decodation
		result = ''
		for i in range(0, len(decodation), 16):
			result += chr(int(decodation[slice(16)], 2))
			decodation = decodation[16:]
		return result
	def egcd(self, a, b):
		if a == 0:
			return (b, 0, 1)
		else:
			g, y, x = self.egcd(b % a, a)
			return (g, x - (b // a) * y, y)
	def modinv(self, a, m):
		g, x, y = self.egcd(a, m)
		if g != 1:raise Exception('SE-1001:modular inverse does not exist')
		else:return x % m
	def find_old_primes(self) -> int:
		prime = []
		with open(f'RSA{self.secure}primes.prsa', encoding = 'utf-8') as file:
			for l in file.readlines():
				x = int(Base110.base110ChangeToInterger(l[:-1]))
				prime.append(x)
		shuffle(prime)
		print('Getting prime P......')
		print(Base110.changeToBase110(prime[0]))
		print('Getting prime Q......')
		print(Base110.changeToBase110(prime[1]))
		print(f'Prime test P:{miller_rabin(prime[0], 5)}')
		print(f'Prime test Q:{miller_rabin(prime[1], 5)}')
		return prime[0], prime[1]
	def find_primes(self) -> int:
		scale = 32
		print('Getting prime P......')
		p = self.GetPrime(randint(- 2 ** scale, 2 ** scale))
		print(Base110.changeToBase110(p))
		with open(f'RSA{self.secure}primes.prsa', 'a', encoding = 'utf-8') as file:file.write(Base110.changeToBase110(p) + '\n')
		print('Getting prime Q......')
		q = self.GetPrime(randint(- 2 ** scale, 2 ** scale))
		print(Base110.changeToBase110(q))
		with open(f'RSA{self.secure}primes.prsa', 'a', encoding = 'utf-8') as file:file.write(Base110.changeToBase110(q) + '\n')
		return p, q
	def GetPrime(self, seed) -> int:
		seed = abs(hash(str(seed)))
		seed = (int(seed ** (10 if self.secure == 'big' else 1)), int(seed ** (15 if self.secure == 'big' else 2)))
		prime = 1
		getRand = lambda:randint(seed[0], seed[1])
		while not miller_rabin(prime, 2):prime = int(f'{getRand()}{getRand()}{getRand()}{getRand()}')
		return prime
N = 'ΠIxJπναQξFkΛHκfΣOΓRΟ3RζFeΒψ4MΛΔμHuωXmΥ1mSJΠΣjΗoΜXCoTΒbΕζΔτΞ6εΣGfΚnVmΚ0XeCδEEVΠΛΜm41ΖΛR5TΛJ1ΜaxθηθοΡΝΜnZPsΚθmΠθWfw6kvΟξ803ΕθΗαwΨΖRTLΒJdΚDAMOq3Lm'
e = 'xΑ6ubWwΕCR1ΔΡPJG7ξpmbre4OIΓmεtno2HωO4KφδLnRkβΑlgPΥmfρωQΤwLΔkMdθγa4FΥSyALκNDEVΠΛΜm41ΖΛR5TΛJ1ΜaxθηθοΡΝΜnZPsΚθmΠθWfw6kvΟξ803ΕθΗαwΨΖRTLΒJdΚDAMOq3Lm'
d = 'κκstzΩ6RΑoΛaΟs3εSρΒNΣvΚΑΘδ1NΒTνυδ7ΚwΒνοοηΗCLsαYPαρdcΒΥvνμ0ωνΧΒχfZωΨΘZr4GνHmyΛDΥntRGIυgmιYarlμbθΦrθtH7yπpJYMσpasΞΛKIn18ElVUj5ΒβC9ΩZκKζM9ΣΜgQJωυb'

code = 'bΓyαρψΡθΛfFΠΠωYΞλΨνφχxYΘ6Ξq5T3ορEΕfεΦAθVκdxVNΑ3νε8i6Ρd3βgNωH0iΑαwΓΚDxα4YN3γυDχ6Rh1kiΠRιΔRDtΙJΝλJ6ζΘχυFΓρE4κΣεrSΝΩΠmU6ΕΒn5UZυpΙεDyνσΔπj9IΦ88TSΜa'
print(RSA.decode(code, N, d))
'''
[, 'SGλΓlκοE2fT2ξζixwglρωθΖΟυhιZMΕΣoSWKψpεnρjα1kκΥJYΨκJπpioΖπ0ΞρεεφnΡbMωζf3iνDγKapA9ΩνΙΨπΤg3PιIgνUισyej8λΩyΤωΖDΨ7Mu8MιΑχ3lΛΝσΣj0fBΨπΘεππoYD1U3χξQ3b']
'''