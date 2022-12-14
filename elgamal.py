import secrets
from math import pow

cr = secrets.SystemRandom()
a=secrets.SystemRandom.randint(cr, 2,10)

# This has been taken from https://www.codespeedy.com/elgamal-encryption-algorithm-in-python/
# We use this implementation as a correct secure implementation of ElGamal encryption although though we can see that the keyGen function might not always generate a safe prime.


#To fing gcd of two numbers
def gcd(a,b):
    if a<b:
        return gcd(b,a)
    elif a%b==0:
        return b
    else:
        return gcd(b,a%b)

#For key generation i.e. large random number
def gen_key(q):
    key= secrets.SystemRandom.randint(cr, pow(10,20),q)
    while gcd(q,key)!=1:
        key=secrets.SystemRandom.randint(cr, pow(10,20),q)
    return key

def power(a,b,c):
    x=1
    y=a
    while b>0:
        if b%2==0:
            x=(x*y)%c
        y=(y*y)%c
        b=int(b/2)
    return x%c

#For asymetric encryption
def encryption(msg,q,h,g):
    ct=[]
    k=gen_key(q)
    s=power(h,k,q)
    p=power(g,k,q)
    for i in range(0,len(msg)):
        ct.append(msg[i])
    #print("g^k used= ",p)
    #print("g^ak used= ",s)
    for i in range(0,len(ct)):
        ct[i]=s*ord(ct[i])
    return ct,p

#For decryption
def decryption(ct,p,key,q):
    pt=[]
    h=power(p,key,q)
    for i in range(0,len(ct)):
        pt.append(chr(int(ct[i]/h)))
    return pt



def main():
    msg=input("Enter message.")
    q=secrets.SystemRandom.randint(cr, pow(10,20),pow(10,50))
    g=secrets.SystemRandom.randint(cr, 2,q)
    key=gen_key(q)
    h=power(g,key,q)
    print("g used=",g)
    print("g^a used=",h)
    ct,p=encryption(msg,q,h,g)
    print("Original Message=",msg)
    print("Encrypted Maessage=",ct)
    pt=decryption(ct,p,key,q)
    d_msg=''.join(pt)
    print("Decryted Message=",d_msg)




def decrypt(ct, p ,key, q):
    pt=decryption(ct,p,key,q)
    d_msg=''.join(pt)
    return d_msg

if __name__ == "__main__":
    main()