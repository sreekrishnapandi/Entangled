__author__ = 'Krish'
import socket
import fcntl
import ctypes

class ifreq(ctypes.Structure):
    _fields_ = [("ifr_ifrn", ctypes.c_char * 16),
                ("ifr_flags", ctypes.c_short)]


IFF_PROMISC = 0x100
SIOCGIFFLAGS = 0x8913
SIOCSIFFLAGS = 0x8914

s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_IP)

ifr = ifreq()
ifr.ifr_ifrn = "en0"

#Populate the ifr_flags field with an ioctl call so that you don't clobber whatever flags are already set on the iface:
fcntl.ioctl(s.fileno(), SIOCGIFFLAGS, ifr) # G for Get
#Add the promiscuous flag:
ifr.ifr_flags |= IFF_PROMISC
#And set the flags on the interface:
fcntl.ioctl(s.fileno(), SIOCSIFFLAGS, ifr) # S for Set


try:
    # get the current Network Interface

    s.bind(('', 0))
    # Enable the Promiscuous mode
    #s.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)


    while True:
        packet, address = s.recvfrom(1500)
        ipheader = packet[:20]
        data = packet[20:]
        print "Header : ", ipheader
        print "Data : ", packet
except socket.error as err:
    print("[-] Error: %s"%str(err))
except KeyboardInterrupt:
    print("[+] Keyboard Interruption captured: Existing")