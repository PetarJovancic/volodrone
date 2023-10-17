import pytest
import logging

from volodrone.volodrone_controller import VolodroneController  

@pytest.fixture
def volodrone_controller():
    return VolodroneController([100, 100, 100], [0, 0, 0])

def test_init(volodrone_controller):
    assert volodrone_controller.world_dimensions == [100, 100, 100]
    assert volodrone_controller.current_position == [0, 0, 0]
    assert volodrone_controller.movement_vector == [0, 0, 0]
    assert volodrone_controller.total_distance == 0
    assert isinstance(volodrone_controller.logger, logging.Logger)

def test_update_position(volodrone_controller):
    volodrone_controller.movement_vector = [1, 2, 3]
    volodrone_controller.update_position()
    assert volodrone_controller.current_position == [1, 2, 3]

def test_calc_total_distance(volodrone_controller):
    volodrone_controller.movement_vector = [1, 2, 3]
    volodrone_controller.calc_total_distance()
    assert volodrone_controller.total_distance == 6

def test_avoid_obstacles(volodrone_controller, caplog):
    volodrone_controller.current_position = [0, 0, 0]
    volodrone_controller.movement_vector = [-1, 0, 0]
    volodrone_controller.avoid_obstacles()
    assert volodrone_controller.current_position == [0, 0, 0]
    # assert "CRASH IMMINENT" in caplog.text

def test_execute_command_valid(volodrone_controller):
    volodrone_controller.execute_command("1, UP, 10")
    assert volodrone_controller.movement_vector == [0, 0, 10]
    assert volodrone_controller.total_distance == 10

def test_execute_command_invalid_direction(volodrone_controller, caplog):
    volodrone_controller.execute_command("1, INVALID, 10")
    assert volodrone_controller.movement_vector == [0, 0, 0]
    assert "Invalid direction: INVALID" in caplog.text

def test_execute_command_negative_values(volodrone_controller, caplog):
    volodrone_controller.execute_command("-1, UP, -10")
    assert volodrone_controller.movement_vector == [0, 0, 0]
    assert "Error parsing command" in caplog.text

def test_execute_command_invalid_format(volodrone_controller, caplog):
    volodrone_controller.execute_command("invalid_format")
    assert volodrone_controller.movement_vector == [0, 0, 0]
    assert "Error parsing command" in caplog.text

def test_execute_command_unexpected_error(volodrone_controller, caplog, monkeypatch):
    def mock_execute_command_error(*args, **kwargs):
        raise Exception("Mocked unexpected error")

    monkeypatch.setattr(volodrone_controller, 'update_position', mock_execute_command_error)
    
    volodrone_controller.execute_command("1, UP, 10")
    assert volodrone_controller.movement_vector == [0, 0, 0]
    assert "Unexpected error: Mocked unexpected error" in caplog.text

def test_execute_command_unspecific_input(volodrone_controller, caplog):
    commands = ["Move forward", "2, LEFT, 5", "1, UP, 10", "Invalid command", "3, FORWARD, 8"]
    volodrone_controller.run_simulation(commands)

    assert "=== Volodrone Initialising" in caplog.text
    assert "=== Volodrone Sensor Data read." in caplog.text
    assert "=== Volodrone Take Off" in caplog.text
    assert "Error parsing command" in caplog.text
    assert "([0, 0, 10])-> (0, 0, 10) [10]" in caplog.text
    assert "([-5, 0, 0])-> (-5, 0, 10) [15]" in caplog.text
    assert "([0, 8, 0])-> (-5, 8, 10) [23]" in caplog.text
    assert "=== Volodrone Landing" in caplog.text

def test_execute_command_out_of_order(volodrone_controller, caplog):
    commands = ["3, FORWARD, 5", "1, UP, 10", "2, LEFT, 5"]
    volodrone_controller.run_simulation(commands)

    assert "=== Volodrone Initialising" in caplog.text
    assert "=== Volodrone Sensor Data read." in caplog.text
    assert "=== Volodrone Take Off" in caplog.text
    assert "([0, 0, 10])-> (0, 0, 10) [10]" in caplog.text
    assert "([-5, 0, 0])-> (-5, 0, 10) [15]" in caplog.text
    assert "([0, 5, 0])-> (-5, 5, 10) [20]" in caplog.text
    assert "=== Volodrone Landing" in caplog.text
