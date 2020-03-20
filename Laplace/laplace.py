"""
The Histogram Encoding with laplace mechanism for local differential privacy.

"""
import numpy as np
import sys


def log(msg, *args):
    if args:
        msg = msg % args
    print(msg, file=sys.stderr)


class Encoder(object):
    """Obfuscates values for a given user using the Histogram Encoding with laplace mechanism."""
    def __init__(self, epsilon, length):
        """
        Args:
            epsilon: parameter controlling privacy (Privacy of HE satisfies epsilon-LDP)
            length: histogram's length

        """
        self._epsilon = epsilon
        self._length = length

    def _internal_encode_bits(self, bits):
        """
        Helper function for simulation / testing.
        Returns:
            integer value after histogram encoding
        """
        b = []
        for i in range(self._length):
            b.append(0.0)
        b[bits] = 1.0
        # print(b)
        return b

    def _internal_perturb(self, b):
        """
               Helper function for simulation / testing.
               Returns:
                   original histogram encoding after adding laplace noise
        """
        b1 = []
        for i in range(self._length):
            laplace_noise = np.random.laplace(loc=0.0, scale=2/self._epsilon)
            b1.append(b[i] + laplace_noise)
            # log('the %d th element', i)
            # log('original value %r', b[i])
            # log('laplace noise %r', laplace_noise)
            # log('perturbed value %r', b1[i])
        # print(b1)
        return b, b1

    def encode_bits(self, bits):
        """
        Encode a string with Histogram Encoding with laplace mechanism.
        Args:
            bits: the string that should be privately transmitted.
        Returns:
            a vector that is the bits after Histogram Encoding with laplace mechanism process
        """
        b = self._internal_encode_bits(bits)
        _, output = self._internal_perturb(b)
        return output



