import socket
from parsers.parser import Parser

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parser = Parser()
        self.exit = False

    def start(self,port=2222):

        print(self.s)
        print(hex(id(self.s)))

        self.s.bind(('', port))
        self.s.listen(5)

        while not self.exit:

            print("Aguardando nova conexão...")
            conn, addr = self.s.accept()
            print(f"Conexão aceita de: {addr}")

            print('newstock',conn)
            print('add',addr)

            while True:

                try:
                    request = conn.recv(4096).decode('utf-8')
                    print(request)
                    if not request: break
                    func, params = self.parser.get_command(request)
                    req = { 'params': params, 'send': lambda res: self.send(conn, res) }
                    func(req)
                except (ConnectionAbortedError,ConnectionResetError):
                    print(f"Conexão com {addr} foi encerrada.")
                    break


    def send(self,conn:socket.socket,res:str):
        conn.sendall(res.encode('utf-8'))


