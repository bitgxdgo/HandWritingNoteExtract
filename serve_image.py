from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import webbrowser
import os

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"启动本地服务器在端口 {port}")
    httpd.serve_forever()

# 在新线程中启动服务器
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()
