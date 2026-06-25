import socket
import threading
import sys
import hashlib
import base64
import time

# --- ألوان وترميزات الـ Matrix المستوحاة من شغفك ---
G = '\033[92m'      # أخضر فسفوري
R = '\033[91m'      # أحمر دموي
Y = '\033[93m'      # أصفر تحذيري
C = '\033[96m'      # سماوي هكر
M = '\033[95m'      # أرجواني فضائي
W = '\033[0m'       # اللون الافتراضي
BC = '\033[1m'      # خط عريض
UNDER = '\033[4m'   # خط تحت النص

SERVER = "irc.libera.chat"
PORT = 6667

def cyber_loading(text, duration=3):
    """شريط تحميل متحرك يعطي شعور الاختراق الحقيقي"""
    sys.stdout.write(f"{Y}[*] {text} ")
    sys.stdout.flush()
    for _ in range(duration * 2):
        time.sleep(0.5)
        sys.stdout.write(f"{G}█{W}")
        sys.stdout.flush()
    print(f" {G}[DONE]{W}")

def generate_secure_keys(room_number, secret_pepper):
    static_base = b"Enjleez_Room_Core_v5.0_"
    room_hash = hashlib.sha256(static_base + room_number.strip().encode() + secret_pepper.strip().encode()).hexdigest()
    room_name = f"#enj_{room_hash[:12]}" 
    chat_key = hashlib.sha256(room_hash.encode()).hexdigest()
    return room_name, chat_key

def xor_encrypt_decrypt(data, key):
    return "".join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def receive_messages(sock, chat_key, room_name, my_nick):
    while True:
        try:
            data = sock.recv(4096).decode('utf-8', errors='ignore')
            if not data:
                break
            
            if data.startswith("PING"):
                sock.send(f"PONG {data.split()[1]}\r\n".encode())
                continue

            if "PRIVMSG" in data and room_name in data:
                sender_nick = data.split('!')[0].replace(':', '')
                if sender_nick != my_nick:
                    raw_message = data.split(f"PRIVMSG {room_name} :")[1].strip()
                    
                    decoded_base64 = base64.b64decode(raw_message.encode()).decode('utf-8')
                    decrypted_message = xor_encrypt_decrypt(decoded_base64, chat_key)
                    
                    # طباعة الرسالة المستلمة بشكل إلكتروني أنيق مع توقيت رقمي
                    timestamp = time.strftime("%H:%M:%S")
                    print(f"\n{M}[{timestamp}] 👽 [Partner] ──> {G}{decrypted_message}{W}")
                    print(f"{C}[🛸 Enjleez-Terminal]: {W}", end="", flush=True)
        except Exception:
            break

def start_chat(sock, chat_key, room_name, my_nick):
    threading.Thread(target=receive_messages, args=(sock, chat_key, room_name, my_nick), daemon=True).start()
    
    print(f"\n{G}{BC}[+] CORE STATUS: SECURE NETWORKING ESTABLISHED{W}")
    print(f"{C}[+] ENCRYPTION: AES-XOR LAYER 2 ACTIVE{W}")
    print(f"{Y}[!] MATRIX SYNCHRONIZED. SYSTEM IS READY.{W}\n")
    print(f"{M}{'-'*60}{W}")
    
    while True:
        try:
            message = input(f"{C}[🛸 Enjleez-Terminal]: {W}")
            if message.lower() == 'exit':
                print(f"\n{R}[-] Terminating secure node connection...{W}")
                break
            if message.strip() == "":
                continue
                
            xor_text = xor_encrypt_decrypt(message, chat_key)
            encrypted_bytes = base64.b64encode(xor_text.encode('utf-8')).decode()
            
            sock.send(f"PRIVMSG {room_name} :{encrypted_bytes}\r\n".encode())
        except (KeyboardInterrupt, SystemExit):
            break
    sock.close()

if __name__ == "__main__":
    # تنظيف الشاشة لإعطاء مظهر برمجي نقي
    print("\033[H\033[J")
    
    # واجهة الشعار السينمائية الفضائية
    print(f"""{G}{BC}
    ███████╗███╗   ██╗██╗██╗      ███████╗███████╗███████╗
    ██╔════╝████╗  ██║██║██║      ██╔════╝██╔════╝╚══███╔╝
    █████╗  ██╔██╗ ██║██║██║      █████╗  █████╗    ███╔╝ 
    ██╔══╝  ██║╚██╗██║██║██║      ██╔══╝  ██╔══╝   ███╔╝  
    ███████╗██║ ╚████║██║███████╗███████╗███████╗███████╗
    ╚══════╝╚═╝  ╚═══╝╚═╝╚══════╝╚══════╝╚══════╝╚══════╝
              {M}{UNDER}👽 QUANTUM ENCRYPTED NODE v6.0 👽{W}
    """)
    print(f"{C}{BC}============================================================{W}")
    
    room_num = input(f"{Y}[?] INITIALIZE ROOM ID (e.g., 8877): {W}")
    pepper = input(f"{Y}[?] ENTER DEEP SPACE PEPPER: {W}")
    
    print(f"\n{C}[*] Calculating cryptographic matrix coordinates...{W}")
    room_name, CHAT_KEY = generate_secure_keys(room_num, pepper)
    time.sleep(1)
    
    try:
        irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc_sock.connect((SERVER, PORT))
        
        my_nick = f"enj_{hashlib.md5((room_num + str(time.time())).encode()).hexdigest()[:6]}"
        
        irc_sock.send(f"USER {my_nick} 0 * :EnjleezUser\r\n".encode())
        irc_sock.send(f"NICK {my_nick}\r\n".encode())
        
        # استدعاء شريط التحميل الوهمي لتأخير الاتصال ليتزامن مع السيرفر بشكل احترافي
        cyber_loading("Connecting to Space Exchange Server", duration=2)
        
        irc_sock.send(f"JOIN {room_name}\r\n".encode())
        cyber_loading("Injecting Cryptographic Keys into Orbit", duration=1)
        
        start_chat(irc_sock, CHAT_KEY, room_name, my_nick)
        
    except Exception as e:
        print(f"{R}[-] Quantum connection ruptured: {e}{W}")
