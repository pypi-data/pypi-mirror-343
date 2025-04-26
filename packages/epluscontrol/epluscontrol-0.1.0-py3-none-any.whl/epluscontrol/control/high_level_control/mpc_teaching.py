from epluscontrol.control.high_level_control.high_level_base import HighLevelController
import cvxpy as cp
import numpy as np
#from datetime import datetime, timedelta
from epluscontrol.control.high_level_control.mpc_visualization_tools import add_visualization_data_collection

class ModelPredictiveControlTeaching(HighLevelController):
    """Model Predictive Controller (MPC) for building temperature control.
    
    This controller implements a model predictive control strategy that optimizes
    heating power based on:
    - Weather forecasts (outdoor temperature, solar radiation)
    - Energy price forecasts
    - Comfort constraints (min/max temperature bounds)
    - Building thermal dynamics (state-space model)
    
    The MPC formulates and solves an optimization problem at each control interval
    to determine the optimal heating power trajectory over a prediction horizon,
    and applies the first control action of this trajectory.
    
    The controller also includes an optional visualization feature to help understand
    the receding horizon approach for educational purposes.
    
    Args:
        time_step (int, optional): Time step between control updates in
            minutes. Currently only supports 60 (hourly updates).
        weather_parser (object): Parser object for weather forecast data,
            providing outdoor temperature and solar radiation predictions.
        grid_parser (object): Parser object for energy grid data,
            providing energy price and carbon intensity predictions.
        low_setpoint_parser (object): Parser for minimum temperature bounds.
        high_setpoint_parser (object): Parser for maximum temperature bounds.
        max_power (float): Maximum heating power in Watts.
        horizon (int): Prediction horizon length (number of time steps).
        model (object): State-space model of the building thermal dynamics.
        enable_visualization (bool): Whether to enable visualization data collection.
    """    
    
    def __init__(self, 
                 time_step=60, 
                 weather_parser=None, 
                 grid_parser=None, 
                 low_setpoint_parser=None,
                 high_setpoint_parser=None, 
                 max_power=500, 
                 horizon=24, 
                 model=None,
                 slack_weight=10e6,
                 enable_visualization=False):
        
        super().__init__(time_step)
        
        # Store parser objects for predictions
        self.weather = weather_parser
        self.grid = grid_parser
        self.low_setpoint = low_setpoint_parser
        self.high_setpoint = high_setpoint_parser        
        
        # MPC parameters
        self.max_power = max_power
        self.horizon = horizon
        self.model = model
        self.x0 = model.x0  # Initial state estimate
        self.slack_weight=slack_weight
        self.setpoint = 20  # Default setpoint as fallback
        self.optimal_heating = None
        
        # Store visualization setting
        self.enable_visualization = enable_visualization
        
        # Print model details for debugging (consider removing in production)
        print("State-Space Model Parameters:")
        print(f"A matrix:\n{self.model.A}")
        print(f"B matrix:\n{self.model.B}")
        print(f"C matrix:\n{self.model.C}")
        print(f"D matrix:\n{self.model.D}")
        print(f"K matrix:\n{self.model.K}")
        print(f"Initial state x0:\n{self.x0}")
        
    def get_setpoint(self, current_time, y_measured, current_heating=None, *args, **kwargs):
        """Calculate the optimal temperature setpoint based on MPC.
        
        This method runs the MPC optimization at regular intervals defined by
        time_step and returns the current setpoint.
        
        Args:
            current_time (datetime): Current timestamp.
            y_measured (float): Current measured zone temperature.
            *args, **kwargs: Additional arguments (not used).
                current_heating (float, optional): Current heating power for visualization.
            
        Returns:
            float: Optimal temperature setpoint.
        """
        # Only run the MPC optimization at the specified time intervals
        if current_time.minute % self.time_step == 0:
            # Get state-space model matrices
            A = self.model.A
            B = self.model.B
            C = self.model.C 
            K = self.model.K
            
            # Extract input columns for readability
            # Assuming B has columns for: [ambient_temp, solar_rad, heating_power]
            Ba = B[:, 0]  # Ambient temperature impact
            Bs = B[:, 1]  # Solar radiation impact
            Bh = B[:, 2]  # Heating power impact
            
            n_x, n_u = B.shape
    
            # Get energy cost forecast
            energy_cost, _, _ = self.grid.get_prediction_horizon(current_time, self.horizon)
            
            # Get weather forecast
            Ta, Qs, _ = self.weather.get_prediction_horizon(current_time, self.horizon)
            
            # Get temperature constraints
            Tmin, _ = self.low_setpoint.get_prediction_horizon(current_time, self.horizon)
            Tmax, _ = self.high_setpoint.get_prediction_horizon(current_time, self.horizon)
    
            # Define optimization variables
            x = cp.Variable((self.horizon + 1, n_x))       # State trajectory
            Qh = cp.Variable(self.horizon, nonneg=True)    # Heating power
            slack = cp.Variable(self.horizon, nonneg=True) # Constraint relaxation
            
            # Update estimated initial state (using newest measurements)
            # if current_heating is not None and self.optimal_heating is not None:
            #     print("Updating State...")
            #     print(f"heat diff: {current_heating-self.optimal_heating}")
            #     self.x0 = self.x0 + Bh*(current_heating-self.optimal_heating)
            
            # Initial condition constraint
            constraints = [x[0] == self.x0.flatten(order="F")]
            
            # State estimation
            y_estimated = C @ self.x0.flatten(order="F")
            
            # Define optimization problem
            cost = 0
            for i in range(self.horizon):
                # System dynamics constraints
                if i == 0:
                    # Include state estimation correction on the first step
                    error = y_measured - y_estimated
                    print(f"Output estimation error = {error}")
                    constraints.append(
                        x[i + 1, :] == A @ x[0, :] + 
                        Ba * Ta[i] + Bs * Qs[i] + Bh * Qh[i] + 
                        K @ error
                    )
                else:
                    constraints.append(
                        x[i + 1, :] == A @ x[i, :] + 
                        Ba * Ta[i] + Bs * Qs[i] + Bh * Qh[i]
                    )
                
                # Temperature comfort constraints with slack variables
                constraints.append(Tmin[i] - slack[i] <= C @ x[i + 1, :])
                constraints.append(C @ x[i + 1, :] <= Tmax[i] + slack[i])
            
                # Heating power constraints
                constraints.append(Qh[i] <= self.max_power)
                constraints.append(Qh[i] >= 0)
                
                # Cost function: energy cost + penalty for comfort violations
                cost += Qh[i] * energy_cost[i] + self.slack_weight*slack[i]
            
            # Solve the optimization problem
            objective = cp.Minimize(cost)
            problem = cp.Problem(objective, constraints)
            problem.solve(verbose=False)
            
            # Store trajectories for visualization
            if self.enable_visualization:
                self.last_state_trajectory = x.value
                self.last_heating_trajectory = Qh.value
            
            # Check if the problem was solved successfully
            if problem.status not in ["optimal", "optimal_inaccurate"]:
                print(f"Warning: MPC optimization problem status: {problem.status}")
                return self.setpoint  # Return previous setpoint if optimization failed
            
            # Update state estimate with first step of optimal trajectory
            self.x0 = x.value[1, :]
            
            # Calculate setpoint from state estimate
            setpoint = float(C @ x.value[1, :])
            
            # Apply setpoint correction based on heating power
            self.optimal_heating = Qh.value[0]
            #setpoint = self._correct_setpoint(setpoint, Tmin, Tmax, self.optimal_heating)
            
            # Update and log the setpoint
            self.setpoint = setpoint
            print(f"Optimal MPC setpoint: {self.setpoint:.2f}°C")
            
        # Return the current setpoint (updated or not)
        return self.setpoint
    
    def _correct_setpoint(self, setpoint, Tmin, Tmax, Qh_opt):
        """Correct the temperature setpoint based on optimal heating power.
        
        Args:
            setpoint (float): Raw calculated setpoint from optimization.
            Tmin (array): Minimum temperature constraint.
            Tmax (array): Maximum temperature constraint.
            Qh_opt (float): Optimal heating power for the current time step.
            
        Returns:
            float: Corrected temperature setpoint (°C).
        """
        if Qh_opt <= 0.01:
            corrected_setpoint = Tmin[0]-0.5
            print("Heating off - setting minimum temperature")
        elif Qh_opt >= self.max_power-0.01:
            corrected_setpoint = Tmax[0]+0.5
            print("Maximum heating power - setting maximum temperature")
        else:
            corrected_setpoint = np.clip(setpoint, Tmin[0], Tmax[0])
            print(f"Normal operation - clipping setpoint between {Tmin[0]:.1f} and {Tmax[0]:.1f}")
        
        return corrected_setpoint


# Add visualization capabilities to the MPC controller
ModelPredictiveControl = add_visualization_data_collection(ModelPredictiveControlTeaching)