"""
Pure-Python implementation of `Hensel lifting \
<https://en.wikipedia.org/wiki/Hensel%27s_lemma>`__ for square roots modulo
a prime power.
"""
from __future__ import annotations
import doctest
from egcd import egcd

def _inv(a, m):
    """
    Return the modular multiplicative inverse of the supplied integer.

    >>> (_inv(7, 11) * 7) % 11
    1
    """
    return egcd(a, m)[1] % m

def _exp(r, p):
    """
    Determine the largest ``k`` such that ``p ** k`` divides ``r``.

    >>> _exp(11 * (7 ** 3), 7)
    3
    """
    e = p
    k = 0
    while r % e == 0:
        e *= p
        k += 1

    return k

def hensel(root: int, prime: int, exponent: int = 1) -> int:
    """
    Lift a square root of a value modulo ``prime ** exponent`` to the square
    root of that same value modulo ``prime ** (exponent + 1)``.

    More specifically, let ``square`` be a nonnegative integer that is the
    least nonnegative residue of the congruence class ``root ** 2`` modulo
    ``prime ** exponent``. Use
    `Hensel lifting <https://en.wikipedia.org/wiki/Hensel%27s_lemma>`__ to
    return an integer that represents the square root modulo
    ``prime ** (exponent + 1)`` of the congruence class represented by the
    integer ``square`` modulo ``prime ** (exponent + 1)``.

    >>> hensel(4, 7)
    39
    >>> hensel(2, 7, 2)
    2

    This function implements a lifting operation even for those cases
    in which the root has the supplied prime as a factor (or is zero).

    >>> hensel(28, 7, 3)
    273
    >>> pow(28, 2, 7 ** 3) == pow(273, 2, 7 ** 4)
    True
    >>> hensel(256, 2, 12)
    512
    >>> pow(256, 2, 2 ** 12) == pow(512, 2, 2 ** 13)
    True

    This function lifts distinct roots to distinct roots when possible.

    >>> def roots(s, m):
    ...     return [r for r in range(0, m) if pow(r, 2, m) == s]
    >>> [hensel(r, 3, 5) for r in roots(81, 3 ** 5)] == roots(81, 3 ** 6)
    True

    However, when the root has the supplied prime as a factor, it may be
    the case that not all roots modulo ``prime ** (exponent + 1)`` can be
    obtained via lifting. In that case, the number of distinct roots that
    can be obtained is equivalent to the number of distinct roots that
    are available to lift.

    >>> [hensel(r, 2, 5) for r in roots(16, 2 ** 5)]
    [12, 28, 44, 60]
    >>> roots(16, 2 ** 6)
    [4, 12, 20, 28, 36, 44, 52, 60]

    Any attempt to invoke this function with arguments that do not have the
    expected types (or do not fall within the supported ranges) raises an
    exception. **If** ``prime`` **is not a prime number, the behavior of this
    function is not specified.**

    >>> hensel('abc', 7)
    Traceback (most recent call last):
      ...
    TypeError: 'str' object cannot be interpreted as an integer
    >>> hensel(2, {})
    Traceback (most recent call last):
      ...
    TypeError: 'dict' object cannot be interpreted as an integer
    >>> hensel(2, 7, [])
    Traceback (most recent call last):
      ...
    TypeError: 'list' object cannot be interpreted as an integer
    >>> hensel(2, -1)
    Traceback (most recent call last):
      ...
    ValueError: prime must be a positive integer
    >>> hensel(2, 7, -1)
    Traceback (most recent call last):
      ...
    ValueError: exponent must be a nonnegative integer

    The examples below verify the correct behavior of the function on a range
    of different inputs.

    >>> all(
    ...     pow(r, 2, p ** k) == pow(hensel(r, p, k), 2, p ** (k + 1))
    ...     for k in range(0, 5)
    ...     for p in [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31]
    ...     for r in range(0, p ** k)
    ... )
    True
    >>> all(
    ...     lifted.issubset(actual) and (
    ...         len(actual) == len(lifted)
    ...         or
    ...         len(actual) == len(lifted) * p
    ...     )
    ...     for k in range(0, 4)
    ...     for p in [2, 3, 5, 7, 11, 13]
    ...     for s in [pow(x, 2, p ** k) for x in range(0, p ** k)]
    ...     for lifted in [set(hensel(r, p, k) for r in roots(s, p ** k))]
    ...     for actual in [roots(s, p ** (k + 1))]
    ... )
    True
    """
    # pylint: disable=too-many-branches
    if not isinstance(root, int):
        raise TypeError(
            "'" + type(root).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if not isinstance(prime, int):
        raise TypeError(
            "'" + type(prime).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if not isinstance(exponent, int):
        raise TypeError(
            "'" + type(exponent).__name__ + "'" +
            ' object cannot be interpreted as an integer'
        )

    if prime < 0:
        raise ValueError('prime must be a positive integer')

    if exponent < 0:
        raise ValueError('exponent must be a nonnegative integer')

    square = pow(root, 2, prime ** exponent)
    if square == 0:
        return (
            root * (prime ** (1 - (exponent % 2)))
            if prime == 2 else
            root * prime if exponent % 2 == 0 else root
        )

    prime_to_exponent = prime ** exponent
    prime_to_exponent_plus_one = prime_to_exponent * prime
    prime_to_exponent_adjusted = prime ** (exponent - _exp(root, prime))

    offset = root % prime_to_exponent_adjusted
    bottom_half = offset < prime_to_exponent_adjusted // 2
    base = min(offset, prime_to_exponent_adjusted - offset)

    # Specialized calculation for the case in which the supplied prime is 2.
    if prime == 2:
        prime_to_exponent_adjusted //= prime
        bottom_half = root % prime_to_exponent_adjusted < prime_to_exponent_adjusted // 2
        lifted = (
            base
            if pow(base, 2, prime_to_exponent_plus_one) == square else
            prime_to_exponent_adjusted - base
        )
    else:
        # Basic Hensel lifting (sufficient for roots that are coprime with the modulus).
        def _lift(value: int) -> int:
            multiple = (
                ((_inv(value, prime) * _inv(2, prime)) % prime)
                *
                (((square - pow(root, 2)) // prime_to_exponent) % prime)
            ) % prime
            return (value + (multiple * prime_to_exponent)) % prime_to_exponent_plus_one

        if root % prime != 0:
            return _lift(root)

        lifted = _lift(base)

        # Perform additional work if the root is not coprime with the modulus.
        # Determine the multiple of the additional prime power needed to adjust the
        # lifted root (in order to account for the fact that it is not coprime with
        # the modulus).
        multiple = (
            (
                ((square - (lifted * lifted)) % prime_to_exponent_plus_one)
                *
                _inv(
                    2 * lifted * prime_to_exponent_adjusted,
                    prime_to_exponent_plus_one
                )
            ) % prime_to_exponent_plus_one
        ) // prime_to_exponent

        lifted = (
            lifted
            +
            ((prime_to_exponent_adjusted * multiple) % prime_to_exponent_plus_one)
        ) % prime_to_exponent_plus_one

    segment = root // prime_to_exponent_adjusted
    return (
        (segment * prime_to_exponent_adjusted * prime) + lifted
        if bottom_half else
        ((segment + 1) * prime_to_exponent_adjusted * prime) - lifted
    )

if __name__ == '__main__':
    doctest.testmod() # pragma: no cover
