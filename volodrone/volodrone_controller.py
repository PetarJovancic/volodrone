import logging
from typing import List


class VolodroneController:
    def __init__(
        self,
        world_dimensions: List[int],
        drone_start_position: List[int],
    ) -> None:
        self.world_dimensions = world_dimensions
        self.current_position = drone_start_position
        self.movement_vector = [0, 0, 0]
        self.total_distance = 0

        self.logger = logging.getLogger(__name__)

    def init_drone(self) -> None:
        """
        Method for simulating initialization of a drone.
        """
        self.logger.info('=== Volodrone Initialising')

    def read_sensor_data(self) -> None:
        """
        Method for simulating sensor data readings.
        """
        self.logger.info("=== Volodrone Sensor Data read.")
        self.logger.info(f"World: (x=range(0, {self.world_dimensions[0]}), "
                         f"y=range(0, {self.world_dimensions[1]}), "
                         f"z=range(0, {self.world_dimensions[2]}))")
        self.logger.info(f"Drone starts at: {tuple(self.current_position)}")

    def take_off(self) -> None:
        """
        Method for simuliating take off stage.
        """
        self.logger.info("=== Volodrone Take Off")

    def update_position(self) -> None:
        """
        Method for updating current position of a drone.
        """
        for i in range(3):
            self.current_position[i] += self.movement_vector[i]
        self.avoid_obstacles()

    def avoid_obstacles(self) -> None:
        """
        Method to check if the drone is about to hit the walls.
        """
        for i in range(3):
            if self.current_position[i] < 0 or \
                    self.current_position[i] >= self.world_dimensions[i]:
                self.logger.warning('CRASH IMMINENT'
                                    ' - AUTOMATIC COURSE CORRECTION')
                # Adjust the movement vector to avoid collision
                self.correction = round(self.movement_vector[i]/2)
                if self.correction >= 10:
                    self.correction = 5
                self.movement_vector[i] = self.correction
                self.current_position[i] = \
                    self.current_position[i] - self.movement_vector[i]

    def calc_total_distance(self) -> None:
        """
        Method for calculating total distance of the movement.
        """
        for i in range(3):
            self.total_distance += abs(self.movement_vector[i])

    def land(self) -> None:
        """
        Method for simulating landing.
        """
        self.logger.info("=== Volodrone Landing")

    def execute_command(self, command: str) -> None:
        """
        Method for executing steering commands

        Args:
            command (str): Command in the string format eg. "01, LEFT, 10"

        Returns:
            None
        """
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

    def run_simulation(self, commands: List[str]) -> None:
        """
        Method for executing steering commands

        Args:
            commands (List[str]): List of commands in the form ["01, LEFT, 10"]
            Default is an empty list.

        Returns:
            None
        """
        commands = commands or []
        self.init_drone()
        self.read_sensor_data()
        self.take_off()

        for command in commands:
            self.execute_command(command)
            self.logger.info(f"{tuple(self.movement_vector)}"
                             f"-> {tuple(self.current_position)}"
                             f" [{self.total_distance}]")

        self.land()
