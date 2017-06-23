from sys import argv
from os import path

#addressants dict
addressantsPackets = {'Ivan': [], 'Dima': [], 'Ostap': [], 'Lesya': []}

#checks if script is run properly with valid arguments
def checkFileArgument():
    if not len(argv)==2:
        print("usage:\n" + argv[0] + " messagesfile")
        exit(1)
    infileName = argv[1]
    if not path.isfile(infileName):
        print("file does not exist")
        exit(1)
    return infileName

#reads packets from file filename
def readPackets(filename):
    with open(filename) as f:
        packetList = f.readlines()
    return packetList

#distributes the packets between addressants
def distributePackets(packetList):
    global addressantsPackets
    for pack in packetList:
        pack = pack.rstrip("\n")
        boolvar = False
        if not pack:#it was just \n
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
    infileName = checkFileArgument()
    packetList = readPackets(infileName)
    distributePackets(packetList)

    for addressant in addressantsPackets:
        with open(addressant+".txt", "w") as f:
                f.writelines('\n'.join(addressantsPackets[addressant]))
        f.close()

if __name__ == '__main__':
    main(argv)