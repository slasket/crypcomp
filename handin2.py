import random
import numpy as np
import handin1


class Dealer:
    def __init__(self, n=3):
        self.n = np.power(2, n)
        self.r = random.randint(0, self.n - 1)
        self.s = random.randint(0, self.n - 1)
        self.mB = np.random.randint(2, size=(self.n, self.n))
        self.tt = np.matrix([
            [1, 0, 0, 0, 0, 0, 0, 0],  # o- /0
            [1, 1, 0, 0, 0, 0, 0, 0],  # o+ /1
            [1, 0, 1, 0, 0, 0, 0, 0],  # b- /2
            [1, 1, 1, 1, 0, 0, 0, 0],  # b+ /3
            [1, 0, 0, 0, 1, 0, 0, 0],  # a- /4
            [1, 1, 0, 0, 1, 1, 0, 0],  # a+ /5
            [1, 0, 1, 0, 1, 0, 1, 0],  # ab-/6
            [1, 1, 1, 1, 1, 1, 1, 1],  # ab+/7
        ])
        # shifting for the mixed truth table
        self.shiftedtt = np.roll(self.tt, self.r, axis=0)
        self.shiftedtt = np.roll(self.shiftedtt, self.s, axis=1)
        #print(self.shiftedtt)
        self.mA = np.bitwise_xor(self.mB, self.shiftedtt)


class Alice:
    def __init__(self, bt, dealerR, mA, dealerN):
        self.bt = bt
        self.u = (bt + dealerR) % dealerN
        self.mA = mA

    def send(self):
        return self.u

    def receive(self, bobans):
        #print(np.bitwise_xor(self.mA, bobans[2]))
        #print("shifted,shifted after xor")
        return np.bitwise_xor(self.mA[self.u, bobans[0]], bobans[1])


class Bob:
    def __init__(self, bt, dealerS, mB, dealerN):
        self.bt = bt
        self.v = (bt + dealerS) % dealerN
        self.mB = mB
        self.u = None

    def receive(self, u):
        self.u = u

    def send(self):
        return [self.v, self.mB[self.u, self.v], self.mB]


def oneTimeTable(aliceBloodType, bobBloodType):
    dealer = Dealer()
    alice = Alice(aliceBloodType, dealer.r, dealer.mA, dealer.n)
    bob = Bob(bobBloodType, dealer.s, dealer.mB, dealer.n)
    bob.receive(alice.send())
    return alice.receive(bob.send())


def testAllCombinations():
    for i in range(8):
        iBin = format(i, "b")
        for j in range(8):
            jBin = format(j, "b")
            oneTimeVal = oneTimeTable(i, j)
            if (handin1.bloodCompLookup(i, j) != oneTimeVal):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j),"OTT:", oneTimeVal)


    return print("All combinations tested")


def main():
    print(oneTimeTable(0, 0))
    print(oneTimeTable(6, 1))
    testAllCombinations()


if __name__ == "__main__":
    main()
