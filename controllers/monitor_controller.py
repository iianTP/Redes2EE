import socket,time,threading,os

class MonitorController:
    def __init__(self):
        self.machines = {}
        self.curr_id = 0
        self.t = threading.Thread(target=self._logger_thread)
        self.t.daemon = True
        self.t.start()

    def _get_machine_ip(self,params,com):
        if not params:
            return None
        machine_id = params[0]
        return self.machines.get(machine_id)
    
    def _logger_thread(self):
        while True:
            for machine,ip in self.machines.items():
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
                        conn.connect((ip,2223))
                        conn.sendall('M_STATUS'.encode('utf-8'))
                        res = conn.recv(2048).decode('utf-8').split('DATA:',1)[1].replace(';',' - ')

                        filename = f"./logs/log-{machine}.txt"
                        timestamp = time.strftime('%Y-%m-%d %H:%M:%S')
                        with open(filename, "a") as f:
                            f.write(f"[{timestamp}] {res}\n")

                except Exception as e:
                    pass

            time.sleep(10)

    def link_machines(self,req):

        try:
            ip_list:list[str] = req['params']
        except Exception as e:
            print(e)
            req['send']('RES:ERROR|MSG:ERRO NA COLETA DE PARÂMETROS')
            return
        
        for ip in ip_list:
            if not ip in self.machines:
                id = f'M{self.curr_id}'
                self.curr_id += 1
                self.machines[id] = ip

        req['send']('RES:OK|DISPLAY:NONE|DATA:SUCESSO')

    def list_machines(self,req):
        res = ''
        for id in self.machines.keys():
            res += id
        
        req['send'](f'RES:OK|DISPLAY:LIST|DATA:{res}')

    def rename_machine(self,req):
        try:
            old_id = req['params'][0]
            new_id = req['params'][1]
        except Exception as e:
            print(e)
            req['send']('RES:ERROR|MSG:ERRO NA COLETA DE PARÂMETROS')
            return
        
        if old_id in self.machines and not new_id in self.machines:
            self.machines[new_id] = self.machines.pop(old_id)
            req['send']('RES:OK|DISPLAY:NONE|DATA:SUCESSO')
            return
        
        req['send'](f'RES:ERROR|MSG:MÁQUINA INFORMADA ({old_id}) NÃO EXISTE OU NOVO ID ({new_id}) JÁ ESTÁ SENDO USADO')

    def get_machine_log(self,req):
        try:
            id = req['params'][0]
        except Exception as e:
            print(e)
            req['send']('RES:ERROR|MSG:ERRO NA COLETA DE PARÂMETROS')
            return
        
        file = f'./logs/log-{id}.txt'

        if os.path.exists(file):
            with open(file,'r') as f:
                log = f.read()
            req['send'](f'RES:OK|DISPLAY:NONE|DATA:\n{log}')
        else:
            req['send']("RES:ERROR|MSG:Nenhum histórico encontrado para esta máquina.")
        

        
    def machine_op(self,req,com:str):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
                ip = self._get_machine_ip(req['params'],com)
                if not ip:
                    req['send']('RES:ERROR|MSG:ID DA MÁQUINA NÃO ENCONTRADO OU NÃO CONECTADO')
                    return

                if req['params']:
                    params = ';'.join(req['params'])
                    com += f':{params}'

                conn.connect((ip,2223))
                conn.sendall(com.encode('utf-8'))
                res = conn.recv(2048).decode('utf-8', errors='ignore')
                print(res)

                try:
                    conn.shutdown(socket.SHUT_WR)
                except Exception:
                    pass

                fields = res.split('|')
                res_dict = {}
                for field in fields:
                    if ':' not in field:
                        continue
                    label, data = field.split(':', 1)
                    res_dict[label] = data

                if 'RES' in res_dict and res_dict['RES'] == 'OK':
                    req['send'](f"RES:OK|DISPLAY:{res_dict['DISPLAY']}|DATA:{res_dict['DATA']}")
                else:
                    req['send']('RES:ERROR|MSG:RESPOSTA INVÁLIDA DA MÁQUINA')
        except (ConnectionRefusedError, TimeoutError, OSError) as exc:
            req['send']('RES:ERROR|MSG:Não foi possível contactar a máquina monitorada.')