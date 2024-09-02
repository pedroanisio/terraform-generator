# Terraform Homelab Configuration

This repository contains the Terraform configurations and scripts used to manage a Proxmox-based homelab environment. The configuration automates the provisioning and management of virtual machines (VMs) within the Proxmox environment using Terraform, allowing for scalable and reproducible infrastructure management.

## Project Structure

- `install.md`: Instructions for installing Terraform on your system.
- `README.md`: This documentation file.
- `build/`: Directory containing scripts and templates to generate Terraform files based on YAML configurations.
  - `generate_tf.py`: Python script that generates Terraform configuration files from YAML files using Jinja2 templates.
  - `vm_config.yaml`: Example configuration file for a VM that will run a VS Code server.
  - `templates/`: Contains Jinja2 templates for generating Terraform configurations.
    - `vm_template.j2`: Jinja2 template used to render the VM configuration into a Terraform file.
- `lab.internal/`: Directory containing configurations specific to the internal lab environment.
  - `vm_config.yaml`: YAML configuration for a VS Code server VM.
  - `vm_config_fileserver.yaml`: YAML configuration for a file server VM used in the lab.
  - `output_codeserver.tf`: Terraform configuration for the VS Code server VM.
  - `base/`: Base Terraform files for managing the lab environment.
    - `output.tf`: Generated Terraform configuration for the VS Code server VM.
    - `providers.tf`: Terraform provider configurations, including the Proxmox provider.
    - `.terraform.lock.hcl`: Terraform lock file to ensure consistent provider versions.
    - `_proxmox_auth.tf`: Contains authentication variables for connecting to the Proxmox API.
    - `.terraform/`: Directory containing Terraform provider binaries and related files.

## How It Works

1. **Configuration**: Define the VM specifications in YAML files located in the `build/` and `lab.internal/` directories. These configurations describe the VM name, description, Proxmox host, OS type, hardware specifications, network settings, and disk configurations.

2. **Template Generation**: The `generate_tf.py` script reads the YAML configuration and uses Jinja2 templates to generate a Terraform configuration file (`output.tf`). The script ensures that all mandatory fields are present and correctly formatted.

3. **Terraform Execution**: The generated Terraform files are used to provision and manage VMs in the Proxmox environment. The base configuration files (`providers.tf`, `_proxmox_auth.tf`) ensure that Terraform can authenticate and interact with the Proxmox API.

4. **Lab Configuration**: The `lab.internal/` directory contains additional configuration files and outputs specific to the internal lab setup. These files define and manage the infrastructure needed for different services, such as the VS Code server and the file server.

## Usage

### Prerequisites

- Install Terraform by following the instructions in `install.md`.
- Ensure you have access to a Proxmox environment and valid API credentials.

### Steps to Generate and Apply Terraform Configuration

1. Update the YAML configuration files (`vm_config.yaml` and `vm_config_fileserver.yaml`) with your desired settings.

2. Run the `generate_tf.py` script to generate the Terraform configuration:
   ```bash
   python3 build/generate_tf.py
   ```
   The generated Terraform file (`output.tf`) will be saved in the `build/` directory.

3. Copy the generated Terraform file to the `lab.internal/` directory:
   ```bash
   cp build/output.tf lab.internal/
   ```

4. Navigate to the `lab.internal/base` directory and initialize Terraform:
   ```bash
   terraform init
   ```

5. Apply the Terraform configuration to provision the VM:
   ```bash
   terraform apply
   ```

## Notes

- The Terraform provider for Proxmox has known limitations, as described in the `README.md` file of the provider. Be aware of these when managing your infrastructure.
- Ensure that any sensitive information, such as API tokens, is securely managed and not exposed in version control.

## License

This project is licensed under the MIT License. See the `LICENSE` file in the `.terraform/providers/registry.terraform.io/telmate/proxmox/3.0.1-rc3/linux_amd64/` directory for more details.

