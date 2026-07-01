from parser import Parser
from controllers.monitor_controller import MonitorController

class MonitorParser(Parser):
    def __init__(self):
        super().__init__()
        self.mc = MonitorController()
        self.commands = {

            'HELP': {
                'func': lambda _: self.help(),
                'desc': 'LISTA COMANDOS DISPONÍVEIS'
            },

            'LINK': {
                'func': lambda req: self.mc.link_machines(req),
                'desc': 'CONECTA 1 OU MAIS MÁQUINAS AO SERVIDOR DE MONITORAMENTO'
            },

            'LIST': {
                'func': lambda _: self.mc.list_machines(),
                'desc': 'LISTA OS IDS DAS MÁQUINAS CONECTADAS'
            },

            'INFO': {
                'func': lambda req: self.mc.machine_info(req),
                'desc': 'FORNECE ATRIBUTOS PRINCIPAIS DE UMA MÁQUINA (parâmetros: ID da máquina)'
            },

            'STATUS': {
                'func': lambda req: self.mc.machine_status(req),
                'desc': 'FORNECE O ESTADO DO HARDWARE DE UMA MÁQUINA (parâmetros: ID da máquina)'
            },

            'PROCS': {
                'func': lambda req: self.mc.machine_procs(req),
                'desc': 'FORNECE LISTA DE PROCESSOS EM EXECUÇÃO NUMA MÁQUINA (parâmetros: ID da máquina)'
            },

            'LOG': {
                'func': lambda _: 1,
                'desc': 'FORNECE RELATÓRIO DO ESTADO DE UMA MÁQUINA'
            },

        }