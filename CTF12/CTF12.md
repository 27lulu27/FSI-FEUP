# CTF Semana #12 - (RSA)

Começamos este CFT calculando os valores aproximados de **p** e **q**, sendo que sabiamos que:
* p é um primo próximo de 2^(500+(((t-1)*10 + g) // 2))
* q é um primo próximo de 2^(501+(((t-1)*10 + g) // 2))

Sendo o nosso o grupo 07 da turma 10, concluimos que:
* p é um primo próximo de 2^(500+(((10-1)*10 + 7) // 2)) = 2^548
* q é um primo próximo de 2^(501+(((10-1)*10 + 7) // 2)) = 2^549

Em seguida implementamos uma função (***miller_rabin***) para testar a primalidade de números, baseada no algoritmo de Miller-Rabin:
```
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
```

E outra (***find_primes_near***) para testar os primos próximos dos valores definidos e assim encontrar os valores de **p** e **q** (sendo que p*q=n):
```
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
```

Definindo os valores de n e do ofset, conseguimos obter os valores reais de **p** e **q**.
```
n = 1697873161311732311596689285449083473254367308664680687185649587159766365942802310900674010400945074037322282869230922934379840692904366246394443542850078590235722227662368964386639122840055516200946210392421273319898714376018533936295272068776264770308644817854803455425113619197760671207280189476543725586448410642137102973884781
offset = ((10-1)*10+7) // 2
```
```
p: 921377545122446619199598286374089084696513969828232526459034741270904336521520715841339532514076847544303802497745079321233052888165232576308943909041185557531591497    
q: 1842755090244893238399196572748178169393027939656465052918069482541808673043041431682679065028153695088607604995490158642466105776330465152617887818082371115063181573
```

Já com os valores de **p**, **q**, **n** e **e** (os últimos dois fornecidos em CTF12_L10G07.cph) falta-nos descobrir o valor de **d**. Para isso utilizamos as funções ***extendedEuclidean*** e ***mod_inverse*** para encontrar o valor de **d**, resolvendo a equação ```d * e mod v = 1```:
```
def extendedEuclidean(a, b):
    if b == 0:
        return (1, 0, a)
    x1, y1, gcd = extendedEuclidean(b, a % b)
    x, y = y1, x1 - (a // b) * y1
    return x, y, gcd

def mod_inverse(e, v):
    x, _, gcd = extendedEuclidean(e, v)
    if gcd != 1:
        raise ValueError("No modular inverse")
    d = x % v
    print(f"d: {d}")
    return d
```

Conseguimos assim obter o valor real de **d**:
```
d: 1402040065060474682072564059232700602798111753823263033540030583607919742925257113711684637607433137262184831535118163592516719084160069770089788907822459879859877860857878048337068184938684166803240120194687358469771503484615478817584339872179983782210427368696060960873960482244225458671048731081883877004213431781414097857039041
```


Desta forma já reunimos todas condições para conseguir decifrar a flag. Com a função ***decrypt*** convertemos a mensagem em hexadecimal para bytes e de bytes para um número inteiro no formato little-endian e aplicamos a operação y^d mod n (sendo y a mensagem cifrada), revertendo assim a operação feita para encriptar a mensagem. Por fim, convertemos o número inteiro que representa a mensagem decifrada para bytes e de bytes para uma string legível, obtendo assim o texto original.
```
def decrypt(ciphertext_hex, n, e, offset):
    p, q = find_primes_near(n, offset)
    
    v = (p - 1) * (q - 1)
    d = mod_inverse(e, v)
    
    ciphertext = int.from_bytes(binascii.unhexlify(ciphertext_hex), "little")
    
    plaintext_int = pow(ciphertext, d, n)
    plaintext_bytes = plaintext_int.to_bytes((plaintext_int.bit_length() + 7) // 8, 'little')
    
    return plaintext_bytes.decode()
```


Conseguimos assim obter a nossa flag:
### flag{jeqaxxeqjqrvmtyy}


*Nota:* É possível encontrar [aqui](https://git.fe.up.pt/fsi/fsi2425/logs/l10g07/-/blob/main/CTF12/ctf12.py) o ficheiro em phyton na integra, utilizado para resolver este desafio.


## Perguntas finais
#### 1. Como consigo usar a informação que tenho para inferir os valores usados no RSA que cifrou a flag?
> Para inferir os valores usados no RSA aproveitamos a informação adicional fornecida na tarefa sobre a localização aproximada dos primos p e q. Estes valores são próximos de 2^(500+offset) e 2^(501+offset), onde o offset é representado ((t-1)*10 + g) // 2, sendo t a nossa turma (10) e g o nosso grupo (7).    
> Com base nisto utilizamos a função find_primes_near para explorar os valores próximos destes, procurando primos p e q que quando multiplicados resultem em n.

#### 2. Como consigo descobrir se a minha inferência está correta?
> A nossa inferência está correta se os valores encontrados para p e q forem ambos primos, se multiplicados resultarem exatamente no módulo n fornecido no desafio e se as operações RSA de criptografia e discriptografia funcionarem direito utilizando estes valores, sendo que a chave pública (e,n) é usada para cifrar e a chave privada (d,n) para decifrar.

#### 3. Finalmente, como posso extrair a minha chave do criptograma que recebi?
> A chave privada d, necessária para decifrar o criptograma é calculada usando a equação d*e mod v = 1, onde v = (p-1) * (q-1). Usamos o algoritmo Extended Euclidean para encontrar o inverso modular d de e em relação a v e assim termos a chave privada completa (d,n).    
> Para extrair o texto original convertemos o criptograma hexadecimal para um número inteiro, usamos a operação de decifração y^d mod n, onde y é a mensagem cifrada em formato numérico e depois convertemos de volta para texto legível, revelando a flag.
