import socket, json, time, email.utils, http, mimetypes,sys


HOST = 'localhost'
PORT = 8080
ALLOWED_PATHS = {
            "/" : "index.html",
            "/index" : "index.html",
            "/index.html" : "index.html",
            "/static/index.css": "static/index.css",
            "/static/index.js" : "static/index.js",
            "/static/favicon.png" : "static/favicon.png",
            "/static/media/background.webp" : "static/media/background.webp",
            "/static/media/mario_themesong.aac" : "static/media/mario_themesong.aac",
            "/static/media/video.webm" : "static/media/video.webm",
            "/static/media/file.pdf" : "static/media/file.pdf",
}
POST_PATH = "/horario"
HEADER_SERVER_MESSAGE = "Server: Simple python web server using Sockets\n"
CONSOLE_SERVER_RUNNING_MESSAGE = "HTTP Server running on http://{}:{}/".format(HOST,PORT)
PATH_NOT_FOUND = "404.html"
INTERNAL_SERVER_ERROR = "500.html"
HEADER_LINE_DELIMITER = '\r\n'
HEADER_END_DELIMITER = '\r\n\r\n'



class Response_Header:
    def __init__(self):
        pass
    def static_header (self, status_code):
        protocol_status = str("HTTP/1.1 "+ str(status_code) + " " + http.HTTPStatus(status_code).phrase + HEADER_LINE_DELIMITER)
        date = str("Date: " + email.utils.formatdate(time.time(), usegmt=True) + HEADER_LINE_DELIMITER)
        return str(protocol_status + HEADER_SERVER_MESSAGE + date)
    def file_header(self, status_code, file_name, content):
        static = self.static_header(status_code)
        content_type = str("Content-Type: " + mimetypes.guess_type(file_name)[0] + HEADER_LINE_DELIMITER)
        content_length = str("Content-Length: " + str(len(content)) + HEADER_END_DELIMITER)
        return str(static + content_type + content_length)
    
class Request_Handler (Response_Header):
    def __init__(self):
        pass
    def handle(self, request):
        try:
            method, path, protocol = request.split(HEADER_LINE_DELIMITER)[0].split(" ")
            print(method, path)
            match method:
                case "GET":
                    if path in ALLOWED_PATHS:
                        file_path = ALLOWED_PATHS[path]
                        mime = mimetypes.guess_type(file_path)[0].split("/")[0]
                        match mime:
                            case "image":
                                image = self.media_retrieve(file_path)
                                return [str(self.file_header(200, file_path, image)), image]
                            case "text":
                                file = self.file_retrieve(file_path)
                                return [str(self.file_header(200, file_path, file)), file]
                            case "audio":
                                audio = self.media_retrieve(file_path)
                                return [str(self.file_header(200, file_path, audio)), audio]
                            case "video":
                                video = self.media_retrieve(file_path)
                                return [str(self.file_header(200, file_path, video)), video]
                            case "application":
                                file = self.media_retrieve(file_path)
                                return [str(self.file_header(200, file_path, file)), file]
                    else:
                        file = self.file_retrieve(PATH_NOT_FOUND)
                        return [str(self.file_header(404, PATH_NOT_FOUND, file)), file]
                case "POST":
                    if path == POST_PATH:
                        horario = str(email.utils.localtime())
                        horario = str({"horario local do servidor" : horario})
                        return [str(self.file_header(200, 'post.json', str(horario))), horario]

                    else:
                        wrong_path = "The API is At /horario"
                        return self.static_header(400) + HEADER_LINE_DELIMITER+ wrong_path
                case _:
                    return self.static_header(405) # Method Not Allowed
        except:
            file = self.file_retrieve(INTERNAL_SERVER_ERROR)
            return [str(self.file_header(500, INTERNAL_SERVER_ERROR, file)), file]
    def file_retrieve(self, file):
        f = open(file, "r")
        return f.read()
    def media_retrieve(self, file):
        f = open(file, "rb")
        return f.read()

class Server (Request_Handler):
    def __init__(self, host, port):
        self.HOST = host
        self.PORT = port
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error as error:
            sys.exit(str(error))
    def run (self):
        try:
            server = self.server
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind((self.HOST, self.PORT))
            server.listen(5)
            print(CONSOLE_SERVER_RUNNING_MESSAGE)
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
                sys.exit("Shutting down the server!")
        except OSError as error:
            sys.exit(str(error))

if __name__ == "__main__":
    server = Server(HOST,PORT)
    server.run()
