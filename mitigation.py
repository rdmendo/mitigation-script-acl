from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
from prettytable import PrettyTable
from netaddr import IPNetwork,AddrFormatError
from colorama import *

nr = InitNornir(config_file='config.yml', dry_run=True)
ip_list = []
RED = '\033[31m'
yellow='\033[93m'
net = ""
task_list = ['divert','no_divert', 'divert_all', 'no_divert_all']
while True:
   try:
      print ('*' * 80)
      print("Supported Task: [DIVERT , NO_DIVERT, DIVERT_ALL, NO_DIVERT_ALL] ")
      print ('*' * 80)
      mitigations = input("DDOS MITIGATION TASK\t\t:\t")
      tasks = mitigations.lower()
      if tasks not in task_list:
         raise Exception("input not a valid task")
      
      if tasks == 'divert_all':
         break
      elif tasks == 'no_divert_all':
         break
      
   except:
      print(RED + ("NOT A VALID TASK") + Style.RESET_ALL)
      continue
      
   try:
        net_ip = input("NETWORK ADDRESS\t\t\t:\t")
        net = IPNetwork(net_ip)
        print ('*' * 80)
        
      
      #will loop the ip_list and verify if the ip is existing or allowed for divert
      
        with open ('/root/nornir_framework/ddos_mitigation/inventory/network_addr.cfg', 'r') as listed_ip:
            for allowed_ip in listed_ip:
                ip_list.append(allowed_ip.strip())

        if net_ip not in ip_list:
            # will raise exception if input is not on the ip_list
            raise Exception (f"{net_ip} not added in ip_list!") 
        break
     
   except AddrFormatError:
        print(RED+(f"INVALID! {net_ip} NOT A VALID IP ADDRESS OR CIDR FORMAT!") + Style.RESET_ALL)
        continue
    
   except:
      print(RED+(f"INVALID! {net_ip} IS NOT ALLOWED FOR DIVERT!") + Style.RESET_ALL)
      continue
      
def divert(task):
        r = task.run (task=text.template_file,
        mitigate = tasks,
        hosts = nr.inventory.hosts,
        net = net,
        name= "BGP CONFIGURATIONS",
        template= "divert.j2",
        path=f"templates/{task.host}")
        
        task.host['config'] = r.result 
     
     # Deploy that configuration to the device using NAPALM

        task.run(task=networking.napalm_configure,
            
             name=f"Loading Configuration on the device",
             replace=False,
             configuration=task.host["config"])
     
nr.data.dry_run = False
print_title("DDOS MITIGATION IS CURRENTLY RUNNING! PLEASE WAIT!")
result = nr.run(task=divert)

if tasks == 'divert':
   print("")
   x = PrettyTable()
   tasks = tasks.upper()
   x.field_names = ["NETWORK ADDRESS", "ACTIVITY", "STATUS"]
   x.add_row([net, tasks, Fore.GREEN + ("SUCCESSFUL")+ Style.RESET_ALL])
   print(x)
   print(yellow + (f"\n{net.ip} has been DIVERTED to INCAPSULA")+ Style.RESET_ALL)
elif tasks == 'no_divert':
   
   print("")
   x = PrettyTable()
   tasks = tasks.upper()
   x.field_names = ["NETWORK ADDRESS", "ACTIVITY", "STATUS"]
   x.add_row([net, tasks, Fore.GREEN + ("SUCCESSFUL")+ Style.RESET_ALL])
   print(x)
   print(yellow + (f"\n{net.ip} has been REMOVED in DIVERTED NETWORKS")+ Style.RESET_ALL)
   
elif tasks == 'divert_all':
   print("")
   x = PrettyTable()
   tasks = tasks.upper()
   x.field_names = ["NETWORK ADDRESS", "ACTIVITY", "STATUS"]
   x.add_row(["113.61.42 - 58.0", tasks, Fore.GREEN + ("SUCCESSFUL")+ Style.RESET_ALL])
   print(x)
   print(yellow +("\nALL NETWORKS HAS BEEN DIVERTED")+ Style.RESET_ALL)

elif tasks == 'no_divert_all':
   print("")
   x = PrettyTable()
   tasks = tasks.upper()
   x.field_names = ["NETWORK ADDRESS", "ACTIVITY", "STATUS"]
   x.add_row(["113.61.42 - 58.0", tasks, Fore.GREEN + ("SUCCESSFUL")+ Style.RESET_ALL])
   print(x)
   print(yellow + ("\nALL NETWORKS HAS BEEN REMOVED IN DIVERT")+ Style.RESET_ALL)

showlogs = input("\nWould you like to see the background process? yes/no: ")

if showlogs == "" or "yes":
      print_result(result)
elif showlogs == 'no' or 'n':
   print("\nTHANK YOU FOR USING DDOS MITIGATION HELPER")
   

