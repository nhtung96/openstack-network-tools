import openstack
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    filename="filename.log",  
    filemode="a",  
    format="%(asctime)s - %(levelname)s - %(message)s" 
)

LOG = logging.getLogger(__name__)

client = openstack.connect(
    auth_url="auth_url",
    project_name="project_name",
    username="project_name",
    password="password",
    region_name="region_name",
    user_domain_name="user_domain_name",
    project_domain_name="project_domain_name"
)


output_file = "available_ips.json"
txt_output_file = "available_ips.txt"

networks = {
    "network-name": "network-subnet",
    "abc": "192.168.1",
}

available_ips = []

for network_name, network_prefix in networks.items():
    LOG.info(f"Checking available IPs for {network_name} ({network_prefix}.0/24)...")

    network = client.network.find_network(network_name)
    if not network:
        LOG.info(f"Network {network_name} not found!")
        continue

    allocated_ips = []
    ports = client.network.ports(network_id=network.id)
    for port in ports:
        fixed_ips = port.fixed_ips
        for fixed_ip in fixed_ips:
            allocated_ips.append(fixed_ip["ip_address"])

    for i in range(1, 255):
        ip = f"{network_prefix}.{i}"
        if ip not in allocated_ips:
            print(ip)
            available_ips.append(ip)

with open(output_file, "w") as f:
    json.dump({"available_ips": available_ips}, f)

with open(txt_output_file, "w") as txt_file:
    txt_file.write("\n".join(available_ips))


LOG.info(f"Available IPs have been saved to {output_file} and {txt_output_file}.")
