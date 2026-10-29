"""Find prime numbers using the Sieve of Eratosthenes."""

from math import isqrt


def sieve(n: int) -> list[int]:
    """Return all prime numbers less than or equal to n.

    Slice assignment marks multiples of each prime in batches.
    """
    if n < 2:
        return []

    is_prime = [True] * (n + 1)
    is_prime[0] = is_prime[1] = False

    for number in range(2, isqrt(n) + 1):
        if is_prime[number]:
            start = number * number
            count = (n - start) // number + 1
            is_prime[start : n + 1 : number] = [False] * count

    return [number for number, prime in enumerate(is_prime) if prime]


def main() -> None:
    """Read an upper bound and print the primes up to that bound."""
    n = int(input("Nhap n: "))
    print(sieve(n))


if __name__ == "__main__":
    main()
