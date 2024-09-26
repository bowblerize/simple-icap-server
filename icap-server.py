import socket

class ICAPServer:
    def __init__(self, host='0.0.0.0', port=1344):
        self.host = host
        self.port = port

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            print(f"ICAP server is running on {self.host}:{self.port}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"Connection from {addr}")
                self.handle_client(client_socket)

    def handle_client(self, client_socket):
        with client_socket:
            request = client_socket.recv(4096).decode('utf-8')
            print(f"Received request:\n{request}")

            if "OPTIONS" in request:
                response = self.create_options_response()
            elif "REQMOD" in request:
                response = self.handle_reqmod(request)
            else:
                response = self.create_icap_error_response()

            client_socket.sendall(response.encode('utf-8'))

    def create_options_response(self):
        # Ответ на запрос OPTIONS
        response = (
            "ICAP/1.0 200 OK\r\n"
            "Methods: REQMOD\r\n"
            "Service: Simple ICAP Server\r\n"
            "ISTag: 1234567890\r\n"
            "Max-Connections: 100\r\n"
            "Options-TTL: 60\r\n"
            "Allow: 204\r\n"  
            "Preview: 1024\r\n"  
            "Encapsulated: null-body=0\r\n"
            "\r\n"
        )
        return response

    def handle_reqmod(self, request):
        if "Preview" in request:
            preview_header = "ICAP/1.0 100 Continue\r\n\r\n"
            return preview_header
        response = (
            "ICAP/1.0 204 No Content\r\n"
            "ISTag: 1234567890\r\n"
            "Encapsulated: null-body=0\r\n"
            "\r\n"
        )
        return response

    def create_icap_error_response(self):
        response = (
            "ICAP/1.0 400 Bad Request\r\n"
            "Server: Simple ICAP Server\r\n"
            "ISTag: 1234567890\r\n"
            "Encapsulated: null-body=0\r\n"
            "\r\n"
        )
        return response

if __name__ == "__main__":
    server = ICAPServer()
    server.start()
