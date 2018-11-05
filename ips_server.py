from socket import socket, AF_INET, SOCK_DGRAM
import sys


def get_dict(ips_file):
    fd = open(ips_file, 'r')
    ret_dict = {}
    for line in fd:
        if line.strip() == "":
            continue
        add_key, ip_val = line.strip().split(',')
        ret_dict[add_key] = ip_val
    fd.close()
    return ret_dict


def append_to_file(data, ips_file):
    fd = open(ips_file, 'a')
    fd.write('\n'+data)
    fd.close()


def ask_parent(parent_server_info, server, query):
    server.sendto(query, parent_server_info)
    data, sender_info = server.recvfrom(2048)
    if sender_info == parent_server_info:
        return data
    return None


def main():
    args = sys.argv[1:]
    my_port, parent_ip, parent_port, ips_file = args
    parent_port = int(parent_port)
    add_ip_dict = get_dict(ips_file)
    s = socket(AF_INET, SOCK_DGRAM)
    source_ip = '0.0.0.0'
    source_port = int(my_port)
    s.bind((source_ip, source_port))
    while True:
        data, sender_info = s.recvfrom(2048)
        print "Query: ", data, " from: ", sender_info
        if data not in add_ip_dict.keys():
            ip_val = ask_parent((parent_ip, parent_port), s, data)
            # Update
            if ip_val is not None:
                add_ip_dict[data] = ip_val
                append_to_file(data+","+ip_val, ips_file)
            else:
                print "Could not achieve ip from parent server please try another query"
                continue
        else:
            ip_val = add_ip_dict[data]
        s.sendto(ip_val, sender_info)


if __name__ == "__main__":
    main()