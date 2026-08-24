# plots
# to mimic nasa plots from their field campaign, make separate directories for each site, this is just the template
# imports
import pandas as pd 
from datetime import datetime
import matplotlib.pyplot as pp
import numpy as np
import netCDF4 as nc
from netCDF4 import num2date


#data import section
file_name1 = 'crocus-NEIU-aqt-a1_20230516_000000.nc'
fn1 = nc.Dataset(file_name1)
file_name2 = 'crocus-NEIU-wxt-a1_20230505_000000.nc'
fn2 = nc.Dataset(file_name2)

o3 = fn1.variables['o3'][:] * 10000
no2 = fn1.variables['no2'][:] * 10000

print(fn1.variables['time'])
print(fn1.variables['time'].units)

#fix time variables
time_values = fn1.variables['time'][:]
base_time = pd.Timestamp("2023-05-16 21:30:56.652365463")
dates = base_time + pd.to_timedelta(time_values, unit='ns')

time2 = fn2.variables['time'][:]
base_time2 = pd.Timestamp("2023-05-05 00:00:00")  # adjust if needed
dates2 = base_time2 + pd.to_timedelta(time2, unit='ns')

# graph (6 plots, 3 rows 2 columns)
fig = pp.figure(figsize=(10,10))
fig, axs = pp.subplots(3, 2, figsize=(14, 14))
fig.suptitle('Crocus Sensor Data\n5/16/2023', fontweight='bold', fontsize=30)


#ozone ppb
ax1 = axs[0, 0]
ax1.set_xlabel('Time', fontweight='bold', fontsize=12)
ax1.set_ylabel('Ozone (ppb)', fontweight='bold', fontsize=12)
ax1.plot(dates, o3 , label='Ozone (ppb)', color='green')
ax1.set_ylim(-30,120)
ax1.legend()
#NO2 ppb
ax2 = axs[0, 1]
ax2.set_xlabel('Time', fontweight='bold', fontsize=12)
ax2.set_ylabel('NO2 (ppb)', fontweight='bold', fontsize=12)
ax2.plot(dates, no2, label='NO2 (ppb)', color='orange')
ax2.set_ylim(-30, 120)
ax2.legend()
#PM2.5 ug/m3
ax3 = axs[1, 0]
ax3.set_xlabel('Time', fontweight='bold', fontsize=12)
ax3.set_ylabel('PM2.5 (ug/m3)', fontweight='bold', fontsize=12)
ax3.plot(dates, fn1.variables['pm2.5'][:], label='PM2.5 (ug/m3)', color='blue')
ax3.set_ylim(0,10)
ax3.legend()
#VOC ohms
ax4 = axs[1, 1]
ax4.set_xlabel('Time', fontweight='bold', fontsize=12)
ax4.set_ylabel('Humidity (%)', fontweight='bold', fontsize=12)
ax4.plot(dates, fn1.variables['humidity'][:], label='Humidity (%)', color='purple')
ax4.set_ylim(0,100)
ax4.legend()
#temp vs humidity
ax5 = axs[2, 0]
ax5.set_xlabel('Time', fontweight='bold', fontsize=12)
ax5.set_ylabel('Temperature (C)', fontweight='bold', fontsize=12)
ax5.plot(dates, fn1.variables['temperature'][:], label='Temperature (C)', color='red')
ax5.set_ylim(0,40)
ax5.legend()
#pressure
ax6 = axs[2, 1]
ax6.set_xlabel('Time', fontweight='bold', fontsize=12)
ax6.set_ylabel('Pressure (hPa)', fontweight='bold', fontsize=12)
ax6.plot(dates, fn1.variables['pressure'][:], label='Pressure (hPa)', color='pink')
ax6.set_ylim(985,990)
ax6.legend()

#save fig
pp.savefig("Thissen_plots.png")
pp.show()
pp.close()