import socket
from parsers.display_parser import DisplayParser

class Client:
    def __init__(self,ip):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_port = ( self._normalize_host(ip), 2222 )
        self.exit = False
        self.dp = DisplayParser()

    @staticmethod
    def _normalize_host(ip):
        host = (ip or '').strip().lower()
        if host in {'', '1', 'localhost', 'local', 'loopback'}:
            return '127.0.0.1'
        return ip.strip()

    def start(self):

        print('Conectando ao servidor...')

        while True:
            try:
                self.s.connect(self.host_port)
                break
            except ConnectionRefusedError:
                continue

        print('Conexão estabelecida.\n')

        while not self.exit:
            
            command = ''
            while command == '' : 
                print('>>>',end='')
                command = input()

            for com in command.split('|'):
                if com == 'EXIT':
                    self.exit = True
                    continue

                self.s.sendall(com.encode('utf-8'))

                self.receive()

    def receive(self):

        try:
            response = self.s.recv(2048).decode('utf-8', errors='ignore')
        except (ConnectionResetError, OSError):
            print('\nConexão encerrada pelo servidor.')
            self.exit = True
            return

        if not response:
            print('\nO servidor fechou a conexão sem enviar uma resposta.')
            self.exit = True
            return

        res_dict = {}

        for field in response.split('|'):
            if ':' not in field:
                continue
            split_field = field.split(':',1)
            label = split_field[0]
            data = split_field[1] if len(split_field) > 1 else ''
            res_dict[label] = data

        print()

        if not res_dict:
            print('Resposta inválida recebida do servidor.')
            return

        if res_dict.get('RES') == 'ERROR':
            print(res_dict.get('MSG', 'Erro desconhecido.'))
        elif res_dict.get('DISPLAY') == 'NONE':
            print(res_dict.get('DATA', ''))
        else:
            display_func,_ = self.dp.get_command(res_dict['DISPLAY'])
            display_func(res_dict['DATA'])

print('ip do servidor de monitoramento: ',end='')
c = Client(input())
c.start()