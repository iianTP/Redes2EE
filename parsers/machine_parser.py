from parser import Parser
from controllers.machine_controller import MachineController

class MachineParser(Parser):
    def __init__(self):
        super().__init__()
        self.mc = MachineController()
        self.commands = {

            'M_INFO': {
                'func': lambda _: self.mc.get_info(),
                'desc': 'LISTA COMANDOS DISPONÍVEIS'
            },

            'M_STATUS': {
                'func': lambda _: self.mc.get_status(),
                'desc': 'LISTA COMANDOS DISPONÍVEIS'
            },

            'M_PROCS': {
                'func': lambda _: self.mc.get_procs(),
                'desc': 'LISTA COMANDOS DISPONÍVEIS'
            },

        }