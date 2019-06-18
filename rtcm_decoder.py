"""
   ----------------------------------------------------------------------------
   Copyright (C) 2019 Francesco Darugna <fd@geopp.de>  Geo++ GmbH,
                      Jannes Wübbena    <jw@geopp.de>  Geo++ GmbH.
   
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

import bitstruct
import numpy as np
import sys

""" RTCM message decoder multi class file
    
    Input:
    - message: data message of the a single type message
    
    Output:
    - decoded: decoded data message for the desidered type
    
    ***************************************************************************
    Description:
    the constructor of the rtcm_decoder class expects the RTCM message content
    as a byte object, without the RTCM message frame. The message will be 
    decoded and be accessed by the dec_msg member (defined by the RTCM message
    type) of the created rtcm_decoder object. The __str__ method can be used
    to print the content of the message in a human readable format.
    ***************************************************************************
    
    List of RTCM-SSR messages considered:
        - 1019: GPS ephemeris
        - 1020: GLONASS ephemeris
        - 1042: Beidou ephemeris
        - 1044: QZSS ephemeris
        - 1045: Galileo F/NAV ephemeris
        - 1046: Galileo I/NAV ephemeris
        - 1057: GPS Orbit message
        - 1058: GPS Clock message
        - 1059: GPS Code bias
        - 1060: GPS combined orbit and clock
        - 1061: GPS URA message
        - 1265: GPS Phase Bias
        - 1063: GLONASS Orbit message
        - 1064: GLONASS Clock message
        - 1065: GLONASS Code bias
        - 1066: GLONASS combined orbit and clock
        - 1067: GLONASS URA message
        - 1266: GLONASS Phase Bias
        - 1240: Galileo Orbit Message
        - 1241: Galileo Clock Message
        - 1242: Galileo Code bias
        - 1243: Galileo combined orbit and clock
        - 1244: Galileo URA message
        - 1245: Galileo High Rate Clock message
        - 1267: Galileo Phase Bias 
        - 1246: QZSS Orbit message
        - 1247: QZSS Clock message
        - 1248: QZSS Code bias
        - 1249: QZSS combined orbit and clock
        - 1250: QZSS URA message
        - 1251: QZSS High Rate Clock message
        - 1268: QZSS Phase Bias
        - 1258: BDS Orbit message
        - 1259: BDS Clock message
        - 1260: BDS Code bias
        - 1261: BDS combined orbit and clock
        - 1262: BDS URA message
        - 1263: BDS High Rate Clock message
        - 1270: BDS Phase Bias
        - 1264: SSR VTEC
    References:
       - RTCM c10403.3
       
