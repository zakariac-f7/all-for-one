import requests
import ipaddress
import time
import socket
from loguru import logger
from humanize import precisedelta
import pyfiglet
import emoji
from tqdm import tqdm
from rich.console import Console

SUCCESS_COLOR = "\033[92m"  # Green
INFO_COLOR = "\033[94m"     # Blue
ERROR_COLOR = "\033[91m"    # Red
RESET_COLOR = "\033[0m"     # Reset color

telegram_channel = "✨https://t.me/+YmBfJE0gd503NjFk✨"

def print_ascii_art():
    ascii_art_text = pyfiglet.figlet_format('Aywa kan hna', font='small')
    logger.info(f"\033[91m{ascii_art_text}\033[0m")

def extract_hosts_from_ranges(ip_ranges):
    hosts = []
    for ip_range in ip_ranges:
        network = ipaddress.ip_network(ip_range)
        for host in network.hosts():
            hosts.append(str(host))
    return hosts

def check_response_types(target_host, timeout):
    try:
        start_time_host = time.time()
        response = requests.get(f"http://{target_host}", timeout=timeout)
        elapsed_time_host = time.time() - start_time_host

        response_text = response.text
        response_code = response.status_code
        server_header = response.headers.get('Server', 'Unknown')

        result_http = f"{target_host} (HTTP) - Response Code: {response_code}, Elapsed Time: {elapsed_time_host:.2f}s, Server: {server_header}"

        logger.success(f"{INFO_COLOR}{result_http}{RESET_COLOR}")

        with open("results.txt", "a") as file:
            file.write(result_http + "\n\n")

    except (requests.exceptions.RequestException, requests.exceptions.Timeout) as e:
        result_http = f"{target_host} (HTTP) - timeout"
        logger.error(f"{INFO_COLOR}{result_http}{RESET_COLOR}")

def check_specific_ports(target_host, timeout, ports):
    for port in ports:
        try:
            start_time_port = time.time()
            with socket.create_connection((target_host, port), timeout=timeout):
                elapsed_time_port = time.time() - start_time_port
                result_port = f"{target_host} (Port {port}) - Open, Elapsed Time: {elapsed_time_port:.2f}s"
                logger.success(f"{SUCCESS_COLOR}{result_port}{RESET_COLOR}")
        except (socket.timeout, socket.error) as e:
            result_port = f"{target_host} (Port {port}) - Closed"
            logger.error(f"{ERROR_COLOR}{result_port}{RESET_COLOR}")

