import mimetypes
import pathlib
import os
import socket
import json
from datetime import datetime
from time import sleep
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, unquote_plus


class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):

        url = urlparse(self.path)

        if url.path == "/":
            self.send_http_file("index.html")
    
        elif url.path == "/contact":
           self.send_http_file("contact.html")
        
        elif url.path == "/thanks":
           self.send_http_file("thanks.html")
        else:
            if pathlib.Path().joinpath(url.path[1:]).exists():
                self.send_static()
            else:
                self.send_http_file('error.html')



    def do_POST(self):

        data = self.rfile.read(int(self.headers['Content-Length']))
        self.simple_client("localhost", 5000, data)
        
        self.send_response(302)
        self.send_header('Location', '/')
        self.end_headers()

    def simple_client(self, host, port, data_form):
        with socket.socket() as s:
            while True:
                try:
                    s.connect((host, port))
                    s.sendall(data_form)
                    break
                except ConnectionRefusedError:
                    sleep(0.5) 

    def parse_form_data(self, data):
        raw_params = data.split("&")
        data = {key.title(): value for key, value in [param.split("=") for param in raw_params]}
        return data

    def send_http_file(self, html_page, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        with open(html_page, "rb") as file:
            self.wfile.write(file.read())

    def send_static(self):

        self.send_response(200)
        mt = mimetypes.guess_type(self.path)
        if mt:
            self.send_header("Content-type", mt[0])
        else:
            self.send_header("Content-type", 'text/plain')
        self.end_headers()
        with open(f'.{self.path}', 'rb') as file:
            self.wfile.write(file.read())

def socket_server(host, port):
    while True:

        with socket.socket() as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind((host, port))
            s.listen(1)
            conn, addr = s.accept()
            print(f"Connected by {addr}")
            with conn:
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    save_data(data)
                    
                    # conn.send(str(data_dict).encode('utf-8'))

def save_data(data): 

    newpath = r'storage/data.json' 
    folder, file= newpath.split("/")
    if not os.path.exists(folder):
        os.mkdir(folder)
    # if not os.path.exists(newpath):
    #     with open('storage/data.json', 'w') as outfile:
    #         pass

    data_parse = unquote_plus(data.decode())
    data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}
    capitals = {}

    if os.path.exists(newpath):
        with open('storage/data.json', 'r') as outfile:
            capitals_json = outfile.read()

        capitals = json.loads(capitals_json)
    capitals.update({str(datetime.now()): data_dict})

    with open('storage/data.json', 'w') as outfile:
        json.dump(capitals, outfile)
    
if __name__ == "__main__":

    server = HTTPServer(("localhost", 5353), MyHandler)
    
    thread = Thread(target=server.serve_forever)
    thread2 = Thread(target=socket_server, args=("localhost", 5000))

    thread.start()
    thread2.start() 