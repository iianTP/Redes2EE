
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

    def list_machines(self):
        for id in self.machines.keys():
            print(id)

    def machine_info(self,req):
        ip = self._get_machine_ip(req['params'])
        if not ip: return


    def machine_status(self,req):
        ip = self._get_machine_ip(req['params'])
        if not ip: return

    def machine_procs(self,req):
        ip = self._get_machine_ip(req['params'])
        if not ip: return