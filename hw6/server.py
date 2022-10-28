import socket
import sys
from _socket import SOL_SOCKET, SO_REUSEADDR
from collections import Counter

from threading import Thread, Lock
from queue import Queue

import re
import json
import requests
from bs4 import BeautifulSoup


def connect_server(address1, address2):
    sock1 = socket.socket()
    sock1.bind(("", address1))
    sock1.listen(0)
    sock1.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    sock2 = socket.socket()
    sock2.bind(("", address2))
    sock2.listen(0)
    sock2.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    conn1 = sock1.accept()[0]
    conn2 = sock2.accept()[0]

    return conn1, conn2, sock1, sock2


def process_url(queue, num, lock, conn, k_words):
    while True:
        url = queue.get()
        if url == '':  # Символ конца передачи (EOT, End of Transmission)
            queue.put(url)
            break
        try:
            req = requests.get(url, timeout=3)
        except requests.ConnectionError:
            res_json = json.dumps({url: 'error'}, ensure_ascii=False)
        except requests.exceptions.MissingSchema:
            res_json = json.dumps({url: 'error'}, ensure_ascii=False)
        except requests.exceptions.ReadTimeout:
            res_json = json.dumps({url: 'error'}, ensure_ascii=False)
        else:
            soup = BeautifulSoup(req.text, features="html.parser")
            words = re.findall(r'[a-zA-Zа-яёА-ЯЁ_]+', soup.text)
            res_counted = Counter(words).most_common(k_words)
            res_dict = {url: {item[0]: item[1] for item in res_counted}}
            res_json = json.dumps(res_dict, ensure_ascii=False)
        conn.send(res_json.encode('utf-8'))
        with lock:
            num[0] += 1
            print(num[0], end=' ')
            if 2 <= num[0] % 10 <= 4 and num[0] % 100 // 10 != 1:
                print("URL'а обработано")
            elif num[0] % 10 == 1 and num[0] % 100 // 10 != 1:
                print("URL обработан")
            else:
                print("URL'ов обработано")


def get_url_from_client(queue, conn):
    while True:
        urls = conn.recv(4096).decode('utf-8').split('\n')
        for url in urls:
            if url:
                queue.put(url)
            if url == '':  # Символ конца передачи (EOT, End of Transmission)
                return


def server_instance(workers_number, k_words, address=10000):
    conn1, conn2, sock1, sock2 = connect_server(address, address + 1)

    lock = Lock()
    queue = Queue()
    num = [0]

    threads = [
        Thread(target=process_url, args=(queue, num, lock, conn2, k_words))
        for i in range(workers_number + 1)
    ]
    threads.append(Thread(target=get_url_from_client, args=(queue, conn1)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    sock1.close()
    sock2.close()


if __name__ == "__main__":
    workers = int(sys.argv[2])
    words = int(sys.argv[4])
    server_instance(workers, words)
