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

import do_rtcmssr_demo
import tkinter as tk

""" Test script to use the RTCM-SSR Python Demonstrator
    starting a GUI interface.
    Input:
    - path       : RTCM binary file path    
    - f_in       : RTCM binary file (e.g. "name.rtc", "name.bin")
    - lat        : user ellipsoidal latitude
    - lon        : user ellipsoidal longitude
    - height     : user ellipsoidal height
    - decoded_out: flag to request decoded msg in txt file output (0/1)
    - year       : year at the time of the message reception
    - doy        : day of the year (doy) at the time of the message reception
    - out_folder : desired folder for the output, if not provided, i.e.==None, 
                   the output folder will be 'path//RTCM_SSR_demo//' 
    
    Output:
    - name.ssr    : txt file of the decoded RTCM message
    - name.osr    : txt file with SSR influence on user location
    - name.ion    : txt file with computed ionospheric parameters,
                     e.g. pierce point
    - ephemeris   : decoded ephemeris 
    - ssr         : decoded RTCM-SSR
    - osr         : computed osr parameters 
"""
# =============================================================================
# Title & Logo
# =============================================================================
window = tk.Tk()
window.title('RTCM-SSR Python Demo')
window.geometry('710x250')
window.grid()
#Setting it up
img = tk.PhotoImage(file='geopp_logo.png')
#Displaying it
imglabel = tk.Label(window, image=img).grid(row=0, column=2,
                                            columnspan=2, rowspan=2,
                                            sticky='w', padx=5, pady=5)        

# =============================================================================
#                         Input and output entries
# =============================================================================
# Insert path to rtc file
first_row = tk.Frame()
first_row.grid(row=0, column=0, sticky='w')
lbl_path = tk.Label(first_row, text="Path to rtcm binary file:    ")
lbl_path.pack(side='left')
txt_path = tk.Entry(first_row, width=40)
txt_path.pack(side='left')
# Insert rtcm-ssr file name
second_row = tk.Frame()
second_row.grid(row=1, column=0, sticky='w')
lbl_file = tk.Label(second_row, text="File name:                          ")
lbl_file.pack(side='left')
txt_file = tk.Entry(second_row, width=20)
txt_file.pack(side='left')
# Insert output folder (optional)
third_row = tk.Frame()
third_row.grid(row=2, column=0, sticky='w', rowspan=2)
lbl_out = tk.Label(third_row, text="Output folder (optional):  ")
lbl_out.pack(side='left')
txt_out = tk.Entry(third_row, width=40)
txt_out.pack(side='left')
# set latitude of rover point
fourth_row = tk.Frame()
fourth_row.grid(row=4, column=0, sticky='w')
lbl_lat = tk.Label(fourth_row, text="Ellips. lat. [deg] ")
lbl_lat.pack(side='left')
txt_lat = tk.Entry(fourth_row, width=20)
txt_lat.pack(side='left')
# set longitude of rover point
fifth_row = tk.Frame()
fifth_row.grid(row=5, column=0, sticky='w')
lbl_lon = tk.Label(fifth_row, text="Ellips. lon. [deg]")
lbl_lon.pack(side='left')
txt_lon = tk.Entry(fifth_row, width=20)
txt_lon.pack(side='left')
# set height of rover point
sixth_row = tk.Frame()
sixth_row.grid(row=6, column=0, sticky='w')
lbl_hei = tk.Label(sixth_row, text="Ellips. hei. [m]    ")
lbl_hei.pack(side='left')
txt_hei = tk.Entry(sixth_row, width=20)
txt_hei.pack(side='left')
# set year and month for gps roll-over week and leap seconds
sixth_row = tk.Frame()
sixth_row.grid(row=7, column=0, sticky='w')
lbl_yr = tk.Label(sixth_row, text="Year:    ")
lbl_yr.pack(side='left')
txt_yr = tk.Entry(sixth_row, width=8)
txt_yr.pack(side='left')
lbl_doy = tk.Label(sixth_row, text="DOY:    ")
lbl_doy.pack(side='left')
txt_doy = tk.Entry(sixth_row, width=4)
txt_doy.pack(side='left')

# =============================================================================
# Read input class
# =============================================================================
class read_input():
    def __init__(self):
        if txt_path.get()[-1]=='\\':
            self.path  = txt_path.get()
        else:
            self.path = txt_path.get() + '\\'
        self.file  = txt_file.get()
        self.year  = int(txt_yr.get())
        self.doy   = int(txt_doy.get())

        if len(txt_lat.get()) == 0:
            lat = 52.5
            lon = 9.5
            hei = 100
        else:
            lat = float(txt_lat.get())
            lon = float(txt_lon.get())
            hei = float(txt_hei.get())
            
        self.rover_coord = [lat, lon, hei]
        
        out_folder       = txt_out.get()
        if len(out_folder) == 0:
            self.out_folder = None
        else:
            if out_folder[-1]=='\\':
                self.out_folder = out_folder
            else:
                self.out_folder = out_folder + '\\'
# =============================================================================
# Decode only
# =============================================================================
def decode_msg():
    inputs = read_input()
    decode_only = 1       
    [ephemeris,
     ssr] = do_rtcmssr_demo.do_rtcmssr_demo(inputs.path + inputs.file,
                                            inputs.rover_coord,
                                            decode_only,
                                            inputs.out_folder,
                                            inputs.year, inputs.doy)
    return [ephemeris, ssr]
# =============================================================================
# Compute SSR influence on rover position
# =============================================================================
def compute_osr():
    inputs = read_input()
    decode_only = 0      
    [ephemeris,
     ssr, osr] = do_rtcmssr_demo.do_rtcmssr_demo(inputs.path + inputs.file,
                                                 inputs.rover_coord,
                                                 decode_only,
                                                 inputs.out_folder,
                                                 inputs.year, inputs.doy)
    return [ephemeris, ssr, osr]

# =============================================================================
# Buttons
# =============================================================================
# Decode RTCM-SSR messages
btn_dec = tk.Button(window, text='Decode RTCM-SSR', command=decode_msg)
btn_dec.grid(row=4, column=1, sticky='w')
# Compute SSR2OSR
btn_osr = tk.Button(window, text='Compute SSR2OSR', command=compute_osr)
btn_osr.grid(row=6, column=1, sticky='w')

# =============================================================================
# 
# =============================================================================
window.mainloop()