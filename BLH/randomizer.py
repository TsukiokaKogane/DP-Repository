import random
import numpy as np
import sys


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


def int2str(integer, length):
    """
    transform a integer to binary bit string, for debug use
    """
    s = ''
    bits = []
    for bit_num in range(length):
        if integer & (1 << bit_num):
            bits.append('1')
        else:
            bits.append('0')
    return ''.join(reversed(bits))


class Randomizer(object):
    # the class implements a epsilon-Basic Randomizer

    # Input: m-bit string and privacy parameter epsilon
    # m-bit string for the input is a integer(so m should not be above 31),
    # as the i-th bit's value indicates sign of i-th position's sign (0 for positive, 1 for negative)

    # Output: a integer
    # For position 0 - 31 bit, there should be 1 and only 1 position to be 1 indicates reporting bit's position
    # position 32 bit stands for sign indicator (0 for positive, 1 for negative)

    def __init__(self, m, epsilon):
        assert m < 32
        self.num_bits = m
        self.epsilon = epsilon

    def encode_bits(self, bits):
        assert bits.bit_length() < 32
        # log('x %s', int2str(bits, 32))
        z = 0   # result
        j = random.randint(0, self.num_bits - 1)    # sample j <- [m] uniformly at random
        # log('j %d', j)
        z |= (1 << j)
        sig = (bits >> j) & 1   # sign indicator
        rand = random.SystemRandom()
        if bits == 0:
            sig += rand.random() < 0.5
        else:
            p = np.exp(self.epsilon)/(np.exp(self.epsilon) + 1)
            # log('p %f', p)
            sig += rand.random() > p
        # log('sig %d', sig)
        sig %= 2
        z |= (sig << 31)
        # log('z %s', int2str(z, 32))
        return z


if __name__ == "__main__":
    r = Randomizer(20, 4)
    print(r.encode_bits((1 << 20)-1))
