import subprocess
import platform

import docker

def start_docker_engine():
    system = platform.system()

    try:
        if system == 'Linux':
            # Command to start Docker on Linux
            subprocess.run(['sudo', 'systemctl', 'start', 'docker'], check=True)
            print("Docker engine started on Linux.")
        
        elif system == 'Windows':
            # Command to start Docker on Windows
            # subprocess.run(['net', 'start', 'com.docker.service'], check=True)
            subprocess.run(['runas', '/user:Administrator', 'net', 'start', 'com.docker.service'], check=True)
            print("Docker engine started on Windows.")
        
        elif system == 'Darwin':  # macOS
            # On macOS, Docker Desktop should be started manually
            print("Please start Docker Desktop manually on macOS.")
        
        else:
            print(f"Unsupported operating system: {system}")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to start Docker engine: {e}")

def stop_docker_engine():
    system = platform.system()

    try:
        if system == 'Linux':
            # Command to stop Docker on Linux
            subprocess.run(['sudo', 'systemctl', 'stop', 'docker'], check=True)
            print("Docker engine stopped on Linux.")
        
        elif system == 'Windows':
            # Command to stop Docker on Windows
            subprocess.run(['net', 'stop', 'com.docker.service'], check=True)
            print("Docker engine stopped on Windows.")
        
        elif system == 'Darwin':  # macOS
            # On macOS, Docker Desktop should be stopped manually
            print("Please stop Docker Desktop manually on macOS.")
        
        else:
            print(f"Unsupported operating system: {system}")
    
    except subprocess.CalledProcessError as e:
        print(f"Failed to stop Docker engine: {e}")


def stop_docker_container(container):
    try:
        # Stop the container
        container.stop()
        print(f"Container {container.id} stopped successfully.")
        
    except docker.errors.APIError as e:
        print(f"Error stopping container: {e}")

def remove_docker_container(container):
    try:
        # Remove the container
        container.remove()
        print(f"Container {container.id} removed successfully.")
    except docker.errors.APIError as e:
        print(f"Error removing container: {e}")