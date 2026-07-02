from parsers.parser import Parser
from controllers.machine_controller import MachineController

class MachineParser(Parser):
    def __init__(self):
        super().__init__()
        self.mc = MachineController()
        self.commands = {

            'M_INFO': lambda req: self.mc.get_info(req),

            'M_STATUS': lambda req: self.mc.get_status(req),

            'M_PROCS': lambda req: self.mc.get_procs(req)

        }