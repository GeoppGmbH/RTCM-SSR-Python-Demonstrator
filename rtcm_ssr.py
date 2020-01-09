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

"""
   Group of classes to create RTCM-SSR objects.
   Input : decoded rtcm-ssr message
   Output: object oriented ssr message
   
   ****************************************************************************
   Description:
   the SSR class is initialized with objects the epochs, the GNSS systems (gps,
   glo,gal, bds, qzs) and the iono_epochs (epochs identified by receiving a
   global ionosphere message). This objects are updated for each epoch there
   is a new message calling the class Msgs.
   
   The Msgs class has as objects the ssr messages,
   i.e. orb, clck, orb_clck, cbias, pbias and iono. 
   The epochs are updated by the method add_epoch of the SSR class, 
   while the content of the messages are updated by using the method update 
   of the Msgs class, called by the method update_ssr of the SSR class. 
   
   Every epoch of received ionospheric message the iono_epochs are updated
   using the method add_iono_epoch of the SSR class.
   In order to get the closest in epoch time global ionosphere message, the SSR
   class has the method get_closest_iono.
"""
class Msgs:
    def __init__(self):
        # initialization
        self.orb      = []
        self.clck     = []
        self.orb_clck = []
        self.cbias    = []
        self.pbias    = []
        self.iono     = []
        
    def __repr__(self):
        return ('SSR objects: orb, clck, orb_clck, cbias, pbias, iono')
    
    def update(self, orb=None, clck=None, orb_clck=None,
                 cbias=None, pbias=None, iono=None):
            if orb is not None:
                self.orb = orb
            if clck is not None:
                self.clck = clck
            if orb_clck is not None:
                self.orb_clck = orb_clck
            if cbias is not None:
                self.cbias = cbias
            if pbias is not None:
                self.pbias = pbias
            if iono is not None:
                self.iono = iono
             
class SSR:
    def __init__(self, epochs=None, iono_epochs=None, gps=None, glo=None,
                 gal=None, bds=None, qzs=None, iono=None):
        if epochs is None:
            self.epochs = []
        else:
            self.epochs = epochs
        
        if iono_epochs is None:
            self.iono_epochs = []
        else:
            self.iono_epochs = iono_epochs
        
        if gps is None:
            self.gps = []
        else:
            self.gps = gps
        
        if glo is None:
            self.glo = []
        else:
            self.glo = glo
            
        if gal is None:
            self.gal = []
        else:
            self.gal = gal 
            
        if bds is None:
            self.bds = []
        else:
            self.bds = bds 

        if qzs is None:
            self.qzs = []
        else:
            self.qzs = qzs
        
        if iono is None:
            self.iono = []
        else:
            self.iono = iono
            
    def __repr__(self):
        return ('SSR objects: epochs, iono_epochs, gps, glo, gal, bds, qzs,' +
                'iono')
               
    def add_epoch(self, epo, sat=None):
        if epo not in self.epochs:
            self.epochs = np.append(self.epochs, epo)
            self.gps = np.append(self.gps, Msgs())
            self.glo = np.append(self.glo, Msgs())
            self.gal = np.append(self.gal, Msgs())
            self.bds = np.append(self.bds, Msgs())
            self.qzs = np.append(self.qzs, Msgs())
            self.iono = np.append(self.iono, Msgs())
    
    def add_iono_epoch(self, epo):
        if epo not in self.iono_epochs:
            self.iono_epochs = np.append(self.iono_epochs, epo)
            
    def update_ssr(self, system, epo, orb=None, clck=None, orb_clck=None,
                       cbias=None, pbias=None, iono=None):
        j = int(np.where(self.epochs == epo)[0])
        if system == 'G':
            self.gps[j].update(orb, clck, orb_clck, cbias, pbias, iono)
        elif system == 'R':
            self.glo[j].update(orb, clck, orb_clck, cbias, pbias, iono)
        elif system == 'E':
            self.gal[j].update(orb, clck, orb_clck, cbias, pbias, iono)
        elif system == 'C':
            self.bds[j].update(orb, clck, orb_clck, cbias, pbias, iono)
        elif system == 'J':
            self.qzs[j].update(orb, clck, orb_clck, cbias, pbias, iono)
        elif system == 'IONO':
            self.iono[j].update(orb, clck, orb_clck, cbias, pbias, iono)
    
    def get_closest_iono(self, ssr, epoch):
        # find the index among the iono epochs
        iono_index = np.where(np.abs(ssr.iono_epochs - epoch) ==
                              np.nanmin(np.abs(ssr.iono_epochs - epoch)))[0]
        # consider the index in the common list of epochs
        if len(iono_index) == 1:    
            index = np.where(ssr.epochs == ssr.iono_epochs[iono_index])[0]
        else:
            index = np.where(ssr.epochs == ssr.iono_epochs[iono_index[0]])[0]
        return ssr.iono[index[0]].iono
        
