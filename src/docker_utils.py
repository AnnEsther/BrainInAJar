import subprocess  # Import subprocess module for running system commands
import platform  # Import platform module to determine the operating system

import docker  # Import docker module to interact with Docker via its Python SDK

# Function to start the Docker engine depending on the operating system
def start_docker_engine():
    system = platform.system()  # Get the name of the operating system

    try:
        if system == 'Linux':
            # Command to start Docker on Linux using systemctl
            subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
            print("Docker engine started on Linux.")
        
        elif system == 'Windows':
            # Command to start Docker on Windows
            # The command requires Administrator privileges
            subprocess.run(['runas', '/user:Administrator', 'net', 'start', 'com.docker.service'], check=True)
            print("Docker engine started on Windows.")
        
        elif system == 'Darwin':  # macOS
            # On macOS, Docker Desktop must be started manually by the user
            print("Please start Docker Desktop manually on macOS.")
        
        else:
            # Handle unsupported operating systems
            print(f"Unsupported operating system: {system}")
    
    except subprocess.CalledProcessError as e:
        # Handle errors that occur when attempting to start Docker
        print(f"Failed to start Docker engine: {e}")

# Function to stop the Docker engine depending on the operating system
def stop_docker_engine():
    system = platform.system()  # Get the name of the operating system

    try:
        if system == 'Linux':
            # Command to stop Docker on Linux using systemctl
            subprocess.run(['sudo', 'systemctl', 'stop', 'docker'], check=True)
            print("Docker engine stopped on Linux.")
        
        elif system == 'Windows':
            # Command to stop Docker on Windows
            subprocess.run(['net', 'stop', 'com.docker.service'], check=True)
            print("Docker engine stopped on Windows.")
        
        elif system == 'Darwin':  # macOS
            # On macOS, Docker Desktop must be stopped manually by the user
            print("Please stop Docker Desktop manually on macOS.")
        
        else:
            # Handle unsupported operating systems
            print(f"Unsupported operating system: {system}")
    
    except subprocess.CalledProcessError as e:
        # Handle errors that occur when attempting to stop Docker
        print(f"Failed to stop Docker engine: {e}")

# Function to stop a specific Docker container
def stop_docker_container(container):
    try:
        # Use the Docker SDK to stop the container
        container.stop()
        print(f"Container {container.id} stopped successfully.")
        
    except docker.errors.APIError as e:
        # Handle errors that occur when stopping the container
        print(f"Error stopping container: {e}")

# Function to remove a specific Docker container
def remove_docker_container(container):
    try:
        # Use the Docker SDK to remove the container
        container.remove()
        print(f"Container {container.id} removed successfully.")
        
    except docker.errors.APIError as e:
        # Handle errors that occur when removing the container
        print(f"Error removing container: {e}")
