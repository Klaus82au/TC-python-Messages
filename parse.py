#!/usr/bin/env python
"""This reads \n terminated 'packets' from the input file and
distributes them between 4 receivers"""
from sys import argv
import re
import json
import load

NUM_OF_ARGS = 2
ENDWORD = " end"
FILE_EXTENSION = ".txt"

re_dict = {'Ivan': lambda pack: len(pack) % 2 == 0,
                  'Dima': lambda pack: pack[0].isupper(),
                  'Lesya': lambda pack: pack.match('* end')}


def check_argument():
    """
    checks if script is run properly with valid arguments
    """
    if not len(argv) == NUM_OF_ARGS:
        print("usage:\n" + argv[0] + " inputfile")
        exit(1)


def read_packets(filename):
    """
    reads packets from file
    @arg1: filename
    """
    try:
        with open(filename) as f:
            packet_list = f.readlines()
    except IOError:
        print("Could not open file!")
        exit(1)
    return packet_list


def distribute_packets(packet_list, receivers_packets):
    """
    distributes the packets between receivers
    @arg1: list of packets
    @arg2: dictionary{receiver's name: list of packets}
    """
    for pack in packet_list:
        pack = pack.rstrip("\n")
        if not pack:
            # it was just '\n' so skip
            continue
        if condition_dict['Lesya'](pack):
            receivers_packets['Lesya'].append(pack)
        if condition_dict['Ivan'](pack):
            receivers_packets['Ivan'].append(pack)
        elif condition_dict['Dima'](pack):
            receivers_packets['Dima'].append(pack)
        elif not condition_dict['Lesya'](pack):
            receivers_packets['Ostap'].append(pack)


def main(argv):
    with open('addressants.json') as addressants_file:
        contacts = json.load(addressants_file)

    receivers_packets = {'Ivan': [], 'Dima': [], 'Ostap': [], 'Lesya': []}
    check_argument()
    packet_string = load.loadFile(argv[1])
    print (packet_string)
    """packet_list = read_packets(argv[1])
    distribute_packets(packet_list, receivers_packets)

    for receiver in receivers_packets:
        with open(receiver + FILE_EXTENSION, "w") as f:
                f.writelines('\n'.join(receivers_packets[receiver]))"""

if __name__ == '__main__':
    main(argv)
