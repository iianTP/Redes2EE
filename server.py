import socket

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
        self.exit = False

        self.commands = {

            # LISTA COMANDOS DISPONÍVEIS
            'HELP': lambda _: 1,

            # CONECTA 1 OU MAIS MÁQUINAS AO SERVIDOR DE MONITORAMENTO (parâmetros: IPs das máquinas)
            'LINK': lambda ips: ips,

            # LISTA OS IDS DAS MÁQUINAS CONECTADAS
            'LIST': lambda _: 1,

            # FORNECE ATRIBUTOS PRINCIPAIS DE UMA MÁQUINA (parâmetros: ID da máquina)
            'INFO': lambda id: id,

            # FORNECE O ESTADO DO HARDWARE DE UMA MÁQUINA (parâmetros: ID da máquina)
            'STATS': lambda id: id,

            # FORNECE LISTA DE PROCESSOS EM EXECUÇÃO NUMA MÁQUINA (parâmetros: ID da máquina)
            'PROCS': lambda id: id,

            # FORNECE RELATÓRIO DO ESTADO DE UMA MÁQUINA
            'LOG':   lambda id: id

        }


    def start(self):

        print(self.s)
        print(hex(id(self.s)))

        self.s.bind(('', 578))
        self.s.listen(5)

        while not self.exit:
            ws, addr = self.s.accept()

            print('newstock',ws)
            print('add',addr)

            request = ws.recv(4096)

            com, params = request.split(':',1)
            params = params.split(';')



    def sent(self,res):
        pass


