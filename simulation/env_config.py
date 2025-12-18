import airsim
import time
import numpy as np
import os
from env_randomizer import Env_Randomizer

os.makedirs("data", exist_ok=True)

ENV_CONFIG = {
    "max_obstacles": 3,
    "sim_area_bounds": ([-30, -30, 0], [30, 30, 0]),
}

EPISODES = 5
STEPS_PER_EPISODE = 50
STEP_TIME = 0.2

# connect to AirSim
client = airsim.CarClient()
client.confirmConnection()
client.enableApiControl(True)

car_controls = airsim.CarControls()
env = Env_Randomizer(client, ENV_CONFIG)

print(" Connected to AirSim")
for episode in range(EPISODES):
    print(f" EPISODE {episode + 1}")
  
    client.reset()
    client.enableApiControl(True)
    time.sleep(1)

    env.random_lighting()
    parking_slot = env.random_parking_slot()
    obstacles = env.random_obstacles()

    print(f"Parking Slot Pose: {parking_slot['pose']}")
    collided = False

    for step in range(STEPS_PER_EPISODE):

         # set the controls for car
        car_controls.throttle = 0.6
        car_controls.steering = np.sin(step * 0.1)
        client.setCarControls(car_controls)

        # get state of the car
        state = client.getCarState()

        collision = client.simGetCollisionInfo() 

        print(f"[Episode {episode+1} - Step {step}] " f"Speed={state.speed:.2f} - "f"Collision={collision.has_collided}")
        if collision.has_collided:
            print(" Collision detected: ending episode")
            collided = True
            break

       # get camera images from the car
        responses = client.simGetImages([airsim.ImageRequest(0, airsim.ImageType.Scene)])
        if responses and responses[0].image_data_uint8:
            filename = f"data/ep{episode}_step{step}.png"
            airsim.write_file(filename, responses[0].image_data_uint8)

        time.sleep(STEP_TIME)

    print(f"Episode {episode + 1} finished - "f"Collision: {collided}")

client.enableApiControl(False)

