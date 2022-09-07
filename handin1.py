tt = [
    [1,0,0,0,0,0,0,0], #o- /0
    [1,1,0,0,0,0,0,0], #o+ /1
    [1,0,1,0,0,0,0,0], #b- /2
    [1,1,1,1,0,0,0,0], #b+ /3
    [1,0,0,0,1,0,0,0], #a- /4
    [1,1,0,0,1,1,0,0], #a+ /5
    [1,0,1,0,1,0,1,0], #ab-/6
    [1,1,1,1,1,1,1,1], #ab+/7
]

def bloodCompLookup(donor, receiver):
    return tt[donor][receiver]



def AND (a, b): #From https://www.geeksforgeeks.org/logic-gates-in-python/
    if a == 1 and b == 1:
        return True
    else:
        return False

def OR(a, b): #From https://www.geeksforgeeks.org/logic-gates-in-python/
    if a == 1 or b ==1:
        return True
    else:
        return False

def check_nth_bit(num, n): #From https://stackoverflow.com/questions/18111488/convert-integer-to-binary-in-python-and-compare-the-bits
    return (num>>n)&1

def bloodCompTest(donor, receiver):
    dA = check_nth_bit(donor, 2)
    dB = check_nth_bit(donor, 1)
    dPos = check_nth_bit(donor, 0)

    rA = check_nth_bit(receiver, 2)
    rB = check_nth_bit(receiver, 1)
    rPos = check_nth_bit(receiver, 0)

    return   AND(
        AND(
            OR(dPos, not rPos),
            OR(dB, not rB)),
        OR(dA, not rA)
    ) #Makes sure r is "less than" d on each bit


def testAllCombinations():
    for i in range(7):
        iBin = format(i, "b")
        for j in range(7):
            jBin = format(j, "b")
            if(bloodCompLookup(i,j) != bloodCompTest(int(iBin), int(jBin))):
                return "Blood compatability mismatch with lookup table"

    return "All combinationd tested"




def main():
    bloodCompLookup(0,7)
    testAllCombinations()

if __name__ == "__main__":
    main()
