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
    def __init__(self, alice, ua, va, wa, xa, ya):

        self.alice = alice
        self.ua = ua
        self.va = va
        self.wa = wa

        self.xa = xa
        self.ya = ya

        self.da = None
        self.d = None
        self.e = None

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
    def __init__(self, bob, ub, vb, wb, xb, yb):

        self.bob = bob

        self.ub = ub
        self.vb = vb
        self.wb = wb

        self.xb = xb
        self.yb = yb

        self.d = None
        self.e = None

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
def andProtocol(alice, bob, dealer, x, y):
    aliceAnd = AliceAnd(alice, dealer.ua, dealer.va, dealer.wa)
    bobAnd = BobAnd(bob, dealer.ub, dealer.vb, dealer.wb)

    bobAnd.received(aliceAnd.calcd(bobAnd.calcdb()))
    bobAnd.receivee(aliceAnd.calce(bobAnd.calceb()))

    Alice.za1 = aliceAnd.calcza()
    Bob.zb1 = bobAnd.calczb()


# Alice class to represent Alice's part of communication
class Alice:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr

        self.za1 = None
        self.za2 = None
        self.za3 = None
        self.za4 = None
        self.za5 = None


# Bob class to represent Bob's part of communication
class Bob:
    def __init__(self, bta, btb, btr):
        self.bta = bta
        self.btb = btb
        self.btr = btr

        self.zb1 = None
        self.zb2 = None
        self.zb3 = None
        self.zb4 = None
        self.zb5 = None

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


    res1 = xorCProtocol(andProtocol(alice, bob, dealer1, xorCProtocol(alice.bta, 1), bob.bta), 1)
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
