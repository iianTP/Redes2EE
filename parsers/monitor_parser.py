from parsers.parser import Parser
from controllers.monitor_controller import MonitorController

class MonitorParser(Parser):
    def __init__(self):
        super().__init__()
        self.mc = MonitorController()
        self.commands = {

            'HELP': {
                'func': lambda req: self.help(req),
                'desc': '-> Lista comandos disponíveis'
            },

            'LINK': {
                'func': lambda req: self.mc.link_machines(req),
                'desc': ':(ip_1);(ip_2);(ip_3);... -> Conecta 1 ou mais máquinas ao servidor de monitoramento'
            },

            'LIST': {
                'func': lambda req: self.mc.list_machines(req),
                'desc': ' -> Lista os IDs das máquinas conectadas'
            },

            'INFO': {
                'func': lambda req: self.mc.machine_info(req),
                'desc': ':(id) -> Fornece atributos principais de uma máquina (parâmetros: ID da máquina)'
            },

            'STATUS': {
                'func': lambda req: self.mc.machine_status(req),
                'desc': ':(id) -> Fornece o estado do hardware de uma máquina'
            },

            'PROCS': {
                'func': lambda req: self.mc.machine_procs(req),
                'desc': ':(id) -> Fornece lista de processos em execução numa máquina'
            },

            'LOG': {
                'func': lambda req: 1,
                'desc': ':(id) -> Fornece relatório do estado de uma máquina'
            },

        }

    def help(self,req):
        for com, info in self.commands.items():
            print(com,info['desc'],'\n')
        
        req['send']('asdasdasdasdasdasdasdasdasd')