from epluscontrol.control.control_managers.base import ControlStrategy


class StandardControl(ControlStrategy):
    """Standard control strategy using high-level and low-level controllers.
    
    This implements the default control behavior where a high-level controller 
    determines setpoints and a low-level controller tracks those setpoints.
    """
    def __init__(self):
        self.data = {"cost": []}  
    
    
    def execute_control(self, state, simulator, current_time):
        """Execute standard control strategy.
        
        Args:
            state: EnergyPlus state object.
            simulator: The Simulator instance.
            current_time: Current simulation datetime.
            
        Returns:
            dict: Contains the 'setpoint' that was determined.
        """        
        # Get current measurement
        sensor_name = simulator.low_level_control.sensor_name
        indoor_temp = simulator.sensor_manager.sensors[sensor_name]["data"][-1]
        
        # Get previous mean heat measurements
        heat_data = simulator.sensor_manager.sensors["Heat Power"]["data"]
        samples = min(simulator.high_level_control.time_step, len(heat_data))
        recent_values = heat_data[-samples:]
        heat_power = sum(recent_values) / len(recent_values)
        
        # Get high-level controller to determine setpoint
        setpoint = simulator.high_level_control.get_setpoint(current_time, indoor_temp, current_heating=heat_power)
        
        if current_time.minute % simulator.low_level_control.time_step == 0:               
                error = setpoint - indoor_temp
                control_output = simulator.low_level_control.get_control_output(error)
                heat_output = simulator.MAX_POWER * control_output          
                simulator.actuator_manager.set_actuator_value(simulator.api, state, heat_output)      
        
        return setpoint