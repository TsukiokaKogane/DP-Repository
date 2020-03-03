import random



def encode(v, d):
    """
    encode `value` with the mechanism.

    Parameters
    ----------
        v: value
        d: binary vector length
    Returns
    -------
        b: Unary Encoding vector
    """
    b = []
    for i in range(d):
        b.append(0)
    b[v] = 1
    return b


def permanent_randomized_response(b, d, f):
    """
    replaces the real value B with a derived randomized noisy value B'

    Parameters
    ----------
        b: real value vector
        d: binary vector length
        f:  a user-tunable parameter controlling the
        level of longitudinal privacy guarantee
    Returns
    -------
        b': randomized value vector
    """
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
    """
    reports a randomized version of B'(B")
    Parameters
    ----------
        b: randomized value vector
        d: binary vector length
        p: Pr [B2[i] = 1] = p if if B1[i] = 1
        q: Pr [B2[i] = 1] = q if if B1[i] = 0
    Returns
    -------
        b': randomized version of b
    """
    for i in range(d):
        r = random.uniform(0, 1)
        if b[i] == 1 and r < p or b[i] == 0 and r < q:
            b[i] = 1
        else:
            # print(str(b[i])+' '+str(r))
            b[i] = 0
    return b


def aggregation(b, d, f, n):
    """
    aggregate the reported data
    Parameters
    ----------
        b:  value vector after perturbation and accumulation
        d: binary vector length
        f:  a user-tunable parameter controlling the
        level of longitudinal privacy guarantee
        n: data size
    Returns
    -------
        b: aggregate version of b"
    """
    for i in range(d):
        b[i] = (b[i] - 0.5 * f * n) / (1 - f)
    return b


def perturbation(b, d, f):
    """
    Parameters
    ----------
        b: real value vector
        d: binary vector length
        f:  a user-tunable parameter controlling the
        level of longitudinal privacy guarantee
    Returns
    -------
        b': value vector after perturbation
    """
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