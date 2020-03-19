RAPPOR ENCODER

=================
NOTE: ALL THE CODE in this section is based on Google's original code and documentation, it's only product of self-studying process and it will only serve that target alone.
for more original information:
http://www.chromium.org/developers/design-documents/rappor
https://github.com/google/rappor
Erlingsson Ú, Pihur V, Korolova A. Rappor: Randomized aggregatable privacy-preserving ordinal response[C]//Proceedings of the 2014 ACM SIGSAC conference on computer and communications security. 2014: 1054-1067.

### 1. Generating Random Bits for RAPPOR
https://github.com/google/rappor/blob/master/doc/randomness.md
```
To ensure privacy, an application using RAPPOR must generate random bits in an unpredictable manner. 
In other words, an adversary that can predict the sequence of random bits used can determine the true values being reported.
Generating random numbers is highly platform-specific -- even language-specific.
 So, libraries implementing RAPPOR should be parameterized by an interface to generate random bits. (This can be thought of as "dependency injection".)

```
#### 1.1 _SecureRandom
- description : an callable object
- function: Returns an integer where each bit has probability p of being 1.
```python
        r = 0
        for i in range(self.num_bits):
            bit = rand.random() < p
            r |= (bit << i)  # using bool as int
        return r
```
- args: params
    - params: rappor.Params
- elements: prob_one , num_bits
    - prob_one: probability p
    - num_bits: length of integer bits

#### 1.2 SecureIrrRand
- description : an interface
- function: IRR randomness interface.
```python
        num_bits = params.num_bloombits
        # IRR probabilities
        self.p_gen = _SecureRandom(params.prob_p, num_bits)
        self.q_gen = _SecureRandom(params.prob_q, num_bits)
```
- args: params
    - params: rappor.Params
- elements : num_bits, p_gen, q_gen
    - num_bits: length of integer bits
    - p_gen: generate a bit string of length num_bits, every bit has probability p being 1
    - q_gen: generate a bit string of length num_bits, every bit has probability q being 1

#### 1.3 Params
- description : parameter container
- function: define all the parameter RAPPOR need
- elements: num_bloombits, num_hashes, num_cohorts, prob_p, prob_q, prob_f
    - num_bloombits: Number of bloom filter bits (k) 16
    - num_hashes: Number of bloom filter hashes (h) 2
    - num_cohorts: Number of cohorts (m) 64
    - prob_p: Probability p 0.50  
    - prob_q: Probability q 0.75   
    - prob_f: Probability f 0.50 

### 2. Core mechanism
#### 2.1  Encode a integer with RAPPOR
2.1.1 Signal
Hash client's value v onto the Bloom filter B of size k using h hash functions.
