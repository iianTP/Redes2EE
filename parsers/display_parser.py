from parsers.parser import Parser
from controllers.display_controller import DisplayController

class DisplayParser(Parser):
    def __init__(self):
        super().__init__()

        self.dc = DisplayController()

        self.commands = {

            'TABLE': { 'func': lambda data: self.dc.display_table(data) },

            'USAGE': { 'func':  lambda data: self.dc.display_usage(data) },

            'LIST': { 'func': lambda data: self.dc.display_list(data) }

        }