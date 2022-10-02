import hashlib as hash
import numpy as np
import secrets
import handin1
import elgamal

cr = secrets.SystemRandom()

# Alice class to represent Alice's part of communication
class Alice:
    def __init__(self, bt):
        self.bt = bt
        self.pkArray = []
        self.p = None
        self.key = None
        self.q = None
        self.g = None
        self.h = None

    # ElGamal key generation as done in the the ElGamal.py file
    def keyGen(self):
        # In practice this would be a large and safe prime, however inorder to quickly test that the algorithm works.
        # This has a chance of failure since the order q chosen might not be prime
        self.q = secrets.SystemRandom.randint(cr, pow(10, 20), pow(10, 50))
        self.g = secrets.SystemRandom.randint(cr, 2, self.q)
        self.key = elgamal.gen_key(self.q)
        self.h = elgamal.power(self.g, self.key, self.q)
        return self.g, self.h

    # Oblivious keygen algorithm
    # Picks h as a random number r between 1 and 2^2n and then r^2 mod q
    def oGen(self):
        g = secrets.SystemRandom.randint(cr, 2, self.q)
        tal = pow(10, 50) + 1
        bitlength = tal.bit_length()
        r = secrets.SystemRandom.randint(cr, 1, pow(2, 2 * bitlength))
        h = pow(r, 2) % self.q
        return [g, h]

    # Generate the array of encryption keys where one key corresponds to an actual encryption key pair
    def createPKArray(self):
        self.keyGen()
        for i in range(0, 8):
            self.pkArray.append(self.oGen())
        self.pkArray[self.bt] = [self.g, self.h]
        return self.pkArray, self.q

    # receive the array of encrypted ciphertexts and decrypt the one that corresponds to alices bloodtype
    def receiveCipherArray(self, cArray):
        ct, p = cArray[self.bt]
        resBits = elgamal.decrypt(ct, p, self.key, self.q)
        #print("ALICE")
        #print(resBits)
        resa = resBits[:128]
        resb = resBits[128:256]
        resr = resBits[256:384]
        #print(resa, resb, resr)
        return resa, resb, resr

    def receiveGarbleYandDecrypt(self, gg, x, y, d):
        inputKeys = self.constructInput(x, y)

        res = self.evaluateGC(gg, inputKeys)

        return self.decrypt(d, res)

    def constructInput(self, x, encryptedy):
        y = self.receiveEncryptedY(encryptedy)
        input = [x[0], x[1], x[2], y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8]]

        #print("x0", x[0])
        #print("y3", y[3])
        inputKeys = [0] * 23

        for i in range(12):
            inputKeys[i] = int(input[i],2)

        return inputKeys

    def receiveEncryptedY(self, y):
        decryptedy = []
        for i in range(9):
            decryptedy.append(y[i*128:(i*128)+128])
        return decryptedy

    def decrypt(self, d, res):
        if res == d[0]:
            return 0
        elif res == d[1]:
            return 1
        else:
            return None

    def evaluation(self, keyLeft, keyRight, garbledGate):
        c1 = int(hash.sha256(bytes(str(keyLeft) + str(keyRight), 'utf-8')).hexdigest(), base=16)
        for i, cipher in enumerate(garbledGate):
            keyCandidate = cipher ^ c1
            bitKey = format(keyCandidate, '0256b')
            # print("bitkey", bitKey)
            if (bitKey[
                -128:]) == "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000":
                return int(bitKey[:128], 2)

    def evaluateGC(self, gates, inputKeys):
        inputKeys[12] = self.evaluation(inputKeys[6], inputKeys[0], gates[0])  # XOR
        inputKeys[13] = self.evaluation(inputKeys[7], inputKeys[1], gates[1])  # XOR
        inputKeys[14] = self.evaluation(inputKeys[8], inputKeys[2], gates[2])  # XOR

        inputKeys[15] = self.evaluation(inputKeys[12], inputKeys[3], gates[3])  # AND
        inputKeys[16] = self.evaluation(inputKeys[13], inputKeys[4], gates[4])  # AND
        inputKeys[17] = self.evaluation(inputKeys[14], inputKeys[5], gates[5])  # AND

        inputKeys[18] = self.evaluation(inputKeys[9], inputKeys[15], gates[6])  # XOR
        inputKeys[19] = self.evaluation(inputKeys[10], inputKeys[16], gates[7])  # XOR
        inputKeys[20] = self.evaluation(inputKeys[11], inputKeys[17], gates[8])  # XOR

        inputKeys[21] = self.evaluation(inputKeys[19], inputKeys[20], gates[9])  # AND
        return self.evaluation(inputKeys[18], inputKeys[21], gates[10])  # AND

        # inputKeys[12] = evaluation(inputKeys[1], inputKeys[2], gates[0])  # XOR
        # inputKeys[13] = evaluation(inputKeys[5], inputKeys[6], gates[1])  # XOR
        # inputKeys[14] = evaluation(inputKeys[9], inputKeys[10], gates[2])  # XOR

        # inputKeys[15] = evaluation(inputKeys[12], inputKeys[3], gates[3])  # AND
        # inputKeys[16] = evaluation(inputKeys[13], inputKeys[7], gates[4])  # AND
        # inputKeys[17] = evaluation(inputKeys[14], inputKeys[11], gates[5])  # AND

        # inputKeys[18] = evaluation(inputKeys[0], inputKeys[15], gates[6])  # XOR
        # inputKeys[19] = evaluation(inputKeys[4], inputKeys[16], gates[7])  # XOR
        # inputKeys[20] = evaluation(inputKeys[8], inputKeys[17], gates[8])  # XOR

        # inputKeys[21] = evaluation(inputKeys[19], inputKeys[20], gates[9])  # AND
        # return evaluation(inputKeys[18], inputKeys[21], gates[10])  # AND


