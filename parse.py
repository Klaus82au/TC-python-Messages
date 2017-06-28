#!/usr/bin/env python3 
from sys import argv
from os import path
#
NUM_OF_ARGS = 2

#checks if script is run properly with valid arguments
def checkArgument():
    if not len(argv)==NUM_OF_ARGS:
        print("usage:\n" + argv[0] + " messagesfile")
        exit(1)


#reads packets from file filename
def readPackets(filename):
        try:
            with open(filename) as f:
                packetList = f.readlines()
        except (OSError, IOError):
            print("Could not open file!")
            exit(1)
        return packetList

#distributes the packets between addressants
def distributePackets(packetList, addressantsPackets):
    for pack in packetList:
        pack = pack.rstrip("\n")
        boolvar = False
        if not pack:#it was just '\n' so skip
            continue
        if len(pack) % 2 == 0:
            boolvar = True
            addressantsPackets['Ivan'].append(pack)
        if len(pack) % 2 == 1 and pack[0].isupper():
            boolvar = True
            addressantsPackets['Dima'].append(pack)
        if pack.endswith(" end"):
            boolvar = True
            addressantsPackets['Lesya'].append(pack)
        if not boolvar:
            addressantsPackets['Ostap'].append(pack)

#main is self explainatory
def main(argv):
    addressantsPackets = {'Ivan': [], 'Dima': [], 'Ostap': [], 'Lesya': []}
    checkArgument()
    packetList = readPackets(argv[1])
    distributePackets(packetList, addressantsPackets)

    for addressant in addressantsPackets:
        with open(addressant+".txt", "w") as f:
                f.writelines('\n'.join(addressantsPackets[addressant]))
        f.close()

if __name__ == '__main__':
    main(argv)
