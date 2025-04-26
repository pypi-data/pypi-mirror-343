from abc import ABC, abstractmethod

class HighLevelController(ABC):
    """Base class for high-level controllers that determine temperature setpoints.
    
    This abstract class defines the interface for all high-level controllers,
    which are responsible for determining the temperature setpoint based on
    various factors such as time, occupancy, or external conditions.
    """
    
    def __init__(self, time_step=60):
        """Initialize the controller with common parameters.
        
        Args:
            time_step (int, optional): Time step between control updates in
                minutes. Defaults to 60.
        """
        self.time_step = time_step
        
        # Initialize an empty data dictionary
        self.data = {}
    
    @abstractmethod
    def get_setpoint(self, current_time, *args, **kwargs):
        """Base implementation of get_setpoint.
        
        Args:
            current_time: The current timestamp
            *args: Additional positional arguments (not used in base)
            **kwargs: Additional keyword arguments (not used in base)
        """
        pass