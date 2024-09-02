import yaml
from jinja2 import Environment, FileSystemLoader

# Load YAML config
with open('vm_config.yaml', 'r') as yaml_file:
    vm_config = yaml.safe_load(yaml_file)

# Define a function to check for mandatory fields
def check_mandatory_fields(config, mandatory_fields):
    missing_fields = []
    for field in mandatory_fields:
        keys = field.split('.')
        sub_config = config
        for key in keys:
            if key in sub_config:
                sub_config = sub_config[key]
            else:
                missing_fields.append(field)
                break
    return missing_fields

# List of mandatory fields (using dot notation for nested fields)
mandatory_fields = [
    'vm.name',
    'vm.description',
    'vm.proxmox_host',
    'vm.template_name',
    'vm.os_type',
    'vm.machine.cpu.model',
    'vm.machine.cpu.cores',
    'vm.machine.cpu.sockets',
    'vm.machine.memory',
    'vm.machine.networks',
    'vm.disks',
    'vm.scsihw',
    'vm.bootdisk',
    'vm.config.agent',
    'vm.config.cicustom_path',
    'vm.config.ssh_key.public_key_path',
]

def extract_ip_and_cidr(ip_with_cidr):
    ip, cidr = ip_with_cidr.split('/')
    return {'ip': ip, 'cidr': cidr}

# Check for missing mandatory fields
missing_fields = check_mandatory_fields(vm_config, mandatory_fields)

if missing_fields:
    print(f"Error: The following mandatory fields are missing: {', '.join(missing_fields)}")
    exit(1)

# Setup Jinja2 environment
env = Environment(loader=FileSystemLoader('.'))
# Register the custom filter
env.filters['extract_ip_and_cidr'] = extract_ip_and_cidr
template = env.get_template('templates/vm_template.j2')

# Render template with YAML data
terraform_output = template.render(vm=vm_config['vm'])

# Save the rendered Terraform to a file
with open('output.tf', 'w') as output_file:
    output_file.write(terraform_output)

print("Terraform configuration generated in 'output.tf'")
