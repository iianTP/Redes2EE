import socket
from parsers.parser import Parser

'''
FORMATO DE REQUEST:
(COMANDO):(PARAMETRO);(PARAMETRO);(PARAMETRO);...

FORMATO DE RESPONSE:
(COMANDO):(LABEL)_(DADO);(LABEL)_(DADO);(LABEL)_(DADO);...

MÚLTIPLOS COMANDOS/CAMPOS -> SEPARAR COM |
'''

class Server:
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.parser = Parser()
        self.exit = False

    def start(self):

        print(self.s)
        print(hex(id(self.s)))

        self.s.bind(('', 2222))
        self.s.listen(5)

        while not self.exit:

            conn, addr = self.s.accept()

            print('newstock',conn)
            print('add',addr)

            request = conn.recv(4096).decode('utf-8')

            func, params = self.parser.get_command(request)

            req = { 'params': params, 'send': self.send }

            func(req)


    def send(self,res):
        pass


