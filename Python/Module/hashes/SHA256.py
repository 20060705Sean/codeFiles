import threading
class SHA256(object):
	def __init__(self, message):
		self.__message = message
		self.__initial = [0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a, 0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19]
		self.__constants = [
			0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5, 0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5, 
			0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3, 0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174, 
			0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc, 0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da, 
			0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7, 0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967, 
			0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13, 0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85, 
			0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3, 0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070, 
			0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5, 0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3, 
			0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208, 0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2
		]
		self.__processed = False
		super(SHA256, self)
	def process(self):
		message = self.__preprocess(str(self.__message))
		message = self.__main_process(message)
		message = list(map(lambda x:hex(int(x, 2))[2:], message))
		return message
	def __preprocess(self, message):
		message = str(message)
		message = self.__transfer_to_binary_ascii(message)
		origin_length = len(message)
		message = self.__append_zero(message)
		message = self.__append_length_message(message, origin_length)
		return message
	def __adjust_length(self, message, char, length, mode):
		lack_chars = length - len(message)
		if lack_chars > 0:
			if mode == 'right':
				return message + char * lack_chars
			elif mode == 'left':
				return char * lack_chars + message
		elif lack_chars == 0:
			return message
		else:
			return message[:length]
	def __transfer_to_binary_ascii(self, message):
		result = [bin(ord(char))[2:] for char in message]
		result = [self.__adjust_length(bin_char, '0', 8, 'left') for bin_char in result]
		result = "".join(result)
		return result
	def __append_zero(self, message):
		dynamic_length = len(message) % 512
		if dynamic_length < 448:
			return f"{message}1{'0' * (448 - dynamic_length - 1)}"
		elif dynamic_length == 448:
			return f"{message}1{'0' * 511}"
		elif dynamic_length > 448:
			return f"{message}1{'0' * (511 - dynamic_length + 448)}"
	def __append_length_message(self, message, length):
		length = self.__adjust_length(bin(length)[2:], '0', 64, 'left')
		return message + length
	def __main_process(self, message):
		self.__bin = lambda x:self.__adjust_length(bin(x)[2:], '0', 64, 'left')
		self.__redefined_xor = lambda x, y:(x := self.__bin(x), y := self.__bin(y), int(''.join([str(int(not (x[i] == y[i]))) for i in range(63)]),))[-1]
		self.__right_shift = lambda x, n:x >> n
		self.__cycle_right_shift = lambda x, n:(x := self.__adjust_length(bin(x)[2:], '0', 64, 'left'), int(x[64 - n:] + x[:64 - n], 2))[1]
		self.__Ch = lambda x, y, z:self.__redefined_xor((x & y), (~ x & z))
		self.__Ma = lambda x, y, z:self.__redefined_xor(self.__redefined_xor((x & y), (y & z)), (z & x))
		self.__SIG0 = lambda x:self.__redefined_xor(self.__redefined_xor(self.__cycle_right_shift(x, 2), self.__cycle_right_shift(x, 13)), self.__cycle_right_shift(x, 22))
		self.__SIG1 = lambda x:self.__redefined_xor(self.__redefined_xor(self.__cycle_right_shift(x, 6), self.__cycle_right_shift(x, 11)), self.__cycle_right_shift(x, 25))
		self.__sig0 = lambda x:self.__redefined_xor(self.__redefined_xor(self.__cycle_right_shift(x, 7), self.__cycle_right_shift(x, 18)), self.__right_shift(x, 3))
		self.__sig1 = lambda x:self.__redefined_xor(self.__redefined_xor(self.__cycle_right_shift(x, 17), self.__cycle_right_shift(x, 19)), self.__right_shift(x, 10))
		self.__mod_32_addition = lambda *k:(sum(k) % (2 ** 32)) if sum(k) > 2 ** 32 else sum(k)
		message = self.__cut_in_specific_length(message, 512)
		threads = [None] * len(message)
		final_result = [None] * len(message)
		for i, chunk in enumerate(message):
			threads[i] = threading.Thread(target = self.__in_chunk_process, args = (chunk, final_result, i))
			threads[i].start()
		for i in range(len(threads)):
			threads[i].join()
		return (final_result)
	def __cut_in_specific_length(self, message, n):
		result = []
		for index in range(0, len(message), n):
			if index != len(message) - n:
				result.append(message[index:index + n])
			elif index == len(message) - n:
				result.append(message[index:])
		return result
	def __in_chunk_process(self, message, final_result, index):
		words = self.__words_structurion(message)
		a, b, c, d, e, f, g, h = self.__initial
		for time in range(64):
			ch = self.__Ch(e, f, g)
			sig1 = self.__SIG1(e)
			ma = self.__Ma(a, b, c)
			sig0 = self.__SIG0(a)
			temp = self.__mod_32_addition(int(words[time], 2), self.__constants[time])
			h = self.__mod_32_addition(h, ch, temp)
			h = self.__mod_32_addition(sig1, h)
			d = self.__mod_32_addition(d, h)
			h = self.__mod_32_addition(ma, h)
			h = self.__mod_32_addition(h, sig0)
			a, b, c, d, e, f, g, h = h, a, b, c, d, e, f, g
			temp = [a, b, c, d, e, f, g, h]
		final_result[index] = ''.join(list(map(lambda x:self.__adjust_length(bin(x)[2:], '0', 32, 'left'), temp)))
	def __words_structurion(self, message):
		result = self.__cut_in_specific_length(message, 32)
		for index in range(16, 64):
			new_word = self.__sig1(int(result[index - 2], 2)) + int(result[index - 7], 2) + self.__sig0(int(result[index - 15], 2)) + int(result[index - 16], 2)
			result.append(bin(new_word % (2 ** 32))[2:])
		return result
