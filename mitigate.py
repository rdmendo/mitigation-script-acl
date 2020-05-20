from datetime import datetime
from nornir import InitNornir
from nornir.plugins.tasks import networking, text
from nornir.plugins.functions.text import print_title, print_result
from nornir.plugins.tasks.networking import netmiko_send_command
from netaddr import IPNetwork, AddrFormatError
from colorama import Fore
from tabulate import tabulate

start_time = datetime.now()
nr = InitNornir(config_file="config.yml", dry_run=True)
ip_list = []
result = ""
net = ""
task_list = ["divert", "no_divert", "divert_all", "no_divert_all"]
table = []
headers = ["HOSTNAME", "NETWORK ADDRESS", "ACTIVITY", "STATUS"]
while True:
    try:
        print("*" * 80)
        print("Supported Task: [DIVERT, NO_DIVERT, DIVERT_ALL, NO_DIVERT_ALL]")
        print("*" * 80)
        mitigations = input("DDOS MITIGATION TASK\t\t:\t")
        tasks = mitigations.lower()
        if tasks not in task_list:
            raise Exception("input not a valid task")

        if tasks == "divert_all":
            break
        elif tasks == "no_divert_all":
            break

    except Exception:
        print(Fore.RED + ("NOT A VALID TASK") + Fore.RESET)
        continue

    try:
        net_ip = input("NETWORK ADDRESS\t\t\t:\t")
        net = IPNetwork(net_ip)
        print("*" * 80)

        # will loop the ip_list and verify
        # if the ip is existing or allowed divert

        with open("inventory/network_addr.cfg", "r") as listed_ip:
            for allowed_ip in listed_ip:
                ip_list.append(allowed_ip.strip())

        if net_ip not in ip_list:
            # will raise exception if input is not on the ip_list
            raise Exception(f"{net_ip} not added in ip_list!")
        break

    except AddrFormatError:
        print(
            Fore.RED
            + (f"INVALID! {net_ip} NOT A VALID IP ADDRESS OR CIDR FORMAT!")
            + Fore.RESET
        )
        continue

    except Exception:
        print(Fore.RED + (f"INVALID! {net_ip} IS NOT ALLOWED FOR DIVERT!") + Fore.RESET)
        continue


def mitigation(task):
    r = task.run(
        task=text.template_file,
        mitigate=tasks,
        hosts=nr.inventory.hosts,
        net=net,
        name="BGP CONFIGURATIONS",
        template="divert.j2",
        path=f"templates/{task.host}",
    )

    task.host["config"] = r.result

    # Deploy that configuration to the device using NAPALM

    task.run(
        task=networking.napalm_configure,
        name="Loading Configuration on the device",
        replace=False,
        configuration=task.host["config"],
    )

show_adv_headers = ["ADVERTISED PREFIXES IN INCAPSULA NETWORK via eBGP"]
# show_adv_headers = ["Network", "Nexthop", "Weight"]
table_adv = []

def show_adv_routes(task):
        hostname = task.host.hostname
        tunnel_ip_r1 = ["172.17.32.161", "172.17.160.9"]
        tunnel_ip_r2 = ["172.17.32.165", "172.17.160.13"]
        
        if hostname == "192.168.1.1":
            for tunnel in tunnel_ip_r1:
                adv_routes = task.run(netmiko_send_command, command_string=f"show ip bgp neighbors {tunnel} advertised-routes",use_textfsm=True)
                task.host['adv_routes'] = adv_routes.result
                net_adv_routes = task.host['adv_routes']
            
            for prefix in net_adv_routes:
                bgp_prefix = prefix['network']
                # bgp_hop = prefix['next_hop']
                # bgp_weight = prefix['weight']
                table_adv.append([bgp_prefix])

def main() -> None:
    nr.data.dry_run = False
    print_title("DDOS MITIGATION IS CURRENTLY RUNNING! PLEASE WAIT!")
    result = nr.run(task=mitigation)
    adv_routes = nr.run(task=show_adv_routes)
    # print_result(adv_routes)
    failed_host = result.failed_hosts.keys()
    hosts = nr.inventory.hosts

    if tasks == "divert":
        activity = tasks.upper()
        for host in hosts:
            if host in failed_host:
                table.append([host, net, activity, Fore.RED + ("FAILED") + Fore.RESET])
            else:
                table.append(
                    [host, net, activity, Fore.GREEN + ("SUCCESS") + Fore.RESET]
                )

    elif tasks == "no_divert":
        activity = tasks.upper()
        for host in hosts:
            if host in failed_host:
                table.append([host, net, activity, Fore.RED + ("FAILED") + Fore.RESET])
            else:
                table.append(
                    [host, net, activity, Fore.GREEN + ("SUCCESS") + Fore.RESET]
                )

    elif tasks == "divert_all":
        activity = tasks.upper()
        for host in hosts:
            if host in failed_host:
                table.append(
                    [
                        host,
                        "113.61.42 - 58.0",
                        activity,
                        Fore.RED + ("FAILED") + Fore.RESET,
                    ]
                )
            else:
                table.append(
                    [
                        host,
                        "113.61.42 - 58.0",
                        activity,
                        Fore.GREEN + ("SUCCESS") + Fore.RESET,
                    ]
                )

    elif tasks == "no_divert_all":
        activity = tasks.upper()
        for host in hosts:
            if host in failed_host:
                table.append(
                    [
                        host,
                        "113.61.42 - 58.0",
                        activity,
                        Fore.RED + ("FAILED") + Fore.RESET,
                    ]
                )
            else:
                table.append(
                    [
                        host,
                        "113.61.42 - 58.0",
                        activity,
                        Fore.GREEN + ("SUCCESS") + Fore.RESET,
                    ]
                )
                
            
if __name__ == "__main__":
    main()
    date_time = datetime.now() - start_time
    print("")
    print(tabulate(table, headers, tablefmt="rst"))
    print(tabulate(table_adv, show_adv_headers,tablefmt="rst"))
    print(Fore.GREEN + "mitigation time: " + Fore.RESET + str(date_time))



