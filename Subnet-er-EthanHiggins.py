import ipaddress
from ipaddress import IPv4Address

def network_id(ipadd):
    network = ipaddress.ip_network(ipadd, strict=False)
    network_id = network.network_address
    return network_id
    
def ipSplit(string): #ended up not using
    parts = string.split(".")
    part1, part2, part3, part4 = parts
    return part1, part2, part3, part4

def subnetr(ip, netid, cidr, num_subnets):
    network = ipaddress.ip_network(str(netid) + '/' + cidr, strict=False)
    subnet_mask = int(cidr)
    new_prefix = subnet_mask
    while len(list(network.subnets(new_prefix=new_prefix))) < num_subnets:
        new_prefix += 1
    new_subnets = list(network.subnets(new_prefix=new_prefix))[:num_subnets]
    return new_subnets, new_prefix


def validate_ip(ip):
    parts = ip.split('.')
    if len(parts) != 4:
        return False
    for part in parts:
        if not part.isdigit() or not 0 <= int(part) <= 255:
            print("Works")
            return False
    return True

def get_usable_range(subnet):
    first_usable = IPv4Address(subnet.network_address + 1)
    last_usable = IPv4Address(subnet.broadcast_address - 1)
    broadcast_address = subnet.broadcast_address
    return first_usable, last_usable, broadcast_address

def get_usable_add(CIDR):
    var = (32-CIDR)
    var2 = (2**var)-2
    var3 = ''
    if var2 > 50000:
        var = str(var)
        var3='2^'+var+'-2'
        return var3
    return var2

subnet = input("Please enter the subnet as xxx.xxx.xxx.xxx: ")
mask = input("Please enter the subnet mask: /")
nets = int(input("How many subnets would you like to create?: "))
print(' ')

if validate_ip(subnet):
    netID = network_id(subnet+'/'+mask)
    part1, part2, part3, part4 = ipSplit(subnet)
    new_subnets, prefix = subnetr(subnet, netID, mask, nets)
    CIDR = get_usable_add(prefix)

    
    print("Subnet              | Range                | # of usable add. | Broadcast Address")
    print("-" * 81)
    for new_subnet in new_subnets:
        first_usable, last_usable, broadcast_address = get_usable_range(new_subnet)
        subnet2 = str(new_subnet).ljust(20)
        range2 = f"{first_usable} - {last_usable}".ljust(36)
        add_count = int(last_usable) - int(first_usable) + 1
        broadcast_str = str(broadcast_address)
        print(f"{subnet2}| {range2}| {CIDR}| {broadcast_str}")
else:
    print("Not a valid IP address. Please start the program again, and enter a valid IP")
