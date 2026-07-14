from parsers.parser import Parser
from controllers.monitor_controller import MonitorController

class MonitorParser(Parser):
    def __init__(self):
        super().__init__()
        self.mc = MonitorController()
        self.commands = {

            'HELP': {
                'func': lambda req: self.help(req),
                'desc': ' -> Lista comandos disponíveis'
            },

            'LINK': {
                'func': lambda req: self.mc.link_machines(req),
                'desc': ':(ip-1)_(ip-2)_(ip-3)_... -> Conecta 1 ou mais máquinas ao servidor de monitoramento'
            },

            'LIST': {
                'func': lambda req: self.mc.list_machines(req),
                'desc': ' -> Lista os IDs das máquinas conectadas'
            },

            'RENAME': {
                'func': lambda req: self.mc.rename_machine(req),
                'desc': ':(id-antigo)_(id-novo) -> Renomeia o ID da máquina informada'
            },

            'INFO': {
                'func': lambda req: self.mc.machine_op(req,'M_INFO'),
                'desc': ':(id) -> Fornece atributos principais de uma máquina (parâmetros: ID da máquina)'
            },

            'STATUS': {
                'func': lambda req: self.mc.machine_op(req,'M_STATUS'),
                'desc': ':(id) -> Fornece o estado do hardware de uma máquina'
            },

            'PROCS': {
                'func': lambda req: self.mc.machine_op(req,'M_PROCS'),
                'desc': ':(id)_(limite)_(tipo-de-ordenação-RAM/CPU) -> Fornece lista de processos em execução numa máquina'
            },

            'LOG': {
                'func': lambda req: self.mc.get_machine_log(req),
                'desc': ':(id) -> Fornece relatório do estado de uma máquina'
            },

        }

    def help(self,req):
        res = []
        count = 1 
        for com, info in self.commands.items():
            res.append(f'{count}_{com}{info['desc']}\n')
            count += 1

        req['send'](f'RES:OK|DISPLAY:HELP|DATA:{';'.join(res)}')