"""
* Credit for functions contained in this file goes to Mr. Terry Jacson
* https://github.com/jacksoninfosec/kuznyechik/blob/main/kuznyechik.py
"""

# x and y are nonnegative integers
# Their associated binary polynomials are multiplied.
# The associated integer to this product is returned.
def multiply_ints_as_polynomials(x, y):
    if x == 0 or y == 0:
        return 0
    z = 0
    while x != 0:
        if x & 1 == 1:
            z ^= y
        y <<= 1
        x >>= 1
    return z


# x is a nonnegative integer
# m is a positive integer
def mod_int_as_polynomial(x, m):
    nbm = number_bits(m)
    while True:
        nbx = number_bits(x)
        if nbx < nbm:
            return x
        mshift = m << (nbx - nbm)
        x ^= mshift


# x,y are 8-bits
# The output value is 8-bits
def kuznyechik_multiplication(x, y):
    z = multiply_ints_as_polynomials(x, y)
    m = int('111000011', 2)
    return mod_int_as_polynomial(z, m)


# The input x is 128-bits (considered as a vector of sixteen bytes)
# The return value is 8-bits
def kuznyechik_linear_function(x):
    C = [148, 32, 133, 16, 194, 192, 1, 251, 1, 192, 194, 16, 133, 32, 148, 1]
    y = 0
    while x != 0:
        y ^= kuznyechik_multiplication(x & 0xff, C.pop())
        x >>= 8
    return y


# Returns the number of bits that are used
# to store the positive integer integer x.
def number_bits(x):
    x = list(bin(x)[2:])
    return len(x)