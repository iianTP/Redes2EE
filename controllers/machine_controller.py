import platform, psutil, cpuinfo

class MachineController:
    def __init__(self):
        self.info = {
            'SO':           platform.system(),
            'E-SO':         platform.release(),
            'V-SO':         platform.version(),
            'ARQ':          platform.architecture(),
            'CPU':          cpuinfo.get_cpu_info()['brand_raw'],
            'FIS-CORES':    psutil.cpu_count(logical=False),
            'LOG-CORES':    psutil.cpu_count(logical=True),
            'RAM':          psutil.virtual_memory().total/(1024**3),
            'DISC':         psutil.disk_usage('/').total/(1024**3)
        }
    
    def get_info(self,req):
        res = []
        for label,data in self.info.items():
            if label in ['RAM','DISC']:
                res.append(f'{label}_{data:.2f}')
            else:
                res.append(f'{label}_{data}')
        req['send'](f'RES:OK|DISPLAY:LIST|DATA:{';'.join(res)}')

    def get_status(self,req):
        mem_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        cpu_usage = psutil.cpu_percent()

        res = f'RAM_{mem_usage};DISC_{disk_usage};CPU_{cpu_usage}'

        req['send'](f'RES:OK|DISPLAY:USAGE|DATA:{res}')

    def get_procs(self,req,sort_method='memory'):

        procs = []

        try:
            limit = int(req['params'][1])
        except Exception:
            req['send']('RES:ERROR|MSG:Um erro ocorreu na coleta de parâmetros.')
            return
        
        for p in psutil.process_iter():
            proc = p.as_dict(attrs=['pid','name','memory_percent','cpu_percent'])
            if not None in proc.values():
                procs.append(proc)

        sorted_procs:list[dict] = sorted(procs, key=lambda p: p[f'{sort_method}_percent'], reverse=True)[:limit]

        proc_str_list = []
        for p in sorted_procs:

            attr_list = [
                f'{p['pid']}',
                p['name'],
                f'{p['memory_percent']:.2f}',
                f'{p['cpu_percent']:.2f}'
            ]

            proc_str_list.append('_'.join(attr_list))

        res = 'ID_NOME_RAM(%)_CPU(%);' + ';'.join(proc_str_list)

        req['send'](f'RES:OK|DISPLAY:TABLE|DATA:{res}')
        
