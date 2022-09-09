import random
import numpy as np
import handin1

# Dealer class to represent trusted dealer as described in the document.
class Dealer:
    def __init__(self, n=3):
        # n is chosen default as 3
        self.n = np.power(2, n)

        # r & s is randomly chosen
        self.r = random.randint(0, self.n - 1)
        self.s = random.randint(0, self.n - 1)

        # mB uniformly random with size n^2
        self.mB = np.random.randint(2, size=(self.n, self.n))

        # original blood compatability table from handin 1
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

        # shifting for the mixed truth table to the right with r steps and down with s steps
        self.shiftedtt = np.roll(self.tt, self.r, axis=0)
        self.shiftedtt = np.roll(self.shiftedtt, self.s, axis=1)

        # constructing mA as the XOR of the shifted table and mB
        self.mA = np.bitwise_xor(self.mB, self.shiftedtt)

# Alice class to represent Alice's part of communication
class Alice:
    # init with the blood type and r, matrix mA and the length n from the dealer.
    def __init__(self, bt, dealerR, mA, dealerN):
        self.bt = bt
        #Local compute u from bt and r mod n
        self.u = (bt + dealerR) % dealerN
        self.mA = mA

    # function to "send" u to Bob
    def send(self):
        return self.u

    # function to "receive" v and mB[u,v] from Bob
    def receive(self, bobans):
        return np.bitwise_xor(self.mA[self.u, bobans[0]], bobans[1])

# Bob class to represent Bob's part of communication
class Bob:
    # init with the blood type and r, matrix mA and the length n from the dealer.
    def __init__(self, bt, dealerS, mB, dealerN):
        self.bt = bt
        #Local compute v from bt and s mod n
        self.v = (bt + dealerS) % dealerN
        self.mB = mB
        # field for "receiving" u
        self.u = None

    # function to "receive" u from Alice
    def receive(self, u):
        self.u = u

    # function to "send" v and mB[u,v] to Alice
    def send(self):
        return [self.v, self.mB[self.u, self.v]]


# Function to preform the protocol between Alice and Bob
def oneTimeTable(aliceBloodType, bobBloodType):
    dealer = Dealer()
    alice = Alice(aliceBloodType, dealer.r, dealer.mA, dealer.n)
    bob = Bob(bobBloodType, dealer.s, dealer.mB, dealer.n)
    bob.receive(alice.send())
    return alice.receive(bob.send())

# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    for i in range(8):
        for j in range(8):
            oneTimeVal = oneTimeTable(i, j)
            if (handin1.bloodCompLookup(i, j) != oneTimeVal):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j),"OTT:", oneTimeVal)

    return print("All combinations tested")

# Main function to call testAllCombinations()
def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
