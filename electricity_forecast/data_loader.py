import pandas as pd
import numpy as np
import os
from typing import Literal
import holidays

# Packages for preprocessing
from sklearn.preprocessing import LabelEncoder

class DataLoader:
    def __init__(self, data_path):
        self.data_path = os.path.dirname(data_path) + '/'
        # self.electricity_filename
        # self.weather_filename
        # self.time_filename

    def load_data(self, set: Literal['original', 'formatted', 'no_missing', 'preprocessed']) -> tuple[pd.DataFrame, pd.DataFrame] | tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        # Implement code to load the historical demand data from the specified path
        # Preprocess the data (e.g., handle missing values, normalize, etc.)
        # Return the preprocessed data
        if set == 'original':
            df_electricity = pd.read_csv(self.data_path + 'historic_demand_2009_2023.csv')
            df_weather = pd.read_csv(self.data_path + 'weather_2009_2023.csv')
            return df_electricity, df_weather
        if set == 'formatted':
            df_electricity = pd.read_csv(self.data_path + 'historic_demand_2009_2023_formatted.csv')
            df_electricity['datetime'] = pd.to_datetime(df_electricity['datetime'])
            df_weather = pd.read_csv(self.data_path + 'weather_2009_2023_formatted.csv')
            df_weather['datetime'] = pd.to_datetime(df_weather['datetime'])
            df_datetime = pd.read_csv(self.data_path + 'time_2009_2023.csv')
            df_datetime['datetime'] = pd.to_datetime(df_datetime['datetime'])
            return df_electricity, df_weather, df_datetime
        if set == 'no_missing':
            df_electricity = pd.read_csv(self.data_path + 'historic_demand_2009_2023_formatted_no_missing.csv')
            df_electricity['datetime'] = pd.to_datetime(df_electricity['datetime'])
            df_weather = pd.read_csv(self.data_path + 'weather_2009_2023_formatted.csv')
            df_weather['datetime'] = pd.to_datetime(df_weather['datetime'])
            df_datetime = pd.read_csv(self.data_path + 'time_2009_2023.csv')
            df_datetime['datetime'] = pd.to_datetime(df_datetime['datetime'])
            return df_electricity, df_weather, df_datetime
    
    def format_electricity_data(self):
        
        # Specify electricity file name
        filename = 'historic_demand_2009_2023.csv'
        formatted_filename = os.path.splitext(filename)[0] + '_formatted.csv' 
        if os.path.isfile(self.data_path + formatted_filename):
            return # Return if data is already under right format   
        # Verify existence of original data
        assert os.path.isfile(self.data_path + filename), 'Electricity demand file does not exist.'
        
        # Load electricity data into a pandas DataFrame
        df_energy = pd.read_csv(self.data_path + filename, index_col=0) # electricity demand

        print(df_energy.info())
        print(df_energy.head(50)) # View data from first 48 periods from 1st day and 2 periods from 2nd day
        print(df_energy.describe()) # Check variables ranges

        # Remove settlement periods over 48
        df_energy_periods_over_48 = df_energy.loc[df_energy['settlement_period'] > 48]
        print(f"Amount of periods over 48 by column: \n{df_energy_periods_over_48.count()}", )
        df_energy_periods_over_48.head()
        df_energy = df_energy.loc[~(df_energy['settlement_period'] > 48)]
        print(df_energy.info())

        # Add time to settlement date for visualization purposes
        time = DataLoader.convert_to_time_string(df_energy['settlement_period'])
        # time = hours.astype(str) + ':' + minutes.astype(str) # Create time
        # Add time
        df_energy['settlement_date'] = df_energy['settlement_date'].astype(str) + ' ' + time
        print(df_energy.head(5))

        # Check duplicates
        duplicates_check = df_energy['settlement_date'].duplicated()
        if any(duplicates_check):
            print('Duplicates found in dataset')
            df_energy.drop_duplicates()
        else:
            print('No duplicates found in dataset')
            
        # Convert the date column to datetime format
        df_energy['settlement_date']=pd.to_datetime(df_energy['settlement_date'])
        # Sorting the data to ensure time continuity
        df_energy.sort_values(by='settlement_date', ascending=True, inplace=True)
        
        # Fill missing time periods
        df_energy.set_index('settlement_date', inplace=True)
        df_energy = df_energy.asfreq('30T', method=None)
        df_energy.reset_index(inplace=True)
        
        # Fill missing 48 periods
        period = df_energy['settlement_period'].isna()
        max_period = df_energy['settlement_period'].max()
        for df_idx in df_energy.index[period]:
            if df_energy['settlement_period'].iloc[df_idx - 1] < max_period:
                df_energy['settlement_period'].iloc[df_idx] = df_energy['settlement_period'].iloc[df_idx - 1] + 1
            else:
                df_energy['settlement_period'].iloc[df_idx] = 1
        
        # Rename columns to match datetime name format (date -> datetime, date related -> date_)
        df_energy.rename(columns={'settlement_date': 'datetime',
                                  'settlement_period': 'date_period',
                                  'is_holiday': 'date_isholiday'}, inplace=True)
        
        # Create dataframe for time features
        df_datetime = pd.DataFrame(df_energy[['datetime', 'date_period', 'date_isholiday']])
        # Remove time features
        del df_energy['date_period']
        del df_energy['date_isholiday']

        print(df_energy.info()) # Display date format
        print(df_energy.head(2)) # Check datetime values after convertion
        
        df_energy.to_csv(self.data_path + formatted_filename, index=False)
        # Save time dataframe
        time_filename = 'time_2009_2023.csv'
        df_datetime.to_csv(self.data_path + time_filename, index=False)
    
    def format_weather_data(self):
        
        # Specify weather file name
        filename = 'weather_2009_2023.csv'
        formatted_filename = os.path.splitext(filename)[0] + '_formatted.csv' 
        if os.path.isfile(self.data_path + formatted_filename):
            return # Return if data is already under right format   
        # Verify existence of original data
        assert os.path.isfile(self.data_path + filename), 'Weather file does not exist.'
        
        # Load weather data into a pandas DataFrame
        df_weather = pd.read_csv(self.data_path + filename)
        df_weather['datetime'] = pd.to_datetime(df_weather['datetime'])
        df_weather.sort_values(by='datetime', ascending=True, inplace=True)
        
        # Resample weather data to fit with half-hour period
        selected_variables = ['tempmax', 'tempmin', 'temp', 'feelslikemax', 'feelslikemin', 'feelslike', 'humidity', 'windspeed']
        df_weather.set_index('datetime', inplace=True)
        df_weather = df_weather[selected_variables]
        df_weather = df_weather.resample('30T').ffill()
        df_weather.reset_index(inplace=True)
        
        # Save formatted weather data    
        df_weather.to_csv(self.data_path + formatted_filename, index=False)
        
    def extract_time_features(self):
        
        # Specify electricity file name
        time_filename = 'time_2009_2023.csv'
        # Verify existence of formatted data
        assert os.path.isfile(self.data_path + time_filename), 'Time file does not exist.'
        
        # Load time data into a pandas DataFrame
        df_datetime = pd.read_csv(self.data_path + time_filename)
        if len(df_datetime.columns) > 3:
            return # Return if features were extracted
        # Convert the date column to datetime format
        df_datetime['datetime'] = pd.to_datetime(df_datetime['datetime'])
        
        # Extract time features      
        df_datetime['date_year'] = df_datetime['datetime'].dt.year
        df_datetime['date_month'] = df_datetime['datetime'].dt.month
        df_datetime['date_day'] = df_datetime['datetime'].dt.day
        df_datetime['date_hour'] = df_datetime['datetime'].dt.hour
        df_datetime['date_minute'] = df_datetime['datetime'].dt.minute
        # df_datetime['date_period'] = df_datetime['datetime'].dt.strftime('%H:%M').str[:2].astype(int) * 2 + \
        #                              df_datetime['datetime'].dt.strftime('%M').astype(int) // 30 + 1
        df_datetime['date_dayofyear'] = df_datetime['datetime'].dt.dayofyear
        df_datetime['date_weekday'] = df_datetime['datetime'].dt.weekday
        df_datetime['date_quarter'] = df_datetime['datetime'].dt.quarter
        df_datetime['date_week'] = df_datetime['datetime'].dt.isocalendar().week
        df_datetime['date_isweekend'] = df_datetime['datetime'].apply(DataLoader.is_weekend)
        # df_datetime['date_isholiday'] = df_energy['is_holiday']
        df_datetime['date_daypart'] = df_datetime['datetime'].dt.hour.apply(DataLoader.get_part_of_day) # Part of the day
        
        for date in df_datetime.loc[df_datetime['date_isholiday'].isna(), 'datetime']:
            df_datetime.loc[df_datetime['datetime'] == date, 'date_isholiday'] = DataLoader.is_holiday(date)
        df_datetime['date_isholiday'] = df_datetime['date_isholiday'].astype(bool)
        
        df_datetime.to_csv(self.data_path + time_filename, index=False)
    
    def handle_missing_data(self, mode: Literal['fill', 'remove_day', 'remove_time']):
        
        # Specify electricity file name
        filename = 'historic_demand_2009_2023_formatted.csv'
        time_filename = 'time_2009_2023.csv'
        no_missing_filename = os.path.splitext(filename)[0] + '_no_missing.csv' 
        if os.path.isfile(self.data_path + no_missing_filename):
            return # Return if data is already processed   
        # Verify existence of formatted data
        assert os.path.isfile(self.data_path + filename), 'Electricity demand formatted file does not exist.'
        
        # Load electricity data into a pandas DataFrame
        df_energy = pd.read_csv(self.data_path + filename) # electricity demand
        
        if mode == 'fill':
            # Fill values 
            df_energy['nd'].ffill(inplace=True)
            df_energy.fillna(0, inplace=True)
            # Load time data into a pandas DataFrame
            assert os.path.isfile(self.data_path + time_filename), 'Time features file does not exist.'
            df_datetime = pd.read_csv(self.data_path + time_filename)
            assert len(df_datetime.columns) > 3, 'No time features extracted'
            # Convert the date column to datetime format
            df_energy['datetime'] = pd.to_datetime(df_energy['datetime'])
            df_datetime['datetime'] = pd.to_datetime(df_datetime['datetime'])
            df_energy_time = pd.merge(df_datetime, df_energy[['datetime', 'nd', 'tsd']], on='datetime', how='left')  
            # Missing values dataframe
            df_missing = df_energy.loc[(df_energy['tsd'] == 0)]
            df_energy_without_missing = df_energy.loc[df_energy['tsd'] > 0]
            if len(df_missing.index) > 0:
                df_energy_without_missing['nd_tsd_diff'] = df_energy_without_missing['tsd'] - df_energy_without_missing['nd']
                hierarchy_dates = ['date_year', 'date_month', 'date_weekday', 'date_period']
                hierarchy_filler = df_energy_without_missing.groupby(hierarchy_dates).mean()
                for missing_index in df_missing.index:
                    missing_value = df_energy.iloc[missing_index, :]
                    hierarchy_values = missing_value[hierarchy_dates]
                    fill_value = np.ceil(missing_value['nd'] + hierarchy_filler.loc[tuple(hierarchy_values), 'nd_tsd_diff']) # Overestimate demand
                    df_energy['tsd'].iloc[missing_index] = fill_value
                    
            # Save data
            # saved_variables = [name for name in df_energy.columns if ('date' in name) or ('nd' == name) or ('tsd' == name)]
            # df_energy = df_energy[saved_variables]
            # df_energy.to_csv(save_dir + os.path.splitext(os.path.split(path)[-1])[0] + '_no_missing.csv', index=False)
                    
            return
        if mode == 'remove_day':
            raise 'Not implemented'
        if mode == 'remove_time':
            df_energy.fillna(0, inplace=True)
            df_energy = df_energy.loc[~(df_energy['tsd'] == 0)]
        # Save dataframe with no missing values
        df_energy.to_csv(self.data_path + no_missing_filename, index=False)
    
    def save_data(self, filename: str, df_data: pd.DataFrame) -> None:
        df_data.to_csv(self.data_path + filename, index=False)
        
    #region Utilities
    
    def convert_to_time_string(time_period):
        # Calculate hours and minutes from the settlement period
        hours = (time_period - 1) // 2 # Get hours
        minutes = (time_period - 1) % 2 * 30 # Get minutes

        # Format the hours and minutes as a string
        hours_str = hours.map(lambda h:  "{:02d}".format(h))
        minutes_str = minutes.map(lambda m:  "{:02d}".format(m))
        time_string = hours_str + ":" + minutes_str + ":00"

        return time_string
    
    # Function to check if a given date is a weekend
    def is_weekend(date):
        return date.weekday() >= 5  # 5 and 6 represent Saturday and Sunday

    # Function to check if a given date is a holiday
    def is_holiday(date):
        # Create a Holiday object for the specific country or region
        # You can specify the country or region using the ISO 3166-1 alpha-2 country code
        # For example, 'US' for United States, 'GB' for United Kingdom, 'IN' for India, etc.
        holiday_obj = holidays.country_holidays('GB')
        return date in holiday_obj

    # Function to determine the part of the day
    def get_part_of_day(hour):
        if 5 <= hour < 12:
            return 'Morning'
        elif 12 <= hour < 17:
            return 'Afternoon'
        elif 17 <= hour < 21:
            return 'Evening'
        else:
            return 'Night'
    
    #endregion