import time
import docker
from docker.types import DeviceRequest

import GLOBALS

def start_tts_container():
    client = docker.from_env()
    container_name = 'TTS'  # Assign a name to your container

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
        container = client.containers.run(**GLOBALS.TTS_DOCKER_CONFIG, detach=True)

    # Execute the command inside the running container
    exec_command = 'python3 TTS/server/server.py --model_name tts_models/en/vctk/vits --use_cuda true'
    exit_code, output = container.exec_run(exec_command, detach=True)
    time.sleep(30)
    # Print the output of the command
    print(f"Container {container_name} is running")

    return container
# start_tts_container()