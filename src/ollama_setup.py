import time
import docker
from docker.types import DeviceRequest

import GLOBALS
import utils

def start_ollama_container():
    client = docker.from_env()
    container_name = 'ollama'
    # Check if the container already exists
    containers = client.containers.list(all=True, filters={'name': container_name})
    container = None

    if containers:
        # Container exists; use the existing container
        container = containers[0]
        if container.status != 'running':
            # Start the container if it's not already running
            container.start()
        else:
            return container
    else:
        # Run the container
        container = client.containers.run(**GLOBALS.LLM_DOCKER_CONFIG, detach=True)

    # Execute the command inside the running container
    exec_command = 'ollama run ' + GLOBALS.LLM_MODEL
    # exec_command = 'ollama run gemma'
    
    exit_code, output = container.exec_run(exec_command, detach=True)
    time.sleep(30)

    # Print the output of the command
    print(f"Container {container_name} is running")

    return container


def start_ollama_container_mac():
    utils.run_command_mac("ollama pull mistral")
    utils.run_command_mac("ollama run mistral")

# start_ollama_container()