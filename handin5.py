import hashlib as hash
import numpy as np
import secrets

class Alice:
    def __init__(self, bt):
        self.bt = bt


class Bob:
    def __init__(self, bt):
        self.bt = bt


def generateGarbleKeys(circuitSize=23):
    wireKeys = np.zeros(circuitSize, dtype=object)

    for i in range(len(wireKeys)):
        randomKey1 = secrets.randbits(128)
        randomKey2 = secrets.randbits(128)
        wireKeys[i] = randomKey1, randomKey2
    return wireKeys

def byte_xor(ba1, ba2):
    return bytes([_a ^ _b for _a, _b in zip(ba1, ba2)])

def garbleMyGate(gate, left, right, output):
    if gate == "AND":
        #[0, 0, 0]
        #[1, 0, 0]
        #[0, 1, 0]
        #[1, 1, 1]
        L0, L1 = left
        R0, R1 = right
        K0, K1 = output
        xd = bytes(str(L0) + str(R0), 'utf-8')
        c1 = hash.sha256(xd).digest() ^ bytes(K0)
        #c2 = byte_xor(hash.sha256(L1 + R0).digest(), K0)
        #c3 = byte_xor(hash.sha256(L0 + R1).digest(), K0)
        #c4 = byte_xor(hash.sha256(L1 + R1).digest(), K1)
        #print(c1)
    elif gate == "XOR":
        pass

def garbleMyCircuit():
    wireKeys = generateGarbleKeys()

    inputWires = 12
    # d = (Z0, Z1)
    d = wireKeys[len(wireKeys)-1]
    garbleMyGate("AND", left=wireKeys[0], right=wireKeys[1], output=wireKeys[2])



def main():
    garbleMyCircuit()


if __name__ == "__main__":
    main()
