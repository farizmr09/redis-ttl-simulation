
# Project Setup Instructions 
This document outlines the steps necessary to set up and run the project. 

## Step 1: Start Docker Containers 
Open a shell or command prompt in the folder where you extracted the files. To start the Docker containers, execute the following command: 
```bash
docker-compose up -d
```
## Step 2: Run Listener Service 
In another terminal window  or tab, navigate to the project folder and  start the listener service by  running:
```bash
python listener_service.py
```

## Step 4: Run Device Simulation
Finally, open a new terminal window or tab. In the project folder, execute the device simulation script with:
```bash
python device_simulation.py
```

Follow these steps in the specified order for a successful setup of the project.