
class Parser:
    def __init__(self):
        self.commands = {}

    def get_command(self,req:str):

        com = req
        params = []

        if ':' in req:
            [com, params] = req.split(':',1)
            params = [p.strip() for p in params.split(';')]

        if not com in self.commands: return self.not_found, []

        return self.commands[com]['func'], params

    def not_found(self,req):
        req['send']('RES:ERROR|MSG:COMANDO NÃO ENCONTRADO (use o comando \'HELP\' para visualizar comandos disponíveis)')