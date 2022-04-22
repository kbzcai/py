import socket
class UdpSend(object):
    udp_socket = None
    def init(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def udp_send(self, data, ip):
        data = "192.168.1." + ip + data + "END"
        send_data = data.encode("utf-8")
        self.udp_socket.sendto(send_data, ("192.168.1." + ip, 50505))
        recv_data = self.udp_socket.recvfrom(1024)
        print(recv_data)

    def close(self):
        self.udp_socket.close()

if __name__ == "__main__":
    udp = UdpSend()
    udp.init()
    udp.udp_send("B0101", "45")