"""

class rtcm_decoder:
    def __init__(self, message, type_len):
        self.msg = message
        self.type_len = type_len
        try:
            message_type = bitstruct.unpack('u12', message)[0]
        except:
            print('The rtcm-file considered does not contained ' +
                  'the RTCM-SSR messages considered in the demo.')
            sys.exit()
            
        self.msg_type = message_type
          
        if message_type == 1019:
            self.dec_msg = gps_ephemeris(message)
        elif message_type == 1057:
            self.dec_msg = gps_orbit(message)
        elif message_type == 1058:
            self.dec_msg = gps_clock(message)
        elif message_type == 1059:
            self.dec_msg = gps_code_bias(message)
        elif message_type == 1060:
            self.dec_msg = gps_orbit_clock(message)
        elif message_type == 1061:
            self.dec_msg = gps_ura(message)
        elif message_type == 1265:
            self.dec_msg = gps_phase_bias(message)
        elif message_type == 1020:
            self.dec_msg = glo_ephemeris(message)
        elif message_type == 1063:
            self.dec_msg = glo_orbit(message)    
        elif message_type == 1064:
            self.dec_msg = glo_clock(message)   
        elif message_type == 1065:
            self.dec_msg = glo_code_bias(message)   
        elif message_type == 1066:
            self.dec_msg = glo_orbit_clock(message) 
        elif message_type == 1067:
            self.dec_msg = glo_ura(message) 
        elif message_type == 1266:
            self.dec_msg = glo_phase_bias(message) 
        elif message_type == 1045:
            self.dec_msg = gal_ephemeris_fnav(message)         
        elif message_type == 1046:
            self.dec_msg = gal_ephemeris_inav(message)   
        elif message_type == 1240:
            self.dec_msg = gal_orbit(message)         
        elif message_type == 1241:
            self.dec_msg = gal_clock(message)  
        elif message_type == 1242:
            self.dec_msg = gal_code_bias(message)         
        elif message_type == 1243:
            self.dec_msg = gal_orbit_clock(message) 
        elif message_type == 1244:
            self.dec_msg = gal_ura(message)         
        elif message_type == 1245:
            self.dec_msg = gal_hr_clock(message)
        elif message_type == 1267:
            self.dec_msg = gal_phase_bias(message)
        elif message_type == 1264:
            self.dec_msg = iono_sph(message)    
        elif message_type == 1042:
            self.dec_msg = bds_ephemeris(message)  
        elif message_type == 1258:
            self.dec_msg = bds_orbit(message)    
        elif message_type == 1259:
            self.dec_msg = bds_clock(message)  
        elif message_type == 1260:
            self.dec_msg = bds_code_bias(message) 
        elif message_type == 1261:
            self.dec_msg = bds_orbit_clock(message)  
        elif message_type == 1262:
            self.dec_msg = bds_ura(message) 
        elif message_type == 1270:
            self.dec_msg = bds_phase_bias(message) 
        elif message_type == 1044:
            self.dec_msg = qzs_ephemeris(message) 
        elif message_type == 1246:
            self.dec_msg = qzs_orbit(message) 
        elif message_type == 1247:
            self.dec_msg = qzs_clock(message)
        elif message_type == 1248:
            self.dec_msg = qzs_code_bias(message) 
        elif message_type == 1249:
            self.dec_msg = qzs_orbit_clock(message)
        elif message_type == 1250:
            self.dec_msg = qzs_ura(message) 
        elif message_type == 1251:
            self.dec_msg = qzs_hr_clock(message)
        elif message_type == 1268:
            self.dec_msg = qzs_phase_bias(message) 
        else:
            self.dec_msg = None            
# =============================================================================
#                              Printing method        
# =============================================================================
# *************************************************************************** #
#                                                                             #
#                       Ephemeris (Kepler elements)                           #
#                                                                             #
# *************************************************************************** #
    def __str__(self):
        if ((self.msg_type == 1019) | (self.msg_type == 1045) | 
            (self.msg_type == 1046) | (self.msg_type == 1042) |
            (self.msg_type == 1044)):
            strg = ('### RTCM 3 - ' + self.dec_msg.gnss +
                    ' Ephemeris Message ' + '<' + str(self.msg_type) + '>' +
                    '\n' +
                    ' Message size [bytes] :  ' + str(self.type_len + 6) +
                    '\n' +
                    ' Data  length [bytes] :  ' + str(self.type_len)   +
                    '\n' +
                    '{:''8} {:''2} {}'.format(' PRN                 ', ':', 
                                              self.dec_msg.sat_id) + '\n'  + 
                    '{:''8} {:''2} {}'.format(' WEEK                ', ':', 
                    self.dec_msg.week)) 
            if ((self.msg_type == 1019)| (self.msg_type == 1044)):
                strg = (strg + '\n' + 
                       '{:''8} {:''1} {:>13.6e}'.format(' TGD                 ',
                       ':', self.dec_msg.tgd) +
                       '\n' +                       
                       '{:''8} {:''2} {}'.format(' IODC                ', ':',
                        self.dec_msg.iodc) + '\n'
                       '{:''8} {:''2} {}'.format(' IODE                ', ':',
                       self.dec_msg.iode))
            elif (self.msg_type == 1045) | (self.msg_type == 1046): 
                strg = (strg + '\n' + 
                       '{:''8} {:''1} {:>13.6e}'.format(' BGD5AE1             ',
                       ':', self.dec_msg.bgd_a) +
                       '\n' +
                       '{:''8} {:''1} {:>13.6e}'.format(' BGD5BE1             ',
                       ':', self.dec_msg.bgd_b) +
                       '\n' + 
                       '{:''8} {:''2} {}'.format(' IODNAV              ', ':',
                        self.dec_msg.iod))
            elif (self.msg_type == 1042): 
                strg = (strg + '\n' + 
                       '{:''8} {:''1} {:>13.6e}'.format(' TGD1             [s]',
                       ':', self.dec_msg.tgd1) +
                       '\n' +
                       '{:''8} {:''1} {:>13.6e}'.format(' TGD2             [s]',
                       ':', self.dec_msg.tgd2) +
                       '\n' + 
                       '{:''8} {:''2} {}'.format(' AODC             [h]',
                       ':', self.dec_msg.aodc) +
                       '\n' +
                       '{:''8} {:''2} {}'.format(' AODE             [h]',
                       ':', self.dec_msg.aode))
            strg = (strg + '\n' +                       
                    '{:''8} {:''2} {}'.format(' T0C              [s]', ':',
                    self.dec_msg.toc) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' AF2          [s/s/s]',
                    ':', self.dec_msg.af_two) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' AF1            [s/s]',
                    ':', self.dec_msg.af_one) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' AF0              [s]',
                    ':', self.dec_msg.af_zero) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' DN           [rad/s]', 
                    ':', self.dec_msg.dn) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' M0             [ras]',
                    ':', self.dec_msg.m0) + '\n' +  
                    '{:''8} {:''1} {:>13.6e}'.format(' E                   ', 
                    ':', self.dec_msg.ecc) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' ROOTA        [m^0.5]', 
                    ':', self.dec_msg.root_a) + '\n' + 
                    '{:''8} {:''2} {}'.format(' T0E              [s]', ':',
                    self.dec_msg.toe) + '\n' + 
                    '{:''8} {:''1} {:>13.8e}'.format(' CIC            [rad]', 
                    ':', self.dec_msg.cic) + '\n' + 
                    '{:''8} {:''1} {:>13.8e}'.format(' CRC              [m]', 
                    ':', self.dec_msg.crc) + '\n' + 
                    '{:''8} {:''1} {:>13.8e}'.format(' CIS            [rad]', 
                     ':', self.dec_msg.cis) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' CRS              [m]', 
                     ':', self.dec_msg.crs) + '\n' +  
                    '{:''8} {:''1} {:>13.6e}'.format(' CUC            [rad]', 
                    ':', self.dec_msg.cuc) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' CUS            [rad]', 
                    ':', self.dec_msg.cus) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' OMEGA0         [rad]', 
                    ':', self.dec_msg.omega_0) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' omega          [rad]', 
                    ':', self.dec_msg.omega) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' I0             [rad]', 
                    ':', self.dec_msg.i0) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' OMEGA.       [rad/s]', 
                    ':', self.dec_msg.omega_dot) + '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' IDOT         [rad/s]', 
                    ':', self.dec_msg.idot) + '\n' + 
                    '{:''8} {:''2} {}'.format(' HEALTH              ', ':',
                    self.dec_msg.health))
            if ((self.msg_type == 1019) | (self.msg_type == 1044)):
                strg = (strg + '\n' + 
                       '{:''8} {:''2} {}'.format(' URA                 ', ':',
                       self.dec_msg.ura) + '\n' +  
                       '{:''8} {:''2} {}'.format(' FIT                 ', ':', 
                       self.dec_msg.interval) + '\n')
            if  (self.msg_type == 1045) | (self.msg_type == 1046):
                strg = (strg + '\n' + 
                       '{:''8} {:''2} {}'.format(' SISA                ', ':',
                       self.dec_msg.sisa) + '\n')            
            if (self.msg_type == 1042):
                strg = (strg + '\n' + 
                       '{:''8} {:''2} {}'.format(' URA                 ', ':',
                       self.dec_msg.ura))  
            
            return strg          
# *************************************************************************** #
#                                                                             #
#                      Ephemeris (state vector)                               #
#                                                                             #
# *************************************************************************** #                     
        elif (self.msg_type == 1020):
            strg = ('### RTCM 3 - ' + self.dec_msg.gnss +
                    ' Ephemeris Message ' + '<' + str(self.msg_type) +  '>' +
                    '\n' +
                    ' Message size [bytes] :  ' + str(self.type_len + 6) +
                    '\n' +
                    ' Data  length [bytes] :  ' + str(self.type_len) +
                    '\n' +
                    '{:''8} {:''2} {}'.format(' GLO SLOT            ', ':', 
                    self.dec_msg.sat_id) + '\n' +
                    '{:''8} {:''2} {}'.format(' FREQ                ', ':',
                    self.dec_msg.freq) + '\n' +
                    '{:''8} {:''2} {}'.format(' DAY NUMBER          ', ':',
                    self.dec_msg.nt) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' T_K [s]             ',
                    ':', self.dec_msg.tk) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' T_B [s]             ',
                    ':', self.dec_msg.tb) + '\n' +  
                    '{:''8} {:''2} {}'.format(' HEALTH Bn           ', ':',
                    self.dec_msg.bn) + '\n' +
                    '{:''8} {:''2} {}'.format(' HEALTH Cn           ', ':',
                    self.dec_msg.cn) + '\n' +
                    '{:''8} {:''2} {}'.format(' HEALTH 2            ', ':',
                    self.dec_msg.msb_bn) + '\n' + 
                    '{:''8} {:''2} {}'.format(' Flag P              ', ':',
                    self.dec_msg.p) + '\n' +
                    '{:''8} {:''2} {}'.format(' Flag P1             ', ':',
                    self.dec_msg.p1) + '\n' +
                    '{:''8} {:''2} {}'.format(' Flag P2             ', ':',
                    self.dec_msg.p2) + '\n' +
                    '{:''8} {:''2} {}'.format(' Flag P3             ', ':',
                    self.dec_msg.p3) + '\n' +
                    '{:''8} {:''2} {}'.format(' Flag P4             ', ':',
                    self.dec_msg.p4) + '\n' +
                    '{:''8} {:''2} {}'.format(' FT                  ', ':',
                    self.dec_msg.ft) + '\n' +
                    '{:''8} {:''2} {}'.format(' MODIFICAT.          ', ':',
                    self.dec_msg.m) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' GAMMA          [s/s]', 
                    ':', self.dec_msg.gamma) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' TAU              [s]',
                    ':', self.dec_msg.tau) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' DELTA TAU        [s]',
                    ':', self.dec_msg.dtau) + '\n' +
                    '{:''8} {:''2} {}'.format(' AGE              [d]',
                    ':', self.dec_msg.en) + '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' X               [km]',
                    ':', self.dec_msg.xn) +  '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' Y               [km]',
                    ':', self.dec_msg.yn) + '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' Z               [km]',
                    ':', self.dec_msg.zn) + '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' XDOT          [km/s]',
                    ':', self.dec_msg.dxn) + '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' YDOT          [km/s]',
                    ':', self.dec_msg.dyn) + '\n' +
                    '{:''8} {:''1} {:>+9.6f}'.format(' ZDOT          [km/s]',
                    ':', self.dec_msg.dzn) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' XDOTDOT     [km/s^2]',
                    ':', self.dec_msg.ddxn) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' YDOTDOT     [km/s^2]',
                    ':', self.dec_msg.ddyn) + '\n' +
                    '{:''8} {:''1} {:>13.6e}'.format(' ZDOTDOT     [km/s^2]',
                    ':', self.dec_msg.ddzn) + '\n' +            
                    '{:''8} {:''1} {:>13.6e}'.format(' avail. add. data 0/1',
                             ':', self.dec_msg.ava) +
                             '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' TauC                ', 
                             ':', self.dec_msg.tau_c) +
                             '\n' + 
                    '{:''8} {:''1} {:>13.6e}'.format(' N4                  ',
                    ':', self.dec_msg.n4) + '\n')

            return strg

# *************************************************************************** #
#                                                                             #
#                                   Orbit                                     #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1057) | (self.msg_type == 1063) |
              (self.msg_type == 1240) | (self.msg_type == 1246) |
              (self.msg_type == 1258)) :
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Orbit Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Reference datum        : ' + 
                    str(self.dec_msg.datum) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n') 
            if self.dec_msg.gnss_short == 'C':
                strg = (strg + '{:^6s}'.format(' SVnr'    ) + 
                        '{:^6s}'.format('toe'       ) +                      
                        '{:^6s}'.format('IOD'     ) +
                        '{:^9s}'.format('Rad [m]' ) +
                        '{:^9s}'.format('Al T [m]') +
                        '{:^9s}'.format('Cr T [m]') +
                        '{:^27s}'.format('DotDelta [mm/s]') + '\n') 
                for j in range(self.dec_msg.n_sat):
                    strg = (strg + ' ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            ''  + '{:>3.0f}'.format(int(self.dec_msg.toe[j])) +                         
                            ' ' +
                            '{:>3.0f}'.format(int(self.dec_msg.gnss_iod[j])) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dr[j]) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dt[j]) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dn[j]) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dot_dr[j]) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dot_dt[j]) +
                            ' ' + '{:>+8.4f}'.format(self.dec_msg.dot_dn[j]) +
                            '\n')
            else:
                strg = (strg + '{:^6s}'.format(' SVnr'    ) + 
                        '{:^8s}'.format('IOD  '     ) +
                        '{:^10s}'.format('Rad [m] ' ) +
                        '{:^11s}'.format('Al T [m] ') +
                        '{:^10s}'.format('Cr T [m] ') +
                        '{:^27s}'.format(' DotDelta [mm/s]') + '\n') 
                for j in range(self.dec_msg.n_sat):
                    strg = (strg + ' ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            '  ' + 
                            '{:>3.0f}'.format(int(self.dec_msg.gnss_iod[j])) +
                            '   ' + '{:>+8.4f}'.format(self.dec_msg.dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dt[j]) +
                            '   ' + '{:>+8.4f}'.format(self.dec_msg.dn[j]) +
                            '    ' + '{:>+8.4f}'.format(self.dec_msg.dot_dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dt[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dn[j]) +
                            '\n')
            return strg     
           
# *************************************************************************** #
#                                                                             #
#                                   Clock                                     #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1058) | (self.msg_type == 1064) | 
              (self.msg_type == 1241) | (self.msg_type == 1247) |
              (self.msg_type == 1259)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Clock Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n' + '{:^6s}'.format('SVnr'    ) + 
                    '{:^9s}'.format('  C0 [m]   ' ) +
                    '{:^9s}'.format(' C1 [mm/s] ') + 
                    '{:^9s}'.format(' C2 [mm/s^2]') + '\n')
            
            for j in range(self.dec_msg.n_sat):
                strg = (strg + ' ' + self.dec_msg.gnss_short + 
                        '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                        '   ' +  '{:>+8.4f}'.format(self.dec_msg.dc0[j]) + 
                        '    ' + '{:>+8.4f}'.format(self.dec_msg.dc1[j]) +
                        '    ' + '{:>+8.4f}'.format(self.dec_msg.dc2[j]) +
                        '\n')
            return strg

# *************************************************************************** #
#                                                                             #
#                             High Rate Clock                                 #
#                                                                             #
# *************************************************************************** #        
        elif ((self.msg_type == 1245) | (self.msg_type == 1263) |
              (self.msg_type == 1251)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' High Rate Clock Message <' +
                    str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n' + '{:^6s}'.format('SVnr'    ) + 
                    '{:^9s}'.format('  High Rate Clock [m]   ' ) + '\n')
            
            for j in range(self.dec_msg.n_sat):
                strg = (strg + ' ' + self.dec_msg.gnss_short + 
                        '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                        '   ' +  '{:>+7.4f}'.format(self.dec_msg.hr_clock[j]) + 
                        '\n')
            return strg

# *************************************************************************** #
#                                                                             #
#                              Code bias                                      #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1059) | (self.msg_type == 1065) |
              (self.msg_type == 1242) | (self.msg_type == 1248) |
              (self.msg_type == 1260)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Code Bias Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n' + '{:^6s}'.format('SVnr'    ) + 
                    '{:^9s}'.format('num biases' ) + 
                    '{:^8s}'.format('type') + 
                    '{:^6s}'.format('signal ') + 
                    '{:^9s}'.format('code bias [m] ') + 
                    '{:^9s}'.format('type ') + '{:^6s}'.format('signal ') +
                    '{:^9s}'.format('code bias [m] ') +
                    '{:^9s}'.format('[...] ') + '\n') 
            
            for j in range(self.dec_msg.n_sat):
                if j == 0:
                    strg = (strg + ' ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            '{:>3s}'.format('  ') + 
                            '{:>3.0f}'.format(int(self.dec_msg.number[j])) + 
                            '{:>5s}'.format('       '))                    
                else:    
                    strg = (strg + '\n ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            '{:>3s}'.format('  ') + 
                            '{:>3.0f}'.format(int(self.dec_msg.number[j])) + 
                            '{:>5s}'.format('       '))                   
                        
                for k in range(int(self.dec_msg.number[j])):
                    strg = (strg + 
                           '{:>2.0f}'.format(self.dec_msg.track[j][k]) +
                           '{:>3s}'.format('    ') + 
                           '{:>4s}'.format(self.dec_msg.name[j][k]) +
                           '{:>3s}'.format('    ') +
                           '{:>+8.4f}'.format(self.dec_msg.bias[j][k]) +
                           '{:>8}'.format('        ') )
            return strg + '\n'
        
# *************************************************************************** #
#                                                                             #
#                          Combined orbit and clock                           #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1060) | (self.msg_type == 1066) |
              (self.msg_type == 1243) | (self.msg_type == 1261)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Orbit and Clock Message <' + str(self.msg_type) + '>' + 
                    '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Reference datum        : ' + 
                    str(self.dec_msg.datum) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n') 
            if self.dec_msg.gnss_short == 'C':
                strg = (strg + '{:^6s}'.format(' SVnr'    ) + 
                        '{:^6s}'.format('toe_mod'       ) +                      
                        '    ' +
                        '{:^6s}'.format('IOD'     ) +
                        '    ' +
                        '{:^9s}'.format('Rad [m]' ) +
                        ' ' +
                        '{:^9s}'.format('Al T [m]') +
                        '  ' +
                        '{:^9s}'.format('Cr T [m]') +
                        '    ' +
                        '{:^27s}'.format('DotDelta [mm/s]') + 
                        '   ' +
                        '{:^9s}'.format(' A0 [m]  ' ) +
                        '{:^9s}'.format(' A1 [mm/s] ') + 
                        '{:^9s}'.format(' A2 [mm/s^2]') + '\n')
                for j in range(self.dec_msg.n_sat):
                    strg = (strg + ' ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            '  '  + '{:>3.0f}'.format(int(self.dec_msg.toe[j])) +                         
                            '   ' +
                            '{:>10.0f}'.format(int(self.dec_msg.gnss_iod[j])) +
                            '   ' +'{:>+8.4f}'.format(self.dec_msg.dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dt[j]) +
                            '   ' + '{:>+8.4f}'.format(self.dec_msg.dn[j]) +
                            '    ' + '{:>+8.4f}'.format(self.dec_msg.dot_dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dt[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dn[j]) +
                            '   ' +  '{:>+8.4f}'.format(self.dec_msg.dc0[j]) + 
                            '    ' + '{:>+7.4f}'.format(self.dec_msg.dc1[j]) +
                            '    ' + '{:>+7.4f}'.format(self.dec_msg.dc2[j]) +
                            '\n')
            else:
                strg = (strg + '{:^6s}'.format(' SVnr'    ) + 
                        '{:^6s}'.format('IOD'     ) +
                        '{:^6s}'.format('P'     ) +
                        '{:^10s}'.format('Rad [m] ' ) +
                        ' ' +
                        '{:^10s}'.format('Al T [m] ') +
                        ' ' +
                        '{:^10s}'.format('Cr T [m] ') +
                        '  ' +
                        '{:^27s}'.format('DotDelta [mm/s]') +
                        '    ' +
                        '{:^9s}'.format(' A0 [m]  ' ) +
                        '{:^9s}'.format(' A1 [mm/s] ') + 
                        '{:^9s}'.format(' A2 [mm/s^2]') + '\n')
                for j in range(self.dec_msg.n_sat):
                    strg = (strg + ' ' + self.dec_msg.gnss_short +
                            '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                            '  ' + 
                            '{:>3.0f}'.format(int(self.dec_msg.gnss_iod[j])) +
                            '  ' +
                            '{:>3.0f}'.format(int(self.dec_msg.p[j])) +
                            '   ' +'{:>+8.4f}'.format(self.dec_msg.dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dt[j]) +
                            '   ' + '{:>+8.4f}'.format(self.dec_msg.dn[j]) +
                            '    ' + '{:>+8.4f}'.format(self.dec_msg.dot_dr[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dt[j]) +
                            '  ' + '{:>+8.4f}'.format(self.dec_msg.dot_dn[j]) +
                            '   ' +  '{:>+8.4f}'.format(self.dec_msg.dc0[j]) + 
                            '    ' + '{:>+7.4f}'.format(self.dec_msg.dc1[j]) +
                            '    ' + '{:>+7.4f}'.format(self.dec_msg.dc2[j]) +
                            '\n')
            return strg

# *************************************************************************** #
#                                                                             #
#                                    URA                                      #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1061) | (self.msg_type == 1067) | 
              (self.msg_type == 1244) | (self.msg_type == 1262)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' URA Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]   : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]   : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s] : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]    : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                    : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'Number of satellites   : ' +  str(self.dec_msg.n_sat) + 
                    '\n' + '{:^6s}'.format(' SVnr  '    ) + ' ' +
                    '{:^8s}'.format(' URA [m] ') + '\n')
            
            for j in range(self.dec_msg.n_sat):
                strg = (strg + ' ' + self.dec_msg.gnss_short + 
                        '{:3s}'.format(self.dec_msg.gnss_id[j]) + 
                        '   ' +  '{:>+7.4f}'.format(self.dec_msg.ura[j]) + 
                        '  [class =' + 
                        '{:2.0f}'.format(int(self.dec_msg.ura_class[j])) +
                        ', value =' + 
                        '{:2.0f}'.format(int(self.dec_msg.ura_value[j])) +
                        ']' + '\n')
            return strg
        
# *************************************************************************** #
#                                                                             #
#                                Phase bias                                   #
#                                                                             #
# *************************************************************************** #
        elif ((self.msg_type == 1265) | (self.msg_type == 1266) | 
              (self.msg_type == 1267) | (self.msg_type == 1268) |
              (self.msg_type == 1270)):
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Phase bias Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]      : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]      : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s]    : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]       : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                       : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                   : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                   : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                   : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    'DispersiveSignalIndicator : ' +
                    str(self.dec_msg.disp_bias) + '\n' + 
                    'MWConsistencyIndicator    : '+
                     str(self.dec_msg.mw) + '\n' + 
                    'Number of satellites      : ' +  str(self.dec_msg.n_sat) + 
                    '\n' + '{:^6s}'.format(' SVnr  '    ) + ' ' +
                    '{:^8s}'.format('Yaw[deg]'     )  +
                    '{:^11s}'.format(' YawRate[deg/s]' )  +
                    '{:^5s}'.format(' nPh ') + 
                    '{:^4s}'.format(' Typ') + 
                    '{:^7s}'.format('    Sig') + 
                    '{:^9s}'.format('    i    ') + 
                    '{:^4s}'.format('w'  ) + 
                    '{:^8s}'.format('dis') + 
                    '{:^9s}'.format('  Bias[m]     ') +
                    '{:^4s}'.format(' Typ') + 
                    '{:^7s}'.format('    Sig') + 
                    '{:^9s}'.format('    i    ') + 
                    '{:^4s}'.format('w'  ) + 
                    '{:^8s}'.format('dis') + 
                    '{:^8s}'.format('  Bias[m]     ') + 
                    '{:^8s}'.format('[...]')  + '\n')
            
            for j in range(self.dec_msg.n_sat):
                if j == 0:
                    strg = (strg + ' ' + self.dec_msg.gnss_short + 
                            '{:>2s}'.format(self.dec_msg.gnss_id[j]) +
                            '{:>3s}'.format('   ') +
                            '{:>8.4f}'.format(self.dec_msg.yaw_angle[j]) +
                            '{:>3s}'.format('   ') +
                            '{:>8.4f}'.format(self.dec_msg.yaw_rate[j]) +
                            '{:>5s}'.format('      ') +
                            '{:>2.0f}'.format(int(self.dec_msg.number[j])) + '')
                else:
                    strg = (strg + '\n ' + self.dec_msg.gnss_short + 
                            '{:>2s}'.format(self.dec_msg.gnss_id[j]) +
                            '{:>3s}'.format('   ') +
                            '{:>8.4f}'.format(self.dec_msg.yaw_angle[j]) +
                            '{:>3s}'.format('   ') +
                            '{:>8.4f}'.format(self.dec_msg.yaw_rate[j]) +
                            '{:>5s}'.format('      ') +
                            '{:>2.0f}'.format(int(self.dec_msg.number[j])) + '')

                for k in range(int(self.dec_msg.number[j])):
                    strg = (strg + '{:>3s}'.format('   ') + 
                            '{:>2.0f}'.format(int(self.dec_msg.track[j][k])) + 
                            '{:>3s}'.format('     ') +
                            '{:>3s}'.format(self.dec_msg.name[j][k]) +
                            '{:>3s}'.format('   ') +
                            '{:>2.0f}'.format(int(self.dec_msg.sig_i[j][k])) +
                            '{:>3s}'.format('    ') +
                            '{:>2.0f}'.format(self.dec_msg.sig_wl[j][k]) + 
                            '{:>3s}'.format('    ') +
                            '{:>2.0f}'.format(self.dec_msg.sig_dis[j][k]) +
                            '{:>3s}'.format('    ') +
                            '{:>+8.4f}'.format(self.dec_msg.bias[j][k]) + 
                            '{:>3s}'.format('    '))    
                
            return strg + '\n'
        
# *************************************************************************** #
#                                                                             #
#                       Ionosphere Spherical Harmonics                        #
#                                                                             #
# *************************************************************************** #
        elif self.msg_type == 1264:
            strg = ('### RTCM 3 - SSR ' + self.dec_msg.gnss +
                    ' Phase bias Message <' + str(self.msg_type) + '>' + '\n' +
                    'Message size [bytes]      : ' + str(self.type_len + 6) + 
                    '\n' +
                    'Data  length [bytes]      : ' + str(self.type_len) +
                    '\n' + self.dec_msg.gnss[0:3] + ' SSR Epoch time [s]    : ' +
                    str(self.dec_msg.epoch) + '\n' +
                    'Update Interval [s]       : ' + str(self.dec_msg.ui) +
                    '\n' +
                    'MMI                       : ' + str(self.dec_msg.mmi) +
                    '\n' +
                    'IOD_ssr                   : ' + str(self.dec_msg.iod) +
                    '\n' +
                    'ssrP_ID                   : ' + 
                    str(self.dec_msg.provider_id)  + '\n' +
                    'ssrS_ID                   : ' + 
                    str(self.dec_msg.solution_id) + '\n' +
                    ' quality indicator [TECU]       : ' + 
                    str(self.dec_msg.quality) +
                    '\n' +
                    ' Number of layers               : ' + 
                    str(self.dec_msg.n_layers) +
                    '\n') 
    
            for l in range(self.dec_msg.n_layers):
                    strg = (strg + 
                            ' h [km]                         : ' + 
                            str(self.dec_msg.height[l]) + '\n' + 
                            ' Spherical Harmonic degree      : ' +
                            str(int(self.dec_msg.degree[l])) + '\n' + 
                            ' Spherical Harmonic order       : ' +
                            str(int(self.dec_msg.order[l])) + '\n' +
                            ' Number of Cosine coefficients  : ' +
                            str(int(self.dec_msg.n_c[l])) + '\n' + 
                            ' Number of Sine   coefficients  : ' + 
                            str(int(self.dec_msg.n_s[l])) + '\n') 
        
            index = 0        
            C_print = []
            S_print = []
            for k in range(int(self.dec_msg.n_c[l])):
                if np.abs(self.dec_msg.c[0][k]) == 163.84:
                    C_print = np.append(C_print,
                                        np.str('{:+7.3f}'.format(self.dec_msg.c[0][k])
                                        ) + '!')
                else:
                    C_print = np.append(C_print,
                                        np.str('{:+7.3f}'.format(self.dec_msg.c[0][k])))
             
            for k in range(int(self.dec_msg.n_s[l])):
                if np.abs(self.dec_msg.s[0][k]) == 163.84:
                    S_print = np.append(S_print,
                                        np.str('{:+7.3f}'.format(self.dec_msg.s[0][k])
                                        ) + '!')
                else:
                    S_print = np.append(S_print,
                                        np.str('{:+7.3f}'.format(self.dec_msg.s[0][k])))
            for j in range(int(self.dec_msg.order[l]) + 1):
                if index < self.dec_msg.n_c[l]:
                    strg = (strg + ' C' + f'{j}' + '[TECU]' + 
                              ': ' +  ",".join(C_print[index: index +
                                                    (int(self.dec_msg.degree[l]) +
                                                     1 - 
                                                     j)] ).replace(",", " ") + 
                            '\n')
                index = index + (int(self.dec_msg.degree[l]) + 1 - j)
  
            index = 0        
            for j in range(int(self.dec_msg.order[l])):
                if index < self.dec_msg.n_s[l]:
                    strg = (strg + ' S' + f'{j+1}' + '[TECU]' + 
                              ': ' + ",".join(S_print[index: index +
                                                    (int(self.dec_msg.degree[l]) +
                                                     1 - 
                                                     (j + 1))] ).replace(",",
                                                                " ") + '\n')                    
                index = index + (int(self.dec_msg.degree[l]) - j)
                
            if (np.any(np.abs(self.dec_msg.c) == 163.84) |
                np.any(np.abs(self.dec_msg.s) == 163.84)):
                strg = (strg + '(Note: ! indicates value is invalid or out of' + 
                        'range -163.835...163.835)')
            return strg

# =============================================================================
#                                    GPS
# =============================================================================
# *************************************************************************** #
#                                                                             #
#                       GPS Ephemeris Message Type 1019                       #
#                                                                             #
# *************************************************************************** #        
class gps_ephemeris:
    def __init__(self, message):
        # Definition of the bits of the message
        content =  ('u12u6u10u4s2s14u8u16s8s16s22u10s16s16s32s16u32s16u32u' + 
                    '16s16s32s16s32s16s32s24s8u6s1s1')
        unpack_bits = bitstruct.unpack(content, message)
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        # Define constants
        pie = 3.14159265358979323846  # 20-decimal places
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the message number, hence it is not considered here
        # GPS satellite ID
        sat_ID = unpack_bits[1]
        # formatting
        sat_ID = str(sat_ID)
        if len(sat_ID) < 2:
            self.sat_id = 'G0' + sat_ID
        else:
            self.sat_id = 'G' + sat_ID
        
        # GPS week number. Range: 0-1023
        week = unpack_bits[2]
        # GPS week rollover problem... week number went from 1023 to 1024
        # on 21st August 1999, but limit is 1023.
        # Need to add logic to account for rollovers. Input is GPS time (s)?
        # 1 GPS week = 604 800 s
        self.week = week + 1024
        
        # GPS SV Accuracy 
        self.ura = unpack_bits[3]
        
        # GPS CODE on L2. 00 = reserved. 01 = P code. 10 = C/A code. 11 = L2C
        self.code_L2 = unpack_bits[4]
        
        # Rate of Inclination Angle
        self.idot = unpack_bits[5] * pow(2, -43) * pie
        
        # Issue of Data (Ephemeris)
        self.iode = unpack_bits[6]
        
        # GPS toc
        self.toc = unpack_bits[7] * pow(2, 4)
        
        # GPS af2
        self.af_two = unpack_bits[8] * pow(2, -55)
        
        # GPS af1
        self.af_one = unpack_bits[9] * pow(2, -43)
        
        # GPS af0
        self.af_zero = unpack_bits[10] * pow(2, -31)
        
        # GPS IODC
        self.iodc = unpack_bits[11]
        
        # Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
        self.crs = unpack_bits[12] * pow(2, -5)
        
        # Mean Motion Difference from Computed Value
        self.dn = unpack_bits[13] * pow(2, -43) * pie
        
        # Mean Anomaly at Reference Time
        self.m0 = unpack_bits[14] * pow(2, -31) * pie
        
        # GPS cuc
        self.cuc = unpack_bits[15] * pow(2, -29)
        
        # GPS eccentricity (e)
        self.ecc = unpack_bits[16] * pow(2, -33)
        
        # Amplitude of the Sine Harmonic Correction Term
        # to the Argument of Latitude
        self.cus = unpack_bits[17] * pow(2, -29)
        
        # Square Root of the Semi-Major Axis
        self.root_a = unpack_bits[18] * pow(2, -19)
        
        # Reference Time Ephemeris
        self.toe = unpack_bits[19] * pow(2, 4)
        
        # Amplitude of the Cosine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cic = unpack_bits[20] * pow(2, -29)
        
        # Longitude of Ascending Node of Orbit Plane at Weekly Epoch (omega_0)
        self.omega_0 = unpack_bits[21] * pow(2, -31) * pie
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cis = unpack_bits[22] * pow(2, -29)
    
        # Inclination Angle at Reference Time
        self.i0 = unpack_bits[23] * pow(2, -31) * pie
        
        # Amplitude of the Cosine Harmonic Correction Term to the Orbit Radius
        self.crc = unpack_bits[24] * pow(2, -5)
        
        # GPS argument of perigee (w) 
        self.omega = unpack_bits[25] * pow(2, -31) * pie
        
        # Rate of Right Ascension
        self.omega_dot = unpack_bits[26] * pow(2, -43) * pie
        
        # GPS t_GD
        self.tgd = unpack_bits[27] * pow(2, -31)
        
        # GPS SV health
        self.health = unpack_bits[28]
        
        # GPS L2 P data flag. L2P-code nav data: 0 = ON; 1 = OFF
        self.L2P = unpack_bits[29]
        
        # GPS fit interval
        self.interval = unpack_bits[30]
    
# *************************************************************************** #
#                                                                             #
#     SSR GPS combined Orbit and Clock Correction Message Type 1060           #
#                                                                             #
# *************************************************************************** #
class gps_orbit_clock:   
    def __init__(self, message):
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GPS Epoch Time 1s
        self.epoch = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])]  

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 65-> 8bytes + 1bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        gps_id  = []
        gps_iod = []
            
        p = []
            
        dr = []
        dt = []
        dn = []
            
        dot_dr = []
        dot_dt = []
        dot_dn = []
            
        dc0 = []
        dc1 = []
        dc2 = []
            
        bit_sat   = self.n_sat * 'u6u8s22s20s20s21s19s19s22s21s27'
        bit_gps_check   = self.n_sat * 'u6u1u7s22s20s20s21s19s19s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        gps_check = bitstruct.unpack(header + bit_gps_check, message)
            
        for i in range(self.n_sat):
        # GPS ID number,
            if s_unpack[11 * i + 9] < 10:
                gps_id = np.append(gps_id, '0' + f'{s_unpack[11 * i + 9]}')
            else:
                gps_id = np.append(gps_id, f'{s_unpack[11 * i + 9]}')
        # GPS IOD: Issue Of Data of GPS ephemeris to reference 
        # the geometric gradients 

            gps_iod = np.append(gps_iod, s_unpack[11 * i + 10])
            p = np.append(p, gps_check[12 * i + 10])               
                   
        # Delta radial
        # Printed in [m]
            dr = np.append(dr, s_unpack[11 * i + 11] * 0.1 * 10 ** (-3))
            
        # Delta along-track
        # Printed in [m]
            dt = np.append(dt, s_unpack[11 * i + 12] * 0.4 * 10 ** (-3))
            
        # Delta cross-track
        # Printed in [m]
            dn = np.append(dn, s_unpack[11 * i + 13] * 0.4 * 10 ** (-3))
            
        # Dot delta radial
        # Printed in [mm/s]
            dot_dr = np.append(dot_dr, s_unpack[11 * i + 14] * 0.001)
            
        # Dot delta along-track
        # Printed in [mm/s]
            dot_dt = np.append(dot_dt, s_unpack[11 * i + 15] * 0.004)
                
        # Dot delta along-track, DF369, Range: +-1.048572[m/s],
        # Res: 0.004[mm/s]
        # Printed in [mm/s]
            dot_dn = np.append(dot_dn, s_unpack[11 * i + 16] * 0.004)
            
        # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s^2]) 
            dc0 = np.append(dc0, s_unpack[11 * i + 17] * 0.1    )  
            dc1 = np.append(dc1, s_unpack[11 * i + 18] * 0.001  )  
            dc2 = np.append(dc2, s_unpack[11 * i + 19] * 0.00002)  

        self.dr = dr
        self.dt = dt
        self.dn = dn
        
        self.dot_dr = dot_dr
        self.dot_dt = dot_dt
        self.dot_dn = dot_dn
        
        self.dc0 = dc0*1e-3
        self.dc1 = dc1
        self.dc2 = dc2
        
        self.gnss_id  = gps_id
        self.gnss_iod = gps_iod
        self.p = p
        
# *************************************************************************** #
#                                                                             #
#                       GPS Code Bias Message Type 1059                       #
#                                                                             #
# *************************************************************************** #
class gps_code_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        header = 'u12u20u4u1u4u16u4u6'
            
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
        
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes+3bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 

        # satellite parameters initialization
        gps_id = []
        number  = []
        track  = []
        bias   = []
        name   = []
            
        n_types = 0
        bit_sat   = 'u6u5'
           
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # GPS ID number,      
            if s_unpack[2 * i + 2 * n_types + 8] < 10:
                gps_id = np.append(gps_id, '0' +
                                   f'{s_unpack[2 * i + 2 * n_types +  8]}')
            else:
                gps_id = np.append(gps_id,
                                   f'{s_unpack[2 * i + 2 * n_types +  8]}')
            
        # N. of Code Biases Processed, DF379, Range: 0-31, Res: 1
            number = np.append(number, s_unpack[2 * i + 2 * n_types + 9])
            track.append([])
            bias.append([]) 
            name.append([])
            bit_track = 'u5s14'
            for j in range(s_unpack[2 * i + 2 * n_types + 9]):
                t_unpack = bitstruct.unpack(header + bit_sat + bit_track,
                                            message)
            # Track indicator, DF380, Range: 0-31, Res: 1
                track[i].append(t_unpack[2 * i + 2 * n_types + 10 + j * 2])
            # Signal name
                GNSS = 'GPS'
                name[i].append(signalID.signals(GNSS,
                               t_unpack[2 * i + 2 * n_types + 10 + j * 2]))
            # Code bias, DF383, Range: +-81.91[m], Res: 0.01[m]
                bias[i].append(t_unpack[2 * i + 2 * n_types + 11 +
                                            j * 2] * 0.01)
                if j < s_unpack[2 * i + 2 * n_types + 9] - 1:
                    bit_track = bit_track + 'u5s14'
            n_types = n_types + s_unpack[2 * i + 2 * n_types + 9]    
            bit_sat = bit_sat + bit_track  + 'u6u5'
            
        self.gnss_id = gps_id
        self.number = number
        self.track = track
        self.name  = name 
        self.bias = bias
                     

# *************************************************************************** #
#                                                                             #
#                          GPS Orbits Message Type 1057                       #
#                                                                             #
# *************************************************************************** #
class gps_orbit:
    def __init__(self, message):
        # Definition of the bits of the header for the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header
        unpack_bits = bitstruct.unpack(header, message)
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
        
        # GPS Epoch Time 1s
        self.epoch = unpack_bits[1]
        
        # SSR Update Interval 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 
        
        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # Satellite Reference Datum
        self.datum = unpack_bits[4]
        
        # IOD SSR
        self.iod = unpack_bits[5]
        
        # SSR Provider ID
        self.provider_id = unpack_bits[6]
        
        # SSR Solution ID
        self.solution_id = unpack_bits[7]
        
        # Number of Satellites
        self.n_sat  = unpack_bits[8]

        # ******************************************************************* #
        #    total number of bits considered so far: 68 -> 8 bytes + 4 bits   #
        # ******************************************************************* #
        #                                                                     # 
        #                            ORBITS part                              #
        #                                                                     #
        # ******************************************************************* #
        
        # GPS orbit parameter initilization
        GPS_ID                = []
        GPS_IODE              = []
        delta_radial          = []
        delta_along_track     = []
        delta_cross_track     = []
        dot_delta_radial      = []
        dot_delta_along_track = []
        dot_delta_cross_track = []
        
        # Satellite specific part of message
        bit_sat  = self.n_sat * 'u6u8s22s20s20s21s19s19' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            if s_unpack[8 * i + 9] < 10:
                GPS_ID = np.append(GPS_ID, '0' + f'{s_unpack[8 * i + 9]}')
            else:
                GPS_ID = np.append(GPS_ID, f'{s_unpack[8 * i + 9]}')

            # u8 = DF071 GPS IODE
            GPS_IODE = np.append(GPS_IODE, s_unpack[8 * i + 10])
            
            # s22 = DF365 Delta Radial
            delta_radial = np.append(delta_radial, s_unpack[8 * i + 11])
            # convert from string to int and change units to meters
            delta_radial[i] = float(delta_radial[i]) / 10000
            
            # s20 = DF366 Delta Along-Track
            delta_along_track = np.append(delta_along_track,
                                          s_unpack[8 * i + 12])
            # convert from string to int and change units to meters
            delta_along_track[i] = float(delta_along_track[i]) / 2500
            
            # s20 = DF367 Delta Cross-Track
            delta_cross_track = np.append(delta_cross_track,
                                          s_unpack[8 * i + 13])
            # convert from string to int and change units to meters
            delta_cross_track[i] = float(delta_cross_track[i]) / 2500
            
            # s21 = DF368 Dot Delta Radial
            dot_delta_radial = np.append(dot_delta_radial,
                                         s_unpack[8 * i + 14])
            # convert from string to int and change units to meters
            dot_delta_radial[i] = float(dot_delta_radial[i]) / 10000
            
            # s19 = DF369 Dot Delta Along-Track
            dot_delta_along_track = np.append(dot_delta_along_track,
                                              s_unpack[8 * i + 15])
            # convert from string to int and change units to meters
            dot_delta_along_track[i] = float(dot_delta_along_track[i]) / 10000
            
            # s19 = DF370 Dot Delta Cross-Track 
            dot_delta_cross_track = np.append(dot_delta_cross_track,
                                              s_unpack[8 * i + 16])
            # convert from string to int and change units to meters
            dot_delta_cross_track[i] = float(dot_delta_cross_track[i]) / 10000

        self.dr = delta_radial
        self.dt = delta_along_track
        self.dn = delta_cross_track
        
        self.dot_dr = dot_delta_radial
        self.dot_dt = dot_delta_along_track 
        self.dot_dn = dot_delta_cross_track
        
        self.gnss_id = GPS_ID
        self.gnss_iod = GPS_IODE

# *************************************************************************** #
#                                                                             #
#                         GPS Clock Message Type 1058                         #
#                                                                             #
# *************************************************************************** #
class gps_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
            
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)

        self.gnss = 'GPS'
        self.gnss_short = 'G'        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes+3bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        # satellite parameters initialization
        GPS_ID = []
        Dcl_A0 = []
        Dcl_A1 = []
        Dcl_A2 = []
            
        bit_sat = self.n_sat * 'u6s22s21s27'                 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
            # GPS ID number 
            if s_unpack[4 * i + 8] < 10:
                GPS_ID = np.append(GPS_ID, '0' + f'{s_unpack[4 * i + 8]}')
            else:
                GPS_ID = np.append(GPS_ID, f'{s_unpack[4 * i + 8]}')
            # Delta Clock C0
            # Printed in [m]
            Dcl_A0 = np.append(Dcl_A0, s_unpack[4 * i + 9] * 0.1 *
                                   10 ** (-3))
            
            # Delta Clock C1
            # Printed in [mm/s]
            Dcl_A1 = np.append(Dcl_A1, s_unpack[4 * i + 10] * 0.001)
            
            # Delta Clock C2
            # Printed in [mm/s^2]
            Dcl_A2 = np.append(Dcl_A2, s_unpack[4 * i + 11] * 0.00002)
        
        self.gnss_id = GPS_ID
        self.dc0 = Dcl_A0
        self.dc1 = Dcl_A1
        self.dc2 = Dcl_A2
        
# *************************************************************************** #
#                                                                             #
#                          GPS URA Message Type 1061                          #
#                                                                             #
# *************************************************************************** #
class gps_ura:
    def __init__(self, message):
        # SSR User Range Accuracy (URA) (1 sigma)
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
            
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes+3bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GPS_ID = []
        URA = []
        URA_class = []
        URA_value = []
            
        bit_sat = self.n_sat * 'u6u3u3' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
        # GPS ID number,  
            if s_unpack[3 * i + 8] < 10:
                GPS_ID = np.append(GPS_ID, '0' + f'{s_unpack[3 * i + 8]}')
            else:
                GPS_ID = np.append(GPS_ID, f'{s_unpack[3 * i + 8]}')
            # SSR URA, DF389, Range: bits 5 – 3: 0 – 7
            #                        bits 2 – 0: 0 – 7
            URA_class = np.append(URA_class, s_unpack[3 * i + 9])
            URA_value = np.append(URA_value, s_unpack[3 * i + 10])
            URA = np.append(URA, ((pow(3, URA_class[i]) * (1 +
                            (URA_value[i] / 4))) - 1) / 1000)
        self.gnss_id = GPS_ID
        self.ura = URA
        self.ura_class = URA_class
        self.ura_value = URA_value
            
# *************************************************************************** #
#                                                                             #
#                       SSR GPS Phase Bias Message 1265                       #
#                                                                             #
# *************************************************************************** #
class gps_phase_bias:
    def __init__(self, message):
        # SSR User Range Accuracy (URA) (1 sigma)
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u1u1u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'GPS'
        self.gnss_short = 'G'
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Dispersive bias consistency indicator
        self.disp_bias = unpack_bits[7]
            
        # MW consistency indicator
        self.mw = unpack_bits[8]

        # Number of satellites
        self.n_sat = unpack_bits[9]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 69-> 8bytes+5bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GPS_ID = []
        num_phase = []
        yaw_angle = []
        yaw_rate = []
            
        track = []
        signal_int = []
        signal_WL = []
        signal_name = []
        signal_dis = []
        phase_bias = []
             
        n_types = 0
        bit_sat   = 'u6u5u9s8'  
           
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # GPS sat ID number     
            if s_unpack[4 * i + 5 * n_types + 10] < 10:
                GPS_ID = np.append(GPS_ID, '0' +
                                       f'{s_unpack[4 * i + 5 * n_types + 10]}')
            else:
                GPS_ID = np.append(GPS_ID,
                                       f'{s_unpack[4 * i + 5 * n_types + 10]}')  
            # N. of Phase Biases Processed
            num_phase = np.append(num_phase,
                                  s_unpack[4 * i + 5 * n_types + 11])
            # Yaw Angle
            # Printed in [deg]
            yaw_angle = np.append(yaw_angle,
                                  (s_unpack[4 * i +
                                            5 * n_types + 
                                            12] * 1 / 256) * 180)           
            # Yaw Rate
            # Printed in [deg/s]
            yaw_rate = np.append(yaw_rate,
                                 (s_unpack[4 * i +
                                           5 * n_types +
                                           13] * 1 / 8192) * 180)
        # ******************************************************************* #
        #                                                                     # 
        #            Phase specific part of the satellite considered          #
        #                                                                     #
        # ******************************************************************* # 
        # phase parameters initialization
            track.append([])
            signal_int.append([])
            signal_WL.append([])
            signal_name.append([])
            signal_dis.append([])
            phase_bias.append([])
                
            bit_phase = 'u5u1u2u4s20'
            for j in range(s_unpack[4 * i + 5 * n_types + 11]):
                p_unpack = bitstruct.unpack(header + 
                                            bit_sat + bit_phase, message)
            
            # Track indicator
                track[i].append(p_unpack[4 * i + 5 * n_types + 14 + j * 5])
            
            # Signal_name:
                GNSS_ID = 'GPS'
                signal_name[i].append(signalID.signals(GNSS_ID,
                                      p_unpack[4 * i + 
                                               5 * n_types + 14 + j * 5]))
                        
            # Signal integer indicator,
                signal_int[i].append(p_unpack[4 * i + 5 * n_types + 15 + 
                                              j * 5])
            
            # Signal wide-lane integer indicator
                signal_WL[i].append(p_unpack[4 * i + 5 * n_types + 
                                             16 + j * 5])
            
            # Signal discontinuity counter
                signal_dis[i].append(p_unpack[4 * i + 5 * n_types + 17 +
                                              j * 5])
            
            # PHASE BIAS
                phase_bias[i].append(p_unpack[4 * i + 5 * n_types + 18 +
                                              j * 5] * 0.0001)

                if j < s_unpack[4 * i + 5 * n_types + 11] - 1:
                    bit_phase = bit_phase + 'u5u1u2u4s20'
                        
            n_types = n_types + s_unpack[4 * i + 5 * n_types + 11]    
            bit_sat = bit_sat + bit_phase  + 'u6u5u9s8'
                          
            self.gnss_id = GPS_ID           
            self.number = num_phase
            self.yaw_angle = yaw_angle
            self.yaw_rate = yaw_rate
            self.track = track
            self.name = signal_name
            self.bias = phase_bias
            self.sig_wl = signal_WL
            self.sig_dis = signal_dis
            self.sig_i = signal_int                 

# =============================================================================
#                                 GLONASS
# =============================================================================
# *************************************************************************** #
#                                                                             #
#               GLONASS Satellite Ephemeris data Message Type 1020            #
#                                                                             #
# *************************************************************************** #
class glo_ephemeris:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header1 = 'u12u6u5u1u1u2u5u6u1u1u1u7'
        header2 = 'u1u23u1u26u1u4u1u23u1u26u1u4u1u23u1u26u1u4'
        header3 = 'u1u1u10u2u1u1u21u1u4u5u1u4u11u2u1u11u1u31u5u1u21u1u7'
            
        header = header1 + header2 + header3
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Satellite ID
        if unpack_bits[1] < 10:
            GLO  = 'R' + '0' + f'{unpack_bits[1]}'
        else:
            GLO  = 'R' + f'{unpack_bits[1]}'
        
        self.sat_id = GLO
        # GLONASS sate freq chan numb [-7...13]
        self.freq = unpack_bits[2] -7
        
        # GLONASS almanac healthy availability
        self.bn   = unpack_bits[4]
        
        # GLONASS almanach healthy
        if self.bn == 0:
            self.cn = 'n/a'
        elif self.bn == 1:
            self.cn   = unpack_bits[3]    
        
        # GLONASS P1
        self.p1   = unpack_bits[5]
            
        # GLONASS tk, first 5 bits: integer number of hours, next six bits
        # integer number of minutes, LSb number of thirty seconds interval
        tk_h = unpack_bits[6]
        tk_m = unpack_bits[7]
        tk_s = unpack_bits[8]
            
        self.tk   = tk_h * 3600 + tk_m * 60 + tk_s * 30
        
        # GLONASS MSb of Bn word
        self.msb_bn = unpack_bits[9]
            
        # GLONASS P2
        self.p2   = unpack_bits[10]
            
        # GLONASS tb
        # Printed in [s]
        self.tb   = unpack_bits[11] * 15 * 60  # [s]
            
        # GLONASS xn(tb), first derivative
        if unpack_bits[12] == 0:
            d_xn =  unpack_bits[13] * 2 ** (-20)
        else:
            d_xn = -unpack_bits[13] * 2 ** (-20)
        self.dxn = d_xn
        
        # GLONASS xn(tb)
        if unpack_bits[14] == 0:
            xn =  unpack_bits[15] * 2 ** (-11)
        else:
            xn = -unpack_bits[15] * 2 ** (-11)            
        self.xn = xn
        
        # GLONASS xn(tb)
        if unpack_bits[16] == 0:
            d2_xn =  unpack_bits[17] * 2 ** (-30)
        else:
            d2_xn = -unpack_bits[17] * 2 ** (-30)
        self.ddxn = d2_xn
        
        # GLONASS yn(tb)
        if unpack_bits[18] == 0:
            d_yn  =  unpack_bits[19] * 2 ** (-20)
        else:
            d_yn  = -unpack_bits[19] * 2 ** (-20)  
        self.dyn = d_yn
        
        # GLONASS yn(tb)
        if unpack_bits[20] == 0:
            yn  =  unpack_bits[21] * 2 ** (-11)
        else:
            yn  = -unpack_bits[21] * 2 ** (-11)  
        self.yn = yn   
        
        # GLONASS yn(tb)
        if unpack_bits[22] == 0:
            d2_yn  =  unpack_bits[23] * 2 ** (-30)
        else:
            d2_yn  = -unpack_bits[23] * 2 ** (-30)
        self.ddyn = d2_yn
        
        # GLONASS zn(tb)
        if unpack_bits[24] == 0:
            d_zn  =  unpack_bits[25] * 2 ** (-20)
        else:
            d_zn  = -unpack_bits[25] * 2 ** (-20)  
        self.dzn = d_zn
        
        # GLONASS zn(tb)
        if unpack_bits[26] == 0:
            zn  =  unpack_bits[27] * 2 ** (-11)
        else:
            zn  = -unpack_bits[27] * 2 ** (-11)  
        self.zn = zn
        
        # GLONASS zn(tb)
        if unpack_bits[28] == 0:
            d2_zn  =  unpack_bits[29] * 2 ** (-30)
        else:
            d2_zn  = -unpack_bits[29] * 2 ** (-30)
        self.ddzn = d2_zn
        
        # GLONASS P3
        self.p3   = unpack_bits[30]
        
        # GLONASS gamma(tb)
        if unpack_bits[31] == 0:
            self.gamma  =  unpack_bits[32] * 2 ** (-40)
        else:
            self.gamma  = -unpack_bits[32] * 2 ** (-40)
        
        # GLONASS-M P, Range 0-3
        self.p    = unpack_bits[33]
        
        # GLONASS-M ln third string
        self.ln_t   = unpack_bits[34]

        # GLONASS tau_n
        if unpack_bits[35] == 0:
            self.tau  =  unpack_bits[36] * 2 ** (-30)
        else:
            self.tau  = -unpack_bits[36] * 2 ** (-30)
        
        # GLONASS dtau_n
        if unpack_bits[37] == 0:
            self.dtau  =  unpack_bits[38] * 2 ** (-30)
        else:
            self.dtau  = -unpack_bits[38] * 2 ** (-30)
        
        # GLONASS En
        self.en   =  unpack_bits[39]
        
        # GLONASS P4
        self.p4 = unpack_bits[40]
            
        # GLONASS-M Ft
        self.ft   = unpack_bits[41]
        
        # GLONASS-M Nt
        self.nt = unpack_bits[42]

        # GLONASS-M M
        self.m   = unpack_bits[43]
        
        # GLONASS Availability additional data
        self.ava   = unpack_bits[44]
        
        # GLONASS N_A
        self.n_a   = unpack_bits[45]
            
        # GLONASS tau_c
        if self.ava == 0:
            self.tau_c = 0
        
        else:
            if unpack_bits[46] == 0:
                self.tau_c  =  unpack_bits[47] * 2 ** (-31)
            else:
                self.tau_c  = -unpack_bits[47] * 2 ** (-31)

        # GLONASS-M N4
        self.n4 = unpack_bits[48]
        
        # GLONASS-M tau_gps 
        if unpack_bits[49] == 0:
            self.tau_gps  =  unpack_bits[50] * 2 ** (-20)
        else:
            self.tau_gps  = -unpack_bits[50] * 2 ** (-20)
            
        # GLONASS-M ln fifth string
        self.ln_f   = unpack_bits[51]
            
# *************************************************************************** #
#                                                                             #
#                  GLONASS Orbit Correction Message Type 1063                 #
#                                                                             #
# *************************************************************************** #
class glo_orbit:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 65-> 8bytes + 1bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        GLO_ID  = []
        GLO_IOD = []
        p       = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        bit_sat = self.n_sat * 'u5u8s22s20s20s21s19s19' 
        bit_GLO_check = self.n_sat * 'u5u1u7s22s20s20s21s19s19'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        R_check = bitstruct.unpack(header + bit_GLO_check, message)
        for i in range(self.n_sat):
        # GLONASS ID number,
            if s_unpack[8 * i + 9] < 10:
                GLO_ID = np.append(GLO_ID, '0' + f'{s_unpack[8 * i +  9]}')
            else:
                GLO_ID = np.append(GLO_ID, f'{s_unpack[8 * i +  9]}')
            # GLONASS IOD: Issue Of Data of GLONASS ephemeris to reference 
            # the geometric gradients 
            GLO_IOD = np.append(GLO_IOD, s_unpack[8 * i + 10])

            p = np.append(p, R_check[9 * i +  10])
                   
            # Delta radial
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[8 * i + 11] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[8 * i + 12] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[8 * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[8 * i + 14] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[8 * i + 15] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[8 * i + 16] * 0.004)

            self.gnss_id = GLO_ID
            self.gnss_iod = GLO_IOD
            self.dr = D_r
            self.dt = D_t
            self.dn = D_n
            self.dot_dr = dot_D_r
            self.dot_dt = dot_D_t
            self.dot_dn = dot_D_n
            self.p = p
# *************************************************************************** #
#                                                                             #
#                     GLONASS Clock Message Type 1064                         #
#                                                                             #
# *************************************************************************** #
class glo_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])]  

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ------> total number of bits considered so far: 64-> 8bytes <------ #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GLO_ID = []
        Dcl_C0 = []
        Dcl_C1 = []
        Dcl_C2 = []
            
        bit_sat = self.n_sat * 'u5s22s21s27' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            # GLONASS ID number,  
            if s_unpack[4 * i + 8] < 10:
                GLO_ID = np.append(GLO_ID, '0' + f'{s_unpack[4 * i + 8]}')
            else:
                GLO_ID = np.append(GLO_ID, f'{s_unpack[4 * i + 8]}')
                            
            # Delta Clock C0
            Dcl_C0 = np.append(Dcl_C0, s_unpack[4 * i + 
                                                9] * 0.1 * 10 ** (-3))
            
            # Delta Clock C1
            # Printed in [mm/s]
            Dcl_C1 = np.append(Dcl_C1, s_unpack[4 * i + 10] * 0.001)
            
            # Delta Clock C2
            # Printed in [mm/s^2]
            Dcl_C2 = np.append(Dcl_C2, s_unpack[4 * i + 11] * 0.00002)
  
        self.gnss_id = GLO_ID
        self.dc0 = Dcl_C0
        self.dc1 = Dcl_C1
        self.dc2 = Dcl_C2
            
# *************************************************************************** #
#                                                                             #
#                     GLONASS Code Bias Message Type 1065                     #
#                                                                             #
# *************************************************************************** #
class glo_code_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ------> total number of bits considered so far: 64-> 8bytes <------ #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 

        # satellite parameters initialization
        GLO_ID = []
        types  = []
        track  = []
        bias   = []
        name   = []
            
        n_types = 0
        bit_sat   = 'u5u5'
            
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # GLONASS ID number
            if s_unpack[2 * i + 2 * n_types + 8] < 10:
                   GLO_ID = np.append(GLO_ID, '0' +
                                      f'{s_unpack[2 * i + 2 * n_types + 8]}')
            else:
                GLO_ID = np.append(GLO_ID,
                                   f'{s_unpack[2 * i + 2 * n_types + 8]}')
            # N. of Code Biases Processed
            types = np.append(types,
                              s_unpack[2 * i + 2 * n_types + 9])
            track.append([])
            bias.append([])
            name.append([])
            bit_track = 'u5s14'
            for j in range(s_unpack[2 * i + 2 * n_types + 9]):
                t_unpack = bitstruct.unpack(header + 
                                            bit_sat + bit_track, message)
            # Track indicator
                track[i].append(t_unpack[2 * i + 2 * n_types + 10 + j * 2])
            # Signal name
                GNSS = 'GLONASS'
                name[i].append(signalID.signals(GNSS,
                               t_unpack[2 * i + 2 * n_types + 10 + j * 2]))
            # Code bias
                bias[i].append(t_unpack[2 * i + 2 * n_types + 11 +
                                            j * 2] * 0.01)
                if j < s_unpack[2 * i + 2 * n_types + 9] - 1:
                    bit_track = bit_track + 'u5s14'
            n_types = n_types + s_unpack[2 * i + 2 * n_types + 9]    
            bit_sat = bit_sat + bit_track  + 'u5u5'
        
        self.gnss_id = GLO_ID
        self.number = types
        self.name = name
        self.bias = bias
        self.track = track

# *************************************************************************** #
#                                                                             #
#   SSR GLONASS combined Orbit and Clock Correction Message Type 1066         #
#                                                                             #
# *************************************************************************** #
class glo_orbit_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 65-> 8bytes + 1bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        GLO_ID  = []
        GLO_IOD = []
            
        p = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        D_C0 = []
        D_C1 = []
        D_C2 = []
            
        bit_sat   = self.n_sat * 'u5u8s22s20s20s21s19s19s22s21s27'
        bit_GLO_check   = self.n_sat * 'u5u1u7s22s20s20s21s19s19s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        R_check = bitstruct.unpack(header + bit_GLO_check, message)
        for i in range(self.n_sat):
            # GPS ID number
            if s_unpack[11 * i + 9] < 10:
                GLO_ID = np.append(GLO_ID, '0' + f'{s_unpack[11 * i + 9]}')
            else:
                GLO_ID = np.append(GLO_ID, f'{s_unpack[11 * i + 9]}')
                                    
            # GPS IOD: Issue Of Data of GPS ephemeris to reference 
            # the geometric gradients 
            GLO_IOD = np.append(GLO_IOD, s_unpack[11 * i + 10])
                
            p = np.append(p, R_check[12 * i + 10])               
                   
            # Delta radial
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[11 * i + 11] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[11 * i + 12] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[11 * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[11 * i + 14] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[11 * i + 15] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[11 * i + 16] * 0.004)
            
            # Delta clock C0, C1, C2, [mm], [mm/s], [mm/s**2]
            D_C0 = np.append(D_C0, s_unpack[11 * i + 17] * 0.1    ) 
            D_C1 = np.append(D_C1, s_unpack[11 * i + 18] * 0.001  ) 
            D_C2 = np.append(D_C2, s_unpack[11 * i + 19] * 0.00002)

        self.gnss_id = GLO_ID
        self.gnss_iod = GLO_IOD
        self.dr = D_r
        self.dn = D_n
        self.dt = D_t
        self.dot_dr = dot_D_r
        self.dot_dn = dot_D_n
        self.dot_dt = dot_D_t
        self.dc0 = D_C0 * 1e-3
        self.dc1 = D_C1
        self.dc2 = D_C2
        self.p = p
        
# *************************************************************************** #
#                                                                             #
#                     GLONASS SV URA Message Type 1067                        #
#                                                                             #
# *************************************************************************** #
class glo_ura:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ------> total number of bits considered so far: 64-> 8bytes <------ #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GLO_ID = []
        URA    = []
        URA_CLASS = []
        URA_VALUE = []
                           
        bit_sat = self.n_sat * 'u5u3u3'
        s_unpack = bitstruct.unpack(header + bit_sat, message)

        for i in range(self.n_sat):
            # GLONASS ID number       
            if s_unpack[3 * i + 8] < 10:
                GLO_ID = np.append(GLO_ID, '0' + f'{s_unpack[3 * i + 8]}')
            else:
                GLO_ID = np.append(GLO_ID, f'{s_unpack[3 * i + 8]}')
                
            # SSR URA
            # URA_CLASS
            Class = s_unpack[3 * i + 9]
            URA_CLASS = np.append(URA_CLASS, Class)

            # URA_VALUE 
            Value = s_unpack[3 * i + 10]
            URA_VALUE = np.append(URA_VALUE, Value)

            if (Value == 0) & (Class == 0):
                print('URA undefined/unknown')
            elif (Value == 7) & (Class == 7):
                print('URA > 5466.5 [mm]')
            # The URA is computed by the following expression:
            # Printed in [m]
            URA = np.append(URA, (3 ** (Class) * (1 + Value / 4) -
                                      1) / 1000)                
            self.ura = URA
            self.ura_class = URA_CLASS
            self.ura_value = URA_VALUE
            self.gnss_id = GLO_ID
            
# *************************************************************************** #
#                                                                             #
#                     SSR GLONASS Phase Bias Message 1266                     #
#                                                                             #
# *************************************************************************** #            
class glo_phase_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u17u4u1u4u16u4u1u1u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'GLONASS'
        self.gnss_short = 'R'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GLONASS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]
        
        # Dispersive Bias Consistency indicator
        self.disp_bias   = unpack_bits[7]
            
        # MW Consistency Indicator
        self.mw     = unpack_bits[8]
            
        # Number of satellites
        self.n_sat     = unpack_bits[9]

        # ******************************************************************* #
        # ------> total number of bits considered so far: 66-> 8bytes + 2 <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        # satellite parameters initialization
        GLO_ID = []
        Nphase = []
        YA     = []
        YR     = []
        # phase parameters initialization
        GLO_ST = []
        SII    = []
        w      = []
        dis    = []
        bias   = []               
        signal_name = []
            
        bit_sat = 'u5u5u9s8' 
        n_phase = 0
        for i in range(self.n_sat):               
            s_unpack = bitstruct.unpack(header + bit_sat, message)
                
            # GLONASS ID number       
            if s_unpack[4 * i + 5 * n_phase + 10] < 10:
                GLO_ID = np.append(GLO_ID, '0' +
                                   f'{s_unpack[4 * i + 5 * n_phase + 10]}')
            else:
                GLO_ID = np.append(GLO_ID,
                                   f'{s_unpack[4 * i + 5 * n_phase + 10]}')  
            # No. of Phase Biases Processed
            Nphase = np.append(Nphase, s_unpack[4 * i + 5 * n_phase + 11])
                
            # Yaw Angle, DF480
            # Printed in [deg]
            YA = np.append(YA, (s_unpack[4 * i + 5 * n_phase +
                                         12] * 1 / 256) * 180)
            # YAW Rate
            # Printed in [deg/s]
            YR = np.append(YR, (s_unpack[4 * i + 5 * n_phase + 
                                         13] * 1 / 8192) * 180)                

        # ******************************************************************* #
        #                                                                     # 
        #            Phase specific part of the satellite considered          #
        #                                                                     #
        # ******************************************************************* # 
        # phase parameters initialization
            GLO_ST.append([])
            SII.append([])
            w.append([])
            signal_name.append([])
            dis.append([])
            bias.append([])
               
            bit_phase = 'u5u1u2u4s20' 
            
            for j in range(s_unpack[4 * i + 5 * n_phase + 11]): 
                p_unpack = bitstruct.unpack(header + bit_sat +
                                            bit_phase, message)
                
                # GLONASS Signal and Tracking Mode Indicator       
                GLO_ST[i].append(p_unpack[4 * i + 5 * n_phase +
                                          5 * j + 14])
                # Signal_name:
                GNSS_ID = 'GLONASS'
                signal_name[i].append(signalID.signals(GNSS_ID,
                                      p_unpack[4 * i + 
                                               5 * n_phase + 5 * j + 14]))
                # Signal Integer Indicator
                SII[i].append(p_unpack[4 * i + 5 * n_phase + 5 * j + 15])
             
                # Signals Wide-Lane Integer Indicator
                w[i].append(p_unpack[4 * i + 5 * n_phase + 5 * j + 16])
            
                # Signal Discontinuity Counter
                dis[i].append(p_unpack[4 * i + 5 * n_phase + 5 * j + 17])
                 
                # Phase Bias
                bias[i].append(p_unpack[4 * i + 5 * n_phase +
                                        5 * j + 18] * 0.0001)

                if j < s_unpack[4 * i + 5 * n_phase + 11] - 1:
                    bit_phase = bit_phase + 'u5u1u2u4s20'
                        
            n_phase = n_phase + s_unpack[4 * i + 5 * n_phase + 11]                         
            bit_sat = bit_sat + bit_phase + 'u5u5u9s8'   
            
            self.gnss_id = GLO_ID
            self.yaw_angle = YA
            self.yaw_rate = YR
            self.number = Nphase
            self.bias = bias
            self.name = signal_name
            self.track = GLO_ST
            self.sig_i = SII
            self.sig_wl = w
            self.sig_dis = dis

# =============================================================================
#                                Galileo
# =============================================================================
# *************************************************************************** #
#                                                                             #
#           GALILEO Satellite Ephemeris F/NAV data Message Type 1045           #
#                                                                             #
# *************************************************************************** #
class gal_ephemeris_fnav:
    def __init__(self, message):
        # Define constants
        pie = 3.1415926535898
        # Definition of the bits of the message
        contents = 'u12u6u12u10u8s14u14s6s21s31s16s16s32s16u32s16u32u14s16' + \
                   's32s16s32s16s32s24s10u2u1u7'
        unpack_bits = bitstruct.unpack(contents, message)
        self.gnss = 'Galileo F/NAV'
        self.gnss_short = 'E'
    
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the message number, hence it is not considered here
        
        # Galileo satellite ID
        sat_ID = unpack_bits[1]
        # formatting
        sat_ID = str(sat_ID)
        if len(sat_ID) < 2:
            self.sat_id = 'E0' + sat_ID
        else:
            self.sat_id = 'E' + sat_ID
        
        # Galileo week number
        self.week = unpack_bits[2]
        
        # Galileo IODnav 
        self.iod = unpack_bits[3]
        
        # Galileo SV SISA
        self.sisa = unpack_bits[4]
        
        # Rate of Inclination Angle
        self.idot = unpack_bits[5] * pow(2, -43) * pie
               
        # Galileo toc
        self.toc = unpack_bits[6] * 60
        
        # Galileo af2
        self.af_two = unpack_bits[7] * pow(2, -59)
        
        # Galileo af1
        self.af_one = unpack_bits[8] * pow(2, -46)
        
        # Galileo af0
        self.af_zero = unpack_bits[9] * pow(2, -34)
            
        # Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
        self.crs = unpack_bits[10] * pow(2, -5)
        
        # Mean Motion Difference from Computed Value
        self.dn = unpack_bits[11] * pow(2, -43) * pie
        
        # Mean Anomaly at Reference Time
        self.m0 = unpack_bits[12] * pow(2, -31) * pie
        
        # Galileo cuc
        self.cuc = unpack_bits[13] * pow(2, -29)
        
        # Galileo eccentricity (e)
        self.ecc = unpack_bits[14] * pow(2, -33)
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Argument of Latitude
        self.cus = unpack_bits[15] * pow(2, -29)
        
        # Square Root of the Semi-Major Axis
        self.root_a = unpack_bits[16] * pow(2, -19)
        
        # Reference Time Ephemeris
        self.toe = unpack_bits[17] * 60
        
        # Amplitude of the Cosine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cic = unpack_bits[18] * pow(2, -29)
        
        # Longitude of Ascending Node of Orbit Plane at Weekly Epoch (omega_0)
        self.omega_0 = unpack_bits[19] * pow(2, -31) * pie
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cis = unpack_bits[20] * pow(2, -29)
    
        # Inclination Angle at Reference Time
        self.i0 = unpack_bits[21] * pow(2, -31) * pie
        
        # Amplitude of the Cosine Harmonic Correction Term to the Orbit Radius
        self.crc = unpack_bits[22] * pow(2, -5)
        
        # Galileo argument of perigee (w) 
        self.omega = unpack_bits[23] * pow(2, -31) * pie
        
        # Rate of Right Ascension
        self.omega_dot = unpack_bits[24] * pow(2, -43) * pie
        
        # Galileo BGD E1/E5 broadcast group delay
        self.bgd_a = unpack_bits[25] * pow(2, -32)
        self.bgd_b = 0
        
        # Galileo SV health, 0 is ok
        self.health = unpack_bits[26]
        
        # Galileo Nav Data Validity status
        self.validity = unpack_bits[27]
        
## *************************************************************************** #
##                                                                             #
##           GALILEO Satellite Ephemeris I/NAVdata Message Type 1046           #
##                                                                             #
## *************************************************************************** #
class gal_ephemeris_inav:
    def __init__(self, message):
        # Define constants
        pie = 3.1415926535898
        # Definition of the bits of the message
        contents = 'u12u6u12u10u8s14u14s6s21s31s16s16s32s16u32s16u32u14s16' + \
                   's32s16s32s16s32s24s10s10u2u1u2u1u2'
        
        unpack_bits = bitstruct.unpack(contents, message)
        
        self.gnss = 'Galileo I/NAV'
        self.gnss_short = 'E'
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the message number, hence it is not considered here
        
        # Galileo satellite ID
        sat_ID = unpack_bits[1]
        # formatting
        sat_ID = str(sat_ID)
        if len(sat_ID) < 2:
            self.sat_id = 'E0' + sat_ID
        else:
            self.sat_id = 'E' + sat_ID
        
        # Galileo week number
        self.week = unpack_bits[2]
       
        # Galileo IODnav 
        self.iod = unpack_bits[3]
        
        # Galileo SV SISA
        self.sisa = unpack_bits[4]
        
        # Rate of Inclination Angle
        self.idot = unpack_bits[5] * pow(2, -43) * pie
               
        # Galileo toc
        self.toc = unpack_bits[6] * 60
        
        # Galileo af2
        self.af_two = unpack_bits[7] * pow(2, -59)        
        # Galileo af1
        self.af_one = unpack_bits[8] * pow(2, -46)
        # Galileo af0
        self.af_zero = unpack_bits[9] * pow(2, -34)
            
        # Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
        self.crs = unpack_bits[10] * pow(2, -5)
        
        # Mean Motion Difference from Computed Value
        self.dn = unpack_bits[11] * pow(2, -43) * pie
        
        # Mean Anomaly at Reference Time
        self.m0 = unpack_bits[12] * pow(2, -31) * pie
        
        # Galileo cuc
        self.cuc = unpack_bits[13] * pow(2, -29)
        
        # Galileo eccentricity (e)
        self.ecc = unpack_bits[14] * pow(2, -33)
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Argument of Latitude
        self.cus = unpack_bits[15] * pow(2, -29)
        
        # Square Root of the Semi-Major Axis
        self.root_a = unpack_bits[16] * pow(2, -19)
        
        # Reference Time Ephemeris
        self.toe = unpack_bits[17] * 60
        
        # Amplitude of the Cosine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cic = unpack_bits[18] * pow(2, -29)
        
        # Longitude of Ascending Node of Orbit Plane at Weekly Epoch (omega_0)
        self.omega_0 = unpack_bits[19] * pow(2, -31) * pie
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cis = unpack_bits[20] * pow(2, -29)
    
        # Inclination Angle at Reference Time
        self.i0 = unpack_bits[21] * pow(2, -31) * pie
        
        # Amplitude of the Cosine Harmonic Correction Term to the Orbit Radius
        self.crc = unpack_bits[22] * pow(2, -5)
        
        # Galileo argument of perigee (w) 
        self.omega = unpack_bits[23] * pow(2, -31) * pie
        
        # Rate of Right Ascension
        self.omega_dot = unpack_bits[24] * pow(2, -43) * pie
        
        # Galileo BGD E5a/E1 broadcast group delay
        self.bgd_a = unpack_bits[25] * pow(2, -32)
        
        # Galileo BGD E5b/E1 broadcast group delay
        self.bgd_b = unpack_bits[26] * pow(2, -32)        
        
        # E1-B Health 
        self.health = unpack_bits[27] 
        
        # E1-B validity 
        self.e1b_v = unpack_bits[28] 
                        
# *************************************************************************** #
#                                                                             #
#                  SSR Galileo Orbit Correction Message Type 1240             #
#                                                                             #
# *************************************************************************** #
class gal_orbit:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        # Satellite ref Datum 
        self.datum = unpack_bits[4]
            
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        GAL_ID  = []
        GAL_IOD = []
        p       = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        bit_sat = self.n_sat * 'u6u10s22s20s20s21s19s19' 
        bit_GAL_check = self.n_sat * 'u6u1u9s22s20s20s21s19s19'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        E_check = bitstruct.unpack(header + bit_GAL_check, message)
        for i in range(self.n_sat): 
        # Galileo ID number,   
            if s_unpack[8 * i +  9] < 10:
                GAL_ID = np.append(GAL_ID, '0' + f'{s_unpack[8 * i + 9]}')
            else:
                GAL_ID = np.append(GAL_ID, f'{s_unpack[8 * i + 9]}')
                
            # Galileo IOD: Issue Of Data of Galileo ephemeris to reference 
            GAL_IOD = np.append(GAL_IOD, s_unpack[8 * i + 10])
    
            p = np.append(p, E_check[9 * i + 11])
                   
            # Delta radial (printed in [m])
            D_r = np.append(D_r, s_unpack[8 * i + 11] * 0.1 * 10 ** (-3))
            # Delta along-track (printed in [m])
            D_t = np.append(D_t, s_unpack[8 * i + 12] * 0.4 * 10 ** (-3))
            # Delta cross-track (printed in [m]
            D_n = np.append(D_n, s_unpack[8 * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial (printed in [mm/s])
            dot_D_r = np.append(dot_D_r, s_unpack[8 * i + 14] * 0.001)
            # Dot delta along-track (printed in [mm/s])
            dot_D_t = np.append(dot_D_t, s_unpack[8 * i + 15] * 0.004)
            # Dot delta along-track (printed in [mm/s])
            dot_D_n = np.append(dot_D_n, s_unpack[8 * i + 16] * 0.004)
    
        self.dr = D_r
        self.dt = D_t
        self.dn = D_n
        self.dot_dr = dot_D_r
        self.dot_dt = dot_D_t
        self.dot_dn = dot_D_n
        
        self.gnss_id = GAL_ID
        self.gnss_iod = GAL_IOD
        
# *************************************************************************** #
#                                                                             #
#                   Galileo Clock Correction Message Type 1241                #
#                                                                             #
# *************************************************************************** #
class gal_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])]  

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes + 3bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization 
        GAL_ID  = []
                        
        D_C0 = []
        D_C1 = []
        D_C2 = []  

        bit_sat  = self.n_sat * 'u6s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            # Galileo ID number     
            if s_unpack[4 * i + 8] < 10:
                GAL_ID = np.append(GAL_ID, '0' + f'{s_unpack[4 * i + 8]}')
            else:
                GAL_ID = np.append(GAL_ID, f'{s_unpack[4 * i + 8]}')
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[4 * i +  9] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[4 * i + 10] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[4 * i + 11] * 0.00002)  

        self.dc0 = D_C0
        self.dc1 = D_C1
        self.dc2 = D_C2
        
        self.gnss_id
            
# *************************************************************************** #
#                                                                             #
#                   SSR Galileo Code Bias Message Type 1242                   #
#                                                                             #
# *************************************************************************** #
class gal_code_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
                    
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 65-> 8bytes + 1bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization 
        GAL_ID  = []
        n_bias = []
                        
        S_TMI = []
        types = []
        Cd_bias = []
        cdb = 0
        bit_sat_0 = 'u6u5'
        bit_sat   = bit_sat_0
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # Galileo ID number,       
            if s_unpack[2 * i + 2 * cdb + 8] < 10:
                GAL_ID = np.append(GAL_ID, '0' +
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
            else:
                GAL_ID = np.append(GAL_ID,
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
                
            # number of signals
            n_bias = np.append(n_bias, s_unpack[2 * i + 2 * cdb + 9])
                
            # ********************************************************* #
            #                                                           # 
            #                   Signal part                             #
            #                                                           #
            # ********************************************************* #                
            bit_sig_0 = 'u5s14'
            bit_sig   = bit_sig_0  
            S_TMI.append([])
            Cd_bias.append([])
            types.append([])

            for j in range(s_unpack[2 * i + 2 * cdb + 9]):
                sig_unpack = bitstruct.unpack(header + bit_sat +
                                              bit_sig, message)
            # Signal and tracking mode identifier   
                GNSS_ID = 'Galileo'
                types[i].append(sig_unpack[2 * i + 2 * cdb +  2 * j + 10])               
                S_TMI[i].append(signalID.signals(GNSS_ID, 
                                sig_unpack[2 * i + 2 * cdb +  2 * j + 10]))
            # signal code bis
                Cd_bias[i].append(sig_unpack[2 * i + 2 * cdb +
                                             2 * j + 11] * 0.01)
                                            
                if j < s_unpack[2 * i + 2 * cdb + 9] - 1: 
                    bit_sig = bit_sig + bit_sig_0
                            
            cdb = cdb + s_unpack[2 * i + 2 * cdb + 9]               
            bit_sat = bit_sat + bit_sig + bit_sat_0                       
            
            self.number = n_bias
            self.name = S_TMI
            self.track = types
            self.bias  = Cd_bias
            
            self.gnss_id = GAL_ID
            
# *************************************************************************** #
#                                                                             #
#    Galileo SSR combined Orbit and Clock Correction Message Type 1243        #
#                                                                             #
# *************************************************************************** #
class gal_orbit_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])]  

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        GAL_ID  = []
        GAL_IOD = []
            
        p = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        D_C0 = []
        D_C1 = []
        D_C2 = []
            
        bit_sat = self.n_sat * 'u6u10s22s20s20s21s19s19s22s21s27'
        bit_GAL_check = self.n_sat * 'u6u1u9s22s20s20s21s19s19s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        E_check = bitstruct.unpack(header + bit_GAL_check, message)
        for i in range(self.n_sat):
        # Galileo ID number,       
            if s_unpack[11 * i + 9] < 10:
                GAL_ID = np.append(GAL_ID, '0' + f'{s_unpack[11 * i + 9]}')
            else:
                GAL_ID = np.append(GAL_ID, f'{s_unpack[11 * i + 9]}')
                    
            # Galileo IOD: Issue Of Data of Galileoephemeris to reference 
            # the geometric gradients 
            GAL_IOD = np.append(GAL_IOD, s_unpack[11 * i + 10])
                
            p = np.append(p, E_check[12 * i + 10])               
                   
            # Delta radial (printed in [m])
            D_r = np.append(D_r, s_unpack[11 * i + 11] * 0.1 * 10 ** (-3))
            # Delta along-track (printed in [m])
            D_t = np.append(D_t, s_unpack[11 * i + 12] * 0.4 * 10 ** (-3))
            # Delta cross-track (printed in [m])
            D_n = np.append(D_n, s_unpack[11 * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial (printed in [mm/s])
            dot_D_r = np.append(dot_D_r, s_unpack[11 * i + 14] * 0.001)
            # Dot delta along-track (printed in [mm/s])
            dot_D_t = np.append(dot_D_t, s_unpack[11 * i + 15] * 0.004)
            # Dot delta along-track (printed in [mm/s])
            dot_D_n = np.append(dot_D_n, s_unpack[11 * i + 16] * 0.004)
            
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[11 * i + 17] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[11 * i + 18] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[11 * i + 19] * 0.00002)  

        self.dr = D_r
        self.dt = D_t
        self.dn = D_n
        self.dot_dr = dot_D_r
        self.dot_dt = dot_D_t
        self.dot_dn = dot_D_n
        self.dc0 = D_C0 * 1e-3
        self.dc1 = D_C1
        self.dc2 = D_C2
        
        self.gnss_id = GAL_ID
        self.gnss_iod = GAL_IOD
        self.p = p
# *************************************************************************** #
#                                                                             #
#                     SSR Galileo URA Message Type 1244                       #
#                                                                             #
# *************************************************************************** #   
class gal_ura:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes + 3 bits<-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        # satellite parameters initialization
        GAL_ID = []
        URA    = []
        URA_CLASS = []
        URA_VALUE = []
                           
        bit_sat = self.n_sat * 'u5u3u3' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
        # Galileo SSR ID number       
            if s_unpack[3 * i + 8] < 10: 
                GAL_ID = np.append(GAL_ID, '0' + f'{s_unpack[3 * i + 8]}')
            else:
                GAL_ID = np.append(GAL_ID, f'{s_unpack[3 * i + 8]}')
                
            # SSR URA
            # URA_CLASS 
            Class = s_unpack[3 * i + 9]
            URA_CLASS = np.append(URA_CLASS, Class)

            # URA_VALUE 
            Value = s_unpack[3 * i + 10]
            URA_VALUE = np.append(URA_VALUE, Value)

            if (Value == 0) & (Class == 0):
                print('URA undefined/unknown')
            elif (Value == 7) & (Class == 7):
                print('URA > 5466.5 [mm]')
            # The URA is computed by the following expression:
            # Printed in [m]
            URA = np.append(URA, (3 ** (Class) * (1 + Value / 4) -
                                  1) / 1000)                
        
        self.ura = URA
        self.ura_class = URA_CLASS
        self.ura_value = URA_VALUE
        
        self.gnss_id = GAL_ID
    
# *************************************************************************** #
#                                                                             #
#             SSR Galileo High Rate Clock Correction Message Type 1245        #
#                                                                             #
# *************************************************************************** #
class gal_hr_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # Galileo Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes +3 bits <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GAL_ID   = []
        HR_clock = []
                           
        bit_sat = self.n_sat * 'u6s22'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            # Galileo ID number       
            if s_unpack[2 * i + 8] < 10:
                GAL_ID = np.append(GAL_ID, '0' + f'{s_unpack[2 * i + 8]}')
            else:
                GAL_ID = np.append(GAL_ID, f'{s_unpack[2 * i + 8]}')
                    
            # High-rate clock correction
            HR_clock = np.append(HR_clock, s_unpack[2 * i +
                                                        9] * 0.1 * 1e-3)             
        self.gnss_id = GAL_ID
        self.hr_clk = HR_clock
        
# *************************************************************************** #
#                                                                             #
#                    SSR Galileo Phase Bias Message 1267                      #
#                                                                             #
# *************************************************************************** #
class gal_phase_bias:
    def __init__(self, message):
        # SSR User Range Accuracy (URA) (1 sigma)
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u1u1u6'
            
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        self.gnss = 'Galileo'
        self.gnss_short = 'E'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Dispersive bias consistency indicator
        self.disp_bias = unpack_bits[7]
            
        # MW consistency indicator
        self.mw = unpack_bits[8]

        # Number of satellites
        self.n_sat = unpack_bits[9]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 69-> 8bytes+5bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        GAL_ID = []
        num_phase = []
        yaw_angle = []
        yaw_rate = []
            
        track = []
        signal_int = []
        signal_WL = []
        signal_dis = []
        phase_bias = []
        signal_name = [] 
        n_types = 0
        bit_sat   = 'u6u5u9s8'  
           
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            
            # Galileo sat ID number 
            if s_unpack[4 * i + 5 * n_types + 10] < 10:
                GAL_ID = np.append(GAL_ID, '0' +
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')
            else:
                GAL_ID = np.append(GAL_ID,
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')    
            # N. of Phase Biases Processed
            num_phase = np.append(num_phase,
                                  s_unpack[4 * i + 5 * n_types + 11])
                
            # Yaw Angle
            # Printed in [deg]
            yaw_angle = np.append(yaw_angle,
                                  (s_unpack[4 * i + 5 * n_types +
                                            12] * 1 / 256) * 180)
            
            # Yaw Rate
            # Printed in [deg/s]
            yaw_rate = np.append(yaw_rate, 
                                 (s_unpack[4 * i + 5 * n_types +
                                           13] * 1 / 8192) * 180)

        # ******************************************************************* #
        #                                                                     # 
        #            Phase specific part of the satellite considered          #
        #                                                                     #
        # ******************************************************************* # 
        # phase parameters initialization
            track.append([])
            signal_int.append([])
            signal_WL.append([])
            signal_dis.append([])
            signal_name.append([])
            phase_bias.append([])
                
            bit_phase = 'u5u1u2u4s20' 

            for j in range(s_unpack[4 * i + 5 * n_types + 11]):
                p_unpack = bitstruct.unpack(header +
                                            bit_sat + bit_phase, message)
            
            # Track indicator
                track[i].append(p_unpack[4 * i + 5 * n_types + 14 + j * 5])
            # Signal_name:
                GNSS_ID = 'Galileo'
                signal_name[i].append(signalID.signals(GNSS_ID,
                                                       p_unpack[4 * i +
                                                                5 * 
                                                                n_types +
                                                                14 +
                                                                j * 5]))
            # Signal integer indicator
                signal_int[i].append(p_unpack[4 * i + 5 * n_types +
                                              15 + j * 5])
            
            # Signal wide-lane integer indicator
                signal_WL[i].append(p_unpack[4 * i + 5 * n_types +
                                             16 + j * 5])
            
            # Signal discontinuity counter
                signal_dis[i].append(p_unpack[4 * i + 5 * n_types +
                                              17 + j * 5])
            
            # PHASE BIAS
                phase_bias[i].append(p_unpack[4 * i + 5 * n_types +
                                              18 + j * 5] * 0.0001)

                if j < s_unpack[4 * i + 5 * n_types + 11] - 1:
                    bit_phase = bit_phase + 'u5u1u2u4s20'
                        
            n_types = n_types + s_unpack[4 * i + 5 * n_types + 11]    
            bit_sat = bit_sat + bit_phase  + 'u6u5u9s8'
            
        self.number = num_phase
        self.track = track
        self.name = signal_name
        self.bias = phase_bias
        self.sig_wl = signal_WL
        self.sig_i  = signal_int
        self.sig_dis = signal_dis
        
        self.gnss_id = GAL_ID
        self.yaw_angle = yaw_angle
        self.yaw_rate = yaw_rate

# =============================================================================
#                                   BeiDou
# =============================================================================

# *************************************************************************** #
#                                                                             #
#                      Beidou Satellite Ephemeris Type 1042                   #
#                                                                             #
# *************************************************************************** #
class bds_ephemeris:
    def __init__(self, message):
        # Define constants
        pie = 3.1415926535898
        # Definition of the bits of the message
        contents = 'u12u6u13u4s14u5u17s11s22s24u5s18s16s32s18u32s18u32u17' + \
                   's18s32s18s32s18s32s24s10s10u1'
        
        unpack_bits = bitstruct.unpack(contents, message)
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the message number, hence it is not considered here
        
        # Beidou satellite ID
        sat_ID = unpack_bits[1]
        # formatting
        sat_ID = str(sat_ID)
        if len(sat_ID) < 2:
            self.sat_id = 'C0' + sat_ID
        else:
            self.sat_id = 'C' + sat_ID
        
        # Beidou week number. 
        self.week    = unpack_bits[2]

        # Beidou SV URAI 
        self.ura    = unpack_bits[3]

        # Rate of Inclination Angle
        self.idot    = unpack_bits[4] * pow(2, -43) * pie
        
        # Beidou AODE
        self.aode    = unpack_bits[5]
        
        # Beidou toc
        self.toc     = unpack_bits[6] * 8
        
        # Beidou af2
        self.af_two  = unpack_bits[7] * pow(2, -66)
        
        # Beidou af1
        self.af_one  = unpack_bits[8] * pow(2, -50)
        
        # Beidou af0
        self.af_zero = unpack_bits[9] * pow(2, -33)
        
        # Beidou AODC
        self.aodc    = unpack_bits[10]
        
        # Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
        self.crs     = unpack_bits[11] * pow(2,  -6)
        
        # Mean Motion Difference from Computed Value
        self.dn      = unpack_bits[12] * pow(2, -43) * pie
        
        # Mean Anomaly at Reference Time
        self.m0      = unpack_bits[13] * pow(2, -31) * pie
        
        # cuc
        self.cuc     = unpack_bits[14] * pow(2, -31)
        
        # eccentricity (e)
        self.ecc     = unpack_bits[15] * pow(2, -33)
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Argument of Latitude
        self.cus     = unpack_bits[16] * pow(2, -31)
        
        # Square Root of the Semi-Major Axis
        self.root_a  = unpack_bits[17] * pow(2, -19)
        
        # Reference Time Ephemeris
        self.toe = unpack_bits[18] * 8
        
        # Amplitude of the Cosine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cic = unpack_bits[19] * pow(2, -31)
        
        # Longitude of Ascending Node of Orbit Plane at Weekly Epoch (omega_0)
        self.omega_0 = unpack_bits[20] * pow(2, -31) * pie
        
        # Amplitude of the Sine Harmonic Correction Term
        # to the Angle of Inclination
        self.cis = unpack_bits[21] * pow(2, -31)
    
        # Inclination Angle at Reference Time
        self.i0 = unpack_bits[22] * pow(2, -31) * pie
        
        # Amplitude of the Cosine Harmonic Correction Term to the Orbit Radius
        self.crc = unpack_bits[23] * pow(2, -6)
        
        #  argument of perigee (w) 
        self.omega = unpack_bits[24] * pow(2, -31) * pie
        
        # Rate of Right Ascension
        self.omega_dot = unpack_bits[25] * pow(2, -43) * pie
        
        # Beidou TGD1 group delay differential
        self.tgd1 = unpack_bits[26] * 0.1 * 1e-9        
        
        # Beidou TGD2 group delay differential
        self.tgd2 = unpack_bits[27] * 0.1 * 1e-9     
        
        # BDS SV Health
        self.health = unpack_bits[28]

# *************************************************************************** #
#                                                                             #
#                   Beidou SSR Orbit Correction Message Type 1258             #
#                                                                             #
# *************************************************************************** #
class bds_orbit:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # Beidou Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
                    
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        BDS_ID  = []
        BDS_IOD = []
        BDS_toe = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        bit_sat = self.n_sat * 'u6u10u24s22s20s20s21s19s19' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat): 
            # Beidou ID number,       
            if s_unpack[9 * i + 8] < 10:
                BDS_ID = np.append(BDS_ID, '0' + f'{s_unpack[9 * i + 8]}')
            else:
                BDS_ID = np.append(BDS_ID, f'{s_unpack[9 * i + 8]}')
                
            # Beidou toe Modulo 
            BDS_toe = np.append(BDS_toe, s_unpack[9 * i + 9] * 8)
            # Beidou IOD: Issue Of Data Beidou ephemeris to reference 
            BDS_IOD = np.append(BDS_IOD, s_unpack[9 * i + 10])
            # Delta radial
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[9 * i + 11] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[9 * i + 12] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[9 * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[9 * i + 14] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[9 * i + 15] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[9 * i + 16] * 0.004)

            self.gnss_id = BDS_ID
            self.gnss_iod = BDS_IOD
            self.toe = BDS_toe
            
            self.dr = D_r
            self.dn = D_n
            self.dt = D_t
            
# *************************************************************************** #
#                                                                             #
#                   Beidou Clock Correction Message Type 1259                 #
#                                                                             #
# *************************************************************************** #
class bds_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # BDS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])]  

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes + 3bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #                     
        # satellite parameters initialization 
        BDS_ID  = []                        
        D_C0 = []
        D_C1 = []
        D_C2 = []  

        bit_sat = self.n_sat * 'u6s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
                
        for i in range(self.n_sat):
            # Beidou ID number
            if s_unpack[4 * i + 8] < 10:
                BDS_ID = np.append(BDS_ID, '0' + f'{s_unpack[4 * i + 8]}')
            else:
                BDS_ID = np.append(BDS_ID, f'{s_unpack[4 * i + 8]}')
                
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[4 * i +  9] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[4 * i + 10] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[4 * i + 11] * 0.00002)  
    
        self.gnss_id = BDS_ID
        
        self.dc0 = D_C0
        self.dc1 = D_C1
        self.dc2 = D_C2
            
# *************************************************************************** #
#                                                                             #
#                   SSR Beidou Code Bias Message Type 1260                    #
#                                                                             #
# *************************************************************************** #
class bds_code_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        # **************************** Parameters *************************** #  
        # unpack_bits[0] is the type, hence it is not considered here
        # Beidou Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
                    
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 65-> 8bytes + 1bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization 
        n_bias = []
        BDS_ID = []
        S_TMI = []
        types = []
        Cd_bias = []
        cdb = 0
        bit_sat_0 = 'u6u5'
        bit_sat   = bit_sat_0
        
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # Beidou ID number
            if s_unpack[2 * i + 2 * cdb + 8] < 10:
                BDS_ID = np.append(BDS_ID, '0' + 
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
            else:
                BDS_ID = np.append(BDS_ID,
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
                
            # number of signals
            n_bias = np.append(n_bias, s_unpack[2 * i + 2 * cdb + 9])
                
            # ********************************************************* #
            #                                                           # 
            #                   Signal part                             #
            #                                                           #
            # ********************************************************* #                
            bit_sig_0 = 'u5s14'
            bit_sig   = bit_sig_0  
            S_TMI.append([])
            Cd_bias.append([])
            types.append([])
                
            for j in range(s_unpack[2 * i + 2 * cdb + 9]):
                sig_unpack = bitstruct.unpack(header + bit_sat +
                                              bit_sig, message)
                # Signal and tracking mode identifier   
                GNSS_ID = 'BDS'
                S_TMI[i].append(signalID.signals(GNSS_ID,
                                sig_unpack[2 * i + 2 * cdb +  2 * j + 10]))
                types[i].append(sig_unpack[2 * i + 2 * cdb +  2 * j + 10])
                # signal code bis
                Cd_bias[i].append(sig_unpack[2 * i + 2 * cdb + 
                                   2 * j + 11] * 0.01)
                                            
                if j < s_unpack[2 * i + 2 * cdb + 9] - 1:
                            bit_sig = bit_sig + bit_sig_0
                            
            cdb = cdb + s_unpack[2 * i + 2 * cdb + 9]               
            bit_sat = bit_sat + bit_sig + bit_sat_0                       
            
            self.gnss_id = BDS_ID
            self.number = n_bias
            self.track = types
            self.name = S_TMI
            self.bias = Cd_bias
            
# *************************************************************************** #
#                                                                             #
#    SSR Beidou combined Orbit and Clock Correction Message Type 1261         #
#                                                                             #
# *************************************************************************** #
class bds_orbit_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # Beidou Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        BDS_ID  = []
        BDS_IOD = []
            
        BDS_toe = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        D_C0 = []
        D_C1 = []
        D_C2 = []
            
        bit_sat = self.n_sat * 'u6u10u24s22s20s20s21s19s19s22s21s27'
            
        # number of parameters
        n = 12
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):      
            # Beidou ID number
            if s_unpack[n * i + 9] < 10:
                BDS_ID = np.append(BDS_ID, '0' + f'{s_unpack[n * i + 9]}')
            else:
                BDS_ID = np.append(BDS_ID, f'{s_unpack[n * i + 9]}')
            # BDS toe Modulo
            BDS_toe = np.append(BDS_toe, s_unpack[n * i + 10] * 8)
            # Beidou IOD: Issue Of Data of QZSS ephemeris to reference 
            # the geometric gradients 
            BDS_IOD = np.append(BDS_IOD, s_unpack[n * i + 11])
                   
            # Delta radial 
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[n * i + 12] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[n * i + 13] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[n * i + 14] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[n * i + 15] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[n * i + 16] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[n * i + 17] * 0.004)
            
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[n * i + 18] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[n * i + 19] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[n * i + 20] * 0.00002)  
                                
            self.gnss_id = BDS_ID
            self.gnss_iod = BDS_IOD
            self.toe = BDS_toe
            self.dr = D_r
            self.dn = D_n
            self.dt = D_t
            self.dot_dr = dot_D_r
            self.dot_dn = dot_D_n
            self.dot_dt = dot_D_t
            self.dc0 = D_C0 * 1e-3
            self.dc1 = D_C1
            self.dc2 = D_C2
                
# *************************************************************************** #
#                                                                             #
#                     SSR Beidou URA Message Type 1262                        #
#                                                                             #
# *************************************************************************** #
class bds_ura:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # Beidou Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes +3 bits <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        BDS_ID = []
        URA    = []
        URA_CLASS = []
        URA_VALUE = []
                           
        bit_sat = self.n_sat * 'u6u3u3'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
            # Beidou ID number
            if s_unpack[3 * i + 8] < 10:
                BDS_ID = np.append(BDS_ID, '0' + f'{s_unpack[3 * i + 8]}')
            else:
                BDS_ID = np.append(BDS_ID, f'{s_unpack[3 * i + 8]}')
                
            # SSR URA
            # URA_CLASS 
            Class = s_unpack[3 * i + 9]
            URA_CLASS = np.append(URA_CLASS, Class)

            # URA_VALUE 
            Value = s_unpack[3 * i + 10]
            URA_VALUE = np.append(URA_VALUE, Value)

            if (Value == 0) & (Class == 0):
                print('URA undefined/unknown')
            elif (Value == 7) & (Class == 7):
                print('URA > 5466.5 [mm]')
            # The URA is computed by the following expression:
            # Printed in [m]
            URA = np.append(URA, (3 ** (Class) * (1 + Value / 4) -
                                  1) / 1000)                
            
            self.gnss_id = BDS_ID
            self.ura = URA
            self.ura_class = URA_CLASS
            self.ura_value = URA_VALUE

# *************************************************************************** #
#                                                                             #
#              SSR Beidou High Rate Clock COrrection Message Type 1263        #
#                                                                             #
# *************************************************************************** #
class bds_hr_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # BDS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes +3 bits <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        BDS_ID   = []
        HR_clock = []
                           
        bit_sat = self.n_sat * 'u6s22'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
        # Beidou ID number
            if s_unpack[2 * i + 8] < 10:
                BDS_ID = np.append(BDS_ID, '0' + f'{s_unpack[2 * i + 8]}')
            else:
                BDS_ID = np.append(BDS_ID, f'{s_unpack[2 * i + 8]}')
                
            # High-rate clock correction
                HR_clock = np.append(HR_clock,
                                     s_unpack[2 * i + 9] * 0.1 * 1e-3)             
                               
        self.gnss_id = BDS_ID
        self.hr_clock = HR_clock
           
# *************************************************************************** #
#                                                                             #
#                      Beidou Phase Bias Message Type 1270                    #
#                                                                             #
# *************************************************************************** #
class bds_phase_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u1u1u6'
            
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'BDS'
        self.gnss_short = 'C'
        # **************************** Parameters *************************** #        
        # unpack_bits[0] is the type, hence it is not considered here            
        # Beidou Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Dispersive bias consistency indicator
        self.disp_bias = unpack_bits[7]
            
        # MW consistency indicator
        self.mw = unpack_bits[8]

        # Number of satellites
        self.n_sat = unpack_bits[9]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 69-> 8bytes+5bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        BDS_ID = []
        num_phase = []
        yaw_angle = []
        yaw_rate = []
            
        track = []
        signal_int = []
        signal_WL = []
        signal_name = []
        signal_dis = []
        phase_bias = []
             
        n_types = 0
        bit_sat_0   = 'u6u5u9s8'
        bit_sat     = bit_sat_0
            
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            # BDS sat ID number     
            if s_unpack[4 * i + 5 * n_types + 10] < 10:
                BDS_ID = np.append(BDS_ID, '0' + 
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')
            else:
                BDS_ID = np.append(BDS_ID, 
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')  
            # N. of Phase Biases Processed
            num_phase = np.append(num_phase, 
                                  s_unpack[4 * i + 5 * n_types + 11])
                
            # Yaw Angle
            # Printed in [deg]
            yaw_angle = np.append(yaw_angle, 
                                  (s_unpack[4 * i + 
                                            5 * n_types +
                                            12] * 1 / 256) * 180)
            # Yaw Rate
            # Printed in [deg/s]
            yaw_rate = np.append(yaw_rate, (s_unpack[4 * i + 
                                                     5 * n_types +
                                                     13] * 1 / 8192) * 180)

        # ******************************************************************* #
        #                                                                     # 
        #            Phase specific part of the satellite considered          #
        #                                                                     #
        # ******************************************************************* # 
        # phase parameters initialization
            track.append([])
            signal_int.append([])
            signal_WL.append([])
            signal_name.append([])
            signal_dis.append([])
            phase_bias.append([])
                
            bit_phase_0 = 'u5u1u2u4s20' 
            bit_phase   = bit_phase_0
            for j in range(s_unpack[4 * i + 5 * n_types + 11]):
                p_unpack = bitstruct.unpack(header + 
                                            bit_sat +
                                            bit_phase, message)

            # Track indicator
                track[i].append(p_unpack[4 * i + 5 * n_types + 14 + j * 5])

            # Signal_name:
                GNSS_ID = 'BDS'
                signal_name[i].append(signalID.signals(GNSS_ID, 
                                          p_unpack[4 * i + 
                                                   5 * n_types + 14 + j * 5]))
            
            # Signal integer indicator
                signal_int[i].append(p_unpack[4 * i + 5 * n_types +
                                              15 + j * 5])
            
            # Signal wide-lane integer indicator
                signal_WL[i].append(p_unpack[4 * i + 5 * n_types +
                                             16 + j * 5])
            
            # Signal discontinuity counter
                signal_dis[i].append(p_unpack[4 * i + 5 * n_types +
                                              17 + j * 5])
            
            # PHASE BIAS
                phase_bias[i].append(p_unpack[4 * i + 5 * n_types + 18 +
                                                  j * 5] * 0.0001)

                if j < s_unpack[4 * i + 5 * n_types + 11] - 1:
                    bit_phase = bit_phase + bit_phase_0
                        
            n_types = n_types + s_unpack[4 * i + 5 * n_types + 11]    
            bit_sat = bit_sat + bit_phase  + bit_sat_0

            self.gnss_id = BDS_ID           
            self.number = num_phase
            self.yaw_angle = yaw_angle
            self.yaw_rate = yaw_rate
            self.track = track
            self.name = signal_name
            self.bias = phase_bias
            self.sig_wl = signal_WL
            self.sig_dis = signal_dis
            self.sig_i = signal_int  

# =============================================================================
#                                   QZSS
# =============================================================================

# *************************************************************************** #
#                                                                             #
#                        QZSS Satellite Ephemeris Type 1044                   #
#                                                                             #
# *************************************************************************** #
class qzs_ephemeris:
    def __init__(self, message):
        # Define constants
        pie = 3.1415926535898
        # Definition of the bits of the message
        contents = 'u12u4u16s8s16s22u8s16s16s32s16u32s16u32u16s16s32s16s' + \
                   '32s16s32s24s14u2u10u4u6s8u10u1'
        
        unpack_bits = bitstruct.unpack(contents, message)
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the message number, hence it is not considered here
        
        # QZSS satellite ID
        sat_ID = unpack_bits[1]
        # formatting
        sat_ID = str(sat_ID + 192)
        if len(sat_ID) < 2:
            self.sat_id = 'J0' + sat_ID
        else:
            self.sat_id = 'J' + sat_ID
        
        # QZSS toc
        self.toc     = unpack_bits[2] * pow(2,   4)
        
        # QZSS af2
        self.af_two  = unpack_bits[3] * pow(2, -55)
        
        # QZSS af1
        self.af_one  = unpack_bits[4] * pow(2, -43)
        
        # QZSS af0
        self.af_zero = unpack_bits[5] * pow(2, -31)
        
        # QZSS IODE
        self.iode    = unpack_bits[6]
        
        # Amplitude of the Sine Harmonic Correction Term to the Orbit Radius
        self.crs     = unpack_bits[7] * pow(2,  -5)
        
        # Mean Motion Difference from Computed Value
        self.dn      = unpack_bits[8] * pow(2, -43) * pie
        
        # Mean Anomaly at Reference Time
        self.m0      = unpack_bits[9] * pow(2, -31) * pie
        
        #  cuc
        self.cuc     = unpack_bits[10] * pow(2, -29)
        
        #  eccentricity (e)
        self.ecc     = unpack_bits[11] * pow(2, -33)
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Argument of Latitude
        self.cus     = unpack_bits[12] * pow(2, -29)
        
        # Square Root of the Semi-Major Axis
        self.root_a  = unpack_bits[13] * pow(2, -19)
        
        # Reference Time Ephemeris
        self.toe     = unpack_bits[14] * pow(2,   4)
        
        # Amplitude of the Cosine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cic     = unpack_bits[15] * pow(2, -29)
        
        # Longitude of Ascending Node of Orbit Plane at Weekly Epoch (omega_0)
        self.omega_0  = unpack_bits[16] * pow(2, -31) * pie
        
        # Amplitude of the Sine Harmonic Correction Term 
        # to the Angle of Inclination
        self.cis     = unpack_bits[17] * pow(2, -29)
    
        # Inclination Angle at Reference Time
        self.i0      = unpack_bits[18] * pow(2, -31) * pie
        
        # Amplitude of the Cosine Harmonic Correction Term to the Orbit Radius
        self.crc     = unpack_bits[19] * pow(2,  -5)
        
        # Argument of perigee (w) 
        self.omega   = unpack_bits[20] * pow(2, -31) * pie
        
        # Rate of Right Ascension
        self.omega_dot = unpack_bits[21] * pow(2, -43) * pie
        
        # Rate of Inclination Angle
        self.idot      = unpack_bits[22] * pow(2, -43) * pie
        
        # QZSS Codes on L2 Channel
        self.cl2 = unpack_bits[23]
        
        # QZSS week number
        self.week = unpack_bits[24] + 1024

        # QZSS URA 
        self.ura = unpack_bits[25]
        
        # QZSS SV Health
        self.health = unpack_bits[26]
        
        # QZSS TGD group delay differential
        self.tgd = unpack_bits[27] * pow(2, -31)     
        
        # QZSS IODC
        self.iodc = unpack_bits[28]
        
        # QZSS fit interval
        self.interval = unpack_bits[29]
        
# *************************************************************************** #
#                                                                             #
#                   QZSS SSR Orbit Correction Message Type 1246               #
#                                                                             #
# *************************************************************************** #
class qzs_orbit:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # QZSS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 
        
        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
                    
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        QZS_ID  = []
        QZS_IOD = []

        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        bit_sat = self.n_sat * 'u4u8s22s20s20s21s19s19' 
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        n = 8
        for i in range(self.n_sat):
            #  ID number,       
            if s_unpack[n * i +  8] < 10:
                QZS_ID = np.append(QZS_ID, s_unpack[n * i + 8])
            else:
                QZS_ID = np.append(QZS_ID, f'{s_unpack[n * i + 8]}')
                    
            #  IOD: Issue Of Data ephemeris to reference 
            QZS_IOD = np.append(QZS_IOD, s_unpack[n * i + 10])
                
            # Delta radial
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[n * i + 11] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[n * i + 12] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[n * i + 13] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[n * i + 14] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[n * i + 15] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[n * i + 16] * 0.004)
                
            self.gnss_id = QZS_ID
            self.gnss_iod = QZS_IOD
            self.dr = D_r
            self.dn = D_n
            self.dt = D_t
            self.dot_dr = dot_D_r
            self.dot_dn = dot_D_n
            self.dot_dt = dot_D_t
            
# *************************************************************************** #
#                                                                             #
#                     QZSS Clock Correction Message Type 1247                 #
#                                                                             #
# *************************************************************************** #
class qzs_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # BDS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes + 3bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization 
        QZS_ID  = []
        D_C0 = []
        D_C1 = []
        D_C2 = []  

        bit_sat = self.n_sat * 'u4s22s21s27'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            # QZSS ID number       
            if s_unpack[4 * i + 8] < 10:
                QZS_ID = np.append(QZS_ID, '0' + f'{s_unpack[4*i +  8]}')
            else:
                QZS_ID = np.append(QZS_ID, f'{s_unpack[4*i +  8]}')
                    
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[4 * i +  9] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[4 * i + 10] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[4 * i + 11] * 0.00002)  

        self.gnss = QZS_ID
        self.dc0 = D_C0
        self.dc1 = D_C1
        self.dc2 = D_C2
            
# *************************************************************************** #
#                                                                             #
#                   SSR QZSS Code Bias Message Type 1248                      #
#                                                                             #
# *************************************************************************** #
class qzs_code_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        # **************************** Parameters *************************** #
        
        # unpack_bits[0] is the type, hence it is not considered here
        # QZSS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
                    
        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 67-> 8bytes + 3bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization 
        QZS_ID  = []
        n_bias = []
                        
        S_TMI = []
        Cd_bias = []
        types = []
        cdb = 0
        bit_sat_0 = 'u4u5'
        bit_sat   = bit_sat_0
        
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
                # QZSS ID number
            if s_unpack[2 * i + 2 * cdb + 8] < 10:
                QZS_ID = np.append(QZS_ID, '0' + 
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
            else:
                QZS_ID = np.append(QZS_ID, 
                                   f'{s_unpack[2 * i + 2 * cdb + 8]}')
            # number of signals
            n_bias = np.append(n_bias, 
                                  s_unpack[2 * i + 2 * cdb + 9])
                
            # ********************************************************* #
            #                                                           # 
            #                   Signal part                             #
            #                                                           #
            # ********************************************************* #                
            bit_sig_0 = 'u5s14'
            bit_sig   = bit_sig_0  
            S_TMI.append([])
            Cd_bias.append([])
            types.append([])
                
            for j in range(s_unpack[2 * i + 2 * cdb + 9]):
                sig_unpack = bitstruct.unpack(header + 
                                              bit_sat + bit_sig, message)
                # Signal and tracking mode identifier   
                GNSS_ID = 'QZSS'
                    
                types[i].append(sig_unpack[2 * i + 
                                2 * cdb +  2 * j +  10])
                S_TMI[i].append(signalID.signals(GNSS_ID, 
                                sig_unpack[2 * i + 2 * cdb +  2 * j + 10]))
                                       
                Cd_bias[i].append(sig_unpack[2 * i + 2 * cdb +
                                             2 * j +  11] * 0.01)
                                            
                if j < s_unpack[2 * i + 2 * cdb + 9] - 1:
                    bit_sig = bit_sig + bit_sig_0
                            
            cdb = cdb + s_unpack[2 * i + 2 * cdb + 9]               
            bit_sat = bit_sat + bit_sig + bit_sat_0                       
            
            self.gnss_id = QZS_ID
            self.number = n_bias
            self.track = types
            self.bias = Cd_bias
            self.name = S_TMI
            
# *************************************************************************** #
#                                                                             #
#      SSR QZSS combined Orbit and Clock Correction Message Type 1249         #
#                                                                             #
# *************************************************************************** #
class qzs_orbit_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)           
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # QZSS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
            
        # Satellite Reference Datum    
        self.datum = f'{unpack_bits[4]}'
        
        # IOD SSR
        self.iod = unpack_bits[5]

        # SSR Provider ID
        self.provider_id = unpack_bits[6]

        # SSR Solution ID
        self.solution_id = unpack_bits[7]

        # Number of satellites
        self.n_sat = unpack_bits[8]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 68-> 8bytes + 4bit <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* #             
        
        # satellite parameters initialization
        QZS_ID  = []
        QZS_IOD = []
            
        D_r = []
        D_t = []
        D_n = []
            
        dot_D_r = []
        dot_D_t = []
        dot_D_n = []
            
        D_C0 = []
        D_C1 = []
        D_C2 = []
            
        bit_sat = self.n_sat * 'u4u8s22s20s20s21s19s19s22s21s27'
            
        # number of parameters
        n = 11
        s_unpack = bitstruct.unpack(header + bit_sat, message)
        for i in range(self.n_sat):
            # QZSS ID number,  
            if s_unpack[n * i + 9] < 10:
                QZS_ID = np.append(QZS_ID, '0' + f'{s_unpack[n * i + 9]}')
            else:
                QZS_ID = np.append(QZS_ID, f'{s_unpack[n * i + 9]}')
                
            # QZSS IOD: Issue Of Data of QZSS ephemeris to reference 
            # the geometric gradients 

            QZS_IOD = np.append(QZS_IOD, s_unpack[n * i + 11])
                   
            # Delta radial
            # Printed in [m]
            D_r = np.append(D_r, s_unpack[n * i + 12] * 0.1 * 10 ** (-3))
            
            # Delta along-track
            # Printed in [m]
            D_t = np.append(D_t, s_unpack[n * i + 13] * 0.4 * 10 ** (-3))
            
            # Delta cross-track
            # Printed in [m]
            D_n = np.append(D_n, s_unpack[n * i + 14] * 0.4 * 10 ** (-3))
            
            # Dot delta radial
            # Printed in [mm/s]
            dot_D_r = np.append(dot_D_r, s_unpack[n * i + 15] * 0.001)
            
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_t = np.append(dot_D_t, s_unpack[n * i + 16] * 0.004)
                
            # Dot delta along-track
            # Printed in [mm/s]
            dot_D_n = np.append(dot_D_n, s_unpack[n * i + 17] * 0.004)
            
            # Delta clock C0, C1, C2 ([mm], [mm/s], [mm/s**2])
            D_C0 = np.append(D_C0, s_unpack[n * i +  18] * 0.1    )  
            D_C1 = np.append(D_C1, s_unpack[n * i +  19] * 0.001  )  
            D_C2 = np.append(D_C2, s_unpack[n * i +  20] * 0.00002)  
                
        self.gnss_id = QZS_ID
        self.gnss_iod = QZS_IOD
        self.dr = D_r
        self.dn = D_n
        self.dt = D_t
        self.dot_dr = dot_D_r
        self.dot_dn = dot_D_n
        self.dot_dt = dot_D_t
        self.dc0 = D_C0
        self.dc1 = D_C1
        self.dc2 = D_C2
        
# *************************************************************************** #
#                                                                             #
#                     SSR QZSS URA Message Type 1250                          #
#                                                                             #
# *************************************************************************** #
class qzs_ura:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # QZSS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes +3 bits <-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        QZS_ID = []
        URA    = []
        URA_CLASS = []
        URA_VALUE = []
                           
        bit_sat = self.n_sat * 'u4u3u3'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
            # QZSS ID number       
            if s_unpack[3 * i + 8] < 10:
                QZS_ID = np.append(QZS_ID, '0' + f'{s_unpack[3 * i +  8]}')
            else:
                QZS_ID = np.append(QZS_ID, f'{s_unpack[3 * i +  8]}')
                
            # SSR URA
            # URA_CLASS             
            Class = s_unpack[3 * i +  9]
            URA_CLASS = np.append(URA_CLASS, Class)

            # URA_VALUE 
            Value = s_unpack[3 * i + 10]
            URA_VALUE = np.append(URA_VALUE, Value)

            if (Value == 0) & (Class == 0):
                print('URA undefined/unknown')
            elif (Value == 7) & (Class == 7):
                print('URA > 5466.5 [mm]')
            # The URA is computed by the following expression:
            # Printed in [m]
            URA = np.append(URA, (3 ** (Class) * (1 +
                                      Value / 4) - 1) / 1000)                

        self.ura = URA
        self.ura_class = URA_CLASS
        self.ura_value = URA_VALUE
        
# *************************************************************************** #
#                                                                             #
#                SSR QZSS High Rate Clock Correction Message Type 1251        #
#                                                                             #
# *************************************************************************** #
class qzs_hr_clock:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
            
        # QZS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Number of satellites
        self.n_sat = unpack_bits[7]

        # ******************************************************************* #
        # --> total number of bits considered so far: 67-> 8bytes + 3 bits<-- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        QZS_ID   = []
        HR_clock = []
                           
        bit_sat = self.n_sat * 'u4s22'
        s_unpack = bitstruct.unpack(header + bit_sat, message)
            
        for i in range(self.n_sat):
            # QZSS ID number  
            if s_unpack[2 * i + 8] < 10:
                QZS_ID = np.append(QZS_ID, '0' + f'{s_unpack[2 * i + 8]}')
            else:
                QZS_ID = np.append(QZS_ID, f'{s_unpack[2 * i + 8]}')
                
            # High-rate clock correction
            HR_clock = np.append(HR_clock, s_unpack[2 * i + 
                                                    9] * 0.1 * 1e-3)             
        self.gnss_id = QZS_ID
        self.hr_clock = HR_clock
        
# *************************************************************************** #
#                                                                             #
#                      QZSS Phase Bias Message Type 1268                      #
#                                                                             #
# *************************************************************************** #
class qzs_phase_bias:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u1u1u6'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        
        self.gnss = 'QZSS'
        self.gnss_short = 'J'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]

        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 

        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'

        # IOD SSR
        self.iod = unpack_bits[4]

        # SSR Provider ID
        self.provider_id = unpack_bits[5]

        # SSR Solution ID
        self.solution_id = unpack_bits[6]

        # Dispersive bias consistency indicator
        self.disp_bias = unpack_bits[7]
            
        # MW consistency indicator
        self.mw = unpack_bits[8]

        # Number of satellites
        self.n_sat = unpack_bits[9]

        # ******************************************************************* #
        # ---> total number of bits considered so far: 69-> 8bytes+5bits <--- #
        # ******************************************************************* #
        #                                                                     # 
        #                            Satellite part                           #
        #                                                                     #
        # ******************************************************************* # 
        
        # satellite parameters initialization
        QZS_ID = []
        num_phase = []
        yaw_angle = []
        yaw_rate = []
            
        track = []
        signal_int = []
        signal_WL = []
        signal_dis = []
        signal_name = []
        phase_bias = []
             
        n_types = 0
        bit_sat = 'u4u5u9s8' 
           
        for i in range(self.n_sat):
            s_unpack = bitstruct.unpack(header + bit_sat, message)
            
            # QZS sat ID number     
            if s_unpack[4 * i + 5 * n_types + 10] < 10:
                QZS_ID = np.append(QZS_ID, '0' + 
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')
            else:
                QZS_ID = np.append(QZS_ID, 
                                   f'{s_unpack[4 * i + 5 * n_types + 10]}')  
            # N. of Phase Biases Processed
            num_phase = np.append(num_phase, 
                                  s_unpack[4 * i + 5 * n_types + 11])
                
            # Yaw Angle
            # Printed in [deg]
            yaw_angle = np.append(yaw_angle, (s_unpack[4 * i + 
                                                       5 * n_types +
                                                       12] *
                                              1 / 256) * 180)
            
            # Yaw Rate
            # Printed in [deg/s]
            yaw_rate = np.append(yaw_rate, (s_unpack[4 * i +
                                                     5 * n_types + 
                                                     13] * 1 / 8192) * 180)

        # ******************************************************************* #
        #                                                                     # 
        #            Phase specific part of the satellite considered          #
        #                                                                     #
        # ******************************************************************* # 
        # phase parameters initialization
            track.append([])
            signal_int.append([])
            signal_WL.append([])
            signal_name.append([])
            signal_dis.append([])
            phase_bias.append([])
            
            bit_phase = 'u5u1u2u4s20' 
                
            for j in range(s_unpack[4 * i + 5 * n_types + 11]):
                p_unpack = bitstruct.unpack(header + bit_sat + 
                                            bit_phase, message)
            
            # Track indicator
                track[i].append(p_unpack[4 * i + 5 * n_types + 14 + j * 5])

            # Signal_name:
                GNSS_ID = 'QZSS'
                signal_name[i].append(signalID.signals(GNSS_ID, 
                                      p_unpack[4 * i + 5 * n_types +
                                               14 + j * 5]))
            
            # Signal integer indicator
                signal_int[i].append(p_unpack[4 * i + 5 * n_types +
                                              15 + j * 5])
            
            # Signal wide-lane integer indicator
                signal_WL[i].append(p_unpack[4 * i + 5 * n_types +
                                             16 + j * 5])
            
            # Signal discontinuity counter
                signal_dis[i].append(p_unpack[4 * i + 5 * n_types +
                                              17 + j * 5])
            
            # PHASE BIAS
                phase_bias[i].append(p_unpack[4 * i + 5 * n_types +
                                              18 + j * 5] * 0.0001)

                if j < s_unpack[4 * i + 5 * n_types + 11] - 1:
                    bit_phase = bit_phase + 'u5u1u2u4s20'
                        
            n_types = n_types + s_unpack[4 * i + 5 * n_types + 11]    
            bit_sat = bit_sat + bit_phase  + 'u4u5u9s8'
                    
        self.number = num_phase
        self.yaw_angle = yaw_angle
        self.yaw_rate = yaw_rate
        self.track = track
        self.name = signal_name
        self.bias = phase_bias
        self.sig_wl = signal_WL
        self.sig_dis = signal_dis
        self.sig_i = signal_int     
        
# =============================================================================
#                                IONOSPHERE
# =============================================================================
# *************************************************************************** #
#                                                                             #
#                          VTEC Message Type 1264                             #
#                                                                             #
# *************************************************************************** # 
class iono_sph:
    def __init__(self, message):
        # Definition of the bits of the header of the message
        header = 'u12u20u4u1u4u16u4u9u2'
        # Unpack the bits of the header    
        unpack_bits = bitstruct.unpack(header, message)
        self.gnss = 'Ionosphere Spherical Harmonics'
        
        # **************************** Parameters *************************** #
        # unpack_bits[0] is the type, hence it is not considered here
        # GPS Epoch Time 1s
        self.epoch  = unpack_bits[1]
        
        # SSR Update Interval
        # SSR Update Interval has a range between 0-15, i.e. : 
        ui_list = [1, 2, 5, 10, 15, 30, 60, 120, 240, 300, 600, 900, 1800,
                   3600, 7200, 10800]
        self.ui = ui_list[int(unpack_bits[2])] 
        
        # Multiple Message Indicator
        self.mmi = f'{unpack_bits[3]}'
        
        # IOD SSR
        self.iod = unpack_bits[4]
        
        # SSR Provider ID
        self.provider_id = unpack_bits[5]
        
        # SSR Solution ID
        self.solution_id = unpack_bits[6]
        
        # VTEC Quality Indicator
        self.quality = unpack_bits[7]
        
        # Number of Ionospheric Layers
        self.n_layers  = unpack_bits[8] + 1

        # ******************************************************************* #
        # ------> total number of bits considered so far: 72-> 9bytes <------ #
        # ******************************************************************* #
        #                                                                     # 
        #                            Layers part                              #
        #                                                                     #
        # ******************************************************************* #
        
        # layer parameters initialization
        height = []
        degree = []
        order  = []
        C      = []
        S      = []
        
        n_C = []
        n_S = []
        
        n = 0
        bit_lay = 'u8u4u4'
        for i in range(self.n_layers):
            l_unpack = bitstruct.unpack(header + bit_lay, message)
        # Height of Ionospheric Layer
        # The resolution is 10[km], therefore the result has to be multiplied 
        # by a factor of 10
            height  = np.append(height, l_unpack[n + 9] * 10)

        # Spherical Harmonics Degree
            degree  = np.append(degree, l_unpack[n + 10] + 1)
        
        # Spherical Harmonics Order
            order   = np.append(order, l_unpack[n + 11] + 1)
        
        # Model Part of the SSR VTEC Ionosphere Spherical Harmonic Cosine 
        # Coefficients
            # num of C coeff
            number_C =  ((degree + 1) * (degree + 2) / 2 -    
                         (degree - order) * (degree - order + 1) / 2)
            n_C = np.append(n_C, number_C)
            
            bit_C = ''    
            for j in range(int(number_C[0])):
                bit_C = bit_C + 's16'
                
            C_unpack = bitstruct.unpack(header + bit_lay + bit_C, message)
            C.append([])
            for j in range(int(number_C[0])):
                C[i].append(C_unpack[j + n + 12] * 0.005)
                
        # Model Part of the SSR VTEC Ionosphere Spherical Harmonic Sine 
        # Coefficients   
            number_S = ((degree + 1) * (degree + 2) / 2 -        
                        (degree - order) * (degree - order + 1) / 2 -
                        (degree + 1))
            n_S = np.append(n_S, number_S)
            
            bit_S = ''    
            for j in range(int(number_S[0])):
                bit_S = bit_S + 's16'
            
            S_unpack = bitstruct.unpack(header + bit_lay +
                                        bit_C + bit_S, message)
            
            S.append([])
            for j in range(int(number_S[0])):
                S[i].append(S_unpack[j + int(number_C[0]) + n + 12] * 0.005)
            
            n = n + number_C + number_S
            bit_lay = bit_lay + 'u8u4u4' + bit_C + bit_S    
        
        self.height = height
        self.degree = degree
        self.order = order
        self.n_c = n_C
        self.c = C
        self.n_s = n_S
        self.s = S

class signalID:
    """
    Traking mode update to "ssr_1_gal_qzss_sbas_bds_v08u" document
    """
    def signals(GNSS, S_TMI):    
        if GNSS == 'GPS':
            sig_list = ['1C', '1P', '1W', '', '', '2C', '2D', '2S', '2L', '2X',
                        '2P', '2W', '', '', '5I', '5Q', '5X', '1S', '1L', '1X']
            signal = sig_list[S_TMI]

        elif GNSS == 'GLONASS':
            sig_list = ['1C', '1P', '2C', '2P', '1A', '1B', '1X',
                        '2A', '2B', '2X', '3I', '3Q', '3X']
            signal = sig_list[S_TMI]        

        elif GNSS == 'Galileo':
            sig_list = ['1A', '1B', '1C', '1X', '1Z', '5I', '5Q', '5X', '7I',
                        '7Q', '7X', '8I', '8Q', '8X', '6A', '6B', '6C', '6X',
                        '6Z']
            signal = sig_list[S_TMI]                
        
        elif GNSS == 'QZSS':
            sig_list = ['1C', '1S', '1L', '2S', '2L', '2X', '5I', '5Q', '5X', 
                        '6S', 'SL', 'SX', '1X', '1Z', '5D', '5P', '5Z', '6E',
                        '6Z']
            signal = sig_list[S_TMI]        

        elif GNSS == 'BDS':
            sig_list = ['2I', '2Q', '2X', '6I', '6Q', '6X', '7I', '7Q', '7X',
                        '1D', '1P', '1X', '5D', '5P', '5X']
            
            signal = sig_list[S_TMI]   

        elif GNSS == 'SBAS':
            sig_list = ['1C', '5I', '5Q', '5X']
            signal = sig_list[S_TMI]           
        
        return signal