#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 09:20:08 2026

@author: lynnethissen
"""

#import
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as pp
import numpy as np
import xarray as xr
import glob



files = sorted(glob.glob("/Users/lynnethissen/Desktop/air_temp_daily_nc/*.grib2"))

ds = xr.open_dataset(
    "/Users/lynnethissen/Desktop/air_temp_daily_nc/fnl_20250921_12_00.grib2",
    engine="cfgrib",
    filter_by_keys={
        "typeOfLevel": "heightAboveGround",
        "level": 2
    }
)
print(ds)



# Select dates and convert Kelvin to Celsius
temp = ds['air'].sel(time=slice('2025-09-14', '2025-09-21')) - 273.15

# Mask temperatures below 0°C
temp = temp.where(temp >= 13)

vmin = temp.min().values
vmax = temp.max().values

for t in temp.time:
    daily = temp.sel(time=t)

    print(
        f"{t.dt.strftime('%Y-%m-%d').item()}: "
        f"Min = {daily.min().item():.2f} °C, "
        f"Max = {daily.max().item():.2f} °C"
    )
    
# figure
fig = pp.figure(figsize=(19,7))

gs = fig.add_gridspec(
    2, 5,
    width_ratios=[1,1,1,1,0.05],
    wspace=0.04,
    hspace=0.02
)

axes = [
    fig.add_subplot(gs[0,0], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,1], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,2], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[0,3], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,0], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,1], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,2], projection=ccrs.PlateCarree()),
    fig.add_subplot(gs[1,3], projection=ccrs.PlateCarree()),
]

# Colorbar axis
cax = fig.add_subplot(gs[:,4])

# plot
levels = np.arange(0, 40, 0.5)

for i, t in enumerate(temp.time):

    ax = axes[i]

    # Filled contours (instead of pcolormesh)
    cf = ax.contourf(
        ds["lon"],
        ds["lat"],
        temp.sel(time=t),
        levels=levels,
        cmap="coolwarm",
        extend="both",
        transform=ccrs.PlateCarree()
    )

    ax.set_extent([-90.0, -86.0, 40.5, 43])

    ax.add_feature(cfeature.STATES, linewidth=0.8)
    ax.add_feature(cfeature.BORDERS, linewidth=0.5)
    ax.add_feature(cfeature.LAKES, alpha=0.2)
    ax.coastlines(resolution="10m")

    ax.set_title(str(t.dt.strftime("%Y-%m-%d").values), fontsize=12)

# colorbar
cbar = fig.colorbar(cf, cax=cax)
cbar.set_label("Temperature (°C)", fontsize=12)

# title
fig.suptitle(
    "NARR Daily Mean Surface Temperature\nSeptember 14–21, 2025",
    fontsize=18
)

pp.savefig("2d_temperature_contours.png", dpi=300, bbox_inches="tight")
pp.show()