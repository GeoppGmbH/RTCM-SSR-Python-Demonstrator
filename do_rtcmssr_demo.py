"""
   ----------------------------------------------------------------------------
   Copyright (C) 2020 Francesco Darugna <fd@geopp.de>  Geo++ GmbH,
                      Jannes B. Wübbena <jw@geopp.de>  Geo++ GmbH.
   
   A list of all the historical RTCM-SSR Python Demonstrator contributors in
   CREDITS.info.
   
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

import bitstruct
import rtcm_decoder
import crcmod
import numpy as np
import coord_and_time_transformations as trafo
import rtcm_ssr2osr
import sort_messages
from datetime import date
import os, errno
import pathlib

""" Decoding of RTCM 3 message and computing influence from SSR components on 
    user position.

    Input:
    - f_in        : complete path of the RTCM-SSR binary file
    - user_llh    : ellipsoidal coordinates of the user position, 
                    lat[deg], lon[deg], height [m] considering WGS84
    - dec_only    : if 1, the demo works as decoder, i.e. the SSR influence on
                    rover position is not performed, but the decoding of 
                    RTCM-SSR messages
    - out_folder  : desired folder for the output, if not provided, i.e.==None, 
                   the output folder will be 'path//RTCM_SSR_demo//' 
    - year        : year at the time of the message reception
    - doy         : day of the year at the time of the message reception
                   
    Output:   
    - print decoded rtcm-ssr messages 
    - print influence from SSR components on user position
    - print ionosphere debug output with information about pierce point and
      Legendre polynomials
    
    ***************************************************************************
    Description:
    decoding the message is performed by finding the RTCM preamble in the byte 
    stream. Then the message length is decoded and the CRC sum check is
    computed (Ref. Numerical Recipes, Press, W. H. et al., 3rd edition,
    cap. 22.4).
    After verification of the CRC the complete message passes to 
    the rtcm_decoder class for decoding.
    
    After decoding the messages the function sort_messages is called to create
    classes of ephemeris and ssr parameters objects.
    
    The computation of the SSR influence on the user location is computed per
    epoch, GNSS system and satellite. After selecting the epoch,
    GNSS, and satellite, the ssr parameters and ephemeris pass to the
    rtcm_ssr2osr class for computing osr parameters.  
    
