import secrets

import handin1
import numpy as np

# Dealer class to represent trusted dealer that generates [u],[v],[w]
class Dealer:
    def __init__(self):
        self.u = secrets.randbits(1)
        self.ua = secrets.randbits(1)
        self.ub = self.u ^ self.ua

        self.v = secrets.randbits(1)
        self.va = secrets.randbits(1)
        self.vb = self.v ^ self.va

        # self.w = (self.ua ^ self.ub) & (self.va ^ self.vb)
        self.w = self.u & self.v
        self.wa = secrets.randbits(1)
        self.wb = self.w ^ self.wa

# Alice class for the and subroutine
class AliceAnd:
    def __init__(self, ua, va, wa, xa):
        self.ua = ua
        self.va = va
        self.wa = wa
        self.xa = xa


        self.ya = None
        self.da = None
        self.d = None
        self.e = None

    def receiveya(self, ya):
        self.ya = ya

    def calcd(self, db):
        self.da = self.xa ^ self.ua
        self.d = self.da ^ db
        return self.d

    def calce(self, eb):
        ea = self.ya ^ self.va
        self.e = ea ^ eb
        return self.e

    def calcza(self):
        # za = self.wa ^ (self.e & self.xa) ^ (self.d & self.ya) ^ (self.e & self.d)
        za = self.wa ^ (self.e & self.xa) ^ (self.d & self.ya) ^ (self.e & self.d)
        return za

# Bob class for the and subroutine
class BobAnd:
    def __init__(self, ub, vb, wb, yb):
        self.ub = ub
        self.vb = vb
        self.wb = wb
        self.yb = yb

        self.xb = None

        self.d = None
        self.e = None

    def receivexb(self, xb):
        self.xb = xb

    def calcdb(self):
        return self.xb ^ self.ub

    def calceb(self):
        return self.yb ^ self.vb

    def received(self, d):
        self.d = d

    def receivee(self, e):
        self.e = e

    def calczb(self):
        # zb = self.wb ^ (self.e & self.xb) ^ (self.d & self.yb) ^ (self.e & self.d)
        zb = self.wb ^ (self.e & self.xb) ^ (self.d & self.yb)
        return zb


# subroutine for and protocol. Takes dealer as input for new U,V,W.
def andProtocol(xa, xb, ya, yb, dealer):
    aliceAnd = AliceAnd(dealer.ua, dealer.va, dealer.wa, xa)
    bobAnd = BobAnd(dealer.ub, dealer.vb, dealer.wb, yb)

    aliceAnd.receiveya(ya)
    bobAnd.receivexb(xb)

    bobAnd.received(aliceAnd.calcd(bobAnd.calcdb()))
    bobAnd.receivee(aliceAnd.calce(bobAnd.calceb()))

    return aliceAnd.calcza(), bobAnd.calczb()


# Alice class to represent Alice's part of communication
class Alice:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr
        self.calcs = [0]*17


# Bob class to represent Bob's part of communication
class Bob:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr
        self.calcs = [0]*17

# Function for simulating XOR with a constant
def xorCProtocol(x, y, c):
    return x ^ c, y

def secretShare(x):
    xa = secrets.randbits(1)
    xb = x ^ xa

    return xa, xb

# BeDOZa protocol for blood type compatability
def bedozaProtocol(aliceBt, bobBt):
    ba = handin1.check_nth_bit(bobBt, 2)
    bb = handin1.check_nth_bit(bobBt, 1)
    br = handin1.check_nth_bit(bobBt, 0)

    aa = handin1.check_nth_bit(aliceBt, 2)
    ab = handin1.check_nth_bit(aliceBt, 1)
    ar = handin1.check_nth_bit(aliceBt, 0)

    dealer1 = Dealer()
    dealer2 = Dealer()
    dealer3 = Dealer()
    dealer4 = Dealer()
    dealer5 = Dealer()

    alice = Alice(aa, ab, ar)
    bob = Bob(ba, bb, br)

    alice.calcs[0], bob.calcs[0] = secretShare(alice.bta)
    alice.calcs[1], bob.calcs[1] = xorCProtocol(alice.calcs[0], bob.calcs[0], 1)
    alice.calcs[2], bob.calcs[2] = secretShare(bob.bta)
    alice.calcs[3], bob.calcs[3] = andProtocol(alice.calcs[1], bob.calcs[1], alice.calcs[2], bob.calcs[2], dealer1)
    alice.calcs[4], bob.calcs[4] = xorCProtocol(alice.calcs[3], bob.calcs[3], 1)

    alice.calcs[5], bob.calcs[5] = secretShare(alice.btb)
    alice.calcs[6], bob.calcs[6] = xorCProtocol(alice.calcs[5], bob.calcs[5], 1)
    alice.calcs[7], bob.calcs[7] = secretShare(bob.btb)
    alice.calcs[8], bob.calcs[8] = andProtocol(alice.calcs[6], bob.calcs[6],  alice.calcs[7], bob.calcs[7], dealer2)
    alice.calcs[9], bob.calcs[9] = xorCProtocol(alice.calcs[8], bob.calcs[8], 1)

    alice.calcs[10], bob.calcs[10] = secretShare(alice.btr)
    alice.calcs[11], bob.calcs[11] = xorCProtocol(alice.calcs[10], bob.calcs[10], 1)
    alice.calcs[12], bob.calcs[12] = secretShare(bob.btr)
    alice.calcs[13], bob.calcs[13] = andProtocol(alice.calcs[11], bob.calcs[11],  alice.calcs[12], bob.calcs[12], dealer3)
    alice.calcs[14], bob.calcs[14] = xorCProtocol(alice.calcs[13], bob.calcs[13], 1)

    alice.calcs[15], bob.calcs[15] = andProtocol(alice.calcs[4], bob.calcs[4],  alice.calcs[9], bob.calcs[9], dealer4)
    alice.calcs[16], bob.calcs[16] = andProtocol(alice.calcs[14], bob.calcs[14],  alice.calcs[15], bob.calcs[15], dealer5)
    res = alice.calcs[16] ^ bob.calcs[16]

    return res


# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    tt = np.array([
        [1, 0, 0, 0, 0, 0, 0, 0],  # o- /0
        [1, 1, 0, 0, 0, 0, 0, 0],  # o+ /1
        [1, 0, 1, 0, 0, 0, 0, 0],  # b- /2
        [1, 1, 1, 1, 0, 0, 0, 0],  # b+ /3
        [1, 0, 0, 0, 1, 0, 0, 0],  # a- /4
        [1, 1, 0, 0, 1, 1, 0, 0],  # a+ /5
        [1, 0, 1, 0, 1, 0, 1, 0],  # ab-/6
        [1, 1, 1, 1, 1, 1, 1, 1],  # ab+/7
    ])
    for i in range(8):
        for j in range(8):
            bedozaRes = bedozaProtocol(i, j)
            if (handin1.bloodCompLookup(i, j) != bedozaRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "BDOZ:", bedozaRes)

            tt[i,j] = bedozaRes
    print(tt)
    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
