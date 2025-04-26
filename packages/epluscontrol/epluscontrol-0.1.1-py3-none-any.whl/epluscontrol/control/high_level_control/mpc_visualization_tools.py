"""
Final Corrected MPC Visualization Tools

This module provides visualization tools for Model Predictive Control (MPC)
with proper time alignment and correctly displayed next setpoint.
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pickle
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure


class MPCVisualizationData:
    """Class for collecting and storing MPC visualization data."""
    
    def __init__(self):
        """Initialize the data storage."""
        self.timestamps = []
        self.actual_temps = []
        self.setpoints = []
        self.heating_powers = []
        self.energy_prices = []
        self.optimizations = []
        
    def add_data_point(self, timestamp, actual_temp, setpoint, heating_power, energy_price=None):
        """Add a single data point to the history."""
        self.timestamps.append(timestamp)
        self.actual_temps.append(actual_temp)
        self.setpoints.append(setpoint)
        self.heating_powers.append(heating_power)
        self.energy_prices.append(0 if energy_price is None else energy_price)
        
    def add_optimization(self, timestamp, horizon_times, predicted_temps, 
                         predicted_heating, temp_min, temp_max, predicted_prices=None):
        """Add optimization result to the history."""
        # Convert numpy arrays to lists for easier serialization
        self.optimizations.append({
            'time': timestamp,
            'horizon_times': horizon_times,
            'predicted_temps': predicted_temps.tolist() if isinstance(predicted_temps, np.ndarray) else predicted_temps,
            'predicted_heating': predicted_heating.tolist() if isinstance(predicted_heating, np.ndarray) else predicted_heating,
            'temp_min': temp_min.tolist() if isinstance(temp_min, np.ndarray) else temp_min,
            'temp_max': temp_max.tolist() if isinstance(temp_max, np.ndarray) else temp_max,
            'predicted_prices': predicted_prices.tolist() if isinstance(predicted_prices, np.ndarray) else predicted_prices
        })
        
    def save(self, filename):
        """Save the collected data to a file."""
        with open(filename, 'wb') as f:
            pickle.dump(self, f)
        print(f"Visualization data saved to: {filename}")
        
    @classmethod
    def load(cls, filename):
        """Load visualization data from a file."""
        with open(filename, 'rb') as f:
            data = pickle.load(f)
        print(f"Visualization data loaded from: {filename}")
        return data


class MPCVisualizer:
    """Interactive MPC visualization tool."""
    
    def __init__(self, data, title="MPC Visualization"):
        """Initialize the visualizer."""
        self.data = data
        self.title = title
        self.current_index = 0
        self.max_index = len(data.optimizations) - 1 if data.optimizations else 0
        
        # Set up the Tkinter window
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry("1000x900")  # Taller to accommodate price plot
        
        # Create frame for controls
        control_frame = ttk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        # Add timestamp display
        self.timestamp_var = tk.StringVar(value="")
        ttk.Label(control_frame, text="Current Time:").pack(side=tk.LEFT)
        ttk.Label(control_frame, textvariable=self.timestamp_var, font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
        
        # Add navigation buttons
        self.prev_btn = ttk.Button(control_frame, text="Previous", command=self._prev_step)
        self.prev_btn.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(control_frame, text="Next", command=self._next_step)
        self.next_btn.pack(side=tk.LEFT, padx=10)
        
        # Add step slider
        slider_frame = ttk.Frame(self.root)
        slider_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        ttk.Label(slider_frame, text="Step:").pack(side=tk.LEFT)
        self.step_var = tk.IntVar(value=0)
        self.slider = ttk.Scale(
            slider_frame, 
            from_=0, 
            to=self.max_index, 
            orient=tk.HORIZONTAL,
            variable=self.step_var,
            command=self._slider_changed
        )
        self.slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.step_label = ttk.Label(slider_frame, text=f"0/{self.max_index}")
        self.step_label.pack(side=tk.LEFT, padx=5)
        
        # Create frame for the plot
        plot_frame = ttk.Frame(self.root)
        plot_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create the figure and canvas
        self.fig = Figure(figsize=(9, 8), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Add toolbar
        toolbar = NavigationToolbar2Tk(self.canvas, plot_frame)
        toolbar.update()
        
        # Create subplots (3 rows for temp, power, and price)
        self.ax_temp = self.fig.add_subplot(3, 1, 1)
        self.ax_power = self.fig.add_subplot(3, 1, 2, sharex=self.ax_temp)
        self.ax_price = self.fig.add_subplot(3, 1, 3, sharex=self.ax_temp)
        
        # Add info text
        info_frame = ttk.LabelFrame(self.root, text="MPC Information")
        info_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)
        
        self.info_text = tk.Text(info_frame, height=3, wrap=tk.WORD)
        self.info_text.pack(fill=tk.X, expand=True, padx=5, pady=5)
        
        # Update display with first step
        if self.max_index >= 0:
            self._update_display(0)
    
    def _prev_step(self):
        """Go to previous step."""
        if self.current_index > 0:
            self.current_index -= 1
            self.step_var.set(self.current_index)
            self._update_display(self.current_index)
    
    def _next_step(self):
        """Go to next step."""
        if self.current_index < self.max_index:
            self.current_index += 1
            self.step_var.set(self.current_index)
            self._update_display(self.current_index)
    
    def _slider_changed(self, value):
        """Handle slider value change."""
        index = int(float(value))
        if index != self.current_index:
            self.current_index = index
            self._update_display(index)
    
    def _update_display(self, index):
        """Update the visualization for the given step index."""
        if index < 0 or index > self.max_index or not self.data.optimizations:
            return
        
        # Get current optimization data
        opt = self.data.optimizations[index]
        current_time = opt['time']
        
        # Find time index in history data
        time_index = 0
        for i, t in enumerate(self.data.timestamps):
            if t >= current_time:
                time_index = i
                break
        
        # Get history data up to current time
        timestamps = self.data.timestamps[:time_index+1]
        actual_temps = self.data.actual_temps[:time_index+1]
        setpoints = self.data.setpoints[:time_index+1]
        heating_powers = self.data.heating_powers[:time_index+1]
        energy_prices = self.data.energy_prices[:time_index+1]
        
        # Clear previous plots
        self.ax_temp.clear()
        self.ax_power.clear()
        self.ax_price.clear()
        
        # Plot actual temperatures (line with markers)
        self.ax_temp.plot(
            timestamps, 
            actual_temps, 
            color='blue', 
            linestyle='-', 
            linewidth=2, 
            marker='o',
            markersize=4,
            label='Actual Temperature'
            )
            
        # Plot past setpoints as stair plot
        self.ax_temp.step(
            timestamps, 
            setpoints, 
            color='red', 
            linewidth=2,
            where='pre',
            marker='o',
            markersize=4,
            label='Implemented Setpoint'
        )
        
        # Get the first predicted temperature (the next setpoint)
        next_setpoint = opt['predicted_temps'][1]
        
        # Get the time of the first prediction point
        next_time = opt['horizon_times'][1]
        
        # Create a plot for just the next setpoint
        self.ax_temp.plot(
            [current_time, next_time], 
            [next_setpoint, next_setpoint],  # Same value for both points to create flat step
            color='black',
            linestyle='-', 
            linewidth=2,
            label='Next Setpoint'
        )
        
        # Highlight the point with a marker
        self.ax_temp.plot(
            [next_time],
            [next_setpoint],
            color='black',
            marker='o',
            markersize=8
        )
        
        # Plot temperature predictions and constraints
        self.ax_temp.plot(
            opt['horizon_times'], 
            opt['predicted_temps'], 
            color='blue', 
            linestyle='--', 
            linewidth=2,
            marker='.',
            markersize=4,
            label='Predicted Temperature'
        )
        
        # Comfort zone (if constraints available)
        self.ax_temp.fill_between(
            opt['horizon_times'][1:],
            opt['temp_min'],
            opt['temp_max'],
            color='lightgreen',
            alpha=0.3,
            label='Comfort Zone'
        )
        
        # # Plot min/max temperature bounds
        # self.ax_temp.step(
        #     opt['horizon_times'],
        #     opt['temp_min'],
        #     color='green',
        #     linestyle=':',
        #     linewidth=1,
        #     where='post',
        #     label='Min Temp'
        # )
            
        # self.ax_temp.step(
        #     opt['horizon_times'],
        #     opt['temp_max'],
        #     color='green',
        #     linestyle=':',
        #     linewidth=1,
        #     where='post',
        #     label='Max Temp'
        # )
        
        # Get the first predicted heating (the next heating action)
        next_heating = opt['predicted_heating'][0]
        
        # Create a stair plot for just the next heating action
        self.ax_power.plot(
            [current_time, next_time], 
            [next_heating, next_heating],
            color='black',
            linestyle='-', 
            linewidth=2,
            label='Next Heating Action'
        )
        
        # Highlight the point with a marker
        self.ax_power.plot(
            [current_time],
            [next_heating],
            color='red',
            marker='o',
            markersize=8
        )
        
        # Plot actual heating (stair plot)
        self.ax_power.step(
            timestamps, 
            heating_powers, 
            color='green', 
            linewidth=2,
            where='pre',
            label='Actual Heating'
        )
        
        # Add markers at the data points
        self.ax_power.plot(
            timestamps[1:], 
            heating_powers[1:], 
            color='green', 
            linestyle='', 
            marker='o',
            markersize=4
        )
        
        # Plot heating predictions as stair plot
        self.ax_power.step(
            opt['horizon_times'][1:], 
            opt['predicted_heating'], 
            color='green', 
            linestyle='--', 
            linewidth=2,
            where='pre',  # Draw steps after the data point
            label='Predicted Heating'
        )
        
        # Add markers at the predicted points
        self.ax_power.plot(
            opt['horizon_times'][1:], 
            opt['predicted_heating'], 
            color='green', 
            linestyle='', 
            marker='.',
            markersize=4
        )
        
        # Plot next energy price as a stair starting at current time
        next_price = opt['predicted_prices'][0]
        
        # Create a stair plot for just the next price
        self.ax_price.step(
            [current_time, next_time], 
            [next_price, next_price],
            color='purple',
            linestyle='-', 
            linewidth=2,
            where='post',
            label='Next Energy Price'
        )
        
        # Highlight the point with a marker
        self.ax_price.plot(
            [current_time],
            [next_price],
            color='purple',
            marker='o',
            markersize=8
        )
        
        # Stair plot for actual prices
        self.ax_price.step(
            timestamps, 
            energy_prices, 
            color='purple', 
            linewidth=2,
            where='post',  # Draw steps after the data point
            label='Actual Price'
        )
        
        # Add markers at the data points
        self.ax_price.plot(
            timestamps[1:], 
            energy_prices[1:], 
            color='purple', 
            linestyle='', 
            marker='o',
            markersize=4
        )
        
        # Stair plot for predicted prices (skip first point which is shown as next price)
        self.ax_price.step(
            opt['horizon_times'][1:], 
            opt['predicted_prices'], 
            color='purple', 
            linestyle='--', 
            linewidth=2,
            where='post',  # Draw steps after the data point
            label='Predicted Price'
        )
        
        # Add markers at the predicted points
        self.ax_price.plot(
            opt['horizon_times'][1:], 
            opt['predicted_prices'], 
            color='purple', 
            linestyle='', 
            marker='.',
            markersize=4
        )
        
        # Mark current time with vertical line
        for ax in [self.ax_temp, self.ax_power, self.ax_price]:
            ax.axvline(x=current_time, color='black', linestyle='-', linewidth=1)
        
        # Format plots
        date_format = mdates.DateFormatter('%H:%M')
        
        self.ax_temp.set_title('MPC Temperature Control', fontsize=12)
        self.ax_temp.set_ylabel('Temperature (°C)', fontsize=10)
        self.ax_temp.grid(True)
        self.ax_temp.legend(loc='best')
        
        self.ax_power.set_title('Heating Power', fontsize=12)
        self.ax_power.set_ylabel('Power (W)', fontsize=10)
        self.ax_power.grid(True)
        self.ax_power.legend(loc='best')
        
        self.ax_price.set_title('Energy Price', fontsize=12)
        self.ax_price.set_ylabel('Price (€/kWh)', fontsize=10)
        self.ax_price.set_xlabel('Time', fontsize=10)
        self.ax_price.grid(True)
        self.ax_price.legend(loc='best')
        
        # Apply date formatter to all x-axes
        for ax in [self.ax_temp, self.ax_power, self.ax_price]:
            ax.xaxis.set_major_formatter(date_format)
        
        # Adjust layout
        self.fig.tight_layout()
        self.canvas.draw()
        
        # Update info display
        self._update_info(index, opt, current_time)
    
    def _update_info(self, index, opt, current_time):
        """Update information display."""
        # Update timestamp and step label
        self.timestamp_var.set(current_time.strftime('%Y-%m-%d %H:%M'))
        self.step_label.config(text=f"{index}/{self.max_index}")
        
        # Update info text
        self.info_text.delete(1.0, tk.END)
        
        # Get next setpoint value
        next_setpoint = "N/A"
        if 'predicted_temps' in opt and opt['predicted_temps'] and len(opt['predicted_temps']) > 0:
            next_setpoint = f"{opt['predicted_temps'][0]:.2f}°C"
        
        # Get next heating action value
        next_heating = "N/A"
        if 'predicted_heating' in opt and opt['predicted_heating'] and len(opt['predicted_heating']) > 0:
            next_heating = f"{opt['predicted_heating'][0]:.1f} W"
        
        # Get next energy price
        next_price = "N/A"
        if 'predicted_prices' in opt and opt['predicted_prices'] and len(opt['predicted_prices']) > 0:
            next_price = f"{opt['predicted_prices'][0]:.4f} €/kWh"
        
        info = (
            f"Optimization Step: {index} | Time: {current_time.strftime('%Y-%m-%d %H:%M')}\n"
            f"Next Setpoint: {next_setpoint} | Next Heating Action: {next_heating} | Next Energy Price: {next_price}\n"
            f"MPC Approach: Optimize over prediction horizon, implement first action, then recalculate at next step"
        )
        
        self.info_text.insert(tk.END, info)
    
    def run(self):
        """Run the visualization window."""
        self.root.mainloop()


def add_visualization_data_collection(mpc_class):
    """Add visualization data collection to an MPC controller class."""
    # Store original methods
    original_init = mpc_class.__init__
    original_get_setpoint = mpc_class.get_setpoint
    
    # Define new initialization with visualization data
    def new_init(self, *args, **kwargs):
        # Call original init
        original_init(self, *args, **kwargs)
        
        # Add visualization data storage
        self.enable_visualization = kwargs.get('enable_visualization', False)
        if self.enable_visualization:
            self.visualization_data = MPCVisualizationData()
            print("MPC visualization data collection enabled")
    
    # Define new get_setpoint with data collection
    def new_get_setpoint(self, current_time, y_measured, current_heating=None, *args, **kwargs):
        # Collect current data point if visualization is enabled
        # Only collect at MPC optimization steps
        if (hasattr(self, 'enable_visualization') and self.enable_visualization 
                and current_time.minute % self.time_step == 0):
            # Get current energy price if grid_parser is available
            current_price = None
            if hasattr(self, 'grid') and self.grid is not None:
                try:
                    # Try to get current energy price (different methods)
                    try:
                        price_value, _, _ = self.grid.get_prediction_horizon(current_time, 1)
                        current_price = price_value[0]
                    except:
                        try:
                            price_value, _, _ = self.grid.get_current_value(current_time)
                            current_price = price_value
                        except:
                            pass
                except:
                    pass
            
            # Add data point to visualization
            self.visualization_data.add_data_point(
                current_time, 
                y_measured, 
                self.setpoint,
                current_heating if current_heating is not None else 0,
                current_price
            )
        
        # Call original method to get the result
        result = original_get_setpoint(self, current_time, y_measured, current_heating, *args, **kwargs)
        
        # Collect optimization data if an optimization was performed
        if (hasattr(self, 'enable_visualization') and self.enable_visualization 
                and hasattr(self, 'last_state_trajectory') and hasattr(self, 'last_heating_trajectory')
                and current_time.minute % self.time_step == 0):
            try:
                # Calculate predicted temperatures from state trajectory
                C = self.model.C
                x_values = self.last_state_trajectory
                Qh_values = self.last_heating_trajectory
                
                if x_values is not None and Qh_values is not None:
                    # Calculate predicted temperatures
                    predicted_temps = []
                    for i in range(self.horizon + 1):
                        if i < len(x_values):
                            temp = float(C @ x_values[i])
                            predicted_temps.append(temp)
                    
                    # Generate horizon timestamps
                    horizon_times = [current_time + timedelta(minutes=self.time_step * i) 
                                     for i in range(len(predicted_temps))]
                    
                    # Get constraints
                    Tmin, _ = self.low_setpoint.get_prediction_horizon(current_time, self.horizon)
                    Tmax, _ = self.high_setpoint.get_prediction_horizon(current_time, self.horizon)
                    
                    # Get predicted energy prices 
                    predicted_prices = None
                    if hasattr(self, 'grid') and self.grid is not None:
                        try:
                            price_values, _, _ = self.grid.get_prediction_horizon(current_time, self.horizon)
                            predicted_prices = price_values
                        except:
                            pass
                    
                    # Store optimization data (trim to match predicted_temps length)
                    if horizon_times and len(horizon_times) == len(predicted_temps):
                        # Get part of Qh_values and other arrays matching the horizon_times length
                        horizon_len = len(horizon_times)
                        Qh_subset = Qh_values[:horizon_len] if len(Qh_values) >= horizon_len else Qh_values
                        Tmin_subset = Tmin[:horizon_len] if len(Tmin) >= horizon_len else Tmin
                        Tmax_subset = Tmax[:horizon_len] if len(Tmax) >= horizon_len else Tmax
                        
                        # Add the optimization data
                        self.visualization_data.add_optimization(
                            current_time,
                            horizon_times,
                            predicted_temps,
                            Qh_subset,
                            Tmin_subset,
                            Tmax_subset,
                            predicted_prices[:horizon_len]
                        )
            except Exception as e:
                print(f"Error collecting visualization data: {e}")
                
        return result
    
    # Replace the original methods with our enhanced versions
    mpc_class.__init__ = new_init
    mpc_class.get_setpoint = new_get_setpoint
    
    # Add visualization generation method
    def generate_visualizations(self, output_dir='./mpc_visualization'):
        """Generate interactive visualization from collected MPC data."""
        if not hasattr(self, 'visualization_data') or not self.enable_visualization:
            print("No visualization data available. Make sure enable_visualization=True was set.")
            return False
            
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save visualization data
        data_file = os.path.join(output_dir, 'mpc_visualization_data.pkl')
        self.visualization_data.save(data_file)
        
        # Launch visualization
        visualizer = MPCVisualizer(self.visualization_data, title="MPC Receding Horizon Visualization")
        visualizer.run()
        
        return True
    
    # Add method to save data without launching visualization
    def save_visualization_data(self, output_dir='./mpc_visualization'):
        """Save visualization data to a file for later use."""
        if not hasattr(self, 'visualization_data') or not self.enable_visualization:
            print("No visualization data available. Make sure enable_visualization=True was set.")
            return None
            
        # Ensure output directory exists
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Save visualization data
        data_file = os.path.join(output_dir, 'mpc_visualization_data.pkl')
        self.visualization_data.save(data_file)
        
        return data_file
    
    # Add visualization methods to the class
    mpc_class.generate_visualizations = generate_visualizations
    mpc_class.save_visualization_data = save_visualization_data
    
    return mpc_class


def load_and_visualize(data_file):
    """Load saved visualization data and display it."""
    try:
        data = MPCVisualizationData.load(data_file)
        visualizer = MPCVisualizer(data, title="MPC Receding Horizon Visualization")
        visualizer.run()
        return True
    except Exception as e:
        print(f"Error loading visualization data: {e}")
        return False