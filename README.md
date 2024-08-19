# BrainInAJar

This project implements a multi-threaded architecture for real-time communication with a Large Language Model (LLM). The system processes prompts, interacts with a Text-to-Speech (TTS) model, and streams audio responses in real-time. The key features include:

- **Real-Time Interaction:** The system sends prompts to the LLM and receives responses without waiting for the entire response.
- **Audio Streaming:** Each sentence from the LLM response is processed individually by a separate thread and converted into audio by the TTS model, which is then streamed.
- **Dynamic Prompt Management:** A user interface allows prompts to be added and sent randomly every minute or at customized intervals.


## System Requirements

- **Hardware:**
  - NVIDIA GPU with CUDA support

- **Software:**
  - CUDA Library:
    - cuBLAS for CUDA 12
    - cuDNN 8 for CUDA 12
  - Docker
  - Ollama (for non-Windows machines)

## Setup Instructions

### 1. Ensure Hardware Compatibility

Make sure your system has an NVIDIA GPU that supports CUDA.

### 2. Install CUDA Libraries

1. **Install CUDA 12:**
   - Download and install CUDA 12 from the [NVIDIA website](https://developer.nvidia.com/cuda-downloads).

2. **Install cuBLAS:**
   - cuBLAS is included with the CUDA Toolkit installation. Verify the installation by checking the `cublas` directory in the CUDA installation path.

3. **Install cuDNN 8:**
   - Download cuDNN 8 from the [NVIDIA website](https://developer.nvidia.com/cudnn). Follow the installation instructions to integrate cuDNN with CUDA 12.

### 3. Set Up Docker

1. **Install Docker:**
   - Follow the [Docker installation guide](https://docs.docker.com/get-docker/) for your operating system.

2. **Verify Docker Engine:**
   - Ensure that Docker Engine is running before executing the program.

### 4. Install Ollama (For Non-Windows Machines)

1. **Download Ollama:**
   - Visit the [Ollama website](https://ollama.com/) to download and install the Ollama package.

### 5. Running the Program

1. **Prepare Docker:**
   - Make sure Docker Engine is active.

2. **Execute the Program:**
   - Run the `main.py` script to start the program.

3. **Build Information:**
   - Use the `.exe` file to obtain the current build details if required.

## Getting Started

### Prerequisites

- Python 3.8+
- Pip

### Installation

```bash
git clone https://github.com/yourusername/braininajar.git
cd braininajar
git checkoot develop
git pull
pip install -r requirements.txt