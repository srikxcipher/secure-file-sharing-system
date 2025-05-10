import socket
import os
import time
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
import hashlib

def get_des_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:8]

p = 23
g = 5
client_private = 15
client_public = pow(g, client_private, p)

client = socket.socket()
client.connect(('127.0.0.1', 5000))

try:
    # Key exchange
    start_time = time.time()
    client.send(str(client_public).encode())
    server_public = int(client.recv(1024).decode())
    shared_key = pow(server_public, client_private, p)
    des_key = get_des_key(shared_key)
    key_exchange_time = time.time() - start_time
    print(f"[+] Key exchange done in {key_exchange_time:.4f}s")

    # Read and encrypt file
    file_path = "original.txt"
    if not os.path.exists(file_path):
        print("[!] File not found.")
        client.close()
        exit()

    with open(file_path, "rb") as f:
        data = f.read()

    cipher = DES.new(des_key, DES.MODE_ECB)
    encrypted_data = cipher.encrypt(pad(data, DES.block_size))

    # Send file size first
    client.send(str(len(encrypted_data)).encode())
    client.recv(1024)  # Wait for READY

    # Send file
    start_transfer = time.time()
    client.sendall(encrypted_data)
    transfer_time = time.time() - start_transfer

    print(f"[+] Encrypted file sent in {transfer_time:.4f}s")

except Exception as e:
    print(f"[!] Client Error: {e}")

client.close()
