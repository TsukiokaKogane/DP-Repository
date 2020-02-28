import random
"""
encode

Parameters
----------
    v: value
    d: binary vector length
Returns
-------
    b: Unary Encoding vector
"""


def encode(v, d):
    b = []
    for i in range(d):
        b.append(0)
    b[v] = 1
    #print(b0)
    return b


def permanent_randomized_response(b, d, f):
    for i in range(d):
        r = random.uniform(0, 1)
        if r * 2 < f:
            b[i] = 1
        elif r < f:
            b[i] = 0
        else:
            pass
    #print(b)
    return b


def instantaneous_randomized_response(b, d, p, q):
    for i in range(d):
        r = random.uniform(0, 1)
        if b[i] == 1 and r <= p or b[i] == 0 and r <= q:
            b[i] = 1
        else:
            b[i] = 0
    return b


def aggregation(b, d, f, n):
    print(b)
    for i in range(d):
        b[i] = (b[i] - 0.5 * f * n) / (1 - f)
    return b


def perturbation(b, d, f):
    b1 = permanent_randomized_response(b, d, f)
    b2 = instantaneous_randomized_response(b1, d, 0.75, 0.25)
    return b2
    # return b1

def test(d, f, n):
    b = []
    for i in range(d):
        b.append(0)
    for i in range(n):
        b1 = perturbation(encode(0, d), d, f)
        for j in range(d):
            b[j] = b[j] + b1[j]
    for i in aggregation(b, d, f, n):
        print(i)

def test1(d, f, n):
    b = []
    for i in range(d):
        b.append(0)

    for i in range(int(n/2)):
        b1 = perturbation(encode(0, d), d, f)
        for j in range(d):
            b[j] = b[j] + b1[j]

    for i in range(int(n/2)):
        b1 = perturbation(encode(1, d), d, f)
        for j in range(d):
            b[j] = b[j] + b1[j]

    for i in aggregation(b, d, f, n):
        print(i)

test(2, 0.5, 1000000)