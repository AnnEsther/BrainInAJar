import time  # Import the time module for handling delays
import docker  # Import the docker module to interact with Docker via Python
from docker.types import DeviceRequest  # Import DeviceRequest from docker.types for handling device requests

import GLOBALS  # Import custom module GLOBALS, which contains global variables and settings
import utils  # Import custom utility functions from the utils module

# Function to start the Ollama container using Docker
def start_ollama_container():
    # Create a Docker client to interact with the Docker service on the local machine
    client = docker.from_env()
    container_name = 'ollama'  # Name of the container to manage

    # Check if the container already exists
    containers = client.containers.list(all=True, filters={'name': container_name})
    container = None  # Initialize a variable to hold the container object

    if containers:  # If a container with the specified name already exists
        container = containers[0]  # Get the first container that matches the name
        if container.status != 'running':  # If the container is not running
            container.start()  # Start the container
    else:
        # If the container does not exist, create and run a new one using the configuration from GLOBALS
        container = client.containers.run(**GLOBALS.LLM_DOCKER_CONFIG, detach=True)

    # Prepare the command to run inside the container
    exec_command = 'ollama run ' + GLOBALS.LLM_MODEL  # The command to start the specified model in Ollama

    # Execute the command inside the running container
    exit_code, output = container.exec_run(exec_command, detach=True)
    
    time.sleep(30)  # Wait for 30 seconds to ensure the model is fully loaded and running

    # Print a message indicating that the container is running
    print(f"Container {container_name} is running")

    return container  # Return the container object

# Function to start Ollama directly on macOS (outside of Docker)
def start_ollama():
    # Pull the specified LLM model using a utility function
    utils.run_command_mac("ollama pull " + GLOBALS.LLM_MODEL)
    # Run the specified LLM model using a utility function
    utils.run_command_mac("ollama run " + GLOBALS.LLM_MODEL)

# Uncomment the following line to start the Ollama container when the script runs
# start_ollama_container()
