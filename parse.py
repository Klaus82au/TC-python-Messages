#!/usr/bin/env python
"""This reads \n terminated 'packets' from the input file and
distributes them between 4 receivers"""
from sys import argv
import re
import json
import scapy.all as scapy
import threading
import time
from os import path

import load

PING_TIMEOUT = 1
NUM_OF_ARGS = 3
ENDWORD = "end"
FILE_EXTENSION = ".txt"
PORT = 1337
DELAY = 0.5
DEFAULT_TIMEOUT = 1
PACK_PREVIEW_LEN = 15

EVEN_LEN_RE = '^([^\n]{2})+$'
CAPITALIZED_RE = '^[A-Z]+.*'
ENDS_WITH_RE = '^.*\s{}$'


def ivan_rule(pack):
    """checks if
    @pack is for Ivan"""
    return re.match(EVEN_LEN_RE, pack)


def dima_rule(pack):
    """checks if
        @pack is for Dima"""
    return not ivan_rule(pack) and re.match(CAPITALIZED_RE, pack)


def lesya_rule(pack):
    """checks if
        @pack is for Lesya"""
    return re.match(ENDS_WITH_RE.format(ENDWORD), pack)


def ostap_rule(pack):
    """checks if
        @pack is for Ostap"""
    return not (ivan_rule(pack) or dima_rule(pack) or lesya_rule(pack))

rules_dict = {'Ivan': ivan_rule, 'Dima': dima_rule, 'Lesia': lesya_rule, 'Ostap': ostap_rule}


def check_argument():
    """
    checks if script is run properly with valid arguments
    """
    if not len(argv) == NUM_OF_ARGS:
        print("usage:\n" + argv[0] + " inputfile" + " jsonfile")
        exit(1)
    #i only check the inputfile, 'cuz it's loaded with C module
    #if there is a problem with json file, there will be an exception
    if not path.isfile(argv[1]):
        print("ERROR: Input file does not exist")
        exit(1)


class PingTimeout(Exception):
    """
    exception
    host is not responding
    """
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return repr(self.code)


class Receiver:
    """
    Contains all info about receiver(ip, name, packet_list)
    methods:
    is_mine(pack) check if @pack is for receiver
    ping() check if host is up
    send(pack) send @pack to host in IP/UDP packet
    sniff_confirm(pack) informs the user if @pack was sent or not
    """
    def __init__(self, name, ip):
        self.name = name
        self.ip = ip
        self.is_mine = lambda: False  #placeholder for the rule
        self.packet_list = []  #store packets
        self.successfully_sent = 0 #number of successfully sent packets, for stats

    def ping(self):
        """
        check if host is up
        :return: True / False
        """
        packet = scapy.IP(dst=self.ip, ttl=20)/scapy.ICMP()
        reply = scapy.sr1(packet, timeout=PING_TIMEOUT, verbose=False)
        return bool(reply)

    def __sniff_confirm(self, pack):
        """
        sniff_confirm(pack) informs the user if @pack was sent or not
        :param pack: packet to check if sent
        :return: True -@pack sent successfully / False - failed to send
        """
        #sniff some packets for some time
        sniffed_packs = scapy.sniff(filter='udp and port {} and dst {}'.format(PORT, self.ip),
                                    timeout=DEFAULT_TIMEOUT)
        #check if we caught our pack
        for udp_packet in sniffed_packs:
            try:
                packet_load = udp_packet.getlayer(scapy.Raw).load
                if udp_packet.getlayer(scapy.IP).dst == self.ip and \
                        packet_load.decode('utf-8') == pack:
                    print('Succsesfully sent \'{}...\' to {}'.format(pack[:PACK_PREVIEW_LEN], self.ip))
                    self.successfully_sent += 1 #info for stats
                    return True
            except UnicodeDecodeError:
                pass
            except AttributeError:
                pass
        #looks like our pack was not sent
        print('Packet \'{}...\' was not sent'.format(pack[:PACK_PREVIEW_LEN]))
        return False

    def send(self, pack):
        """
        send(pack) send @pack to host in IP/UDP packet
        and sniff if it was sent
        """
        print("sending \'{}...\' to {}".format(pack[:PACK_PREVIEW_LEN], self.ip))
        #start sniffing thread to make sure our pack was sent
        thread = threading.Thread(
            target=self.__sniff_confirm, args=(pack,))
        thread.start()
        time.sleep(DELAY) #w8 some time to be able to catch this packet
        #constructing pack
        ip_pack = scapy.IP(dst=self.ip)/scapy.UDP(sport=PORT, dport=PORT)/scapy.Raw(pack)
        #sending pack
        scapy.send(ip_pack, verbose=False)
        #waiting for the thread to finish(it runs for DEFAULT_TIMEOUT seconds)
        thread.join()


class Idol:
    """
    a Controller class
    methods:
    __get receivers - Loads receivers data from json file
    __set_rules set is_mine method for every receiver
    distribute_packets distributes packets between the receivers
    summary - prints summary of sent packets
    """
    def __init__(self, json_file, rules_dict):
        self.list_of_receivers = []
        self.__get_receivers(json_file)
        self.__set_rules(rules_dict)

    def __get_receivers(self, json_file):
        """
        Loads receivers data from json file
        :param json_file: file to load from
        """
        try:
            with open(json_file) as receivers_file:
                contacts = json.load(receivers_file)
                for name in contacts:
                    self.list_of_receivers.append(Receiver(name, contacts[name]))
        except IOError:
            print("ERROR: Failed to open json file")
            exit(1)

    def __set_rules(self, rules_dict):
        """
        set is_mine method for every receiver
        :param rules_dict: dictionary {'name': rule_func}
        """
        for receiver in self.list_of_receivers:
            if receiver.name in rules_dict:
                receiver.is_mine = rules_dict[receiver.name]
            else:
                print("ERROR: Failed to set rules")
                exit(1)

    def distribute_packets(self, packet_list):
        """
        distribute packets from
        :param packet_list:
        between receivers
        """
        for pack in packet_list:
            if not pack:#ignore empty string
                continue
            for receiver in self.list_of_receivers:
                if receiver.is_mine(pack):
                    receiver.packet_list.append(pack)
                    if receiver.ping():
                        receiver.send(pack)
                    else:
                        print('Host {} is not responding'.format(receiver.ip))

    def summary(self):
        """
        prints summary of sent packets
        """
        for receiver in self.list_of_receivers:
            print("\nSuccessfully sent {} of {} packets to {} at {}".format(receiver.successfully_sent,
                  len(receiver.packet_list), receiver.name, receiver.ip))


def main(argv):

    check_argument()

    idol = Idol(argv[2], rules_dict)
    idol.distribute_packets(load.loadFile(argv[1]).split('\n'))
    idol.summary()

if __name__ == '__main__':
    main(argv)
