import logging
from volodrone.volodrone_controller import VolodroneController

if __name__ == "__main__":
    # Example usage:
    world_dimensions = [10, 10, 10]  # Dimensions of the world in centimeters
    drone_start = [5, 5, 5]  # Starting position of the drone

    # commands = ["01, LEFT, 2",
    #             "02, UP, 2",
    #             "03, RIGHT, 1",
    #             "04, DOWN, 1",
    #             "05, BACKWARD, 2",
    #             "06, FORWARD, 1"]
    # commands = ["01, LEFT, 2", 
    #             "02, UP, 2", 
    #             "03, RIGHT, 1"]
    # commands = ["01, LEFT, 10"]
    commands = ["01, fdf, 10"]

    logging.basicConfig(level=logging.INFO)
    controller = VolodroneController(world_dimensions, drone_start)
    controller.run_simulation(commands)