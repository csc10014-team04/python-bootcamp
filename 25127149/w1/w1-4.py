from math import isqrt


def sieve(n: int) -> list[int]:
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, isqrt(n) + 1):
        if is_prime[i]:
            start = i * i
            count = (n - start) // i + 1
            is_prime[start:n + 1:i] = [False] * count

    return [i for i, prime in enumerate(is_prime) if prime]
    
"""
Return primes up to n.

Unlike the C++ version, Python can mark multiple entries
at once using slice assignment.
"""


n = int(input("Nhap n: "))
print(sieve(n))
