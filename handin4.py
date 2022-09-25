import secrets
import random

import handin1
import elgamal
import numpy as np


# Alice class to represent Alice's part of communication
class Alice:
    def __init__(self, bt):
        self.bt = bt
        self.pkArray = []
        self.p = None
        self.key = None
        self.q = None
        self.g = None
        self.h = None

    def keyGen(self):
        self.q = random.randint(pow(10,20),pow(10,50))
        self.g = random.randint(2, self.q)
        self.key = elgamal.gen_key(self.q)
        self.h = elgamal.power(self.g, self.key, self.q)
        return self.g, self.h

    def oGen(self):
        g = random.randint(2, self.q)
        tal = pow(10,50) + 1
        bitlength = tal.bit_length()
        r = random.randint(1, pow(2, 2 * bitlength))
        rmodq = r % self.q
        h = pow(rmodq, 2) % self.q
        return [g, h]

    def createPKArray(self):
        self.keyGen()
        for i in range(0, 8):
            self.pkArray.append(self.oGen())
        self.pkArray[self.bt] = [self.g, self.h]
        return self.pkArray, self.q

    def receiveCipherArray(self, cArray):
        ct, p = cArray[self.bt]
        res = elgamal.decrypt(ct, p, self.key, self.q)
        return res


# Bob class to represent Bob's part of communication
class Bob:
    def __init__(self, bt):
        self.bt = bt

    def receiveArray(self, pkArray, q):
        nparray = np.array(handin1.tt)
        btSlice = nparray[:, self.bt]
        resArray = []
        for i in range(0, 8):
            m = btSlice[i]
            resArray.append(elgamal.encryption(str(m), q, pkArray[i][1], pkArray[i][0]))

        return resArray

# OT protocol for blood type compatability
def ot(aliceBt, bobBt):
    alice = Alice(aliceBt)
    bob = Bob(bobBt)
    pkArray, q = alice.createPKArray()
    resArray = bob.receiveArray(pkArray, q)
    res = alice.receiveCipherArray(resArray)
    return int(res)


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
            otRes = ot(i, j)
            otResArray[i][j] = otRes
            if (handin1.bloodCompLookup(i, j) != otRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", otRes)
    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
