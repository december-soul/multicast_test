import datetime 
import struct
import socket
import sys
import binascii


# multicast parameter
# can be udp://225.1.10.44:30120 or 225.1.10.44 30120
if sys.argv[1].startswith('udp://'):
    args = sys.argv[1].replace("udp://", "").strip().split(":")
    MIP=args[0]
    MPORT=int(args[1])
else:
    MIP=sys.argv[1] #"225.1.2.1"
    MPORT=int(sys.argv[2]) #30120

# open file to dump multicast data to file
f =  open('test_' + MIP + "_" + str(MPORT) + '.ts', 'wb')

# open socket
addrinfo = socket.getaddrinfo(MIP,None)[0]
s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((MIP,MPORT))
group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
mreq = group_bin + struct.pack('=I', socket.INADDR_ANY)
s.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
while True:
     data, sender = s.recvfrom(1500)
     #while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
     print (str(datetime.datetime.utcnow().strftime("%H:%M:%S") ) + " received " + str(len(data)) +  " bytes from sender=" + str(sender[0]) + ":" + str(sender[1]) + '  data=' + str(binascii.hexlify(data)[:30]) + " ...")
     f.write(data)

f.close()
