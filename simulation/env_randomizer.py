import airsim
import random
import numpy as np
from typing import Dict, List, Any

class Env_Randomizer:

    def __init__(self, client: airsim.CarClient, config: Dict[str, Any]):
        """
        Args:
            client (airsim.CarClient): Connection to the AirSim simulator
            config (Dict[str, Any]): contains keys like max_obstacles,sim_area_bounds and light_intensity_range
        """
        self.client = client
        self.config = config

        self.max_obstacles = config.get("max_obstacles", 3)
        self.sim_area_bounds = config.get(
            "sim_area_bounds", ([-30, -30, 0], [30, 30, 0])
        )
        self.light_intensity_range = config.get(
            "light_intensity_range", (0.8, 1.2)
        )

    def gen_random_position(self) -> airsim.Vector3r:
        low, high = self.sim_area_bounds
        x = random.uniform(low[0], high[0])
        y = random.uniform(low[1], high[1])
        z = low[2]
        return airsim.Vector3r(x, y, z)

    def random_lighting(self) -> Dict[str, str]:
        """
        The time is restricted to daylight hours (06:00 to 18:59)

        Returns:
             the generated time string
        """
        hour = random.randint(6, 18)
        minute = random.randint(0, 59)
        time_str = f"2025-01-01 {hour:02d}:{minute:02d}:00"

        print(f"[Lighting] Time of day set to {time_str}")

        self.client.simSetTimeOfDay(
            is_enabled=True,
            start_datetime=time_str,
            celestial_clock_speed=0.0,
            update_interval_secs=1.0
        )

        return {"time": time_str}

    def random_parking_slot(self) -> Dict[str, airsim.Pose]:
        """
        Returns:
             a random pose for the target parking slot
        """
        pos = self.gen_random_position()
        yaw = random.uniform(0, 2 * np.pi)
        pose = airsim.Pose(pos, airsim.to_quaternion(0, 0, yaw))

        print(f"[Parking Slot] x={pos.x_val:.1f}, y={pos.y_val:.1f}, yaw={yaw:.2f}")
        return {"pose": pose}

    def random_obstacles(self) -> List[Dict[str, Any]]:
        """
        Generates metadata for a set of random obstacles

        Returns:
             The position and orientation and a random scaling factor between 0.5 and 2.0.
        """
        obstacles = []

        for i in range(self.max_obstacles):
            pos = self.gen_random_position()
            yaw = random.uniform(0, 2 * np.pi)
            scale = random.uniform(0.5, 2.0)

            print(f"[Obstacle {i}] x={pos.x_val:.1f}, y={pos.y_val:.1f}, scale={scale:.2f}")

            obstacles.append({
                "pose": airsim.Pose(pos, airsim.to_quaternion(0, 0, yaw)),
                "scale": scale
            })

        return obstacles