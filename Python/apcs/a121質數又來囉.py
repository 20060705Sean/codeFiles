import random

class xrange():
    def __init__(self, c):
        self.c = c
        self.count = 0
    def __iter__(self):
        while self.count != self.c:
            yield self.count
            self.count += 1


def miller_rabin(n, k):

    # Implementation uses the Miller-Rabin Primality Test
    # The optimal number of rounds for this test is 40
    # See http://stackoverflow.com/questions/6325576/how-many-iterations-of-rabin-miller-should-i-use-for-cryptographic-safe-primes
    # for justification

    # If number is even, it's a composite number

    if n == 1:
        return False
    if n == 2:
        return True
    elif n == 3:
        return True

    if n % 2 == 0:
        return False

    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    for _ in xrange(k):
        a = random.randrange(2, n - 1)
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
u3er1nput = []
try:
    while True:u3er1nput.append(tuple(map(int, input().split())))
except EOFError:
    pass
for t in u3er1nput:
    amount = 0
    for i in range(t[0], t[1] + 1):
        amount += 1 if miller_rabin(i,3) else 0
    print(amount)