'''
class Sha256:
    ks = [
        0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
        0x3956c25b, 0x59f111f1, 0x923f82a4, 0xab1c5ed5,
        0xd807aa98, 0x12835b01, 0x243185be, 0x550c7dc3,
        0x72be5d74, 0x80deb1fe, 0x9bdc06a7, 0xc19bf174,
        0xe49b69c1, 0xefbe4786, 0x0fc19dc6, 0x240ca1cc,
        0x2de92c6f, 0x4a7484aa, 0x5cb0a9dc, 0x76f988da,
        0x983e5152, 0xa831c66d, 0xb00327c8, 0xbf597fc7,
        0xc6e00bf3, 0xd5a79147, 0x06ca6351, 0x14292967,
        0x27b70a85, 0x2e1b2138, 0x4d2c6dfc, 0x53380d13,
        0x650a7354, 0x766a0abb, 0x81c2c92e, 0x92722c85,
        0xa2bfe8a1, 0xa81a664b, 0xc24b8b70, 0xc76c51a3,
        0xd192e819, 0xd6990624, 0xf40e3585, 0x106aa070,
        0x19a4c116, 0x1e376c08, 0x2748774c, 0x34b0bcb5,
        0x391c0cb3, 0x4ed8aa4a, 0x5b9cca4f, 0x682e6ff3,
        0x748f82ee, 0x78a5636f, 0x84c87814, 0x8cc70208,
        0x90befffa, 0xa4506ceb, 0xbef9a3f7, 0xc67178f2,
    ]

    hs = [
        0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
        0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19,
    ]

    M32 = 0xFFFFFFFF

    def __init__(self, m = None):
        self.mlen = 0
        self.buf = b''
        self.k = self.ks[:]
        self.h = self.hs[:]
        self.fin = False
        if m is not None:
            self.update(m)

    @staticmethod
    def pad(mlen):
        mdi = mlen & 0x3F
        length = (mlen << 3).to_bytes(8, 'big')
        padlen = 55 - mdi if mdi < 56 else 119 - mdi
        return b'\x80' + b'\x00' * padlen + length

    @staticmethod
    def ror(x, y):
        return ((x >> y) | (x << (32 - y))) & Sha256.M32

    @staticmethod
    def maj(x, y, z):
        return (x & y) ^ (x & z) ^ (y & z)

    @staticmethod
    def ch(x, y, z):
        return (x & y) ^ ((~x) & z)

    def compress(self, c):
        w = [0] * 64
        w[0 : 16] = [int.from_bytes(c[i : i + 4], 'big') for i in range(0, len(c), 4)]

        for i in range(16, 64):
            s0 = self.ror(w[i - 15],  7) ^ self.ror(w[i - 15], 18) ^ (w[i - 15] >>  3)
            s1 = self.ror(w[i -  2], 17) ^ self.ror(w[i -  2], 19) ^ (w[i -  2] >> 10)
            w[i] = (w[i - 16] + s0 + w[i - 7] + s1) & self.M32

        a, b, c, d, e, f, g, h = self.h

        for i in range(64):
            s0 = self.ror(a, 2) ^ self.ror(a, 13) ^ self.ror(a, 22)
            t2 = s0 + self.maj(a, b, c)
            s1 = self.ror(e, 6) ^ self.ror(e, 11) ^ self.ror(e, 25)
            t1 = h + s1 + self.ch(e, f, g) + self.k[i] + w[i]

            h = g
            g = f
            f = e
            e = (d + t1) & self.M32
            d = c
            c = b
            b = a
            a = (t1 + t2) & self.M32

        for i, (x, y) in enumerate(zip(self.h, [a, b, c, d, e, f, g, h])):
            self.h[i] = (x + y) & self.M32

    def update(self, m):
        if m is None or len(m) == 0:
            return

        assert not self.fin, 'Hash already finalized and can not be updated!'

        self.mlen += len(m)
        m = self.buf + m

        for i in range(0, len(m) // 64):
            self.compress(m[64 * i : 64 * (i + 1)])

        self.buf = m[len(m) - (len(m) % 64):]

    def digest(self):
        if not self.fin:
            self.update(self.pad(self.mlen))
            self.digest = b''.join(x.to_bytes(4, 'big') for x in self.h[:8])
            self.fin = True
        return self.digest

    def hexdigest(self):
        tab = '0123456789abcdef'
        return ''.join(tab[b >> 4] + tab[b & 0xF] for b in self.digest())

def test():
    import secrets, hashlib, random
    for itest in range(500):
        data = secrets.token_bytes(random.randrange(257))
        a, b = hashlib.sha256(data).hexdigest(), Sha256(data).hexdigest()
        assert a == b, (a, b)
    for itest in range(500):
        a, b = hashlib.sha256(), Sha256()
        for j in range(random.randrange(10)):
            data = secrets.token_bytes(random.randrange(129))
            a.update(data)
            b.update(data)
        a, b = a.hexdigest(), b.hexdigest()
        assert a == b, (a, b)
    print('Sha256 tested successfully.')

if __name__ == '__main__':
    test()'''