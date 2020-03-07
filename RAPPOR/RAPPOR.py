"""
The RAPPOR mechanism for local differential privacy.

"""
from random import SystemRandom
import hashlib
import struct


class Params(object):
    """
    RAPPOR encoding parameters.
    These affect privacy/anonymity.  See the paper for details.
    """
    def __init__(self):
        self.num_bloombits = 16      # Number of bloom filter bits (k)
        self.num_hashes = 2          # Number of bloom filter hashes (h)
        self.num_cohorts = 64        # Number of cohorts (m)
        self.prob_p = 0.50           # Probability p
        self.prob_q = 0.75           # Probability q
        self.prob_f = 0.50           # Probability f
        # For testing

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return repr(self.__dict__)


class _SecureRandom(object):
    """
     Returns an integer where each bit has probability p of being 1.
    """
    def __init__(self, prob_one, num_bits):
        self.prob_one = prob_one
        self.num_bits = num_bits

    def __call__(self):
        p = self.prob_one
        rand = SystemRandom()
        r = 0
        for i in range(self.num_bits):
            bit = rand.random() < p
            r |= (bit << i)  # using bool as int
        return r


class SecureIrrRand(object):
    """
    Python's os.random()
    """

    def __init__(self, params):
        """
        Parameters
        params: rappor.Params
        """
        num_bits = params.num_bloombits
        # IRR probabilities
        self.p_gen = _SecureRandom(params.prob_p, num_bits)
        self.q_gen = _SecureRandom(params.prob_q, num_bits)


def to_big_endian(i):
    """Convert an integer to a 4 byte big endian string.  Used for hashing."""
    # https://docs.python.org/3/library/struct.html
    # - Big Endian (>) for consistent network byte order.
    # - L means 4 bytes when using >
    return struct.pack('>L', i)


def signal():
    """
    Hash client's value v onto the Bloom filter B of size k using h hash functions.

    Parameters
    ----------

    Returns
    -------

    """
    pass


def permanent_randomized_response():
    """
    For each client's value v and bit i in B, create a binary reporting value Bi' which equals to
    Bi' = 1 with probability  0.5f
    Bi' = 0 with probability  0.5f
    Bi' = Bi with probability  1 - f

    Parameters
    ----------

    Returns
    -------

    """
    pass


def instantaneous_randomized_response():
    """
    Allocate a bit array S of size k and initialize to 0. Set each bit i in S with probabilities
    P(Si = q) = q if Bi' = 1
    P(Si = q) = p if Bi' = 0

    Parameters
    ----------

    Returns
    -------

    """
    pass


def report():
    """
    Send the generated report S to the server.

    Parameters
    ----------

    Returns
    -------

    """
    pass

