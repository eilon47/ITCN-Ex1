from socket import socket, AF_INET, SOCK_DGRAM
import sys

if __name__ == '__main__':
    args = sys.argv[1:]
    dest_ip, dest_port = args
    s = socket(AF_INET, SOCK_DGRAM)
    dest_port = int(dest_port)
    website = raw_input("Please enter a website: ")
    while not website == 'quit':
        s.sendto(website, (dest_ip, dest_port))
        data, sender_info = s.recvfrom(2048)
        print "The IP of " + website + " is: ", data
        website = raw_input("Please enter a website: ")
    s.close()