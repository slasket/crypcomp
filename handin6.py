import random
import secrets
import handin1

cr = secrets.SystemRandom()


def keyGen(n, psec=500, qsec=100000, rsec=30):
    p = secrets.SystemRandom.getrandbits(cr, psec)
    if p % 2 == 0:
        p = p + 1
    qi = []
    ri = []
    yi = []
    for i in range(n):
        q = secrets.SystemRandom.getrandbits(cr, qsec)
        qi.append(q)
        r = secrets.SystemRandom.getrandbits(cr, rsec)
        ri.append(r)
        yi.append(p * qi[i] + 2 * ri[i])
    return p, qi, ri, yi


def encrypt(m, yi):
    s = secrets.SystemRandom.randint(cr, 1, 100)
    random_yi = random.sample(yi, s)
    for i, y in enumerate(random_yi):
        m = m + y
    return m


def decrypt(c, p):
    m = (c % p) % 2
    return m


class Alice:
    def __init__(self, bt):
        self.bt = bt
        p, qi, ri, yi = keyGen(100)
        self.p = p
        self.qi = qi
        self.ri = ri
        self.yi = yi

    def choose(self):
        a = handin1.check_nth_bit(self.bt, 2)
        b = handin1.check_nth_bit(self.bt, 1)
        r = handin1.check_nth_bit(self.bt, 0)

        m1 = (encrypt(a, self.yi), encrypt(b, self.yi), encrypt(r, self.yi))

        return m1

    def share_pk(self):
        return self.yi

    def retrieve(self, m2):
        res = decrypt(m2, self.p)

        return res


class Bob:
    def __init__(self, bt):
        self.bt = bt

    def transfer(self, m1, yi):
        a = handin1.check_nth_bit(self.bt, 2)
        b = handin1.check_nth_bit(self.bt, 1)
        r = handin1.check_nth_bit(self.bt, 0)

        m2 = (encrypt(a, yi),
              encrypt(b, yi),
              encrypt(r, yi))

        one = encrypt(1, yi)

        res_encrypted = (
                (one + ((one + m1[0]) * m2[0])) *
                (one + ((one + m1[1]) * m2[1])) *
                (one + ((one + m1[2]) * m2[2]))
        )

        return res_encrypted


def protocol(i, j):
    alice = Alice(i)
    bob = Bob(j)

    m1 = alice.choose()
    m2 = bob.transfer(m1, alice.share_pk())
    res = alice.retrieve(m2)
    return res


# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    otResArray = [
        [1, 0, 0, 0, 0, 0, 0, 0],  # o- /0
        [1, 1, 0, 0, 0, 0, 0, 0],  # o+ /1
        [1, 0, 1, 0, 0, 0, 0, 0],  # b- /2
        [1, 1, 1, 1, 0, 0, 0, 0],  # b+ /3
        [1, 0, 0, 0, 1, 0, 0, 0],  # a- /4
        [1, 1, 0, 0, 1, 1, 0, 0],  # a+ /5
        [1, 0, 1, 0, 1, 0, 1, 0],  # ab-/6
        [1, 1, 1, 1, 1, 1, 1, 1],  # ab+/7
    ]
    for i in range(8):
        for j in range(8):
            gcRes = protocol(i, j)
            otResArray[i][j] = gcRes
            if (handin1.bloodCompLookup(i, j) != gcRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", gcRes)
        # for i in range(8):
        # print(otResArray[i])
    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
