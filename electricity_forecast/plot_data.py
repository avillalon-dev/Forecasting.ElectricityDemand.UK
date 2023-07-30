import matplotlib.pyplot as plt
import plotly.graph_objects as go
import seaborn as sns
import pandas as pd
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
            ax = axes[i-2]
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