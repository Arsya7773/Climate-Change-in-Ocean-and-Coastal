import xarray as xr
import matplotlib.pyplot as plt

# Load the dataset
file_path = 'Indonesia_sst_mon.nc'
ds = xr.open_dataset(file_path)

# Adjust the time slice in case of slight misalignment with actual data
sst_2004_2013 = ds['sst'].sel(
    time=slice('2004-01-01', '2013-12-31'), 
    lat=slice(-11, -8),  # Slicing from higher to lower latitude
    lon=slice(119, 126)
).mean(dim='time', skipna=True)

sst_indonesia = ds['sst'].sel(
    time=slice('2004-01-01', '2013-12-31')
).mean(dim='time', skipna=True)

# Create a figure with two rows and one column
fig, axes = plt.subplots(2, 1, figsize=(8, 8))

# Plot the first map with latitude and longitude slicing
im1 = sst_indonesia.plot(ax=axes[0], cmap='coolwarm', vmin=25, vmax=30)
axes[0].set_title('Average SST for 2004-2013 (Whole Indonesia)')
axes[0].set_xlabel('Longitude')
axes[0].set_ylabel('Latitude')

# Plot the second map with latitude and longitude slicing
im2 = sst_2004_2013.plot(ax=axes[1], cmap='coolwarm', vmin=25, vmax=30)
axes[1].set_title('Average SST for 2004-2013 (Kepulauan Sunda Kecil)')
axes[1].set_xlabel('Longitude')
axes[1].set_ylabel('Latitude')

# Adjust layout
plt.tight_layout()
plt.show()