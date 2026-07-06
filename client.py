import socket

class Client:
    def __init__(self,ip):
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.host_port = ( ip, 2222 )
        self.exit = False

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

            if command == 'EXIT':
                self.exit = True
                continue

            self.s.sendall(command.encode('utf-8'))

            self.receive()

    def receive(self):
        response = self.s.recv(2048).decode('utf-8')
        res_dict = {}

        for field in response.split('|'):
            split_field = field.split(':',1)
            label = split_field[0]
            data = split_field[1]
            res_dict[label] = data

        if res_dict['RES'] == 'ERROR':
            print(res_dict['MSG'])
        elif res_dict['RES'] == 'OK':
            print(res_dict['DATA'])


print('ip do servidor de monitoramento: ',end='')
c = Client(input())
c.start()