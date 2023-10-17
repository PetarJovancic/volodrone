import pytest
import logging

from volodrone.volodrone_controller import VolodroneController  

@pytest.fixture
def volodrone_controller():
    return VolodroneController([10, 10, 10], [5, 5, 5])

def test_update_position(volodrone_controller):
    volodrone_controller.movement_vector = [-2, 0, 0]
    volodrone_controller.update_position()
    assert volodrone_controller.current_position == [3, 5, 5]

def test_calc_total_distance(volodrone_controller):
    volodrone_controller.movement_vector = [1, 2, 3]
    volodrone_controller.calc_total_distance()
    assert volodrone_controller.total_distance == 6

def test_avoid_obstacles(volodrone_controller):
    volodrone_controller.movement_vector = [-10, 0, 0]
    volodrone_controller.update_position()
    volodrone_controller.avoid_obstacles()
    assert volodrone_controller.current_position == [0, 5, 5]

def test_execute_command_valid(volodrone_controller):
    volodrone_controller.execute_command("01, UP, 3")
    assert volodrone_controller.movement_vector == [0, 0, 3]

def test_execute_command_invalid_direction(volodrone_controller):
    volodrone_controller.execute_command("01, INVALID, 10")
    assert volodrone_controller.movement_vector == [0, 0, 0]

def test_execute_command_negative_values(volodrone_controller):
    volodrone_controller.execute_command("01, UP, -10")
    assert volodrone_controller.movement_vector == [0, 0, 0]

def test_execute_command_invalid_format(volodrone_controller):
    volodrone_controller.execute_command("invalid_format")
    assert volodrone_controller.movement_vector == [0, 0, 0]

def test_execute_command_unexpected_error(volodrone_controller, monkeypatch):
    def mock_execute_command_error(*args, **kwargs):
        raise Exception("Mocked unexpected error")

    monkeypatch.setattr(volodrone_controller, 'update_position', mock_execute_command_error)
    
    volodrone_controller.execute_command("01, UP, 1")
    assert volodrone_controller.movement_vector == [0, 0, 0]
