import laplace as lap


def test():
    e = lap.Encoder(4.0, 10)
    print(e.encode_bits(5))


test()
