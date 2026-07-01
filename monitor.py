from server import Server
from parsers.monitor_parser import MonitorParser

class Monitor(Server):
    def __init__(self):
        super().__init__()
        self.parser = MonitorParser()