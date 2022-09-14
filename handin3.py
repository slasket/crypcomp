import random
import numpy as np

import random


class Dealer:
    def __init__(self):
        self.u = random.randint(0, 1)
        self.ua = random.randint(0, 1)
        self.ub = self.u ^ self.ua

        self.v = random.randint(0, 1)
        self.va = random.randint(0, 1)
        self.vb = self.v ^ self.va

        # self.w = (self.ua ^ self.ub) & (self.va ^ self.vb)
        self.w = self.u & self.v
        self.wa = random.randint(0, 1)
        self.wb = self.w ^ self.wa


class Alice:
    def __init__(self, ua, va, wa, x):
        self.ua = ua
        self.va = va
        self.wa = wa

        self.x = x
        self.xa = random.randint(0, 1)
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
        za = (self.wa ^ self.e) & (self.xa ^ self.d) & (self.ya ^ self.e) & self.d
        return za


class Bob:
    def __init__(self, vb, ub, wb, y):
        self.ub = ub
        self.vb = vb
        self.wb = wb

        self.y = y
        self.ya = random.randint(0, 1)
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
        zb = (self.wb ^ self.e) & (self.xb ^ self.d) & (self.yb ^ self.e) & self.d
        return zb


def protocol(x, y):
    dealer = Dealer()
    alice = Alice(dealer.ua, dealer.va, dealer.wa, x)
    bob = Bob(dealer.ub, dealer.vb, dealer.wb, y)

    alice.receiveya(bob.shareya())
    bob.receivexb(alice.sharexb())

    bob.received(alice.calcd(bob.calcdb()))
    bob.receivee(alice.calce(bob.calceb()))

    return alice.calcza() ^ bob.calczb()


def main():
    print("0,0")
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print(protocol(0, 0))
    print("1,0")
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print(protocol(1, 0))
    print("0,1")
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print(protocol(0,1))
    print("1,1")
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))
    print(protocol(1,1))


if __name__ == "__main__":
    main()
