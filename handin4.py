import secrets

import handin1

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

# BeDOZa protocol for blood type compatability
def ot(aliceBt, bobBt):
    return 0

# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    for i in range(8):
        for j in range(8):
            otRes = ot(i, j)
            if (handin1.bloodCompLookup(i, j) != otRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", otRes)

    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
