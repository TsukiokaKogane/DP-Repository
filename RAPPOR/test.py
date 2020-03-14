"""
The RAPPOR mechanism test program

"""
import RAPPOR as r


class MockRandom(object):
  """Returns one of three random values in a cyclic manner.
  Mock random function that involves *some* state, as needed for tests that
  call randomness several times. This makes it difficult to deal exclusively
  with stubs for testing purposes.
  """

  def __init__(self, cycle, params):
    self.p_gen = MockRandomCall(params.prob_p, cycle, params.num_bloombits)
    self.q_gen = MockRandomCall(params.prob_q, cycle, params.num_bloombits)


class MockRandomCall:
  def __init__(self, prob, cycle, num_bits):
    self.cycle = cycle
    self.n = len(self.cycle)
    self.prob = prob
    self.num_bits = num_bits

  def __call__(self):
    counter = 0
    r = 0
    for i in range(0, self.num_bits):
      rand_val = self.cycle[counter]
      counter += 1
      counter %= self.n  # wrap around
      r |= ((rand_val < self.prob) << i)
    return r


def test1():
    secert = 1
    p = r.Params()
    cohort = p.num_cohorts
    # rand = MockRandom([0.0, 0.6, 0.0], params)
    e = r.Encoder(p, 0, 'secret', r.SecureIrrRand(p))
    irr = e.encode_bits(21)
    print(irr)


test1()
