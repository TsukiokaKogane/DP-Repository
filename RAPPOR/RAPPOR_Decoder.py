from RAPPOR import Params, get_bloom_bits, log, bit_string
import numpy.matlib
import numpy as np
from sklearn.linear_model import Lasso


class Report(object):
    def __init__(self, cohort, irr):
        self.cohort = cohort
        self.irr = irr


def get_bloom(bloom_bits):
    bloom = 0
    for bit_to_set in bloom_bits:
        bloom |= (1 << bit_to_set)
    return bloom


class Decoder(object):
    def __init__(self, params):
        self.params = params

    def decode(self, candidates, reports=[]):
        c = np.zeros((self.params.num_cohorts, self.params.num_bloombits), dtype=np.float)
        # t = np.zeros((self.params.num_bloombits, self.params.num_cohorts), dtype=np.float)
        X_train = np.zeros((self.params.num_cohorts*self.params.num_bloombits, len(candidates)), dtype=np.float)
        Y_train = np.zeros(self.params.num_cohorts*self.params.num_bloombits, dtype=np.float)
        n_cnt = np.zeros(self.params.num_cohorts, dtype=np.float)
        p = self.params.prob_p
        q = self.params.prob_q
        f = self.params.prob_f

        for r in reports:
            n_cnt[r.cohort] += 1.0
            for j in range(self.params.num_bloombits):
                if (r.irr >> j) & 1:
                    c[(r.cohort, j)] += 1.0
        # print(c)
        for i in range(self.params.num_cohorts):
            for j in range(self.params.num_bloombits):
                # t[(i, j)] = (c[(i, j)] - (p + 0.5 * f * q - 0.5 * f * q - 0.5 * f * p) * n_cnt[i]) \
                #              / ((1.0 - f) * (q - p))
                Y_train[i*self.params.num_bloombits + j] = \
                        (c[(i, j)] - (p + 0.5 * f * q - 0.5 * f * q - 0.5 * f * p) * n_cnt[i]) / ((1.0 - f) * (q - p))
        for c in range(len(candidates)):
            for i in range(self.params.num_cohorts):
                bloom = get_bloom(get_bloom_bits(candidates[c], i, self.params.num_hashes, self.params.num_bloombits))
                msk = bloom
                for j in range(self.params.num_bloombits):
                    X_train[(i*self.params.num_bloombits + j, c)] = (msk >> j) & 1

        reg = Lasso(alpha=0.1)
        reg.fit(X_train, Y_train)
        print(reg.coef_)


if __name__ == "__main__":
    pass
