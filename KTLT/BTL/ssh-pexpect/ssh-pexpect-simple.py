#!/usr/bin/env python
import pexpect

ssh_newkey = 'Are you sure you want to continue connecting'
# my ssh command line
p=pexpect.spawn('ssh ubuntu@192.168.29.130 uname -a')

i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==0:
    print("I say yes")
    p.sendline('yes')
    i=p.expect([ssh_newkey,'password:',pexpect.EOF])
if i==1:
    print("I give password", end=' ')
    p.sendline("ubuntu")
    p.expect(pexpect.EOF)    
elif i==2:
    print("I either got key or connection timeout")
    pass
print(p.before) # print out the result