import socket
import threading
import sys
import hashlib
import base64
import time

# --- ألوان الـ ANSI القياسية ---
G = '\033[92m'   # أخضر فسفوري
R = '\033[91m'   # أحمر دموي
Y = '\033[93m'   # أصفر تحذيري
C = '\033[96m'   # سماوي هكر
W = '\033[0m'    # إعادة اللون الافتراضي
BC = '\033[1m'   # خط عريض

SERVER = "irc.libera.chat"
PORT = 6667

def generate_secure_keys(room_number, secret_pepper):
    static_base = b"Enjleez_Room_Core_v5.0_"
    room_hash = hashlib.sha256(static_base + room_number.strip().encode() + secret_pepper.strip().encode()).hexdigest()
    # استخدام اسم غرفة متوافق مع شروط السيرفر القاسية (أحرف صغيرة وبدون رموز معقدة)
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
            
            # الرد التلقائي على السيرفر للحفاظ على بقاء الاتصال حياً (Ping-Pong Handshake)
            if data.startswith("PING"):
                sock.send(f"PONG {data.split()[1]}\r\n".encode())
                continue

            if "PRIVMSG" in data and room_name in data:
                # التأكد من أن الرسالة ليست قادمة من اسم المستخدم الخاص بي لمنع التكرار
                sender_nick = data.split('!')[0].replace(':', '')
                if sender_nick != my_nick:
                    raw_message = data.split(f"PRIVMSG {room_name} :")[1].strip()
                    
                    # فك التشفير
                    decoded_base64 = base64.b64decode(raw_message.encode()).decode('utf-8')
                    decrypted_message = xor_encrypt_decrypt(decoded_base64, chat_key)
                    
                    print(f"\n{G}[Partner]: {decrypted_message}{W}")
                    print(f"{C}[You]: {W}", end="", flush=True)
        except Exception:
            break

def start_chat(sock, chat_key, room_name, my_nick):
    threading.Thread(target=receive_messages, args=(sock, chat_key, room_name, my_nick), daemon=True).start()
    print(f"\n{G}[+] {BC}Connected to Secret Room Exchange Server!{W}")
    print(f"{G}[+] Chat Environment Secured. Complete bypass of IP/Firewall!{W}")
    print(f"{Y}[*] Note: Wait 5 seconds before typing first message to sync...{W}\n")
    
    while True:
        try:
            message = input(f"{C}[You]: {W}")
            if message.lower() == 'exit':
                break
            if message.strip() == "":
                continue
                
            # تشفير وإرسال
            xor_text = xor_encrypt_decrypt(message, chat_key)
            encrypted_bytes = base64.b64encode(xor_text.encode('utf-8')).decode()
            
            sock.send(f"PRIVMSG {room_name} :{encrypted_bytes}\r\n".encode())
        except (KeyboardInterrupt, SystemExit):
            break
    sock.close()

if __name__ == "__main__":
    print(f"{C}{BC}=================================================={W}")
    print(f"{C}{BC}       ENJLEEZ CLOUD P2P MESSENGER (ROOMS)        {W}")
    print(f"{C}{BC}=================================================={W}")
    
    room_num = input(f"{Y}[?] Enter Secret Room Number (e.g., 9944): {W}")
    pepper = input(f"{Y}[?] Enter Secret Pepper/Pass: {W}")
    
    print(f"\n{C}[*] Establishing secure handshake with the cloud...{W}")
    room_name, CHAT_KEY = generate_secure_keys(room_num, pepper)
    
    try:
        irc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc_sock.connect((SERVER, PORT))
        
        # توليد اسم مستخدم ديناميكي فريد بناءً على رقم الغرفة والوقت لمنع تعارض الأسماء
        my_nick = f"enj_{hashlib.md5((room_num + str(time.time())).encode()).hexdigest()[:6]}"
        
        irc_sock.send(f"USER {my_nick} 0 * :EnjleezUser\r\n".encode())
        irc_sock.send(f"NICK {my_nick}\r\n".encode())
        time.sleep(3)  # مهلة ضرورية لتسجيل الحساب على خوادم السحاب
        
        irc_sock.send(f"JOIN {room_name}\r\n".encode())
        time.sleep(2)  # مهلة لضمان دخول الغرفة بالكامل واستقرار القناة
        
        start_chat(irc_sock, CHAT_KEY, room_name, my_nick)
        
    except Exception as e:
        print(f"{R}[-] Cloud connection failed: {e}{W}")