# Bob class to represent Bob's part of communication
class Bob:
    def __init__(self, bt):
        self.bt = bt
        self.wireKeys = self.generateGarbleKeys()

    # Receive the array of encryption keys, bob then selectes the slicing of the truth table corresponding to his bloodtype.
    # Then encrypt the slicing using the keys given by alice.
    def receiveArray(self, pkArray, q):
        resArray = []
        for i in range(0, 8):
            a = handin1.check_nth_bit(i, 2)
            b = handin1.check_nth_bit(i, 1)
            r = handin1.check_nth_bit(i, 0)
            m = self.ggEncryptAlice(a, b, r)
            resArray.append(elgamal.encryption(str(m), q, pkArray[i][1], pkArray[i][0]))

        return resArray

    def ggEncryptAlice(self, a, b, r):
        bita = format(self.wireKeys[0][a], '0128b')
        bitb = format(self.wireKeys[1][b], '0128b')
        bitr = format(self.wireKeys[2][r], '0128b')
        return str(bita) + str(bitb) + str(bitr)

    def ggEncryptBob(self):
        a = handin1.check_nth_bit(self.bt, 2)
        b = handin1.check_nth_bit(self.bt, 1)
        r = handin1.check_nth_bit(self.bt, 0)
        bita = format(self.wireKeys[3][a], '0128b')
        bitb = format(self.wireKeys[4][b], '0128b')
        bitr = format(self.wireKeys[5][r], '0128b')

        bit1 = format(self.wireKeys[6][1], '0128b')
        bit2 = format(self.wireKeys[7][1], '0128b')
        bit3 = format(self.wireKeys[8][1], '0128b')
        bit4 = format(self.wireKeys[9][1], '0128b')
        bit5 = format(self.wireKeys[10][1], '0128b')
        bit6 = format(self.wireKeys[11][1], '0128b')
        #print("bob bit1", bit1)
        #print("in6", format(self.wireKeys[6][1], '0128b'))
        #print("in0", format(self.wireKeys[0][0], '0128b'))
        return str(bita) + str(bitb) + str(bitr) + str(bit1) + str(bit2) + str(bit3) + str(bit4) + str(bit5) + str(bit6)

    def garbleMyCircuit(self):
        wireKeys = self.wireKeys
        gates = []

        gates.append(self.garbleMyGate("XOR", left=wireKeys[6], right=wireKeys[0], output=wireKeys[12]))
        gates.append(self.garbleMyGate("XOR", left=wireKeys[7], right=wireKeys[1], output=wireKeys[13]))
        gates.append(self.garbleMyGate("XOR", left=wireKeys[8], right=wireKeys[2], output=wireKeys[14]))

        gates.append(self.garbleMyGate("AND", left=wireKeys[12], right=wireKeys[3], output=wireKeys[15]))
        gates.append(self.garbleMyGate("AND", left=wireKeys[13], right=wireKeys[4], output=wireKeys[16]))
        gates.append(self.garbleMyGate("AND", left=wireKeys[14], right=wireKeys[5], output=wireKeys[17]))

        gates.append(self.garbleMyGate("XOR", left=wireKeys[9], right=wireKeys[15], output=wireKeys[18]))
        gates.append(self.garbleMyGate("XOR", left=wireKeys[10], right=wireKeys[16], output=wireKeys[19]))
        gates.append(self.garbleMyGate("XOR", left=wireKeys[11], right=wireKeys[17], output=wireKeys[20]))

        gates.append(self.garbleMyGate("AND", left=wireKeys[19], right=wireKeys[20], output=wireKeys[21]))
        gates.append(self.garbleMyGate("AND", left=wireKeys[18], right=wireKeys[21], output=wireKeys[22]))

        #gates.append(garbleMyGate("XOR", left=wireKeys[1], right=wireKeys[2], output=wireKeys[12]))
        #gates.append(garbleMyGate("XOR", left=wireKeys[5], right=wireKeys[6], output=wireKeys[13]))
        #gates.append(garbleMyGate("XOR", left=wireKeys[9], right=wireKeys[10], output=wireKeys[14]))

        #gates.append(garbleMyGate("AND", left=wireKeys[12], right=wireKeys[3], output=wireKeys[15]))
        #gates.append(garbleMyGate("AND", left=wireKeys[13], right=wireKeys[7], output=wireKeys[16]))
        #gates.append(garbleMyGate("AND", left=wireKeys[14], right=wireKeys[11], output=wireKeys[17]))

        #gates.append(garbleMyGate("XOR", left=wireKeys[0], right=wireKeys[15], output=wireKeys[18]))
        #gates.append(garbleMyGate("XOR", left=wireKeys[4], right=wireKeys[16], output=wireKeys[19]))
        #gates.append(garbleMyGate("XOR", left=wireKeys[8], right=wireKeys[17], output=wireKeys[20]))

        #gates.append(garbleMyGate("AND", left=wireKeys[19], right=wireKeys[20], output=wireKeys[21]))
        #gates.append(garbleMyGate("AND", left=wireKeys[18], right=wireKeys[21], output=wireKeys[22]))

        return gates

        # print(inputKeys)

        # print(evaluation(inputKeys[1], inputKeys[2], gates[0]))
        # evaluateGC(gates, inputKeys)

        # if inputKeys[22] == wireKeys[22][1]:
        #    return 1
        # elif inputKeys[22] == wireKeys[22][0]:
        #    return 0
        # else:
        #    return "shit"

    def decryptionTable(self):
        return self.wireKeys[22][0], self.wireKeys[22][1]

    def generateGarbleKeys(self, circuitSize=23):
        wireKeys = np.zeros(circuitSize, dtype=object)

        for i in range(len(wireKeys)):
            randomKey1 = secrets.randbits(128)
            randomKey2 = secrets.randbits(128)
            wireKeys[i] = randomKey1, randomKey2
        return wireKeys

    def garbleMyGate(self, gate, left, right, output):
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


