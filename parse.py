import sys
import os.path

#global vars:

#packetList - list of packets from da file
packetList = []
#addressants dict
addrDict = {'Ivan': [], 'Dima': [], 'Ostap': [], 'Lesya': []}

#if i further implement thuis with a class,
#  i won't need global vars(perhaps)

def getInfile():
    infileName = ""
    if len(sys.argv) > 2:
        print("only takes 1 argument")
    infileName = sys.argv[1]
    if not os.path.isfile(infileName):
        print("file does not exist")
    return infileName

def readPackets(filename):
    global packetList
    packetList = []
    with open(filename) as f:
        packetList = f.readlines()

def processPackets(list):
    global addrDict
    for pack in list:
        pack = pack.strip("\n") #should i put this back later?
        boolvar = False
        if not pack:#it was just \n
            continue
        if len(pack) % 2 == 0:
            boolvar = True
            addrDict['Ivan'].append(pack+'\n')
        if len(pack) % 2 == 1 and pack[0].isupper():
            boolvar = True
            addrDict['Dima'].append(pack+'\n')
        if pack.endswith(" end"):
            boolvar = True
            addrDict['Lesya'].append(pack+'\n')
        if not boolvar:
            addrDict['Ostap'].append(pack+'\n')


def main(argv):
    infileName = getInfile()
    readPackets(infileName)
    processPackets(packetList)

    for addressant in addrDict:
        with open(addressant+".txt", "w") as f:
                f.writelines(addrDict[addressant])
        f.close()

if __name__ == '__main__':
    main(sys.argv)