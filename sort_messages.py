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


import ephemeris
import rtcm_ssr
import coord_and_time_transformations as trafo
"""
    Function to sort the decoded messages into ephemeris and ssr parameters. 
    Ephemeris and ssr are then sorted into the different gnss system. 
    Input:
        - message type
        - decoded msg
        - ephemeris to be updated
        - ssr to be updated 
        - n4: GLONASS four-year interval number
        - ls: GLONASS leap second
    Output:
        - ephemeris object oriented representation
        - ssr       object oriented representation
    ****************************************************************************
    Description:
    the input decoded msg passes to the Ephemeris class when this is an 
    ephemeris message, while when it contains ssr parameters is passed to the
    SSR class. For each new ssr message the ssr output is update through the 
    method update_ssr of the SSR class.
"""

def sort_msg(msg_type, dec_msg, eph=None, ssr=None, n4=None, ls=None):
    if eph is None:
        eph = ephemeris.Ephemeris()
    if ssr is None:
        ssr = rtcm_ssr.SSR()
    
    if msg_type == 1264:
        system = 'IONO'
    else:
        system = dec_msg.gnss_short

    if ((msg_type == 1019) | (msg_type == 1045) | 
        (msg_type == 1046) | (msg_type == 1020)|
        (msg_type == 1042) | (msg_type == 1044)):
                
        eph.add_system(system)
        
        eph.add_ephemeris_msg(dec_msg, system)
                   
    elif (ls is not None):
        if system == 'R':
            if n4 is None:
                # if no ephemeris are available the epoch considered
                # will be the GLONASS epoch
                epoch = dec_msg.epoch
            else:
            # glonass time 2 gps time. The function takes as input 
            # the glonass day, the glonass time and the leap seconds
                # start a loop to find a satellite with known ephemeris
                # to compute the week
                ii = 0
                ref_eph = []
                while ((len(ref_eph) == 0) & (ii<len(dec_msg.gnss_id))):
                    ref_eph = eph.get_closest_epo(dec_msg.epoch, eph.glo,
                                                  system +
                                                  str(dec_msg.gnss_id[0]))
                    ii += 1
                [week, epoch] = trafo.glo_time2gps_time(ref_eph[0].nt,
                                                        dec_msg.epoch, 
                                                        n4,
                                                        ls)
        else:
            epoch = dec_msg.epoch
        
        ssr.add_epoch(epoch)
        # orbit
        if ((msg_type == 1057) | (msg_type == 1063) |
            (msg_type == 1240) | (msg_type == 1246) |
            (msg_type == 1258)):
            ssr.update_ssr(system, epoch, orb=dec_msg)
        # clock
        elif ((msg_type == 1058) | (msg_type == 1064) | 
              (msg_type == 1241) | (msg_type == 1247) |
              (msg_type == 1259)): 
            ssr.update_ssr(system, epoch, clck=dec_msg)
        # orbit & clock
        elif ((msg_type == 1060) | (msg_type == 1066) |
              (msg_type == 1243) | (msg_type == 1261)):
            ssr.update_ssr(system, epoch, orb_clck=dec_msg)
        # code bias
        elif ((msg_type == 1059) | (msg_type == 1065) |
              (msg_type == 1242) | (msg_type == 1248) |
              (msg_type == 1260)):
            ssr.update_ssr(system, epoch, cbias=dec_msg)
        # phase bias
        elif ((msg_type == 1265) | (msg_type == 1266) | 
              (msg_type == 1267) | (msg_type == 1268) |
              (msg_type == 1270)): 
            ssr.update_ssr(system, epoch, pbias=dec_msg)
        # iono
        elif msg_type == 1264:
            ssr.update_ssr(system, epoch, iono=dec_msg)
            ssr.add_iono_epoch(epoch)
        
    return eph, ssr
        
        