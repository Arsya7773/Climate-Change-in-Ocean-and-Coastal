import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
import pandas as pd

# Load the dataset
file_path = 'Indonesia_sst_mon.nc'
ds = xr.open_dataset(file_path)

# Define the time slices for each decade and calculate the mean SST
time_slices = {
    "1984-1993": slice('1984-01-01', '1993-12-31'),
    "1994-2003": slice('1994-01-01', '2003-12-31'),
    "2004-2013": slice('2004-01-01', '2013-12-31'),
    "2014-2023": slice('2014-01-01', '2023-12-31'),
    "1984-2023": slice('1984-01-01', '2023-12-31')
}

# Calculate monthly SST time series
sst_monthly = ds['sst'].mean(dim=['lat', 'lon'])

# Identify outliers using z-scores
z_scores = (sst_monthly - sst_monthly.mean(dim='time')) / sst_monthly.std(dim='time')
outliers = np.abs(z_scores) > 3  # Define outliers as values with z-scores greater than 3

# Interpolate to replace outliers
sst_monthly_cleaned = sst_monthly.where(~outliers, drop=False)  # Keep non-outliers
sst_monthly_interpolated = sst_monthly_cleaned.interpolate_na(dim='time', method='linear')

# Plot the interpolated monthly SST time series
plt.figure(figsize=(12, 6))
sst_monthly_interpolated.plot(label='Interpolated Monthly SST', color='orange', linewidth=0.7)
plt.xticks(pd.date_range("1984-01-01", "2023-12-01", freq="YS"), rotation=45)
plt.title('Monthly SST Time Series (1984-2023) - Interpolated')
plt.xlabel('Time')
plt.ylabel('Sea Surface Temperature (°C)')
plt.legend()
plt.show()

# Now plot the annual SST with interpolated data
sst_annual_interpolated = sst_monthly_interpolated.resample(time='1Y').mean()  # Resample to annual data
plt.figure(figsize=(12, 6))
sst_annual_interpolated.plot(label='Interpolated Annual SST', color='purple', linewidth=1.5)
plt.xticks(pd.date_range("1984-01-01", "2023-12-01", freq="YS"), rotation=45)
plt.title('Annual SST Time Series (1984-2023) - Interpolated')
plt.xlabel('Time')
plt.ylabel('Sea Surface Temperature (°C)')
plt.legend()
plt.show()
