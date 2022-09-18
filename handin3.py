import secrets

import handin1

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
    def __init__(self, ua, va, wa, x):
        self.ua = ua
        self.va = va
        self.wa = wa

        self.x = x
        self.xa = secrets.randbits(1)
        self.xb = self.x ^ self.xa

        self.ya = None
        self.da = None
        self.d = None
        self.e = None

    def sharexb(self):
        return self.xb

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
    def __init__(self, ub, vb, wb, y):
        self.ub = ub
        self.vb = vb
        self.wb = wb

        self.y = y
        self.ya = secrets.randbits(1)
        self.yb = self.y ^ self.ya

        self.xb = None

        self.d = None
        self.e = None

    def shareya(self):
        return self.ya

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
def andProtocol(x, y, dealer):
    aliceAnd = AliceAnd(dealer.ua, dealer.va, dealer.wa, x)
    bobAnd = BobAnd(dealer.ub, dealer.vb, dealer.wb, y)

    aliceAnd.receiveya(bobAnd.shareya())
    bobAnd.receivexb(aliceAnd.sharexb())

    bobAnd.received(aliceAnd.calcd(bobAnd.calcdb()))
    bobAnd.receivee(aliceAnd.calce(bobAnd.calceb()))

    return aliceAnd.calcza() ^ bobAnd.calczb()


# Alice class to represent Alice's part of communication
class Alice:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr


# Bob class to represent Bob's part of communication
class Bob:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr

# Function for simulating XOR with a constant
def xorCProtocol(x, c):
    return x ^ c

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

    res1 = xorCProtocol(andProtocol(xorCProtocol(alice.bta, 1), bob.bta, dealer1), 1)
    res2 = xorCProtocol(andProtocol(xorCProtocol(alice.btb, 1), bob.btb, dealer2), 1)
    res3 = xorCProtocol(andProtocol(xorCProtocol(alice.btr, 1), bob.btr, dealer3), 1)
    res4 = andProtocol(res1, res2, dealer4)
    res5 = andProtocol(res3, res4, dealer5)

    return res5


# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    for i in range(8):
        for j in range(8):
            bedozaRes = bedozaProtocol(i, j)
            if (handin1.bloodCompLookup(i, j) != bedozaRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "BDOZ:", bedozaRes)

    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
