from tabulate import tabulate

class DisplayController:

    def display_list(self,data:str):
        split_data = [r.split('_') for r in data.split(';')]
        print(tabulate(split_data))

    def display_table(self,data:str):
        split_data = [p.split('_') for p in data.split(';')]
        print(tabulate(split_data,headers='firstrow',tablefmt='fancy_outline'))

    def display_usage(self,data:str):

        split_data = data.split(';')
        fields = [f.split('_',1) for f in split_data]

        for f in fields:
            label = f[0]
            percent = float(f[1])
            self._print_usage_bar(label,percent)
        
    def _print_usage_bar(self,label,percent):
        filled = '█' * int(percent)
        space = '-' * int(100 - percent)
        print(f'{label}: [{filled}{space}] - {percent}%\n')

