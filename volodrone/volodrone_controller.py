import logging

class VolodroneController:
    def __init__(self, world_dimensions, drone_start_position):
        self.world_dimensions = world_dimensions
        self.current_position = drone_start_position
        self.movement_vector = [0, 0, 0]
        self.total_distance = 0

        # Configure logging
        self.logger = logging.getLogger(__name__)

    def update_position(self):
        # Update the position based on the movement vector
        for i in range(3):
            self.current_position[i] += self.movement_vector[i]
        self.avoid_obstacles()
    
    def calc_total_distance(self):
        for i in range(3):
            self.total_distance += abs(self.movement_vector[i])      

    def avoid_obstacles(self):
        # Check if the drone is about to hit the walls
        for i in range(3):
            if self.current_position[i] < 0\
                or self.current_position[i] >= self.world_dimensions[i]:
                self.logger.warning(f'CRASH IMMINENT' 
                                    f' - AUTOMATIC COURSE CORRECTION')
                # Adjust the movement vector to avoid collision
                self.movement_vector[i] = round(self.movement_vector[i]/2)
                self.current_position[i] = \
                            self.current_position[i] - self.movement_vector[i]

    def read_sensor_data(self):
        # Simulate sensor data reading
        self.logger.info("=== Volodrone Sensor Data read.")
        self.logger.info(f"World: (x=range(0, {self.world_dimensions[0]}), "
                         f"y=range(0, {self.world_dimensions[1]}), "
                         f"z=range(0, {self.world_dimensions[2]}))")
        self.logger.info(f"Drone starts at: {tuple(self.current_position)}")

    def init_drone(self):
        self.logger.info('=== Volodrone Initialising')

    def take_off(self):
        self.logger.info("=== Volodrone Take Off")

    def land(self):
        self.logger.info("=== Volodrone Landing")

    def execute_command(self, command):
        try:
            order, direction, distance = command.split(", ")
            direction = direction.upper()
            order, distance = int(order), int(distance)

            if order <= 0 or distance <= 0:
                raise ValueError("Order and distance must be positive values")
            
            direction_mapping = {
                "LEFT": [-distance, 0, 0],
                "RIGHT": [distance, 0, 0],
                "UP": [0, 0, distance],
                "DOWN": [0, 0, -distance],
                "FORWARD": [0, distance, 0],
                "BACKWARD": [0, -distance, 0]
            }
            self.movement_vector = direction_mapping.get(direction, None)
            
            if not self.movement_vector:
                raise ValueError(f"Invalid direction: {direction}")
                
            self.update_position()
            self.calc_total_distance()
        except ValueError as e:
            self.logger.error(f"Error parsing command: {e}. "
                              f"Skipping command: {command}. "
                              f"Reseting movement vector to [0, 0, 0]\n")
            self.movement_vector = [0, 0, 0]
        except Exception as e:
            self.logger.error(f"Unexpected error: {e}. "
                              f"Reseting movement vector to [0, 0, 0]\n")       
            self.movement_vector = [0, 0, 0] 

    def run_simulation(self, commands):
        self.init_drone()
        self.read_sensor_data()
        self.take_off()

        for command in commands:
            self.execute_command(command)
            self.logger.info(f"{tuple(self.movement_vector)}" 
                             f"-> {tuple(self.current_position)}" 
                             f" [{self.total_distance}]")

        self.land()