# OT protocol for blood type compatability
#def ot(aliceBt):
#    alice = Alice(aliceBt)
#    bob = Bob()
#    pkArray, q = alice.createPKArray()
#    resArray = bob.receiveArray(pkArray, q)
#    resa, resb, resr = alice.receiveCipherArray(resArray)
#    return resa, resb, resr


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
            gcRes = protocol(i, j)
            otResArray[i][j] = gcRes
            if (handin1.bloodCompLookup(i, j) != gcRes):
                print("Blood compatability mismatch with lookup table")
                print("input:", i, j)
                print("table:", handin1.bloodCompLookup(i, j), "OT:", gcRes)
    return print("All combinations tested")


def protocol(aliceBt, bobBt):
    alice = Alice(aliceBt)
    bob = Bob(bobBt)

    # OT protocol
    pkArray, q = alice.createPKArray()
    resArray = bob.receiveArray(pkArray, q)

    # Result from OT protocol; encrypted Alice BT
    resa, resb, resr = alice.receiveCipherArray(resArray)

    gg = bob.garbleMyCircuit()
    encrytedy = bob.ggEncryptBob()
    d = bob.decryptionTable()

    #print("bob6", bob.wireKeys[6][1])
    #print("bob0", bob.wireKeys[0][0])

    res = alice.receiveGarbleYandDecrypt(gg, (resa, resb, resr), encrytedy, d)

    return res


def main():
    #protocol(0, 0)
    testAllCombinations()

    #gates = []
    #wireKeys = generateGarbleKeys()
    #gates.append(garbleMyGate("XOR", left=wireKeys[6], right=wireKeys[0], output=wireKeys[12]))
    #res = evaluation(wireKeys[6][1], wireKeys[0][0], gates[0])
    #print(res)

    #y = format(42, '06b') #101010
    #decryptedy = []
    #for i in range(3):
    #    decryptedy.append(y[i*2:(i*2 + 2)])
    #print(decryptedy)


if __name__ == "__main__":
    main()
