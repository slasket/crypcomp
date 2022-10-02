import hashlib as hash
import numpy as np
import secrets
import handin1


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
        if (bitKey[
            -128:]) == "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
            return int(bitKey[:128], 2)


def garbleMyGate(gate, left, right, output):
    L0, L1 = left
    R0, R1 = right
    K0, K1 = output
    K0_with_redundancy = K0 << 128  # int.from_bytes(bytearray(K0.to_bytes(128, "big")) + bytearray(128), "big")
    K1_with_redundancy = K1 << 128  # int.from_bytes(bytearray(K1.to_bytes(128, "big")) + bytearray(128), "big")
    if gate == "AND":
        # [0, 0, 0]
        # [1, 0, 0]
        # [0, 1, 0]
        # [1, 1, 1]
        c1 = int(hash.sha256(bytes(str(L0) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c2 = int(hash.sha256(bytes(str(L1) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c3 = int(hash.sha256(bytes(str(L0) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c4 = int(hash.sha256(bytes(str(L1) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        ciphertexts = np.random.permutation(np.array([c1, c2, c3, c4]))
        return ciphertexts
    elif gate == "XOR":
        # [0, 0, 0]
        # [1, 0, 1]
        # [0, 1, 1]
        # [1, 1, 0]
        c1 = int(hash.sha256(bytes(str(L0) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        c2 = int(hash.sha256(bytes(str(L1) + str(R0), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        c3 = int(hash.sha256(bytes(str(L0) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K1_with_redundancy
        c4 = int(hash.sha256(bytes(str(L1) + str(R1), 'utf-8')).hexdigest(), base=16) ^ K0_with_redundancy
        ciphertexts = np.random.permutation(np.array([c1, c2, c3, c4]))
        return ciphertexts


def garbleMyCircuit(aliceBt, bobBt):

    ba = handin1.check_nth_bit(bobBt, 2)
    bb = handin1.check_nth_bit(bobBt, 1)
    br = handin1.check_nth_bit(bobBt, 0)

    aa = handin1.check_nth_bit(aliceBt, 2)
    ab = handin1.check_nth_bit(aliceBt, 1)
    ar = handin1.check_nth_bit(aliceBt, 0)


    wireKeys = generateGarbleKeys()

    inputWires = 2
    # d = (Z0, Z1)
    d = wireKeys[len(wireKeys) - 1]

    gates = []
    # garbledGateXOR1 = garbleMyGate("XOR", left=wireKeys[1], right=wireKeys[2], output=wireKeys[12])
    # garbledGateXOR2 = garbleMyGate("XOR", left=wireKeys[5], right=wireKeys[6], output=wireKeys[13])
    # garbledGateXOR3 = garbleMyGate("XOR", left=wireKeys[9], right=wireKeys[10], output=wireKeys[14])

    # garbledGateAND3 = garbleMyGate("AND", left=wireKeys[12], right=wireKeys[3], output=wireKeys[15])
    # garbledGateAND4 = garbleMyGate("AND", left=wireKeys[13], right=wireKeys[7], output=wireKeys[16])
    # garbledGateAND5 = garbleMyGate("AND", left=wireKeys[14], right=wireKeys[11], output=wireKeys[17])

    # garbledGateXOR6 = garbleMyGate("XOR", left=wireKeys[0], right=wireKeys[15], output=wireKeys[18])
    # garbledGateXOR7 = garbleMyGate("XOR", left=wireKeys[4], right=wireKeys[16], output=wireKeys[19])
    # garbledGateXOR8 = garbleMyGate("XOR", left=wireKeys[8], right=wireKeys[17], output=wireKeys[20])

    # garbledGateAND9 = garbleMyGate("AND", left=wireKeys[19], right=wireKeys[20], output=wireKeys[21])
    # garbledGateAND10 = garbleMyGate("AND", left=wireKeys[18], right=wireKeys[21], output=wireKeys[22])

    gates.append(garbleMyGate("XOR", left=wireKeys[1], right=wireKeys[2], output=wireKeys[12]))
    gates.append(garbleMyGate("XOR", left=wireKeys[5], right=wireKeys[6], output=wireKeys[13]))
    gates.append(garbleMyGate("XOR", left=wireKeys[9], right=wireKeys[10], output=wireKeys[14]))

    gates.append(garbleMyGate("AND", left=wireKeys[12], right=wireKeys[3], output=wireKeys[15]))
    gates.append(garbleMyGate("AND", left=wireKeys[13], right=wireKeys[7], output=wireKeys[16]))
    gates.append(garbleMyGate("AND", left=wireKeys[14], right=wireKeys[11], output=wireKeys[17]))

    gates.append(garbleMyGate("XOR", left=wireKeys[0], right=wireKeys[15], output=wireKeys[18]))
    gates.append(garbleMyGate("XOR", left=wireKeys[4], right=wireKeys[16], output=wireKeys[19]))
    gates.append(garbleMyGate("XOR", left=wireKeys[8], right=wireKeys[17], output=wireKeys[20]))

    gates.append(garbleMyGate("AND", left=wireKeys[19], right=wireKeys[20], output=wireKeys[21]))
    gates.append(garbleMyGate("AND", left=wireKeys[18], right=wireKeys[21], output=wireKeys[22]))

    input = [1, 1,
             aa, ba,
             1, 1,
             ab, bb,
             1, 1,
             ar, br]
    inputKeys = [0] * 23

    for i in range(12):
        inputKeys[i] = wireKeys[i][input[i]]

    #print(inputKeys)

    #print(evaluation(inputKeys[1], inputKeys[2], gates[0]))
    inputKeys[12] = evaluation(inputKeys[1], inputKeys[2], gates[0])  # XOR
    inputKeys[13] = evaluation(inputKeys[5], inputKeys[6], gates[1])  # XOR
    inputKeys[14] = evaluation(inputKeys[9], inputKeys[10], gates[2])  # XOR

    inputKeys[15] = evaluation(inputKeys[12], inputKeys[3], gates[3])  # AND
    inputKeys[16] = evaluation(inputKeys[13], inputKeys[7], gates[4])  # AND
    inputKeys[17] = evaluation(inputKeys[14], inputKeys[11], gates[5])  # AND

    inputKeys[18] = evaluation(inputKeys[0], inputKeys[15], gates[6])  # XOR
    inputKeys[19] = evaluation(inputKeys[4], inputKeys[16], gates[7])  # XOR
    inputKeys[20] = evaluation(inputKeys[8], inputKeys[17], gates[8])  # XOR

    inputKeys[21] = evaluation(inputKeys[19], inputKeys[20], gates[9])  # AND
    inputKeys[22] = evaluation(inputKeys[18], inputKeys[21], gates[10])  # AND

    #print("res", inputKeys[22])
    #print("svar0", wireKeys[22][0])
    #print("svar1", wireKeys[22][1])

    if inputKeys[22] == wireKeys[22][1]:
        return 1
    elif inputKeys[22] == wireKeys[22][0]:
        return 0
    else:
        return "shit"
    # for i, gate in enumerate(gates):
    #    print(evaluation((inputKeys[(i*2)-1]),
    #                     (inputKeys[(i*2)]),
    #                     gate))

    # aL0, aL1 = wireKeys[0]
    # aR0, aR1 = wireKeys[1]
    # svar0 = evaluation(aL1, aR1, garbledGate1)
    # print("svar0", svar0)

    # bL0, bL1 = wireKeys[3]
    # bR0, bR1 = wireKeys[4]
    # svar1 = evaluation(bL1, bR1, garbledGate2)
    # print("svar1", svar1)
    # forket, svar = wireKeys[8]
    # cL0, cL1 = wireKeys[2]
    # cR0, cR1 = wireKeys[5]
    # print("cL1", cL1)
    # print("cR1", cR1)
    # temp1 = evaluation(svar0, svar1, garbledGate3)
    ##temp2 = evaluation(cL1, cR1, garbledGate3)

    # print("Result")
    # print(temp1)
    ##print(temp2)
    # print(svar)


# Function to test all blood type combinations through the protocol compared with the original unshifted truth table from handin 1.
def testAllCombinations():
    otResArray = [
    [1, 0, 0, 0, 0, 0, 0, 0],  # o- /0
    [1, 1, 0, 0, 0, 0, 0, 0],  # o+ /1
    [1, 0, 1, 0, 0, 0, 0, 0],  # b- /2
    [1, 1, 1, 1, 0, 0, 0, 0],  # b+ /3
    [1, 0, 0, 0, 1, 0, 0, 0],  # a- /4
    [1, 1, 0, 0, 1, 1, 0, 0],  # a+ /5
    [1, 0, 1, 0, 1, 0, 1, 0],  # ab-/6
    [1, 1, 1, 1, 1, 1, 1, 1],  # ab+/7
]
    for i in range(8):
        for j in range(8):
            gcRes = garbleMyCircuit(i, j)
            otResArray[i][j] = gcRes
            if (handin1.bloodCompLookup(i, j) != gcRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", gcRes)
    return print("All combinations tested")


def main():
    testAllCombinations()


if __name__ == "__main__":
    main()
