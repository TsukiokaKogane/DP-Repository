"""
The RAPPOR mechanism test program

"""
import RAPPOR as ra
from RAPPOR_Decoder import Decoder, Report
from random import randint


if __name__ == "__main__":
    candidates = [b'v1', b'v2', b'v3']
    p = ra.Params()
    # print(p.num_bloombits)
    d = Decoder(p)
    repo = []

    for i in range(100000):
        for c in candidates:
            cohort = randint(0, 20)
            e = ra.Encoder(p, cohort, b'secret', ra.SecureIrrRand(p))
            irr = e.encode(c)
            repo.append(Report(cohort, irr))
    d.decode(candidates, repo)
