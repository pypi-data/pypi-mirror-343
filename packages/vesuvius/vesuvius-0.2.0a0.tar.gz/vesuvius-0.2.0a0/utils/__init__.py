# Import utility functions to expose at the module level
import os
import yaml
import requests
from setup.accept_terms import get_installation_path

def list_files():
    """
    Load and return the scrolls configuration data from a YAML file.
    This function reads the scrolls.yaml file and returns its contents as a dictionary.
    """
    install_path = get_installation_path()
    scroll_config = os.path.join(install_path, 'setup', 'configs', f'scrolls.yaml')
    with open(scroll_config, 'r') as file:
        data = yaml.safe_load(file)
    return data

def list_cubes():
    """
    Load and return the cubes configuration data from a YAML file.
    This function reads the cubes.yaml file and returns its contents as a dictionary.
    """
    install_path = get_installation_path()
    cubes_config = os.path.join(install_path, 'setup', 'configs', f'cubes.yaml')
    with open(cubes_config, 'r') as file:
        data = yaml.safe_load(file)
    return data

def is_aws_ec2_instance():
    """
    Determine if the current system is an AWS EC2 instance.
    Returns: bool - True if running on AWS EC2, False otherwise.
    """
    try:
        # Query EC2 instance metadata to check if running on AWS EC2
        response = requests.get("http://169.254.169.254/latest/meta-data/", timeout=2)
        if response.status_code == 200:
            return True
    except requests.RequestException:
        return False
    return False

# Define what to expose
__all__ = ['list_files', 'list_cubes', 'is_aws_ec2_instance']