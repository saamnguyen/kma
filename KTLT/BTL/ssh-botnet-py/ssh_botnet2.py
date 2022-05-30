#!/usr/bin/env python3
# Coded by CyberCommands
import os
import optparse
from pexpect import pxssh

os.system('cls' if os.name == 'nt' else 'clear')
print('''
======================================
THIS IS A SIMPLE SSH BOT CONTROL UNIT.
--------------------------------------
        Coded by CyberCommands
======================================''')

class Client:
    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.session = self.connect()
    
    def connect(self):
        try:
            s = pxssh.pxssh()
            s.login(self.host, self.user, self.password)
            return s
        except Exception as e:
            print(e)
            print('\033[91m[-] Error Connecting \033[0m')
    
    def send_command(self, cmd):
        self.session.sendline(cmd)
        self.session.prompt()
        return self.session.before
    
def botnet_command(command):
    for client in Botnet:
        output = client.send_command(command)
        print('[*] Output from ' + client.host)
        print('\033[32m[+] \033[0m' +str(output, encoding='utf-8')+ '\n')

def add_client(host, user, password):
    client = Client(host, user, password)
    Botnet.append(client)

order = input("Command >> ")
Botnet = []
add_client('192.168.29.130', 'ubuntu', 'ubuntu')
#add_client('host', 'username', 'password')
botnet_command(order)