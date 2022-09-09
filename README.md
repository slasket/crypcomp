# Cryptographic Computing
Svend Christensen AU604608, Simon Sørensen AU599666, Aske Bay Glenting AU586304

##### Handin 2:
To run the code for handin2 run the main method in the handin2.py file.
The main method simulates the OTT protocol with 3 classes, The dealer, Alice and Bob.


##### Handin 1:
Blood table: https://www.hema-quebec.qc.ca/sang/savoir-plus/groupes-sanguins.en.html  
![alt text](https://i.imgur.com/Mdq8ZCb.png)  
From the table above it can be seen that as one person is the donor, three simple rules decide wheter the blood types care combatible:

If the donor's blood type contains a "+", then the recipient also has to contain a "+"

If the donor's blood type contains an "A", then the recipient also has to contain an "A"

If the donor's blood type contains a "B", then the recipient also has to contain an "B"


With these simple rules a circuit can be constructed as follows  
![alt text](https://i.imgur.com/QwRlo1K.png)

In main method all combinations of blood types are tested for compatability in correspondance with the lookup table.