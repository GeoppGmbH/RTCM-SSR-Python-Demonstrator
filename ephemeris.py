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

import numpy as np

"""
   Group of classes to create ephemeris objects.
   Input : decoded ephemeris message
   Output: object oriented ephemeris message
   
   ****************************************************************************
   Description:
   the Ephemeris class is initialized with the objects: systems (GNSSs of 
   received ephemeris messages), gps, glo, gal, bds and qzs. When the ephemeris
   message of a new system is received, the system is appended to the systems
   object by the method add_system.
   
   The GNSS objects, e.g. gps, are defined by the GNSS class,
   which has the objects sat, sat_epochs and eph. sat is a list of satellite ID
   with received ephemeris, sat_epochs has, for each satellite of sat,
   the list of epoch of received ephemeris. eph is the content of the 
   ephemeris which is defined by the class StateAcc if the GNSS is GLONASS,
   by the class Elements if not. 
   
   Every time a new message is read, the GNSS object, e.g. gps, is updated by
   using the methods add_sv of the Satellite class to add a new satellite
   and add_epoch of the Epochs class to update the epochs and add a new decoded
   ephemeris message. 
   
   A method to get the closest in time ephemeris of a specific satellite is 
   included in the Ephemeris class: get_closest_epo.
"""

class Elements:
    def __init__(self, dec_msg):
        self.sat_id = dec_msg.sat_id
        
        self.root_a    = dec_msg.root_a
        self.dn        = dec_msg.dn
        self.ecc       = dec_msg.ecc
        self.i0        = dec_msg.i0
        self.idot      = dec_msg.idot
        self.omega_0   = dec_msg.omega_0
        self.omega_dot = dec_msg.omega_dot
        self.omega     = dec_msg.omega
        self.m0        = dec_msg.m0
        self.crc       = dec_msg.crc
        self.crs       = dec_msg.crs
        self.cuc       = dec_msg.cuc
        self.cus       = dec_msg.cus
        self.cic       = dec_msg.cic
        self.cis       = dec_msg.cis
        self.af0       = dec_msg.af_zero
        self.af1       = dec_msg.af_one
        self.af2       = dec_msg.af_two
        self.toe       = dec_msg.toe
        self.toc       = dec_msg.toc
        self.week      = dec_msg.week
        
    def __repr__(self):
        return ("Orbital elements of sat " + self.sat_id + " at epoch " +
                str(self.toe))
class StateAcc:
    def __init__(self, dec_msg):
        self.sat_id = dec_msg.sat_id
        
        self.xn = dec_msg.xn
        self.yn = dec_msg.yn
        self.zn = dec_msg.zn
        
        self.dxn = dec_msg.dxn
        self.dyn = dec_msg.dyn
        self.dzn = dec_msg.dzn
        
        self.ddxn = dec_msg.ddxn
        self.ddyn = dec_msg.ddyn
        self.ddzn = dec_msg.ddzn
        
        self.tb = dec_msg.tb
        self.nt = dec_msg.nt
        self.n4 = dec_msg.n4
        
        self.gamma = dec_msg.gamma
        self.tau   = dec_msg.tau
        self.tau_c = dec_msg.tau_c
        self.ch    = dec_msg.freq
        
    def __repr__(self):
        return ("State vector and acc of sat " + self.sat_id + " at epoch " +
                str(self.tb))
        
class Epochs:
    def __init__(self, dec_msg, epochs=None, ephemeris=None):
        if epochs is None:
            self.epochs = []
        else:
            self.epochs = epochs
            
        if ephemeris is None:
            self.ephemeris = []
        else:
            self.ephemeris = ephemeris
        self.dec_msg = dec_msg
        
    def add_epo(self, epo):
        if epo not in self.epochs:
            self.epochs = np.append(self.epochs, epo) 
            
            if self.dec_msg.gnss_short == 'R':
                self.ephemeris = np.append(self.ephemeris,
                                           StateAcc(self.dec_msg))
            else:
                self.ephemeris = np.append(self.ephemeris,
                                           Elements(self.dec_msg))

class Satellite:
    def __init__(self, satellites=None):
        if satellites is None:
            self.prn = []
        else:
            self.prn = satellites
            
    def add_sv(self, sv):
        if sv not in self.prn:
            self.prn = np.append(self.prn, sv)
            
class GNSS:
    def __init__(self, dec_msg=None, epo=None, sv=None, eph=None,
                 epochs=None, satellites=None):
        if eph is None:
            self.eph = {}
        else: self.eph = eph
        
        if epochs is None:
            self.sat_epochs = {}
        else:
            self.sat_epochs = epochs
            
        sat = Satellite(satellites)

        try:
            epoch_list = Epochs(dec_msg, self.sat_epochs[sv],
                                self.eph[sv])
        except KeyError:
            epoch_list = Epochs(dec_msg)
        
        if dec_msg is None:
            self.sat = []
        else:
            sat.add_sv(sv)
            self.sat = sat.prn
            epoch_list.add_epo(epo)
            self.sat_epochs[sv] = epoch_list.epochs 
            self.eph[sv] = epoch_list.ephemeris
    
    def __repr__(self):
        return ('GNSS ephemeris class with objects: sat, sat_epochs[sv],' +
                'eph[sv]')

class Ephemeris:
    def __init__(self):
        
        self.systems = []
        self.gps = GNSS()
        self.glo = GNSS()
        self.gal = GNSS()
        self.bds = GNSS()
        self.qzs = GNSS()
        

    def add_ephemeris_msg(self, dec_msg, system):
        if system == 'G':
            self.gps = GNSS(dec_msg, dec_msg.toe, dec_msg.sat_id,
                            self.gps.eph, self.gps.sat_epochs, self.gps.sat)
        elif system == 'R':
            self.glo = GNSS(dec_msg, dec_msg.tb, dec_msg.sat_id,
                            self.glo.eph, self.glo.sat_epochs, self.glo.sat)
        elif system == 'E':
            self.gal = GNSS(dec_msg, dec_msg.toe, dec_msg.sat_id,
                            self.gal.eph, self.gal.sat_epochs, self.gal.sat)
        elif system == 'C':
            self.bds = GNSS(dec_msg, dec_msg.toe, dec_msg.sat_id,
                            self.bds.eph, self.bds.sat_epochs, self.bds.sat)
        elif system == 'J':
            self.qzs = GNSS(dec_msg, dec_msg.toe, dec_msg.sat_id,
                            self.qzs.eph, self.qzs.sat_epochs, self.qzs.sat)
        
        
    def __repr__(self):
        return ('Ephemeris class with objects: systems, gps, glo, gal, bds,' + 
                'qzs')
            
    def add_system(self, system):
        if system not in self.systems:
            self.systems = np.append(self.systems, system)
    
    def get_closest_epo(self, epo, gnss, sv):
        try:
            index = np.where(np.abs(gnss.sat_epochs[sv] - epo) ==
                             np.min(np.abs(gnss.sat_epochs[sv] - epo)))
            closest_eph = gnss.eph[sv][index[0]]
        except KeyError:
            # In this case, there is no ephemeris for that satellite
            closest_eph = []
        return closest_eph
        