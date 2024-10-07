import socket, json, time, email.utils, http, mimetypes,sys

CLRF = '\r\n'
CLRF_HEADER_END = '\r\n\r\n'
ALLOWED_PATHS = {
            "/" : "index.html",
            "/index" : "index.html",
            "/index.html" : "index.html",
            "/static/index.css": "static/index.css",
            "/static/index.js" : "static/index.js",
            "/static/favicon.png" : "static/favicon.png",
            "/static/media/background.webp" : "static/media/background.webp"
}
HEADER_SERVER_MESSAGE = "Server: Simple python web server using Sockets\n"
PATH_NOT_FOUND = "404.html"
INTERNAL_SERVER_ERROR = "500.html"
HOST = 'localhost'
PORT = 8080


class Response_Header:
    def __init__(self):
        pass
    def static_header (self, status_code):
        protocol_status = str("HTTP/1.1 "+ str(status_code) + " " + http.HTTPStatus(status_code).phrase + CLRF)
        date = str("Date: " + email.utils.formatdate(time.time(), usegmt=True) + CLRF)
        return str(protocol_status + HEADER_SERVER_MESSAGE + date)
    def file_header(self, status_code, file_name, content):
        static = self.static_header(status_code)
        content_type = str("Content-Type: " + mimetypes.guess_type(file_name)[0] + CLRF)
        content_length = str("Content-Length: " + str(len(content)) + CLRF_HEADER_END)
        return str(static + content_type + content_length)
    
class Request_Handler (Response_Header):
    def __init__(self):
        pass
    def handle(self, request):
        try:
            method, path, protocol = request.split(CLRF)[0].split(" ")
            print(method, path)
            match method:
                case "GET":
                    if path in ALLOWED_PATHS:
                        file_path = ALLOWED_PATHS[path]
                        mime = mimetypes.guess_type(file_path)[0].split("/")[0]
                        match mime:
                            case "image":
                                image = self.image_retrieve(file_path)
                                return [str(self.file_header(200, file_path, image)), image]
                            case "text":
                                file = self.file_retrieve(file_path)
                                return [str(self.file_header(200, file_path, file)), file]
                    else:
                        file = self.file_retrieve(PATH_NOT_FOUND)
                        return [str(self.file_header(404, PATH_NOT_FOUND, file)), file]
                case "POST":
                    return self.static_header(501) # To be Implemented
                case _:
                    return self.static_header(405) # Method Not Allowed
        except:
            file = self.file_retrieve(INTERNAL_SERVER_ERROR)
            return [str(self.file_header(500, INTERNAL_SERVER_ERROR, file)), file]
    def file_retrieve(self, file):
        f = open(file, "r")
        return f.read()
    def image_retrieve(self, file):
        f = open(file, "rb")
        return f.read()

class Server (Request_Handler):
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            print(error)
            sys.exit
    def run (self):
        try:
            server = self.server
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.HOST, self.PORT))
            server.listen(5)
            print("HTTP Server running on http://{}:{}/".format(self.HOST,self.PORT))
            try:
                while True:
                    conn, addr = server.accept()
                    request = conn.recv(1024).decode()
                    if request != "":
                        response = self.handle(request)
                        for item in response:
                            if type(item) == bytes:
                                conn.send(item)
                            else:
                                conn.send(item.encode())
                    conn.close()
            except KeyboardInterrupt:
                self.server.close()
                print("Shutting down the server!")
        except OSError as error:
            print(error)


if __name__ == "__main__":
    server = Server(HOST,PORT)
    server.run()
