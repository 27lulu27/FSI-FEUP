import binascii
import random

# Algoritmo Miller-Rabin para testar se um número é primo
def miller_rabin(n, k=40):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


# Encontrar os valores reais de p e q
def find_primes_near(n, offset, range_limit=100000000):
    t = 500 + offset
    p1 = 2 ** t
    
    for dp in range(0, range_limit):
        p = p1 + dp
        if miller_rabin(p):
            q = n // p
            if n % p == 0 and miller_rabin(q):
                print(f"p: {p}")
                print(f"q: {q}")
                return p, q
    raise ValueError("Primes not found in range.")


# Algoritmo Extended Euclidean
def extendedEuclidean(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, gcd = extendedEuclidean(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return x, y, gcd


# Inversos Multiplicativos (função para encontrar o valor de d)
def mod_inverse(e, v):
    x, _, gcd = extendedEuclidean(e, v)
    if gcd != 1:
        raise ValueError("No modular inverse")
    d = x % v
    print(f"d: {d}")
    return d


# Função para decifrar a mensagem (F^(−1) (sk, y) = y^d mod n)
def decrypt(ciphertext_hex, n, e, offset):
    p, q = find_primes_near(n, offset)
    
    v = (p - 1) * (q - 1)
    d = mod_inverse(e, v)
    
    ciphertext = int.from_bytes(binascii.unhexlify(ciphertext_hex), "little")
    
    plaintext_int = pow(ciphertext, d, n)
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'little')
    
    return plaintext_bytes.decode()


n = 1697873161311732311596689285449083473254367308664680687185649587159766365942802310900674010400945074037322282869230922934379840692904366246394443542850078590235722227662368964386639122840055516200946210392421273319898714376018533936295272068776264770308644817854803455425113619197760671207280189476543725586448410642137102973884781
e = 65537
ciphertext_hex = "06f6f0c76d3fbfaf5718e5e000923f00b32d36af3441762eea0362a117cf9ae8ca73ef80d6eb960aa584242a3b1fe198494eaa9afc45c06d2d9201f4fa6b7b82ab3ae93bcb45d101b4cf7a106dabe1e73a9dbcb66d7cff317ff8a1e8c4f0eafba68ca34dffccb92471cc50f76ce829d172633519720aa79d609ad195146e6f8eca8c0ffe4e073ec9ed0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000"
t = 10
g = 7
offset = ((t-1)*10+g) // 2


try:
    plaintext = decrypt(ciphertext_hex, n, e, offset)
    print("Decrypted message:", plaintext)
except ValueError as ve:
    print("Error during decryption:", ve)