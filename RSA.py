

from tools_RSA import *


class RSA:
    def __init__(self):
        self.p = prime_gen(64)
        self.q = prime_gen(64)
        self.n = self.q * self.p
        self.euler_n = (self.q - 1) * (self.p - 1)
        self.open_exponent = random.randint(2, self.euler_n - 1)
        while True:
            if gcd1(self.open_exponent, self.euler_n)[0] == 1:
                break
            else:
                self.open_exponent = random.randint(2, self.euler_n - 1)
        self.closed_exponent = gcd1(self.euler_n, self.open_exponent)[2] % self.euler_n

    def encode1(self, txt):
        txt = replacing_words(str(txt))
        res = fastpow(txt, self.open_exponent, module=self.n)
        return res

    def decode2(self, text):
        res = fastpow(text, self.closed_exponent, module=self.n)
        return replacing_words(res)