import simpy
import statistics
import Building
from LiftRandoms import LiftRandoms


class Main(object):
    """
    Represents the main simulation object that initializes and runs the simulation.

    Attributes:
        num_up (int): The number of elevators that move upwards.
        num_down (int): The number of elevators that move downwards.
        num_floors (int): The number of floors in the building.
    """

    def __init__(self, num_up, num_down, num_floors):
        """
        Initializes a new instance of the Main class.

        Args:
            num_up (int): The number of elevators that move upwards.
            num_down (int): The number of elevators that move downwards.
            num_floors (int): The number of floors in the building.

        """
        self.env = simpy.Environment()
        self.num_up = num_up
        self.num_down = num_down
        self.num_floors = num_floors
        self.building = None

    def run(self, duration):
        """
        Runs the simulation for a specified duration.

        Args:
            duration (float): The duration of the simulation in seconds.

        """
        self.building = Building.Building(self.env, self.num_up, self.num_down, self.num_floors)
        self.building.initialise()
        self.env.process(self.building.simulate())
        # self.env.run(until=duration)
        
        while self.env.peek() < duration:
            self.env.step()

    def get_average_waiting_time(self):
        waiting_time = []
        people = self.building.get_all_persons()
        for person in people:
            if person.has_completed_trip():
                waiting_time.append(person.get_wait_time())

        if len(waiting_time) == 0:
            return -1
        else:
            return statistics.mean(waiting_time)

Test = Main(num_up=2, num_down=1, num_floors=9)
Test.run(86400)
print(len(Test.building.get_all_persons()))