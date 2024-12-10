import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from scipy.stats import linregress

def create_vo2max_plot(ax, data):
    dates = np.array(data['Start Time']).astype(np.datetime64)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_format = mdates.DateFormatter('%Y')

    # formatting the X axis ticks
    ax.set_title('V02 Max Trends Over Time')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_format)
    ax.xaxis.set_minor_locator(months)

    ax.plot(dates, data['VO2max'], label='VO2max')
    ax.legend(loc='best')

def create_hr_running_races_plot(ax, data):
    dates = np.array(data['Start Time']).astype(np.datetime64)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_format = mdates.DateFormatter('%Y')

    # formatting the X axis ticks
    ax.set_title('Heart Rate Trends Over Time In Running Races')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_format)
    ax.xaxis.set_minor_locator(months)

    # Plot average and max heart rate
    ax.plot(dates, data['Average Heart Rate (bpm)'], linestyle='-')
    ax.plot(dates, data['Max. Heart Rate (bpm)'], linestyle='-')

    # Calculate regression for average heart rate
    avg_hr_slope, avg_hr_intercept, _, _, _ = linregress(
        np.arange(len(dates)), data['Average Heart Rate (bpm)']
    )
    # Regression line for average heart rate
    ax.plot(dates, avg_hr_slope * np.arange(len(dates)) + avg_hr_intercept,
            label='Avg HR', linestyle='-.')

    # Calculate regression for max heart rate
    max_hr_slope, max_hr_intercept, _, _, _ = linregress(
        np.arange(len(dates)), data['Max. Heart Rate (bpm)']
    )
    # Regression line for max heart rate
    ax.plot(dates, max_hr_slope * np.arange(len(dates)) + max_hr_intercept,
            label='Max HR', linestyle='-.')

    # Show legend and plot
    ax.legend(loc='best')
    ax.set_xlabel('Time')
    ax.set_ylabel('Heart Rate (bpm)')

def create_hr_plot(ax, data):
    dates = np.array(data['Start Time']).astype(np.datetime64)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_format = mdates.DateFormatter('%Y')

    # formatting the X axis ticks
    ax.set_title('Heart Rate Trends Over Time In All Activities')
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_format)
    ax.xaxis.set_minor_locator(months)

    # Plot average and max heart rate
    ax.plot(dates, data['Average Heart Rate (bpm)'], linestyle='-')
    ax.plot(dates, data['Max. Heart Rate (bpm)'], linestyle='-')

    # Calculate regression for average heart rate
    avg_hr_slope, avg_hr_intercept, _, _, _ = linregress(
        np.arange(len(dates)), data['Average Heart Rate (bpm)']
    )
    # Regression line for average heart rate
    ax.plot(dates, avg_hr_slope * np.arange(len(dates)) + avg_hr_intercept,
            label='Avg HR', linestyle='-.')

    # Calculate regression for max heart rate
    max_hr_slope, max_hr_intercept, _, _, _ = linregress(
        np.arange(len(dates)), data['Max. Heart Rate (bpm)']
    )
    # Regression line for max heart rate
    ax.plot(dates, max_hr_slope * np.arange(len(dates)) + max_hr_intercept,
            label='Max HR', linestyle='-.')

    # Show legend and plot
    ax.legend(loc='best')
    ax.set_xlabel('Time')
    ax.set_ylabel('Heart Rate (bpm)')

def create_hr_plot_weekly(ax, data, title='Heart Rate Trends Over Time In All Activities'):
    data['Start Time'] = pd.to_datetime(data['Start Time'], utc=True)
    data.set_index('Start Time', inplace=True) # Set 'Start Time' as the index for resampling

    # Resample the data by week and calculate the mean
    weekly_avg_hr = data['Average Heart Rate (bpm)'].resample('W').mean()
    weekly_max_hr = data['Max. Heart Rate (bpm)'].resample('W').mean()
    weekly_avg_hr = weekly_avg_hr.dropna()
    weekly_max_hr = weekly_max_hr.dropna()

    # Reset the index so 'Start Time' is a column again
    weekly_avg_hr = weekly_avg_hr.reset_index()
    weekly_max_hr = weekly_max_hr.reset_index()

    dates = np.array(weekly_avg_hr['Start Time']).astype(np.datetime64)
    years = mdates.YearLocator()
    months = mdates.MonthLocator()
    years_format = mdates.DateFormatter('%Y')

    # Calculate regression using the resampled data
    avg_hr_slope, avg_hr_intercept, _, _, _ = linregress(
        np.arange(len(weekly_avg_hr)), weekly_avg_hr['Average Heart Rate (bpm)']
    )
    max_hr_slope, max_hr_intercept, _, _, _ = linregress(
        np.arange(len(weekly_max_hr)), weekly_max_hr['Max. Heart Rate (bpm)']
    )

    # Plotting
    ax.set_title(title)
    ax.xaxis.set_major_locator(years)
    ax.xaxis.set_major_formatter(years_format)
    ax.xaxis.set_minor_locator(months)

    # Plot the resampled average and max heart rate data
    ax.plot(dates, weekly_avg_hr['Average Heart Rate (bpm)'], linestyle='-', label='Avg HR')
    ax.plot(dates, weekly_max_hr['Max. Heart Rate (bpm)'], linestyle='-', label='Max HR')

    # Plot the regression lines based on the resampled data
    ax.plot(dates, avg_hr_slope * np.arange(len(dates)) + avg_hr_intercept,
            linestyle='-.', label='Avg HR Trend')
    ax.plot(dates, max_hr_slope * np.arange(len(dates)) + max_hr_intercept,
            linestyle='-.', label='Max HR Trend')

    # Show legend and plot
    ax.legend(loc='best')
    ax.set_xlabel('Time')
    ax.set_ylabel('Heart Rate (bpm)')