import time  # Import time module for sleep functionality
import docker  # Import docker module for Docker container management
from docker.types import DeviceRequest  # Import DeviceRequest for device management

import GLOBALS  # Import global settings

def start_tts_container():
    """
    Start a Docker container for Text-to-Speech (TTS) processing.
    
    - Checks if a container with the name 'TTS' exists and is running.
    - Starts the container if it is not running.
    - Creates and runs the container if it does not exist.
    - Executes a TTS server command inside the container.
    - Waits for the server to initialize and prints a status message.
    
    Returns:
    - The Docker container instance.
    """
    client = docker.from_env()  # Create a Docker client connected to the Docker daemon
    container_name = 'TTS'  # Name assigned to the container

    # Check if the container with the specified name already exists
    containers = client.containers.list(all=True, filters={'name': container_name})
    container = None

    if containers:
        # Container exists; use the existing container
        container = containers[0]
        if container.status != 'running':
            # Start the container if it is not already running
            container.start()
        # Uncomment if you want to return the container immediately
        # return container
    else:
        # Container does not exist; create and run a new container
        container = client.containers.run(**GLOBALS.TTS_DOCKER_CONFIG, detach=True)

    # Define the command to run inside the container
    exec_command = 'python3 TTS/server/server.py --model_name tts_models/en/vctk/vits --use_cuda true'
    # Execute the command inside the running container
    exit_code, output = container.exec_run(exec_command, detach=True)

    # Wait for 30 seconds to allow the server to initialize
    time.sleep(30)

    # Print a message indicating that the container is running
    print(f"Container {container_name} is running")

    return container  # Return the Docker container instance

# Uncomment the following line to start the TTS container when the script is run
# start_tts_container()
