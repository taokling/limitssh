# encoding=utf-8
import time, traceback, socket

def start():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('10.8.3.110', 22))

    data = sock.recv(1024)
    print(data)
    data = "SSH-2.0-nsssh2_6.0.0017 NetSarang Computer, Inc"
    sock.sendall(data.encode("utf-8"))
    time.sleep(0.5)
    data = sock.recv(1024)
    print(data)

def main():
    try:
        start()
    except Exception as e:
        traceback.print_exc(e)

if __name__ == "__main__":
    main()