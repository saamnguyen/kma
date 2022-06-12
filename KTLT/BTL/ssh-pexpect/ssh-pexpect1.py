#!/usr/bin/env python
import pexpect
import struct, fcntl, os, sys, signal, termios

def sigwinch_passthrough (sig, data):
    # Check for buggy platforms (see pexpect.setwinsize()).
    if 'TIOCGWINSZ' in dir(termios):
        TIOCGWINSZ = termios.TIOCGWINSZ
    else:
        TIOCGWINSZ = 1074295912 # assume
    s = struct.pack ("HHHH", 0, 0, 0, 0)
    a = struct.unpack ('HHHH', fcntl.ioctl(sys.stdout.fileno(), TIOCGWINSZ , s))
    global global_pexpect_instance
    global_pexpect_instance.setwinsize(a[0],a[1])

ssh_newkey = 'Are you sure you want to continue connecting'
p=pexpect.spawn('ssh ubuntu@192.168.29.130')
i=p.expect([ssh_newkey,'password:',pexpect.EOF,pexpect.TIMEOUT],1)
if i==0:
    print("I say yes")
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    print("I give password", end=' ')
    p.sendline("ubuntu")
elif i==2:
    print("I either got key or connection timeout")
    pass
elif i==3: #timeout
    pass
p.sendline("\r")
global global_pexpect_instance
global_pexpect_instance = p
signal.signal(signal.SIGWINCH, sigwinch_passthrough)

try:
    p.interact()
    sys.exit(0)
except:
    sys.exit(1)