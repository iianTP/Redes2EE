import socket

class MonitorController:
    def __init__(self):
        self.machines = {}
        self.curr_id = 0

    def _get_machine_ip(self,params):

        if not len(params) == 1: return False

        id = params[0]
        return self.machines[id]

    def link_machines(self,req):

        ip_list:list[str] = req['params']

        for ip in ip_list:
            if not ip in self.machines:
                id = f'M{self.curr_id}'
                curr_id += 1
                self.machines[id] = ip

    def list_machines(self,req):
        res = ''
        for id in self.machines.keys():
            res += id
        
        req['send'](f'RES:OK|DATA:{res}')

    def machine_op(self,req,com:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
            ip = self._get_machine_ip(req['params'])
            if not ip: return
            conn.connect((ip,2222))
            conn.sendall(com.encode('utf-8'))
            res = conn.recv(2048).decode('utf-8')
