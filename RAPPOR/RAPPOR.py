"""
The RAPPOR mechanism for local differential privacy.

"""
from random import SystemRandom
import hashlib
import struct
import hmac
import sys


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


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
        # TODO: fix annotation
        num_bits = params.num_bloombits
        # IRR probabilities
        self.p_gen = _SecureRandom(params.prob_p, num_bits)
        self.q_gen = _SecureRandom(params.prob_q, num_bits)


def to_big_endian(i):
    """
    Convert an integer to a 4 byte big endian string.  Used for hashing.
    """
    # https://docs.python.org/3/library/struct.html
    # - Big Endian (>) for consistent network byte order.
    # - L means 4 bytes when using >
    return struct.pack('>L', i)


def bit_string(irr, num_bloombits):
    """
    Like bin(), but uses leading zeroes, and no '0b'.
    """
    s = ''
    bits = []
    for bit_num in range(num_bloombits):
        if irr & (1 << bit_num):
            bits.append('1')
        else:
            bits.append('0')
    return ''.join(reversed(bits))


def get_bloom_bits(word, cohort, num_hashes, num_bloombits):
    """
    Return an array of bits to set in the bloom filter.
    In the real report, we bitwise-OR them together.  In hash candidates, we put
    them in separate entries in the "map" matrix.
    """
    # TODO: fix annotation
    value = to_big_endian(cohort) + word  # Cohort is 4 byte prefix.
    md5 = hashlib.md5(value)

    digest = md5.digest()

    # Each has is a byte, which means we could have up to 256 bit Bloom filters.
    # There are 16 bytes in an MD5, in which case we can have up to 16 hash
    # functions per Bloom filter.
    if num_hashes > len(digest):
        raise RuntimeError("Can't have more than %d hashes" % md5)

    # log('hash_input %r', value)
    # log('Cohort %d', cohort)
    # log('MD5 %s', md5.hexdigest())

    # TODO: utility test
    return [digest[i] % num_bloombits for i in range(num_hashes)]


def get_prr_masks(secret, word, prob_f, num_bits):
    h = hmac.new(secret.encode(), word, digestmod=hashlib.sha256)
    log('secret %s', secret.encode())
    log('word %s, secret %s, HMAC-SHA256 %s', word, secret, h.hexdigest())

    # Now go through each byte
    digest_bytes = h.digest()
    assert len(digest_bytes) == 32

    # Use 32 bits.  If we want 64 bits, it may be fine to generate another 32
    # bytes by repeated HMAC.  For arbitrary numbers of bytes it's probably
    # better to use the HMAC-DRBG algorithm.
    log('num_bits %d max of %d',  num_bits, len(digest_bytes))
    if num_bits > len(digest_bytes):
        raise RuntimeError('%d bits is more than the max of %d', num_bits, len(digest_bytes))

    threshold128 = prob_f * 128

    uniform = 0
    f_mask = 0

    for i in range(num_bits):
        byte = digest_bytes[i]
        log('%d byte %d', i, byte)

        u_bit = byte & 0x01  # 1 bit of entropy
        uniform |= (u_bit << i)  # maybe set bit in mask

        rand128 = byte >> 1  # 7 bits of entropy
        noise_bit = (rand128 < threshold128)
        f_mask |= (noise_bit << i)  # maybe set bit in mask
    log('uniform %s, f_mask  %s', uniform, f_mask)
    return uniform, f_mask


class Encoder(object):
    """Obfuscates values for a given user using the RAPPOR privacy algorithm."""

    def __init__(self, params, cohort, secret, irr_rand):
        """
        Args:
            params: RAPPOR Params() controlling privacy
            cohort: integer cohort, for Bloom hashing.
            secret: secret string, for the PRR to be a deterministic function of the
            reported value.
            irr_rand: IRR randomness interface.
        """
        # RAPPOR params.  NOTE: num_cohorts isn't used.  p and q are used by
        # irr_rand.
        self.params = params
        self.cohort = cohort  # associated: MD5
        self.secret = secret  # associated: HMAC-SHA256
        self.irr_rand = irr_rand  # p and q used

    def _internal_encode_bits(self, bits):
        """
        Helper function for simulation / testing.
        Returns:
            The PRR and IRR.  The PRR should never be sent over the network.
        """
        # Compute Permanent Randomized Response (PRR).
        uniform, f_mask = get_prr_masks(
         self.secret, to_big_endian(bits), self.params.prob_f,
         self.params.num_bloombits)

        # Suppose bit i of the Bloom filter is B_i.  Then bit i of the PRR is
        # defined as:
        #
        # 1   with prob f/2
        # 0   with prob f/2
        # B_i with prob 1-f

        # Uniform bits are 1 with probability 1/2, and f_mask bits are 1 with
        # probability f.  So in the expression below:
        #
        # - Bits in (uniform & f_mask) are 1 with probability f/2.
        # - (bloom_bits & ~f_mask) clears a bloom filter bit with probability
        # f, so we get B_i with probability 1-f.
        # - The remaining bits are 0, with remaining probability f/2.

        prr = (bits & ~f_mask) | (uniform & f_mask)

        # log('U %s / F %s', bit_string(uniform, num_bits),
        #    bit_string(f_mask, num_bits))

        # log('B %s / PRR %s', bit_string(bloom_bits, num_bits),
        #    bit_string(prr, num_bits))

        # Compute Instantaneous Randomized Response (IRR).
        # If PRR bit is 0, IRR bit is 1 with probability p.
        # If PRR bit is 1, IRR bit is 1 with probability q.
        p_bits = self.irr_rand.p_gen()
        q_bits = self.irr_rand.q_gen()

        irr = (p_bits & ~prr) | (q_bits & prr)

        return prr, irr  # IRR is the rappor

    def _internal_encode(self, word):
        """
        Helper function for simulation / testing.
        Returns:
            The Bloom filter bits, PRR, and IRR.  The first two values should never
            be sent over the network.
        """
        bloom_bits = get_bloom_bits(word, self.cohort, self.params.num_hashes, self.params.num_bloombits)

        bloom = 0
        for bit_to_set in bloom_bits:
            bloom |= (1 << bit_to_set)

        prr, irr = self._internal_encode_bits(bloom)
        return bloom, prr, irr

    def encode_bits(self, bits):
        """
        Encode a string with RAPPOR.
        Args:
            bits: An integer representing bits to encode.
        Returns:
            An integer that is the IRR (Instantaneous Randomized Response).
        """
        _, irr = self._internal_encode_bits(bits)
        return irr

    def encode(self, word):
        """
        Encode a string with RAPPOR.
        Args:
            word: the string that should be privately transmitted.
        Returns:
            An integer that is the IRR (Instantaneous Randomized Response).
        """
        _, _, irr = self._internal_encode(word)
        return irr

