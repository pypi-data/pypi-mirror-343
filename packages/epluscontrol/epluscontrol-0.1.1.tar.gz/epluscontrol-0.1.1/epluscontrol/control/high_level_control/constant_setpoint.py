from epluscontrol.control.high_level_control.high_level_base import HighLevelController


class ConstantSetpoint(HighLevelController):
    """Controller that randomly switches between min and max setpoints.
    
    This controller is useful for testing system responses or for generating
    excitation signals for system identification.
    
    Args:
        setpoint (float): Temperature setpoint in °C. Defaults to 20.
        time_step (int, optional): Time step between control updates in
            minutes. Defaults to 60.   
    """
    
    def __init__(self, time_step=60, setpoint=20):
    
        super().__init__(time_step)
        self.setpoint = setpoint
    
        
    def get_setpoint(self, current_time, *args, **kwargs):
        """Returns the constant setpoint
        
        Args:
            current_time (datetime): The current simulation time.
            
        Returns:
            float: The temperature setpoint in degrees Celsius.
        """
                
        return self.setpoint

