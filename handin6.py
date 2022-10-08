import random
import secrets
import handin1

cr = secrets.SystemRandom()

# Key generation. Generates public and secret key
#shit
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

# Encryption function that samples a random amount of yis from the public key for encryption
def encrypt(m, yi):
    s = secrets.SystemRandom.randint(cr, 1, 100)
    random_yi = random.sample(yi, s)
    for i, y in enumerate(random_yi):
        m = m + y
    return m

# Decryption function that samples mods with the secret key p and 2
def decrypt(c, p):
    m = (c % p) % 2
    return m

# Alice class representing one party of the communication
class Alice:
    def __init__(self, bt):
        self.bt = bt
        p, qi, ri, yi = keyGen(100)
        self.p = p
        self.qi = qi
        self.ri = ri
        self.yi = yi

    # Alice encrypts her blood type and returns it
    def choose(self):
        a = handin1.check_nth_bit(self.bt, 2)
        b = handin1.check_nth_bit(self.bt, 1)
        r = handin1.check_nth_bit(self.bt, 0)

        m1 = (encrypt(a, self.yi), encrypt(b, self.yi), encrypt(r, self.yi))

        return m1

    # shares public key
    def share_pk(self):
        return self.yi

    # decrypts the received message
    def retrieve(self, m2):
        res = decrypt(m2, self.p)

        return res

# Bob class representing one party of the communication
class Bob:
    def __init__(self, bt):
        self.bt = bt

    # Receives an encrypted message, encrypts Bobs message and calculates the blood type compatability function
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

# Function that simulates the d-HE scheme between Alice and Bob
def protocol(i, j):
    alice = Alice(i)
    bob = Bob(j)

    m1 = alice.choose()
    m2 = bob.transfer(m1, alice.share_pk())
    res = alice.retrieve(m2)
    return res


# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    for i in range(8):
        for j in range(8):
            gcRes = protocol(i, j)
            if (handin1.bloodCompLookup(i, j) != gcRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", gcRes)
    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
