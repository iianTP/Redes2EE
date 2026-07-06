from server import Server
from parsers.machine_parser import MachineParser

class Machine(Server):
    def __init__(self):
        super().__init__()
        self.parser = MachineParser()


m = Machine()
m.start(port=2223)