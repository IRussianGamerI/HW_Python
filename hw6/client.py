import socket
import sys
from threading import Thread
from queue import Queue


def connect_client(address1, address2):
    sock1 = socket.socket()
    sock2 = socket.socket()

    sock1.connect(("", address1))
    sock2.connect(("", address2))
    return sock1, sock2


def process_urls(queue, sock1, sock2):
    while not queue.empty():
        url = queue.get()
        sock1.sendall(url.encode('utf-8'))
        data = sock2.recv(1024).decode('utf-8')
        print(data)


def get_urls_from_file(filename: str):
    with open(filename, 'r', encoding="utf8") as file:
        urls = file.readlines()
    return urls


def client_instance(thread_num, urls, address=10000):
    sock1, sock2 = connect_client(address, address + 1)

    queue = Queue()
    for url in urls:
        if not url.endswith('\n'):
            queue.put(url + '\n')
        else:
            queue.put(url)
    queue.put('')  # Символ конца передачи (EOT, End of Transmission)

    threads = [Thread(target=process_urls, args=(queue, sock1, sock2)) for i in range(thread_num)]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    sock1.close()
    sock2.close()


if __name__ == "__main__":
    thread_number = int(sys.argv[1])
    name = sys.argv[2]
    urls = get_urls_from_file(name)
    client_instance(thread_number, urls)
