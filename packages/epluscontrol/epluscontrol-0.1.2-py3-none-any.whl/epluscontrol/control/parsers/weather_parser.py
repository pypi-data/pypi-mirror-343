import pandas as pd
import matplotlib.pyplot as plt

class WeatherParser:
    def __init__(self, filepath):
        # Read the CSV file
        self.data = pd.read_csv(filepath)
        
        # Convert timestamp to datetime
        self.data['Timestamp'] = pd.to_datetime(self.data['Timestamp'])
        
        # Add hour_timestamp column for easier lookup
        self.data['hour_timestamp'] = self.data['Timestamp'].dt.floor('h')
    
    def get_values(self, timestamp):
        """
        Get weather data for a specific timestamp
        
        Parameters:
        -----------
        timestamp : datetime
            The timestamp to look up
            
        Returns:
        --------
        tuple: (outdoor_temp, solar_radiation)
            Weather values for the given timestamp, or (None, None) if not found
        """
        hour_timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
        row = self.data[self.data['hour_timestamp'] == hour_timestamp]
        
        if not row.empty:
            return row['outdoor'].iloc[0], row['solar'].iloc[0]
        return None, None
    
    def get_prediction_horizon(self, timestamp, N):
        """
        Get weather data for a prediction horizon of N hours starting from timestamp
        
        Parameters:
        -----------
        timestamp : datetime
            The starting timestamp
        N : int
            Number of hours in the prediction horizon (including current hour)
        
        Returns:
        --------
        tuple: (outdoor_temps, solar_values, timestamps)
            Lists containing the weather values and timestamps for the N hours
        """
        # Round to the nearest hour
        hour_timestamp = timestamp.replace(minute=0, second=0, microsecond=0)
        
        # Create list of hour timestamps for the prediction horizon
        timestamps = [hour_timestamp + pd.Timedelta(hours=i) for i in range(N)]
        
        # Get data for each timestamp
        outdoor_temps = []
        solar_values = []
        
        for ts in timestamps:
            # Find matching row
            row = self.data[self.data['hour_timestamp'] == ts]
            if not row.empty:
                outdoor_temps.append(row['outdoor'].iloc[0])
                solar_values.append(row['solar'].iloc[0])
            else:
                # Handle missing data
                outdoor_temps.append(None)
                solar_values.append(None)
        
        return outdoor_temps, solar_values, timestamps
    
    def plot_data(self, days=7):
        """
        Plot the weather data for the specified number of days
        
        Parameters:
        -----------
        days : int
            Number of days to plot (default is 7)
        """
        # Get the first days worth of data
        end_date = self.data['Timestamp'].min() + pd.Timedelta(days=days)
        plot_data = self.data[self.data['Timestamp'] <= end_date].copy()
        
        # Create the figure
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
        
        # Plot outdoor temperature
        ax1.plot(plot_data['Timestamp'], plot_data['outdoor'], color='blue')
        ax1.set_ylabel('Temperature (°C)', color='blue')
        ax1.tick_params(axis='y', labelcolor='blue')
        ax1.grid(True)
        ax1.set_title('Outdoor Temperature')
        
        # Plot solar radiation
        ax2.plot(plot_data['Timestamp'], plot_data['solar'], color='orange')
        ax2.set_ylabel('Solar Radiation (W/m²)', color='orange')
        ax2.tick_params(axis='y', labelcolor='orange')
        ax2.grid(True)
        ax2.set_title('Solar Radiation')
        
        # Add overall title and format x-axis
        plt.suptitle('Weather Data')
        plt.xlabel('Timestamp')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()