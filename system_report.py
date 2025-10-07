import subprocess 
import os 

def run_command(command):
    try:
        result = subprocess.run(command, capture_output = True, text = True, shell = True)
        return result.stdout.strip()
    except Exception as e: 
        return f"Error executing command: {e}"

def get_ip():
    return run_command("hostname -I").split()[0]

def get_gateway():
    output = run_command("ip route show default")
    if output:
        try: 
            gateway = output.split()[2]
            return gateway 
        except IndexError:
            return "Not found" 
    return "Not found" 

def get_dns_servers():
    dns_list = []
    if os.path.exists("/etc/resolv.conf"):
        with open("/etc/resolv.conf","r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("nameserver"):
                    dns_list.append(line.split()[1])
    return dns_list


if __name__ ==  "__main__":

    #creating variables for all commands
    current_date = subprocess.check_output(["date"], text = True)
    hostname = subprocess.check_output(["hostname"], text = True)
    domain = subprocess.check_output(["domainname"], text = True)
    ip = get_ip()
    gateway = get_gateway()

    #code for operationg system 
    operating_system = subprocess.check_output(["cat", "/etc/redhat-release"], text = True).strip()
    version = operating_system.split()[3]
    
    kernel = subprocess.check_output(["uname", "-r"], text = True).strip()
    cpu_model = subprocess.check_output(["grep 'model name' /proc/cpuinfo | head -n 1 | cut -d ':' -f2"],shell = True, text=True).strip()
    processors = subprocess.check_output(["nproc"], text = True).strip()

    #logical cores 
    cores = logical_cores = subprocess.check_output(["nproc"], text = True).strip()


    # code for the drive space
    output = subprocess.check_output(["df", "-h", "/"], text = True).strip()
    lines = output.splitlines()
    disk_info = lines[1].split()
    total_space = disk_info[1]
    used_space = disk_info[2]
    free_space = disk_info[3]

    #code for total and available ram
    totalram = subprocess.check_output(["free", "-h"], text = True).strip()
    lines = output.splitlines()
    mem_line = lines[1].split()
    total_ram = mem_line[1]
    #available ram is not showing the correct number idk how to do it
    available_ram = mem_line[2]
    

    # code for the netmask
    network_mask = ""
    first_octet = int(ip.split(".")[0])
    if 1 <= first_octet <= 126:
     network_mask = "255.0.0.0"
    elif 128 <= first_octet <= 191:
        network_mask = "255.255.0.0"
    elif 192 <= first_octet <= 223:
        network_mask = "255.255.255.0"
    else:
        print("Multicast, Experimental, or Reserved")
    

    #the output
    print("System Report - ", current_date)

    print("Device Information")
    print("Hostname: ", hostname)
    print("Domain:", domain, "\n")

    print("Network Information")
    print("IP Address: " + ip)
    print("Gateway: " + gateway)
    print("Network Mask: " + network_mask)

    dns_servers = get_dns_servers()
    print("DNS1: " , dns_servers[0] if len(dns_servers) > 0 else "Not found")
    print("DNS2: ", dns_servers[1] if len(dns_servers) > 1 else "Not found")

    print("\n", "Operating System Information")
    print("Operating System: ", operating_system)
    print("OS Version: ", version)
    print("Kernal Version: ", kernel)
    
    print("\n", "Storage Information")
    print("System Drive Total: ", total_space)
    print("System Drive Used: ", used_space)
    print("System Drive Free: " , free_space)

    
    print("\n", "Processor Information")
    print("CPU Model: ", cpu_model)
    print("Number of processors: ", processors)
    print("Number of cores: ", cores)


    print("\n", "Memory Information")
    print("Total RAM: ", total_ram, "GB")
    print("Available RAM: ", available_ram, "GB")
    

