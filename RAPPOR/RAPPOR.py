"""
The RAPPOR mechanism for local differential privacy.

"""
import random


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

