import socket
import time
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
import hashlib

def get_des_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:8]

p = 23
g = 5
server_private = 6
server_public = pow(g, server_private, p)

server = socket.socket()
server.bind(('0.0.0.0', 5000))
server.listen(1)
print("Server listening...")

conn, addr = server.accept()
print("Connected by", addr)

try:
    # Key exchange
    start_time = time.time()
    client_public = int(conn.recv(1024).decode())
    conn.send(str(server_public).encode())
    shared_key = pow(client_public, server_private, p)
    des_key = get_des_key(shared_key)
    key_exchange_time = time.time() - start_time
    print(f"[+] Key exchange done in {key_exchange_time:.4f}s")

    # Receive file size
    file_size = int(conn.recv(1024).decode())
    conn.send(b'READY')

    # Receive file data
    received_data = b''
    while len(received_data) < file_size:
        data = conn.recv(4096)
        if not data:
            break
        received_data += data

    # Save encrypted file
    with open("received_encrypted.des", "wb") as f:
        f.write(received_data)

    # Decrypt and save
    try:
        cipher = DES.new(des_key, DES.MODE_ECB)
        decrypted_data = unpad(cipher.decrypt(received_data), DES.block_size)
        with open("decrypted_received.txt", "wb") as f:
            f.write(decrypted_data)
        print("[+] File decrypted and saved as 'decrypted_received.txt'")
    except ValueError:
        print("[!] Decryption failed: possibly wrong key or corrupted file.")

except Exception as e:
    print(f"[!] Server Error: {e}")

conn.close()
server.close()
