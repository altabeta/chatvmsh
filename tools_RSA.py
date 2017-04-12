import math, random, time


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return (a)


def replacing_words(text):
    dict_r = {'a': '11', 'b': '12', 'c': '13', 'd': '14', 'e': '15', 'f': '16', 'g': '17', 'h': '18', 'i': '19',
              'j': '20',
              'k': '21', 'l': '22', 'm': '23', 'n': '24', 'o': '25', 'p': '26', 'q': '27', 'r': '28', 's': '29',
              't': '30',
              'u': '31', 'v': '32', 'w': '33', 'x': '34', 'y': '35', 'z': '36', ' ': '37'}
    if type(text) == int:
        text = str(text)
        for i, j in dict_r.items():
            text = text.replace(j, i)
        return text
    if type(text) == str:
        for i, j in dict_r.items():
            text = text.replace(i, j)
        return int(text)


primes_tab = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71]


def prime_func(inputNumber):
    global primes_tab
    last_elem = primes_tab[-1]
    while primes_tab[-1] < inputNumber:
        last_elem += 2
        checkup = math.ceil(math.sqrt(last_elem))
        for num in primes_tab:
            if num > checkup:
                stat = 1
                break
            if last_elem % num == 0:
                stat = 0
                break
        if stat == 0:
            continue
        else:
            primes_tab += [last_elem]
    return primes_tab


primes_tab = prime_func(2 ** 10)


def miller_rabin(inputNumber, iterationsNum):
    assert iterationsNum >= 1
    if inputNumber <= 3:
        if n > 1:
            return True
        else:
            return False
    elif inputNumber % 2 == 0:
        return False
    counter = 0
    num = num1 = inputNumber - 1
    rng_func = random.SystemRandom()
    while num % 2 == 0:
        num //= 2
        counter += 1
    for count_prime in range(iterationsNum):
        a = rng_func.randint(2, inputNumber - 2)
        b = pow(a, num, inputNumber)
        if b != 1 & b != num1:
            i = 1
            while b != num1 & i <= counter - 1:
                b = (b ** 2) % num
                if b == 1:
                    return False
                i += 1
            if b != num1:
                return False
    return True


def prime_gen(keysize):
    global primes_tab
    rng_func = random.SystemRandom()
    if keysize <= 20:
        while True:
            num = rng_func.randint(2 ** (keysize - 1), (2 ** keysize) - 1)
            checkup_1 = math.ceil(math.sqrt(num))
            for a1 in primes_tab:
                if a1 > checkup_1:
                    return num
                if num % a1 == 0:
                    break
    c = 0.1
    bit_q = math.ceil(c * (keysize ** 2))
    prime_func(bit_q)
    m = 20
    if keysize > 2 * m:
        while True:
            rng_r = rng_func.uniform(0, 1)
            r = 2 ** (rng_r - 1)
            if (keysize - r * keysize) > m:
                break
    else:
        r = 0.5
    q = prime_gen(math.floor(r * keysize) + 1)
    ii = 2 ** (keysize - 1) // (2 * q)
    success = 0
    while success == 0:
        rng_candidate = rng_func.randint(ii + 1, 2 * ii)
        n_candidate = 2 * rng_candidate * q + 1
        indicate = 1
        for p in primes_tab:
            if p > bit_q:
                break
            if n_candidate % p == 0:
                indicate = 0
                break
        if indicate == 0:
            continue
        if miller_rabin(n_candidate, 2) == True:
            a = rng_func.randint(2, n_candidate - 2)
            if pow(a, n_candidate - 1, n_candidate) == 1:
                b = pow(a, 2 * rng_candidate, n_candidate)
                if gcd(b - 1, n_candidate) == 1:
                    success = 1
    return (n_candidate)


def fastpow(base, exponent, module=None):
    d = base
    result = 1
    while exponent:
        if exponent % 2 == 1:
            result *= d
        d *= d
        if module:
            result %= module
            d %= module
        exponent //= 2
    return result


def gcd1(a, b):
    x0, y0, x1, y1 = 1, 0, 0, 1
    while b != 0:
        q = a // b
        a, b = b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return a, x0, y0