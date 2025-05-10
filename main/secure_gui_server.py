import socket
import threading
import time
import hashlib
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from tkinter import Tk, Label, Text, Button, END, Scrollbar, RIGHT, Y

p = 23
g = 5
server_private = 6
server_public = pow(g, server_private, p)

def get_des_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:8]

def log(msg):
    log_area.insert(END, msg + "\n")
    log_area.see(END)

def start_server():
    def handler():
        try:
            server = socket.socket()
            server.bind(('0.0.0.0', 5000))
            server.listen(1)
            log("[...] Server listening on port 5000...")
            conn, addr = server.accept()
            log(f"[+] Connection from {addr}")

            client_public = int(conn.recv(1024).decode())
            conn.send(str(server_public).encode())
            shared_key = pow(client_public, server_private, p)
            des_key = get_des_key(shared_key)
            log(f"[+] Key exchange completed")

            file_size = int(conn.recv(1024).decode())
            conn.send(b'READY')
            log(f"[i] Expecting encrypted file of size: {file_size} bytes")

            received_data = b''
            while len(received_data) < file_size:
                data = conn.recv(4096)
                if not data:
                    break
                received_data += data
            log(f"[+] Received encrypted file ({len(received_data)} bytes)")

            conn.send(b'HASH')
            expected_hash = conn.recv(1024).decode()
            log(f"[i] Received expected SHA-256 hash: {expected_hash}")

            try:
                cipher = DES.new(des_key, DES.MODE_ECB)
                decrypted_data = unpad(cipher.decrypt(received_data), DES.block_size)
                with open("decrypted_received.txt", "wb") as f:
                    f.write(decrypted_data)
                log("[+] File decrypted and saved as 'decrypted_received.txt'")

                actual_hash = hashlib.sha256(decrypted_data).hexdigest()
                if actual_hash == expected_hash:
                    log("[✅] File integrity verified successfully.")
                else:
                    log("[❌] File integrity check FAILED.")
                    log(f"[i] Actual hash: {actual_hash}")

            except ValueError:
                log("[!] Decryption failed. Possibly wrong key or corrupted file.")

            conn.close()
            server.close()
        except Exception as e:
            log(f"[!] Error: {e}")

    threading.Thread(target=handler).start()

app = Tk()
app.title("Secure File Receiver")
app.geometry("600x400")
Label(app, text="Secure File Receiver (Diffie-Hellman + DES)", font=("Helvetica", 14)).pack(pady=10)
Button(app, text="Start Server", command=start_server, bg="#2196F3", fg="white", padx=20, pady=10).pack()
log_area = Text(app, height=15, width=70)
log_area.pack(pady=10)
scroll = Scrollbar(app, command=log_area.yview)
scroll.pack(side=RIGHT, fill=Y)
log_area.configure(yscrollcommand=scroll.set)
app.mainloop()