"""

def do_rtcmssr_demo(f_in, user_llh, dec_only=None, out_folder=None,
                    year=None, doy=None):
# =============================================================================
# get the year, month and compute leap seconds
# =============================================================================
    if year is None:
        year = date.today().year
    else:
        year = year
    if doy is None:
        month = date.today().month
        dom   = date.today().day
        [year, doy] = trafo.date_to_doy(year, month, dom)
    else:
        doy = doy
        [year, month, dom] = trafo.doy_to_date(year, doy)
    # compute leap seconds.
    # This quantity will be considered for GLONASS w.r.t. GPS time
    ls_glo = trafo.get_ls_from_date(year, month)
    
# =============================================================================
#  open output files   
# =============================================================================
    if out_folder is None:
        out_folder = os.getcwd() + os.path.sep + 'RTCM_SSR_demo' + os.path.sep
    else:
        out_folder = out_folder
    try:    
        os.makedirs(out_folder)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    if dec_only == 1:
        dec_out = open(out_folder + os.path.basename(f_in) + '.ssr', 'w')
    else:
        osr_output = open(out_folder + os.path.basename(f_in) + '.osr', 'w')
        iono_output = open(out_folder + os.path.basename(f_in) + '.ion', 'w')
        dec_out = open(out_folder + os.path.basename(f_in) + '.ssr', 'w')
        
# =============================================================================
#   Input data    
# =============================================================================
    receiver = {}
    
    user_xyz = trafo.ell2cart(user_llh[0], user_llh[1], user_llh[2])
    receiver['ellipsoidal'] = np.array(user_llh)
    receiver['cartesian'  ] = np.array(user_xyz)
    
    with open(f_in, 'rb') as f:
        data = f.read()

# =============================================================================
#                        Loop over the whole message  
# =============================================================================
    # Description of the preamble 
    preamble = b'\xd3'
    i = 0
    
    # initialization of ephemeris and ssr variables
    eph0 = None
    ssr0 = None
    types_list = [] # list of the message types contained in the rtcm file
    while i <= len(data):
        if data[i:i + 1] == preamble:
            frame_header    = data[i:i + 3]
            # Getting RTCM header consisting of preamble (8 bit),
            # reserved bits (6 bit) and messange length (10) bit
            try:
                frame_header_unpack = bitstruct.unpack('u8u6u10', frame_header)
            except ValueError:
                print('Found not completed message.')
                i = i + 1
                continue
            msg_len   = frame_header_unpack[2]
            
            # check CRC for the completeness of the message
            msg_complete = data[i : i + 6 + msg_len]
            # create the function for CRC-24Q
            crc_fun = crcmod.crcmod.mkCrcFun(0x1864CFB,rev=False,
                                             initCrc=0x000000, xorOut=0x000000)
            # compute crc value for the complete msg, if correctly received,
            #  it should be 0
            crc_value = crc_fun(msg_complete)
            if crc_value == 0:
                msg_content   = data[i + 3:i + 3 + msg_len]
                # decode message
                read_msg = rtcm_decoder.rtcm_decoder(msg_content, msg_len,
                                                     year, doy)
                # extract the message
                msg_type = read_msg.msg_type
                
                if dec_only is not None:
                    try:
                        print(read_msg, file = dec_out)
                    except TypeError:
                        # in this case an unkwonn message has been considered
                        print('Be aware: received possible unknown message.')
                dec_msg = read_msg.dec_msg
# =============================================================================
#                              Sort messages
# =============================================================================                
                if dec_msg is not None: # this might happen for 
                                        # unknown message number,
                                        # e.g. not considered by the demo
                    types_list = np.append(types_list, msg_type)
                    # collect ephemeris data
                    ephemeris = sort_messages.sort_msg(msg_type, dec_msg,
                                                       eph=eph0)[0]
                    eph0 = ephemeris
                    # get the GLONASS four-year interval number 
                    # starting from 1996
                    try:
                        n4_list = []
                        # get number of week day from eph
                        if np.size(eph0.glo.sat) != 0:
                            eph_sat_list = eph0.glo.sat
                            eph_epochs = eph0.glo.sat_epochs
                            for sv in eph_sat_list:
                                for e in range(len(eph_epochs[sv])):
                                    n4_list = np.append(n4_list,
                                                        eph0.glo.eph[sv][e].n4)
                            # n4 might be 0 even in this case, when
                            # the GLONASS additional data are not reliable
                            if len(n4_list[np.where(n4_list!=0)[0]])==0:
                                n4 = 0
                            elif np.isnan(np.nanmean(n4_list[np.where(n4_list!=0)[0]])) == True:
                                n4=0
                            else:
                                n4 = np.nanmean(n4_list[np.where(n4_list!=0)[0]])
                        else:
                            n4 = 0
                        if ((n4 == 0) | (np.size(eph0.glo.sat) == 0)):
                            
                            if np.size(eph0.gps.sat) != 0:
                                eph_sat_list = eph0.gps.sat
                                eph_epochs = eph0.gps.sat_epochs
                                eph_ref = eph0.gps
                            else:
                                if np.size(eph0.gal.sat) != 0:
                                    eph_sat_list = eph0.gal.sat
                                    eph_epochs = eph0.gal.sat_epochs
                                    eph_ref = eph0.gal
                                else:
                                    if np.size(eph0.bds.sat) != 0:
                                        eph_sat_list = eph0.bds.sat
                                        eph_epochs = eph0.bds.sat_epochs
                                        eph_ref = eph0.bds

                            gps_time = []
                            gps_week = []
                            for sv in eph_sat_list:
                                for e in range(len(eph_epochs[sv])):
                                    gps_time = np.append(gps_time,
                                                         eph_epochs[sv][e])
                                    gps_week = np.append(gps_week, 
                                                         eph_ref.eph[sv][e].week)
                            time = np.nanmean(gps_time)
                            week = np.nanmean(gps_week)
                            [year, doy,
                             hh, mm,
                             ss] = trafo.gpsTime2y_doy_hms(week, time)
                            n4 = int((year - 1995) / 4)
                                            # collect rtcm ssr data
                        try:
                            state_space = sort_messages.sort_msg(msg_type,
                                                                 dec_msg,
                                                                 eph=eph0,
                                                                 ssr=ssr0,
                                                                 n4=n4,
                                                                 ls=ls_glo)[1]
                        except IndexError:
                            print('Warning: probably ephemeris are missing' + 
                                  ' for some satellites, please check the ' + 
                                  'ephemeris source.')
                            i = i + msg_len + 6
                            continue
                    except UnboundLocalError:
                        state_space = sort_messages.sort_msg(msg_type, dec_msg,
                                                             eph=eph0,
                                                             ssr=ssr0,
                                                             ls=ls_glo)[1]
                
                    ssr0 = state_space     
                i = i + msg_len + 6
            else:
                i = i + 1
        else:
            i = i + 1
    
    dec_out.close() 
    print('### Decoded RTCM-SSR message types:' + '\n' +
          str(np.unique(types_list).astype('int')) + ' ###')
    if dec_only == 1:
        return eph0, ssr0
    else:
        print('### Starting computing SSR influence on rover location.')
# =============================================================================
#                            Print output
# =============================================================================
    # check if there are ephemeris
    if ((np.size(ephemeris.gps.sat) == 0) & (np.size(ephemeris.glo.sat) == 0) & 
        (np.size(ephemeris.gal.sat) == 0) & (np.size(ephemeris.bds.sat) == 0) &
        (np.size(ephemeris.qzs.sat) == 0)):
        print('No available ephemeris --> no influence of SSR parameters' +
              ' is computed, return decoded RTCM-SSR messages.')
        return [], ssr0, []
    elif np.size(ssr0.epochs) == 0:
        print('No received RTCM-SSR corrections --> no influence of SSR' +
              ' parameters is computed, return decoded ephemeris.')
        return eph0, [], []
        
    osr = []
    for epoch in sorted(ssr0.epochs):
        j = int(np.where(ssr0.epochs == epoch)[0])
        # print epoch header
        lat    = receiver['ellipsoidal'][0]
        lon    = receiver['ellipsoidal'][1]
        height = receiver['ellipsoidal'][2]                    
        print('#****************************************' +
              '*****************************************' + 
              '************************************ ' + '\n' + 
              '# Influence from SSR components on LLH position:' +
              ' lat: ' + 
              f'{lat}' + '  lon: ' + f'{lon}' + '  height: ' + 
              f'{height}' + '.' + '\n' +
              '# Satellite elevation is output in [deg], while all the other' +
              ' parameters are in [m].' + '\n' + 
              '# Frequencies used for wup, ' + 
              'iono impact, code and phase bias are L1, G1, E1, B1-2,'+ '\n' + 
              '# respectively for ' + 
              'GPS/QZSS(1C), GLONASS(1C), Galileo(1X) and Beidou(2I).' + '\n' + 
              '# Eph. week       time       SV       elev     sv_clk ' + 
              '   sv_orb     iono_gl    shapiro      wup      phbias' +
              '      cbias' + '\n' + 
              '# ---------------------------------------' + 
              '-----------------------------------------' + 
              '------------------------------------ ',
              file = osr_output)
        for system in eph0.systems:
            # check if any satellite of the GNSS system  considered received
            # any correction for the current epoch
            if system == 'G':               
                if (not ssr0.gps[j].orb and not ssr0.gps[j].clck and 
                    not ssr0.gps[j].orb_clck and not ssr0.gps[j].cbias and
                    not ssr0.gps[j].pbias):
                    continue
                else:
                    ssr = ssr0.gps[j]
            elif system == 'R':               
                if (not ssr0.glo[j].orb and not ssr0.glo[j].clck and 
                    not ssr0.glo[j].orb_clck and not ssr0.glo[j].cbias and
                    not ssr0.glo[j].pbias):
                    continue
                else:
                    ssr = ssr0.glo[j]
            if system == 'E':               
                if (not ssr0.gal[j].orb and not ssr0.gal[j].clck and 
                    not ssr0.gal[j].orb_clck and not ssr0.gal[j].cbias and
                    not ssr0.gal[j].pbias):
                    continue
                else:
                    ssr = ssr0.gal[j]
            if system == 'C':               
                if (not ssr0.bds[j].orb and not ssr0.bds[j].clck and 
                    not ssr0.bds[j].orb_clck and not ssr0.bds[j].cbias and
                    not ssr0.bds[j].pbias):
                    continue
                else:
                    ssr = ssr0.bds[j]
            
            if system == 'J':               
                if (not ssr0.qzs[j].orb and not ssr0.qzs[j].clck and 
                    not ssr0.qzs[j].orb_clck and not ssr0.qzs[j].cbias and
                    not ssr0.qzs[j].pbias):
                    continue
                else:
                    ssr = ssr0.qzs[j]
            
            if not ssr.orb:
                if not ssr.clck:
                    if not ssr.orb_clck:
                        if not ssr.cbias:
                            if not ssr.pbias:
                                continue
                            else:
                                sat_list = ssr.pbias.gnss_id
                                gnss_short = ssr.pbias.gnss_short
                        else:
                             sat_list = ssr.cbias.gnss_id
                             gnss_short = ssr.cbias.gnss_short
                    else:
                        sat_list = ssr.orb_clck.gnss_id
                        gnss_short = ssr.orb_clck.gnss_short
                else:
                    sat_list = ssr.clck.gnss_id
                    gnss_short = ssr.clck.gnss_short
            else:
                sat_list = ssr.orb.gnss_id
                gnss_short = ssr.clck.gnss_short
            
            # sat counter
            for sv in sorted(sat_list):
                ID = gnss_short + sv
                # get for the closest ephemeris for that satellite if available
                try:
                    if system == 'G':
                        ephemeris = eph0.get_closest_epo(epoch,
                                                         eph0.gps, ID)[0]
                    elif system == 'R':
                        ephemeris = eph0.get_closest_epo(epoch,
                                                         eph0.glo, ID)[0]
                    elif system == 'E':
                        ephemeris = eph0.get_closest_epo(epoch,
                                                         eph0.gal, ID)[0]
                    elif system == 'C':
                        ephemeris = eph0.get_closest_epo(epoch,
                                                         eph0.bds, ID)[0]
                    elif system == 'J':
                        ephemeris = eph0.get_closest_epo(epoch,
                                                         eph0.qzs, ID)[0]
                except:
                    print('No ephemeris available for satellite ' + ID)
                    continue

                # get the closest in time ionosphere corrections if available
                try:
                    ionosphere = ssr0.get_closest_iono(ssr0, epoch)
                except:
                    print('No ionosphere corrections available for epoch ' +
                          str(epoch))
                    ionosphere = []
                
                if system == 'R':
                    ls = ls_glo
                elif system == 'C':
                    ls = 14
                else:
                    ls = 0
                    
                # defined the tracking mode. For this demo only some particular
                # tracking modes are considered as examples
                if system == 'C':
                    track_mode = '2I'
                elif system == 'E':
                    track_mode = '1X'
                else:
                    track_mode = '1C'
                
                dt = 0
                
                osr_out = rtcm_ssr2osr.RtcmSsr2osr(ssr, ephemeris,
                                                   epoch, ionosphere,
                                                   ID, track_mode,
                                                   ls, n4,
                                                   receiver, dt, iono_output)
                # print osr of the visible satellite and save it
                if float(osr_out.el) >= 0:
                    osr = np.append(osr, osr_out)
                    print(osr_out, file = osr_output)

# =============================================================================
#      close output files                
# =============================================================================
    osr_output.close()
    iono_output.close()
    print('### Completed SSR influence computation.')
    return eph0, ssr0, osr
