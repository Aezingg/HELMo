import csv
import subprocess
import time


# Constante! :D
COMMUNITY = "SuperSecsy"
IP = "localhost"
OID_CPU = {"cpu_users": 9, "cpu_system": 10, "cpu_idle": 11}
OID_RAM = {"used_ram": 6, "free_ram": 11, "shared_ram": 13, "buffered_ram": 14, "cached_memory": 15}
OID_INTERFACE = {"lo_in": "10.1", "wifi_in": "10.2", "lo_out": "16.1", "wifi_out": "16.2"}

header = False


def to_csv(data):
    global header
    with open("stats.csv", 'a', newline='') as file:
        col = ['cpu_users', 'cpu_system', "cpu_idle", "used_ram", "free_ram", "shared_ram", "buffered_ram", "cached_memory", "lo_in", "wifi_in", "lo_out", "wifi_out"]
        writer = csv.DictWriter(file, col)
        if not header:
            writer.writeheader()
            header = True
        else:
            writer.writerow(data)


def info_interface(oid_interface_dict):
    metrics = {}

    for k, v in oid_interface_dict.items():
        oid = f"1.3.6.1.2.1.2.2.1.{v}"
        print(oid)
        cmd = f"snmpget -v2c -c {COMMUNITY} {IP} {oid} -O v"
        result = subprocess.check_output(cmd, shell=True).decode()[:-1]
        metrics[k] = int(result.split(":")[1])

    return metrics


def info_cpu(oid_cpu_dict):
    metrics = {"cpu_users": 0, "cpu_system": 0, "cpu_idle": 0}

    for k, v in oid_cpu_dict.items():
        oid = f"1.3.6.1.4.1.2021.11.{v}.0"
        print(oid)
        cmd = f"snmpget -v2c -c {COMMUNITY} {IP} {oid} -O v"
        result = subprocess.check_output(cmd, shell=True).decode()[:-1]
        metrics[k] = int(result.split(":")[1])

    return metrics


def info_ram(oid_ram_dict):
    metrics = {}

    for k, v in oid_ram_dict.items():
        oid = f"1.3.6.1.4.1.2021.4.{v}.0"
        print(oid)
        cmd = f"snmpget -v2c -c {COMMUNITY} {IP} {oid} -O v"
        result = subprocess.check_output(cmd, shell=True).decode()[:-1]
        metrics[k] = int(result.split(":")[1][:-2])

    return metrics


def _main():
    start = time.time()
    print("hello")
    for i in range(0, 240):
        data_cpu = info_cpu(OID_CPU)
        data_ram = info_ram(OID_RAM)
        data_if = info_interface(OID_INTERFACE)
        tout_ensemble_data = data_cpu | data_ram | data_if
        to_csv(tout_ensemble_data)
        time.sleep(0.83)
        i += 1
        print(i) # Mon tel
    end = time.time()
    print(end - start)


if __name__ == '__main__':
    _main()



