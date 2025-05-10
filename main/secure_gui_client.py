import socket
import hashlib
from Crypto.Cipher import DES
from Crypto.Util.Padding import pad
from tkinter import Tk, Label, Button, filedialog, Text, END, Scrollbar, RIGHT, Y

p = 23
g = 5
client_private = 15
client_public = pow(g, client_private, p)

def get_des_key(shared_key):
    return hashlib.sha256(str(shared_key).encode()).digest()[:8]

def log(msg):
    log_area.insert(END, msg + "\n")
    log_area.see(END)

def send_file():
    filepath = filedialog.askopenfilename()
    if not filepath:
        return

    log(f"Selected file: {filepath}")
    try:
        with open(filepath, "rb") as f:
            data = f.read()
    except FileNotFoundError:
        log("[!] File not found.")
        return

    client = socket.socket()
    try:
        client.connect(('127.0.0.1', 5000))
    except:
        log("[!] Could not connect to server.")
        return

    try:
        # Key Exchange
        client.send(str(client_public).encode())
        server_public = int(client.recv(1024).decode())
        shared_key = pow(server_public, client_private, p)
        des_key = get_des_key(shared_key)
        log("[+] Key exchange done")

        # Encrypt data
        cipher = DES.new(des_key, DES.MODE_ECB)
        encrypted_data = cipher.encrypt(pad(data, DES.block_size))

        # Save encrypted data to a file
        encrypted_filename = "encrypted_received_file.txt"
        with open(encrypted_filename, "wb") as encrypted_file:
            encrypted_file.write(encrypted_data)

        log(f"[+] Encrypted file saved as '{encrypted_filename}'")

        # Send file length, data, and hash
        client.send(str(len(encrypted_data)).encode())
        client.recv(1024)
        client.sendall(encrypted_data)
        client.recv(1024)

        file_hash = hashlib.sha256(data).hexdigest()
        client.send(file_hash.encode())
        log(f"[+] File sent.")
        log(f"[i] SHA-256 hash sent: {file_hash}")

    except Exception as e:
        log(f"[!] Error: {str(e)}")

    client.close()

app = Tk()
app.title("Secure File Sender")
app.geometry("600x400")
Label(app, text="Secure File Sender (Diffie-Hellman + DES)", font=("Helvetica", 14)).pack(pady=10)
Button(app, text="Send File", command=send_file, bg="#4CAF50", fg="white", padx=20, pady=10).pack()
log_area = Text(app, height=15, width=70)
log_area.pack(pady=10)
scroll = Scrollbar(app, command=log_area.yview)
scroll.pack(side=RIGHT, fill=Y)
log_area.configure(yscrollcommand=scroll.set)
app.mainloop()
