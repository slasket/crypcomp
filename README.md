# Cryptographic Computing
Svend Christensen AU604608, Simon Sørensen AU599666, Aske Bay Glenting AU586304

### Handin 4:
To run the code for handin4, run the main method in the handin4.py file.
This simulates the 1 out of 8 oblivious transfer protocol for the blood compatability function using El Gamal as the PKE scheme. To summarize, Alice generates a keypair for El Gamal as well as 7 other using OGen which she sends to Bob. Bob then encrypts the 8 messages using the 8 different keys, which he sends back to Alice. Since Alice knows her choice bit b, she simply decrypts the corresponding message and reads the result. The test run compares the result of all possible bloodtype combinations of donor and recipient with the values given by a truthtable structure containing the same information.

### Handin 3:
To run the code for handin3, run the main method in the handin3.py file.
The main method simulates the BeDOZa protocol. Preforming the AND operation is by far the hardest, and is implemented as a method call itself.
This method call takes a dealer with the corresponding u ,v and w for Alice and Bob, they then preform the AND operation as described in 2-OTTT-BeDOZa-Passive PDF.
One implementation quirk is that the protocol is implemented such that a dealer is made for every AND that is preformed. An implementation skip is that the XORing with ones are preformed "locally" by a method call alone with no secret sharing, since alice can XOR her input with one and then just use that as input for ANDing.



### Handin 2:
To run the code for handin2 run the main method in the handin2.py file.
The main method simulates the OTT protocol with 3 classes, The dealer, Alice and Bob.
Like handin1, the protocol is tested by a method that tests all possible combinations of blood types with a simple table lookup.


### Handin 1:
Blood table: https://www.hema-quebec.qc.ca/sang/savoir-plus/groupes-sanguins.en.html  
![alt text](https://i.imgur.com/Mdq8ZCb.png)  
From the table above it can be seen that as one person is the donor, three simple rules decide whether the blood types care compatible:

If the donor's blood type contains a "+", then the recipient also has to contain a "+"

If the donor's blood type contains an "A", then the recipient also has to contain an "A"

If the donor's blood type contains a "B", then the recipient also has to contain an "B"


With these simple rules a circuit can be constructed as follows  
![alt text](https://i.imgur.com/QwRlo1K.png)

In main method all combinations of blood types are tested for compatability in correspondance with the lookup table.
