#!/usr/bin/env python
"""This reads \n terminated 'packets' from the input file and
distributes them between 4 receivers"""
from sys import argv
import re
import json
import scapy.all as scapy
import pdb

import load

PING_TIMEOUT = 2
NUM_OF_ARGS = 2
ENDWORD = " end"
FILE_EXTENSION = ".txt"
PORT = 1337

EVEN_LEN_RE = '^([^\n]{2})+$'
CAPITALIZED_RE = '^[A-Z]+.*'
ENDS_RE = '^.*\send$'


def ivan_rule(pack):
    return re.match(EVEN_LEN_RE, pack)


def dima_rule(pack):
    return not ivan_rule(pack) and re.match(CAPITALIZED_RE, pack)


def lesya_rule(pack):
    return re.match(ENDS_RE, pack)


def ostap_rule(pack):
    return not (ivan_rule(pack) or dima_rule(pack) or lesya_rule(pack))

rules_dict = {'Ivan': ivan_rule, 'Dima': dima_rule, 'Lesia': lesya_rule, 'Ostap': ostap_rule}


def check_argument():
    """
    checks if script is run properly with valid arguments
    """
    if not len(argv) == NUM_OF_ARGS:
        print("usage:\n" + argv[0] + " inputfile")
        exit(1)


class PingTimeout(Exception):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class Receiver:

    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.is_mine = lambda: False  #placeholder for the rule
        self.packet_list = []  #store packets

    def ping(self):
        packet = scapy.IP(dst=self.ip, ttl=20)/scapy.ICMP()
        reply = scapy.sr1(packet, timeout=PING_TIMEOUT)
        if not (reply is None):
            pass #everything is fine, host up
        else:
            raise PingTimeout(2)

    def send(self, pack):
        ip_pack = scapy.IP(dst=self.ip)/scapy.UDP(sport=PORT, dport=PORT)/pack
        scapy.sendp(ip_pack)

class Idol:
    """a Controller class"""

    def __init__(self):
        self.list_of_receivers = []
        self.__num_of_sent_packs = 0

    def get_receivers(self, json_file):
        with open(json_file) as receivers_file:
            #TODO exceptions
            contacts = json.load(receivers_file)
            for name in contacts:
                self.list_of_receivers.append(Receiver(name, contacts[name]))

    def set_rules(self, rules_dict):
        for receiver in self.list_of_receivers:
            receiver.is_mine = rules_dict[receiver.name]

    def distribute_packets(self, packet_list):
        for pack in packet_list:
            for receiver in self.list_of_receivers:
                if receiver.is_mine(pack):
                    receiver.packet_list.append(pack)
                    try:
                        receiver.ping()
                        receiver.send(pack)
                    except PingTimeout:
                        print('Host {} is not responding'.format(receiver.ip))



        


def main(argv):

    check_argument()

    idol = Idol()
    idol.get_receivers("addressants.json")
    idol.set_rules(rules_dict)

    idol.distribute_packets(load.loadFile(argv[1]).split('\n'))


if __name__ == '__main__':
    main(argv)
