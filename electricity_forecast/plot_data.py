import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime

def plot_variables(data: pd.DataFrame, features: list, start_date: datetime, end_date: datetime):
    idx = (data['datetime'] >= start_date) & (data['datetime'] <= end_date)
    # Plotting all variables in dataframe
    
    # Create subplots
    fig, axes = plt.subplots(nrows=len(features), ncols=1, figsize=(10, 2*len(features)))

    # Iterate over each column (excluding the 'date' column)
    for i, column in enumerate(features):
        if 'date' not in column:
            # Set the current subplot
            ax = axes[i]
            # Plot the variable against the date
            ax.scatter(data.loc[idx, 'datetime'], data.loc[idx, column], marker='o')
            # Set the title and labels for each subplot
            # ax.set_title(column)
            ax.set_xlabel('Timestamp')
            ax.set_ylabel(column)
    # Adjust the spacing between subplots
    plt.tight_layout()
    # Show the plot
    plt.show()

def static_chart(data: pd.DataFrame, start_date: datetime, end_date: datetime):
    idx = (data['datetime'] >= start_date) & (data['datetime'] <= end_date)
    # Plotting the electricity demand
    plt.figure(figsize=(10, 6))
    plt.scatter(data.loc[idx, 'datetime'], data.loc[idx, 'tsd'], marker='o')
    plt.xlabel('Timestamp')
    plt.ylabel('Demand (MW)')
    plt.title('Electricity Demand')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.show()
    
def interactive_chart(data: pd.DataFrame, start_date: datetime, end_date: datetime):
    # Create a trace for the seasonal data
    trace = go.Scatter(
        x=data['datetime'],  # x-axis values (e.g., months, days, etc.)
        y=data['tsd'],  # y-axis values (seasonal data)
        mode='lines+markers',  # plot as a line with markers 'lines+markers'
        name='Seasonal Data'  # name of the trace
    )

    # Create the layout for the plot
    layout = go.Layout(
        title='Seasonal Data Plot',  # title of the plot
        xaxis=dict(
            title='Time',  # x-axis label
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label='1d', step='day', stepmode='backward'),
                    dict(count=7, label='1w', step='day', stepmode='backward'),
                    dict(count=1, label='1m', step='month', stepmode='backward'),
                    dict(count=4, label='4m', step='month', stepmode='backward'),
                    dict(count=1, label='YTD', step='year', stepmode='todate'),
                    dict(count=1, label='1y', step='year', stepmode='backward'),
                    dict(step='all')
                ])
            ),
            rangeslider=dict(visible=True),  # add a lower bar for panning and zooming
            type='date'  # set the x-axis type to 'date'
        ),
        yaxis=dict(title='Seasonal Value')  # y-axis label
    )

    # Create the figure and add the trace and layout
    fig = go.Figure(data=[trace], layout=layout)

    # Show the plot
    fig.show()
    
def distribution_plot(data: pd.DataFrame):
    
    plt.figure(figsize=(10, 6))
    sns.histplot(data=data, x="tsd", bins=500, color="b")
    sns.kdeplot()
    plt.xlabel('Demand (MW)')
    plt.title('Electricity Demand distribution')
    plt.show()
    
def plot_seasonal_day_week(data: pd.DataFrame):
    # Plot day and week features
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_minute', y='tsd')
    plt.xlabel('Minutes')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_hour', y='tsd')
    plt.xlabel('Hours')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_period', y='tsd', hue='date_isholiday')
    plt.xlabel('Half-hour Period')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_period', y='tsd', hue='date_isweekend')
    plt.xlabel('Half-hour Period')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_daypart', y='tsd', hue='date_isholiday')
    plt.xlabel('Day parts')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_daypart', y='tsd', hue='date_isweekend')
    plt.xlabel('Day parts')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_weekday', y='tsd', hue='date_isweekend')
    plt.xticks(ticks=np.sort(data['date_weekday'].unique()), labels=["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    plt.xlabel('Days of the week')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_isweekend', y='tsd', hue='date_isholiday')
    plt.xlabel('Is Weekend')
    plt.ylabel('Demand (MW)')
    
def plot_seasonal_month_year(data: pd.DataFrame):
    # Plot month and year features
    # day_holiday_mean = data[['date_dayofyear', 'date_isholiday', 'tsd']] \
    #                     .groupby(['date_dayofyear', 'date_isholiday']) \
    #                     .mean()
    # day_holiday_mean.reset_index()
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_day', y='tsd', hue='date_isweekend')
    plt.xlabel('Days of the month')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_dayofyear', y='tsd')
    # plt.plot(day_holiday_mean['date_dayofyear'], day_holiday_mean['tsd'])
    plt.xlabel('Day of year')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_week', y='tsd')
    plt.xlabel('Week of year')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_month', y='tsd', hue='date_isweekend')
    plt.xlabel('Month')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_month', y='tsd', hue='date_isholiday')
    plt.xlabel('Month')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_quarter', y='tsd')
    plt.xlabel('Quarter')
    plt.ylabel('Demand (MW)')
    plt.figure(figsize=(15,5))
    sns.boxplot(data, x='date_year', y='tsd')
    plt.xlabel('Year')
    plt.ylabel('Demand (MW)')
    
def plot_features_demand(data: pd.DataFrame, features: list):    
    # Create subplots
    fig, axes = plt.subplots(nrows=len(features), ncols=1, figsize=(10, 2*len(features)))

    # Iterate over each column (excluding the 'date' column)
    for i, column in enumerate(features):
        # Set the current subplot
        ax = axes[i]
        # Plot the feature against the demand
        ax.scatter(data[column], data['tsd'], marker='o')
        # Set the title and labels for each subplot
        # ax.set_title(column)
        ax.set_xlabel(column)
        ax.set_ylabel('Demand (MW)')
    # Adjust the spacing between subplots
    plt.tight_layout()
    # Show the plot
    plt.show()
    
def plot_timeseries_split(data: pd.DataFrame, ts_splitter, threshold_date):
    fig, axes = plt.subplots(5, 1, figsize=(15, 15), sharex=True)
    df_cv = data.copy()
    df_cv.set_index('datetime', inplace=True)
    fold = 0
    for train_index, test_index in ts_splitter.split(df_cv[df_cv.index < threshold_date]):
        train = df_cv.iloc[train_index]
        test = df_cv.iloc[test_index]

        train["tsd"].plot(
            ax=axes[fold], label="Training set", title=f"Data Train-test split fold {fold}",
        )
        test["tsd"].plot(ax=axes[fold], label="Test set")
        axes[fold].axvline(test.index.min(), color="k", ls="--")
        axes[fold].legend(loc="center", bbox_to_anchor=(1.075, 0.5))

        axes[fold].set_title("Prediction on test set - week")
        axes[fold].set_ylabel("Energy Demand (MW)")
        axes[fold].set_xlabel("Timestamp")
        fold += 1
    plt.show()