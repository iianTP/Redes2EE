import socket

class MonitorController:
    def __init__(self):
        self.machines = {}
        self.curr_id = 0

    def _get_machine_ip(self,params,com):
        id = params[0]
        return self.machines[id]

    def link_machines(self,req):

        ip_list:list[str] = req['params']

        for ip in ip_list:
            if not ip in self.machines:
                id = f'M{self.curr_id}'
                self.curr_id += 1
                self.machines[id] = ip

        req['send']('RES:OK|DATA:SUCCESS')

    def list_machines(self,req):
        res = ''
        for id in self.machines.keys():
            res += id
        
        req['send'](f'RES:OK|DATA:{res}')

    def machine_op(self,req,com:str):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:

            ip = self._get_machine_ip(req['params'],com)
            if not ip: 
                req['send']('RES:ERROR|MSG:Ocorreu um erro no reconhecimento do IP da máquina')
                return
            
            if req['params']:
                params = ';'.join(req['params'])
                com += f':{params}'
            
            conn.connect((ip,2223))
            conn.sendall(com.encode('utf-8'))
            res = conn.recv(2048).decode('utf-8')
            print(res)

            try:
                conn.shutdown(socket.SHUT_WR)
            except Exception:
                pass

            fields = res.split('|')
            res_dict = { label: data for f in fields for [label,data] in [f.split(':',1)]}

            if 'RES' in res_dict and res_dict['RES'] == 'OK':
                req['send'](f'RES:OK|DATA:{res_dict['DATA']}')