import os
import subprocess
import json
import shutil
from infradrone.utils import load_config, generate_ssh_keys, BASE_DIR

def deploy_instance(provider, os_name, template, instance_name, allowed_ports):
    config = load_config()
    working_dir = 'working_dir'

    instance_dir = os.path.abspath(os.path.join(working_dir, instance_name))
    os.makedirs(instance_dir, exist_ok=True)

    # Generate RSA ssh keys for non-GCP providers
    if provider != 'gcp':
        ssh_key_name = instance_name
        ssh_key_path = generate_ssh_keys(instance_dir, ssh_key_name, config['DEFAULT_SSH_PASSWORD'])

    # Initialize terraform
    terraform_dir = os.path.join(instance_dir, 'terraform')
    os.makedirs(terraform_dir, exist_ok=True)

    # Copy main.tf and variables.tf
    template_dir = os.path.join('tf', provider, os_name, template)
    shutil.copy(os.path.join(template_dir, 'main.tf'), terraform_dir)
    shutil.copy(os.path.join(template_dir, 'variables.tf'), terraform_dir)

    # Clear the screen
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    subprocess.run(['terraform', 'init', '-input=false'], cwd=terraform_dir)

    if provider == 'yc':
        # Run terraform
        terraform_vars = {
            'INFRADRONE_ssh_keys_dir': instance_dir,
            'INFRADRONE_ssh_key_name': ssh_key_name,
            'INFRADRONE_ssh_user': config['DEFAULT_SSH_USER'],
            'INFRADRONE_vm_instance_name': instance_name,
            'INFRADRONE_allowed_ports': allowed_ports,
            'INFRADRONE_provider_token': config['PROVIDERS']['yc']['YC_TOKEN'],
            'INFRADRONE_provider_cloud_id': config['PROVIDERS']['yc']['YC_CLOUD_ID'],
            'INFRADRONE_provider_folder_id': config['PROVIDERS']['yc']['YC_FOLDER_ID'],
            'INFRADRONE_cloud_prefix': config['PROVIDERS']['yc']['YC_CLOUD_PREFIX'],
            'INFRADRONE_zone':  config['PROVIDERS']['yc']['YC_ZONE']
        }
    elif provider == 'gcp':
        terraform_vars = {
            'INFRADRONE_credentials_file': config['PROVIDERS']['gcp']['GCP_CREDENTIALS_FILE'],
            'INFRADRONE_project_id': config['PROVIDERS']['gcp']['GCP_PROJECT_ID'],
            'INFRADRONE_zone': config['PROVIDERS']['gcp']['GCP_ZONE'],
            'INFRADRONE_vm_zone': config['PROVIDERS']['gcp']['GCP_VM_ZONE'],
            'INFRADRONE_network': config['PROVIDERS']['gcp']['GCP_NETWORK'],
            'INFRADRONE_subnet': config['PROVIDERS']['gcp']['GCP_SUBNET'],
            'INFRADRONE_vm_instance_name': instance_name,
            'INFRADRONE_allowed_ports': allowed_ports
        }

    # Clear the screen
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

    terraform_vars_list = [f'-var={key}={value}' for key, value in terraform_vars.items()]
    terraform_log_path = os.path.join(instance_dir, 'terraform.log')
    with open(terraform_log_path, 'w') as log_file:
        result = subprocess.run(['terraform', 'apply', '-auto-approve'] + terraform_vars_list, cwd=terraform_dir, stdout=log_file, stderr=log_file)

    if result.returncode != 0:
        return False, f"Terraform apply failed. Check the logs for details: {terraform_log_path}"

    # Get terraform output
    result = subprocess.run(['terraform', 'output', '-json'], cwd=terraform_dir, capture_output=True, text=True)
    output = json.loads(result.stdout)
    instance_ip = output['instance_ip']['value']

    # Add to ssh.json
    ssh_config_path = os.path.join(BASE_DIR, 'ssh.json')
    if os.path.exists(ssh_config_path):
        with open(ssh_config_path, 'r') as f:
            ssh_config = json.load(f)
    else:
        ssh_config = {'connections': {}}

    if provider == 'yc':
        with open(f'{ssh_key_path}.pub', 'r') as f:
            public_key = f.read()

        with open(ssh_key_path, 'r') as f:
            private_key = f.read()

        ssh_config['connections'][instance_name] = {
            'name': instance_name,
            'user': config['DEFAULT_SSH_USER'],
            'pass': config['DEFAULT_SSH_PASSWORD'],
            'ip': instance_ip,
            'public_key': public_key,
            'private_key': private_key,
            'provider': 'yc'
        }
    elif provider == 'gcp':
        ssh_config['connections'][instance_name] = {
            'name': instance_name,
            'ip': instance_ip,
            'provider': 'gcp'
        }

    with open(ssh_config_path, 'w') as f:
        json.dump(ssh_config, f, indent=4)

    return True, instance_ip