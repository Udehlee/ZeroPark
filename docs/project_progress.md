# ZeroPark Project Progress Log

## Project Overview

ZeroPark is an AI-powered autonomous parking system that teaches a car to park itself without human intervention. Think of it as a smart personal valet for your car.

## Phase 1: Setup and installation

### Project Setup

- Python Environment – Managed with Poetry to keep dependencies tidy.

- Conda Environment – Optional, conda activate ai makes life easier.

- Dependency Management – pyproject.toml and poetry.lock keep track of packages and versions.

### Libraries Installed

- numpy, torch, torchvision

- matplotlib

- opencv-contrib-python

- airsim, msgpack-rpc-python

### Simulator Setup

AirSim Installation

- Downloaded precompiled AirSimNH (small urban neighborhood) – light enough to run on my system.

-  Extracted and checked folder structure:
```sh
AirSimNH/
  ├── WindowsNoEditor/
  │   └── AirSimNH.exe
  └── settings.json
```
- Tested connection using Python:
```sh
import airsim

client = airsim.CarClient()
client.confirmConnection()
print("Connected to AirSim!")
```

- Success The Python client talks to the simulator without opening the visuals

## Phase 2: Basic Vehicle Control & Sensors (IN PROGRESS 🚧)

This phase is about actually moving a car in the simulator and seeing what it sees.

### Vehicle Control (Python API)

- Connected to AirSim car environment using Python API.

- Enable API control

- Arm the vehicle

- Send basic driving commands (throttle, steering, brake)

Successfully moved the car forward and turned it using code.
 Vehicle responds correctly to Python commands.

### Sensor Setup & Data Access

- Attached and accessed basic sensors such as 

Front RGB camera

Depth / distance information

- Learned how AirSim returns sensor data:

Images as arrays (or files like .png, .pfm)

Depth values as floating-point maps

Verified camera output by saving images to disk and inspecting them.

### Observed generated files:

- .png,  normal RGB image

- .pfm,  depth image (floating-point depth values)

