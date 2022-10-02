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

def evaluation(keyLeft, keyRight, garbledGate):
    c1 = int(hash.sha256(bytes(str(keyLeft) + str(keyRight), 'utf-8')).hexdigest(), base=16)
    for i, cipher in enumerate(garbledGate):
        keyCandidate = cipher ^ c1
        bitKey = format(keyCandidate, '0256b')
        if (bitKey[-128:]) == "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
            return int(bitKey[:128],2)

def garbleMyGate(gate, left, right, output):
    L0, L1 = left
    R0, R1 = right
    K0, K1 = output
    K0_with_redundancy = K0 << 128 #int.from_bytes(bytearray(K0.to_bytes(128, "big")) + bytearray(128), "big")
    K1_with_redundancy = K1 << 128 #int.from_bytes(bytearray(K1.to_bytes(128, "big")) + bytearray(128), "big")
    if gate == "AND":
        #[0, 0, 0]
        #[1, 0, 0]
        #[0, 1, 0]
        #[1, 1, 1]
        c1 = int(hash.sha256(bytes(str(L0) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c2 = int(hash.sha256(bytes(str(L1) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c3 = int(hash.sha256(bytes(str(L0) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c4 = int(hash.sha256(bytes(str(L1) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        ciphertexts = np.random.permutation(np.array([c1, c2, c3, c4]))
        return ciphertexts
    elif gate == "XOR":
        #[0, 0, 0]
        #[1, 0, 1]
        #[0, 1, 1]
        #[1, 1, 0]
        c1 = int(hash.sha256(bytes(str(L0) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c2 = int(hash.sha256(bytes(str(L1) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        c3 = int(hash.sha256(bytes(str(L0) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        c4 = int(hash.sha256(bytes(str(L1) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        ciphertexts = np.random.permutation(np.array([c1, c2, c3, c4]))
        return ciphertexts


def garbleMyCircuit():
    wireKeys = generateGarbleKeys()

    inputWires = 2
    # d = (Z0, Z1)
    d = wireKeys[len(wireKeys)-1]
    garbledGate1 = garbleMyGate("AND", left=wireKeys[0], right=wireKeys[1], output=wireKeys[2])
    garbledGate2 = garbleMyGate("AND", left=wireKeys[3], right=wireKeys[4], output=wireKeys[5])
    garbledGate3 = garbleMyGate("AND", left=wireKeys[2], right=wireKeys[5], output=wireKeys[8])
    aL0, aL1 = wireKeys[0]
    aR0, aR1 = wireKeys[1]
    svar0 = evaluation(aL1, aR1, garbledGate1)
    print("svar0", svar0)

    bL0, bL1 = wireKeys[3]
    bR0, bR1 = wireKeys[4]
    svar1 = evaluation(bL1, bR1, garbledGate2)
    print("svar1", svar1)
    forket, svar = wireKeys[8]
    cL0, cL1 = wireKeys[2]
    cR0, cR1 = wireKeys[5]
    print("cL1", cL1)
    print("cR1", cR1)
    temp1 = evaluation(svar0, svar1, garbledGate3)
    #temp2 = evaluation(cL1, cR1, garbledGate3)

    print("Result")
    print(temp1)
    #print(temp2)
    print(svar)


def main():
    garbleMyCircuit()


if __name__ == "__main__":
    main()
