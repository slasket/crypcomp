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
    print("Eval")
    for i, cipher in enumerate(garbledGate):
        keyCandidate = cipher ^ c1
        print(format(keyCandidate, '0128b'))
        if (format(keyCandidate, '0128b')[-128:]) == "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
            return format(keyCandidate, '0256b')[:128]

def garbleMyGate(gate, left, right, output):
    L0, L1 = left
    R0, R1 = right
    K0, K1 = output
    K0_with_redundancy = K0 << 128 #int.from_bytes(bytearray(K0.to_bytes(128, "big")) + bytearray(128), "big")
    K1_with_redundancy = K1 << 128 #int.from_bytes(bytearray(K1.to_bytes(128, "big")) + bytearray(128), "big")
    print("gg")
    print(K1_with_redundancy)
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
    garbledGate = garbleMyGate("XOR", left=wireKeys[0], right=wireKeys[1], output=wireKeys[2])
    L0, L1 = wireKeys[0]
    R0, R1 = wireKeys[1]
    K0, K1 = wireKeys[2]
    temp = evaluation(L1, R1, garbledGate)
    print("k0", format(K0, '0128b'))
    print("k1", format(K1, '0128b'))
    print("Result")
    print(temp)
    print(format(K0, '0128b'))


def main():
    garbleMyCircuit()


if __name__ == "__main__":
    main()
