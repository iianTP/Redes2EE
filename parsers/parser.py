
class Parser:
    def __init__(self):
        self.commands = {}

    def get_command(self,req:str):

        com, params = req.split(':',1)
        params = [p.strip() for p in params.split(';')]

        if not com in self.commands: return

        return self.commands[com]['func'], params
    
    def help(self):
        for com, info in self.commands.items():
            print(com,info['desc'],'\n')

    def not_found(self,req):
        req['send']('RES:ERROR|MSG:COMANDO NÃO ENCONTRADO (use o comando \'HELP\' para visualizar comandos disponíveis)')