# Write_up

## Crypto_easy

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.51.47.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.51.47.png)

문제 파일을 열어보면, 다음과 같은 Ciphertext를 볼 수 있다.

우선 제일 끝의 문자가 '=' 인 것을 보면 base64로 인코딩 되었음을 눈치챌 수 있을 것이다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.52.04.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.52.04.png)

위처럼 decode를 해보면 아래와 같은 암호문이 나온다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.52.57.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__2.52.57.png)

FLAG형식이 나오는데, 내부의 Flag는 암호화되어 있음을 알 수 있다.

여기서, affine암호를 복호화해보면, 정상적인 플래그가 나온다. 

또, 그 암호화 키는 (5,3) 임을 알 수 있다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.06.11.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.06.11.png)

FLAG : KOREA{Congratulaionnn_Now_you_are_Classic_Cipher_MMMMaster_YEAHH}

## Crypto_medium

문제 파일을 열어보면 아래와 같이 2개의 문제가 보인다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.09.56.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.09.56.png)

### medium_1

```python
from math import gcd
from Crypto.Util.number import bytes_to_long, getPrime, isPrime
from secret import flag, flag1, flag2
assert flag == flag1 + flag2

def getTwinPrime(N):
    while True:
        p = getPrime(N)
        if isPrime(p + 2):
            return p

KEYSIZE = 1024

p = getTwinPrime(KEYSIZE)
q1 = getPrime(KEYSIZE)
q2 = getPrime(KEYSIZE)

n1 = p * q1
n2 = (p + 2) * q2
e2 = bytes_to_long(b'KOREA_2020')
print(hex(n1))
print(hex((p - 1) * (q1 - 1)))

print(hex(n2))
print(hex(pow(bytes_to_long(flag1), e2, n2)))
```

우선, 두 소수의 곱인 n1과, phi(n1)을 알려준 상태이다. phi(n1)이 주어져있으면 우리는 n1을 소인수분해할 수 있고, 이를 이용하여 n2도 소인수분해할 수 있을 것이다.

```scheme
phi(n) = (p-1) * (q-1) = pq - p - q + 1
			 = pq - p - q + 1 
			 = n - p - (n/p) + 1

phi(n) * p = n * p - p * p - n + p

p^2 + (phi(n) - n + 1) * p + n = 0 을 만족하는 근 => p or q 
```

python의 z3를 이용하면 이차방정식의 근은 쉽게 구할 수 있다.

그 후, n2를 소인수분해 하여 phi(n2)를 구할 수 있는데, 문제는 gcd(e2,n2) == 16 이라는 점이다.

그래서 우선 16은 남겨두고, e2 / 16 을 e로 생각하여 RSA 복호화를 진행하면

m ^ 16을 구할 수 있다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.22.37.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.22.37.png)

이 값은 현재 m^16인데, 이를 소인수분해 툴에 넣어보면 특정 값의 16제곱으로 나타나게 된다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.23.28.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.23.28.png)

이를 hex로 변환해보면, 우리는 flag1을 얻을 수 있다.

```scheme
Flag1 : KOREA{WOW!!_You_
```

### medium2

```python
from Crypto.Util.number import getPrime, bytes_to_long
import random
from secret import flag, flag1, flag2
assert flag == flag1 + flag2

N = 9931755185060178541819350703860525202998395176620817326533726321103289514714482398301463938123540046323657927466230539048399765245482297315320621294942552040969779600220746703802727865488282400532525716200713822333260195215975219729008945628323420484667363474732308988705045216466104088114390575938974751250735732965167191025807650844438927688743083443181909932562840801876087928020419912615909929547090716236393628363582762357491323519758592285176474021090624649128022651674058738105123425788673915904447407748389441605828693561972112169848435886546096942841894411370737399277884692796708444598630421441967316945299
e = 0x10001
m = bytes_to_long(flag)

random_list = [0 for i in range(128)]
for i in range(128):
    random_list[i] = random.randint(1, 256)
with open('enc.txt', 'w') as f:
    i = 0
    while m:
        padding = random.randint(0, 2**1536) ** 2
        message = padding << random_list[i % 128] + m % 2
        cipher = pow(message, e, N)
        f.write(str(cipher)+'\n')
        m /= 2
        i += 1
```

아래에서 사용하는 분모는 르장드르 기호를 의미한다.

![Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.46.58.png](Write_up%2019e75134d3474bdd983e01ad50ffe0bb/_2020-10-16__3.46.58.png)

현재 우리는 flag[0] 부터 flag[128] 까지 알고 있기  때문에,  이를 이용해 좌변의 random2가 들어있는 식의 르장드르 값을 알 수 있다.

즉, radom_list 에 대한 정보를 얻었기 때문에 이를 이용하면 이제 역으로 flag의 비트들을 모두 복호화할 수 있다.

```python
FLAG : "KOREA{WOW!!_You_c4n_factorize_large_1nteger_and_now_you_know_jacobiii##_now_you_4re_RSA_master}"
```