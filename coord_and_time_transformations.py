"""
   ----------------------------------------------------------------------------
   Copyright (C) 2020 Francesco Darugna <fd@geopp.de>  Geo++ GmbH,
                      Jannes B. Wübbena <jw@geopp.de>  Geo++ GmbH.
   
   A list of all the historical RTCM-SSR Python Demonstrator contributors in
   CREDITS.info
   
   The first author has received funding from the European Union's Horizon 2020
   research and innovation programme under the Marie Sklodowska-Curie Grant
   Agreement No 722023.
   ----------------------------------------------------------------------------

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published
    by the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import numpy as np
import math
import rtcm_ssr2osr

def ell2cart(lat, long, height):
    """ Coordinates transformation using WGS84 ellipsoid definition
    
    Input: 
        - lat   : ellipsoidal latitude
        - lon   : ellipsoidal longitude
        - height: ellipsoidal height
    Output:
        - [x,y,z] vector of geocentric-cartesian coordinates
        
    Reference:
        - "Satellite Geodesy", Seeber 
    """

    h = height
    lat  = np.radians(lat)
    long = np.radians(long)

    a = rtcm_ssr2osr.Constants().WGS84_a
    f = rtcm_ssr2osr.Constants().WGS84_f
    
    N_bar = a / np.sqrt(1 - f * (2 - f) * (np.sin(lat)) ** 2)
    
    # Cartesian coordinates:
    
    x = (                 N_bar + h) * np.cos(lat) * np.cos(long)
    y = (                 N_bar + h) * np.cos(lat) * np.sin(long)
    z = (((1 - f) ** 2) * N_bar + h) * np.sin(lat)
    
    cart = np.array([x, y, z])
    
    return cart

def gpsTime2y_doy_hms(week, gpsTime):
    """ Function to convert GPS time to year, doy and hour minutes seconds
    """
    iepy = 1980
    iepd = 6
    
    # Hour of the day
    ss = math.fmod(gpsTime, rtcm_ssr2osr.Constants().day_seconds)
    hh = np.floor(ss / 3600)
    
    # Conversion to time of year 

    # Number of days since iepy
    ndy = week * 7 + np.floor((gpsTime - ss) / 
                              rtcm_ssr2osr.Constants().day_seconds +
                              0.5) + iepd - 1
    
    # Number of years since iepy
    ny = np.floor(ndy / 365.25)
    
    # Current year
    iy = np.floor(iepy + ny) 
    
    # Day of the year
    DOY = np.floor(ndy - ny * 365.25 + 1) 
    
    # Minutes
    ss = math.fmod(ss, 3600)
    mm = np.floor(ss / 60)
    
    # Seconds
    ss = math.fmod(ss, 60)
    
    return iy, DOY, hh, mm, ss

def gps_time_from_y_doy_hms(year, doy, hh, mm, sec):
    """
        Compute gps time from date as year, doy, hours, minutes, seconds
    """
    iepy = 1980
    iepd = 6
    if year<100:
        if year>80: 
            year += 1900 
        else: 
            year += 2000
            
    ndy = ((year-iepy) * 365 + doy - iepd + ((year - 1901) / 4) -
           ((iepy - 1901) / 4))
    
    week = (ndy / 7)
    time = (round((week - int(week))*7) *
            rtcm_ssr2osr.Constants().day_seconds + hh * 3600.0e0 +
            mm * 60.0e0 + sec)
    return int(week), time

def date_to_doy(year, mon, day):
    """
        Compute day of the year from year, month and day of the month
    """
    
    leap = 0
    if np.mod(year, 4) == 0:
        leap = 1
	
    doy = (mon - 1) * 30 + mon / 2 + day
    if mon > 2:
        doy =  doy - 2 + leap
    
    if (( mon > 8 )  & (np.mod(mon, 2)!= 0)):
        doy = doy + 1
    
    return int(doy)

def doy_to_date(year, doy):
    """
        Compute date as year, month, day of the month from year and day of year
    """
    mon = np.int(doy/30) + 1
    dom = -1
    while dom < 0:
        dom = doy - date_to_doy(year, mon, 0)
        mon -= 1
    mon += 1 
    if dom == 0:
        mon -=1
        if ((mon==11)|(mon==4)|(mon==6)|(mon==9)):
            dom = 30
        elif mon==2:
            if np.mod(year,4)==0:
                dom = 29
            else:
                dom=28
        else:
            dom=31
    return [year, mon, dom]

def glo_time2gps_time(glo_day, glo_time, glo_year, ls):

    # Moscow day -> UTC day 
    if glo_time >= 10800.0:
        utc_time = glo_time - 10800.0
    else:
        utc_time = glo_time - 10800.0 + rtcm_ssr2osr.Constants().day_seconds
        
    # compute gregorian date
    [day, mon, year] = glo_time2greg_day(glo_day, glo_year)
    
    # compute day of the year
    doy = date_to_doy(year, mon, day)
    
    # get gps week and time
    [gps_week, gps_time] = gps_time_from_y_doy_hms(year, doy, 0, 0, utc_time +
                                                   ls)
    return gps_week, gps_time

def glo_time2greg_day(nt, n4):
    """
        Compute Gregorian day from glonass time.
        Reference: GLONASS ICD
    """
   
    JD0 = 1461.0*(n4 - 1.0) + nt + 2450082.5 
    # julian date for the current date
    JDN = JD0 + 0.5
    
    a = JDN + 32044.0
    b = int((4.0 * a + 3.0) / 146097.0)
    c = a - int(146097.0 * b / 4.0)
    d = int((4 * c + 3.0) / 1461.0)
    e = c - int(1461.0 * d / 4)
    m = int((5 * e + 2.0) / 153.0) 
    
    day  = e - int((153.0 * m + 2.0) / 5) + 1
    mon  = m + 3.0 - 12.0 * int(m / 10)
    year = 100.0 * b + d - 4800.0 + int(m / 10)
    
    return day, mon, year

def get_ls_from_date(year, month):
    """
        Function to get leap seconds since 1999. After 31st of December 1998
        the leap seconds were 14. 
        The function covers the updates after that time.
    """
    if ((year > 2005) & (year < 2009)):
        ls = 14
    elif ((year >= 2009) & (year < 2012)):
        ls = 15
    elif year == 2012:
        if month < 7:
            ls = 15 
        else:
            ls = 16
    elif ((year > 2012) & (year < 2015)):
        ls = 16
    elif year == 2015:
        if month< 7:
            ls = 16
        else:
            ls = 17
    elif year == 2016:
        if month < 7:
            ls = 17
        else:
            ls = 18
    elif year > 2016:
        ls = 18
    else:
        ls = 14
        
    return ls