def select_target_hosts():
    console = Console()

    cloudflare_ranges_ipv4 = (
        '104.16.0.0/12',
        '103.21.244.0/22',
        '103.22.200.0/22',
        '103.31.4.0/22',
        '141.101.64.0/18',
        '108.162.192.0/18',
        '190.93.240.0/20',
        '188.114.96.0/20',
        '197.234.240.0/22',
        '198.41.128.0/17',
        '162.158.0.0/15',
        '172.64.0.0/13',
        '131.0.72.0/22',
    )

    cloudfront_ranges_ipv4 = (
        "120.52.22.96/27",
        "205.251.249.0/24",
        "180.163.57.128/26",
        "204.246.168.0/22",
        "111.13.171.128/26",
        "18.160.0.0/15",
        "205.251.252.0/23",
        "54.192.0.0/16",
        "204.246.173.0/24",
        "54.230.200.0/21",
        "120.253.240.192/26",
        "116.129.226.128/26",
        "130.176.0.0/17",
        "108.156.0.0/14",
        "99.86.0.0/16",
        "205.251.200.0/21",
        "13.32.0.0/15",
        "120.253.245.128/26",
        "13.224.0.0/14",
        "70.132.0.0/18",
        "15.158.0.0/16",
        "111.13.171.192/26",
        "13.249.0.0/16",
        "18.238.0.0/15",
        "18.244.0.0/15",
        "205.251.208.0/20",
        "65.9.128.0/18",
        "130.176.128.0/18",
        "58.254.138.0/25",
        "54.230.208.0/20",
        "3.160.0.0/14",
        "116.129.226.0/25",
        "52.222.128.0/17",
        "18.164.0.0/15",
        "111.13.185.32/27",
        "64.252.128.0/18",
        "205.251.254.0/24",
        "54.230.224.0/19",
        "71.152.0.0/17",
        "216.137.32.0/19",
        "204.246.172.0/24",
        "18.172.0.0/15",
        "120.52.39.128/27",
        "118.193.97.64/26",
        "18.154.0.0/15",
        "54.240.128.0/18",
        "205.251.250.0/23",
        "180.163.57.0/25",
        "52.46.0.0/18",
        "52.82.128.0/19",
        "54.230.0.0/17",
        "54.230.128.0/18",
        "54.239.128.0/18",
        "130.176.224.0/20",
        "36.103.232.128/26",
        "52.84.0.0/15",
        "143.204.0.0/16",
        "144.220.0.0/16",
        "120.52.153.192/26",
        "119.147.182.0/25",
        "120.232.236.0/25",
        "54.239.192.0/19",
        "18.64.0.0/14",
        "120.52.12.64/26",
        "99.84.0.0/16",
        "130.176.192.0/19",
        "52.124.128.0/17",
        "204.246.164.0/22",
        "13.35.0.0/16",
        "204.246.174.0/23",
        "36.103.232.0/25",
        "119.147.182.128/26",
        "118.193.97.128/25",
        "120.232.236.0/26",
        "204.246.176.0/20",
        "65.8.0.0/16",
        "65.9.0.0/17",
        "108.138.0.0/15",
        "120.253.241.160/27",
        "64.252.64.0/18",
        "13.113.196.64/26",
        "13.113.203.0/24",
        "52.199.127.192/26",
        "13.124.199.0/24",
        "3.35.130.128/25",
        "52.78.247.128/26",
        "13.233.177.192/26",
        "15.207.13.128/25",
        "15.207.213.128/25",
        "52.66.194.128/26",
        "13.228.69.0/24",
        "52.220.191.0/26",
        "13.210.67.128/26",
        "13.54.63.128/26",
        "43.218.56.128/26",
        "43.218.56.192/26",
        "43.218.56.64/26",
        "43.218.71.0/26",
        "99.79.169.0/24",
        "18.192.142.0/23",
        "35.158.136.0/24",
        "52.57.254.0/24",
        "13.48.32.0/24",
        "18.200.212.0/23",
        "52.212.248.0/26",
        "3.10.17.128/25",
        "3.11.53.0/24",
        "52.56.127.0/25",
        "15.188.184.0/24",
        "52.47.139.0/24",
        "3.29.40.128/26",
        "3.29.40.192/26",
        "3.29.40.64/26",
        "3.29.57.0/26",
        "18.229.220.192/26",
        "54.233.255.128/26",
        "3.231.2.0/25",
        "3.234.232.224/27",
        "3.236.169.192/26",
        "3.236.48.0/23",
        "34.195.252.0/24",
        "34.226.14.0/24",
        "13.59.250.0/26",
        "18.216.170.128/25",
        "3.128.93.0/24",
        "3.134.215.0/24",
        "52.15.127.128/26",
        "3.101.158.0/23",
        "52.52.191.128/26",
        "34.216.51.0/25",
        "34.223.12.224/27",
        "34.223.80.192/26",
        "35.162.63.192/26",
        "35.167.191.128/26",
        "44.227.178.0/24",
        "44.234.108.128/25",
        "44.234.90.252/30",
    )

    fastly_ranges_ipv4 = (
        '103.244.50.0/24',
        '103.245.222.0/23',
        '103.245.224.0/24',
        '104.156.80.0/20',
        '140.248.64.0/18',
        '140.248.128.0/17',
        '146.75.0.0/17',
        '151.101.0.0/16',
        '157.52.64.0/18',
        '167.82.0.0/17',
        '167.82.128.0/20',
        '167.82.160.0/20',
        '167.82.224.0/20',
        '172.111.64.0/18',
        '185.31.16.0/22',
        '199.27.72.0/21',
        '199.232.0.0/16',
    )

    akamaighost_ranges_ipv4 = (
        '2.16.0.0/13',
        '23.0.0.0/12',
        '23.192.0.0/11',
        '23.32.0.0/11',
        '23.64.0.0/14',
        '23.72.0.0/13',
        '88.221.0.0/16',
        '95.100.0.0/15',
        '96.6.0.0/15',
        '184.24.0.0/13',
        '184.84.0.0/14',
    )

    console.print("khtar chno biti T scanni:")
    console.print("[purple]1. Cloudflare[/purple]")
    console.print("[purple]2. Cloudfront[/purple]")
    console.print("[purple]3. Fastly[/purple]")
    console.print("[purple]4. Akamai[/purple]")


    choice = input("khtar ra9m libiti: ")

    if choice == "1":
        timeout = int(input("Enter the timeout in seconds (default is 3): ") or "3")
        return extract_hosts_from_ranges(cloudflare_ranges_ipv4), timeout, choice
    elif choice == "2":
        timeout = int(input("Enter the timeout in seconds (default is 3): ") or "3")
        return extract_hosts_from_ranges(cloudfront_ranges_ipv4), timeout, choice
    elif choice == "3":
        timeout = int(input("Enter the timeout in seconds (default is 3): ") or "3")
        return extract_hosts_from_ranges(fastly_ranges_ipv4), timeout, choice
    elif choice == "4":
        timeout = int(input("Enter the timeout in seconds (default is 3): ") or "3")
        return extract_hosts_from_ranges(akamaighost_ranges_ipv4), timeout, choice
    else:
        console.print("Invalid choice. Exiting.")
        exit()

def main():
    start_time = time.time()
    console = Console()
    print_ascii_art()
    console.print(emoji.emojize(':warning: Warning: Wach adrari hanyin  :warning:'))
    console.print(f"Telegram Channel: {telegram_channel}")
    console.print("=" * 66)
    selected_target_hosts, timeout, choice = select_target_hosts()
    console.print("=" * 66)
    for target_host in tqdm(selected_target_hosts, desc=f"{emoji.emojize(':rocket: Scanning Araliya dok hostat 7abak')}"):
        check_response_types(target_host, timeout)
        if choice == "6" and timeout is not None:
            ports_to_check = [21, 22, 23, 25, 53, 80, 110, 137, 138, 139, 143, 443, 445, 548, 587, 993, 995, 1433, 1701, 1723, 3306, 5432, 8008, 8443, 666, 2302, 3453, 3724, 4000, 5154, 6112, 6113, 6114, 6115, 6116, 6117, 6118, 6119, 7777, 10093, 10094, 12203, 14567, 25565, 26000, 27015, 27910, 28000, 50000, 515, 631, 3282, 3389, 5190, 5050, 4443, 1863, 6891, 1503, 5631, 5632, 5900, 6667, 119, 375, 425, 1214, 412, 1412, 2412, 4661, 4662, 4665, 5500, 6346, 6881, 6882, 6883, 6884, 6885, 6886, 6887, 6888, 6889]
            check_specific_ports(target_host, timeout, ports_to_check)
    console.print("=" * 40)
    total_time = time.time() - start_time
    console.print(f"{emoji.emojize(':alarm_clock: Total Time Elapsed')}: {INFO_COLOR}{precisedelta(total_time)}{RESET_COLOR}")

if __name__ == "__main__":
    main()