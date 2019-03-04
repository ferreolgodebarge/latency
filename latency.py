import os
import sys
import csv
import re

dir_path = os.path.dirname(os.path.realpath(__file__))
temp_file = os.path.join(dir_path, "raw")
fieldnames = ['ip_addr', 'sent', 'recieved',
              'lost', 'percentage', 'min', 'max', 'avg']
error_dict = {
    "ip_addr": "Unknown",
    "sent": "Unknown",
    "recieved": "Unknown",
    "lost": "Unknown",
    "percentage": "Unknown",
    "min": "Unknown",
    "max": "Unknown",
    "avg": "Unknown"
}


def ping_server(input_file: str, number: int) -> int:
    ipv4 = read_ip_addr(input_file)
    write_header_csv()
    if os.name == 'nt':
        print("System Windows")
        for server_ip in ipv4:
            response = os.system("ping -n " + str(number) +
                                 " " + server_ip + " > " + temp_file)
            if response != 0:
                stats = error_dict
                stats["ip_addr"] = server_ip
            else:
                stats = win_parse_ping("raw")
            os.remove(temp_file)
            write_row_csv(stats)
    elif os.name == 'posix':
        print("System Unix")
        for server_ip in ipv4:
            response = os.system("ping -c " + str(number) +
                                " " + server_ip + " > " + temp_file)
            if response != 0:
                stats = error_dict
                stats["ip_addr"] = server_ip
            else:
                stats = unx_parse_ping("raw")
            os.remove(temp_file)
            write_row_csv(stats)
    else:
        print("Unable to determine OS")
        response = 1
    return response


def win_parse_ping(raw_file: str) -> dict:
    stats = dict()
    with open(raw_file, 'r') as f:
        content = f.readlines()
        ip_address = re.findall(r"[0-9]+.[0-9]+.[0-9]+.[0-9]+", content[-4])
        overview_numbers = re.findall(r"[0-9]+", content[-3])
        stats_numbers = re.findall(r"[0-9]+", content[-1])
        stats["ip_addr"] = ip_address[0]
        stats["sent"] = overview_numbers[0]
        stats["recieved"] = overview_numbers[1]
        stats["lost"] = overview_numbers[2]
        stats["percentage"] = overview_numbers[3]
        stats["min"] = stats_numbers[0]
        stats["max"] = stats_numbers[1]
        stats["avg"] = stats_numbers[2]
    return stats


def unx_parse_ping(raw_file: str) -> dict:
    stats = dict()
    with open(raw_file, 'r') as f:
        content = f.readlines()
        ip_address = re.findall(r"[0-9]+.[0-9]+.[0-9]+.[0-9]+", content[-3])
        overview_numbers = re.findall(r"[0-9]+", content[-2])
        stats_numbers = re.findall(r"[0-9]+.[0-9]+", content[-1])
        stats["ip_addr"] = ip_address[0]
        stats["sent"] = overview_numbers[0]
        stats["recieved"] = overview_numbers[1]
        stats["lost"] = overview_numbers[2]
        stats["percentage"] = int(overview_numbers[2]) / int((overview_numbers[0]))
        stats["min"] = stats_numbers[0]
        stats["max"] = stats_numbers[2]
        stats["avg"] = stats_numbers[1]
    return stats


def write_header_csv() -> None:
    with open('ping_output.csv', 'w') as f:
        w = csv.DictWriter(f, fieldnames,  delimiter=';', lineterminator='\n')
        w.writeheader()


def write_row_csv(stats: dict) -> None:
    with open('ping_output.csv', 'a') as f:
        w = csv.DictWriter(f, fieldnames,  delimiter=';', lineterminator='\n')
        w.writerow(stats)


def read_ip_addr(input_file: str) -> list:
    ip_addr = list()
    with open(input_file, 'r') as f:
        line = f.readline()
        while line:
            ip_address = re.findall(r"[0-9]+.[0-9]+.[0-9]+.[0-9]+", line)
            if len(ip_address) == 1:
                ip_addr.append(ip_address[0])
                line = f.readline()
            else:
                print(
                    "Unauthorized ip address format: XXX.XXX.XXX.XXX expected, " + line + " recieved")
                break
    return ip_addr


if __name__ == '__main__':
    ping_server(sys.argv[1], sys.argv[2])
