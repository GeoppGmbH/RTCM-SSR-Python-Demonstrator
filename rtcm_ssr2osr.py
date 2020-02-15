"""
   ----------------------------------------------------------------------------
   Copyright (C) 2020 Francesco Darugna <fd@geopp.de>  Geo++ GmbH,
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

import numpy as np
from scipy.integrate import ode
import coord_and_time_transformations as trafo
from numpy import linalg as LA
import iono_computation

"""
    Set of classes to translate SSR parameters in OSR. 
"""

class RtcmSsr2osr:
    """
        Class to compute the SSR influence on user position using
        decoded RTCM-SSR messages.
        It works for specific epoch, GNSS system, satellite.
        
        Input:
            - ssr: ssr parameters at the considered epoch, for the considered
                    GNSS system
            - ephemeris: ephemeris of the satellite considered
            - epoch: specific epoch time of received message to compute
                     the ssr influence 
            - ionosphere: closest in time received ionospheric rtcm-ssr msg
            - ID: ID of the specific satellite considered, e.g. "G01"
            - track_mode: track mode of the considered signal, e.g. "1C"
            - ls: leap second for the specific system
            - n4: GLONASS four-year interval number 
            - receiver: receiver WGS84 ellipsoidal coordinates and
                        cartesian coordinates
            - dt:  interval of time w.r.t. epoch
            - f_out_iono: output file for the ionospheric parameters
        Output:
            callable objects for the following corrections:
            - orbit 
            - clock
            - code bias
            - phase bias
            - global ionosphere
            - shapiro effect
            - wind-up effect
            
        ***********************************************************************
        Description:  
        firstly, the satellite state vector is computed passing the ephemeris
        message to the class Orbit. The ssr influence on the user position
        is then computed for each satellite for all the components calling the 
        classes OrbCorr, ClockCorr, CodeBias, PhaseBias, ShapiroEffect and
        WindUp. The __str__ method can be used to print the content of 
        the message in a human readable format.
    """
    
    def __init__(self, ssr, ephemeris, epoch, ionosphere,
                 ID, track_mode, ls, n4,
                 receiver, dt, f_out_iono):
        self.ID = ID
        system = self.ID[0]
        sv = self.ID[1:]
        xyz = receiver['cartesian']
        if system == 'R':
            # here we are interested only in the week since the epoch has
            # already been set in GPS time
            [week, epo_t] = trafo.glo_time2gps_time(ephemeris.nt, 0, n4,
                                                    ls)
        elif system == 'E':
            # Week needs to be defined w.r.t. GST started Ref. Galileo ICD
            [week0, gps_time0] = trafo.gps_time_from_y_doy_hms(1999, 235, 
                                                               0, 0, 0)
            week = week0 + ephemeris.week
        elif system == 'C':
            # Week needs to be defined w.r.t. BDT started Ref. Beidou ICD
            [week0, gps_time0] = trafo.gps_time_from_y_doy_hms(2006, 2, 
                                                               0, 0, 0)
            week = week0 + ephemeris.week
        else:
            week = ephemeris.week
        self.week = week
        orbit_p = Orbit(system, xyz, ls, epoch, week)
        # compute satellite state vector correcting for the satellite clock
        sat_clock = 'corrected' 
        self.sat_state = orbit_p.compute_state_vector(ephemeris,
                                                      sat_clock)   
        # compute satellite state vector without correcting for the satellite
        # clock
        sat_clock = 'uncorrected' 
        self.sat_state_tr = orbit_p.compute_state_vector(ephemeris,
                                                      sat_clock)          
        # receiver coordinates
        lat    = receiver['ellipsoidal'][0]
        lon    = receiver['ellipsoidal'][1]
        height = receiver['ellipsoidal'][2]

        self.rec = receiver['cartesian']

        # frequency to be considered for correction computation as example
        # GPS/QZSS(L1), GLONASS(L1), Galileo(E1) and Beidou(2I)
        if system == 'R':
            ch = ephemeris.ch
            fr = (1602 + ch * 9/16)  * 1e6
        elif system == 'C':
            fr = 1561.098 * 1e6
        else:
            ch = 0
            fr = 2 * 77 * 10.23 * 1e6          
              
        # compute orbit obs line corrections
        if np.any(ssr.orb):
            self.orb = OrbCorr(ssr.orb,self.sat_state_tr, self.rec, sv).corr
        
        elif np.any(ssr.orb_clck):
            self.orb = (OrbCorr(ssr.orb_clck,self.sat_state_tr, 
                                self.rec, sv).corr)
        else:
            self.orb = []
        
        orb_out = self.make_output_format(self.orb)
        
        # compute clock obs line corrections
        # the delta time in this version of the demo is considered 0
        # since all the corrections are computed when received
        if np.any(ssr.clck):
            self.clck = ClockCorr(ssr.clck, dt, sv).corr
        elif np.any(ssr.orb_clck):
            self.clck = ClockCorr(ssr.orb_clck, dt, sv).corr
        else:
            self.clck  = []
        clck_out = self.make_output_format(self.clck)
            
        # code and phase bias
        if np.any(ssr.cbias):
            self.cbias = CodeBias(ssr.cbias, sv, track_mode).corr
        else:
            self.cbias = []
        cbias_out = self.make_output_format(self.cbias)
    
        if np.any(ssr.pbias):
            self.pbias = PhaseBias(ssr.pbias, sv, track_mode).corr
        else:
            self.pbias = []   
        pbias_out = self.make_output_format(self.pbias)
        
        # compute relativistic shapiro effect
        self.shap = ShapiroEffect(self.sat_state_tr[0:3],
                                                      self.rec).corr
        shap_out =  self.make_output_format(self.shap)
        
        # compute global ionosphere
        if np.any(ionosphere):
            self.global_iono =  GlobalIono(ionosphere, epoch,
                                                            system, ID,
                                                            self.sat_state,
                                                            self.rec, fr,
                                                            f_out_iono).corr
        else:
            self.global_iono = []
        global_iono_out = self.make_output_format(self.global_iono)
        
        # compute wind up effect              
        if np.any(ssr.pbias):
            self.wup = WindUp(ssr.pbias, sv, dt,self.sat_state, fr,
                              self.rec, lat, lon).corr
        else:
            self.wup  = []
        wup_out = self.make_output_format(self.wup)
            
        # ellipsoidal elevation
        angular_position = iono_computation.PiercePoint(self.sat_state[0:3],
                                                        self.rec,
                                                        height)
        [az, el] = angular_position.compute_az_el(np.deg2rad(lat),
                                                  np.deg2rad(lon))
        self.el = '{:7.3f}'.format(np.rad2deg(el))
        self.epoch = epoch
        self.strg = ('   ' + '{:8.0f}'.format(self.week) +
                     '   ' + '{:8.4f}'.format(self.epoch) + '    ' +
                     f'{self.ID}'    + '    ' +
                     self.el         + '  '   +
                     clck_out        + '  '   +
                     orb_out         + '   '  +
                     global_iono_out + '   '  +
                     shap_out      + '   '  + 
                     wup_out         + '   '  +
                     pbias_out       + '   '  +
                     cbias_out)
        
    def __str__(self):
        return self.strg    
    
    def __repr__(self):
        return ('OSR objects: week, epoch, ID, orb, clck, cbias, pbias,'  +
                'global_iono, wup, shap')
    
    def make_output_format(self, value):
        """
            Method to prepare the right format for the output. If the variable
            is empty then the output will be n/a.
        """
        if np.size(value) == 0:
            value_out = '{:8s}'.format('    n/a')
        else:
            value_out = '{:8.4f}'.format(value)
        return value_out

# =============================================================================
# OSR orbit corrections
# =============================================================================
class OrbCorr:
    """ Orbit correction computation.
        Input:
            - ssr orbit corrections
            - satellite state vector at the transmission time
            - index of desired satellite
        Output:
            orbit correction along the line of sight
    """
    def __init__(self, orb, state_tr, rec, sv):
        i = np.where(orb.gnss_id == sv)
        if np.size(i) == 0:
            self.corr = []
        else:
            i = int(i[0])
            # compute radial, along-track and cross-track satellite coordinates
            sat_tr = state_tr[0:3]
            vel_tr = state_tr[3:]
            alo = vel_tr / LA.norm(vel_tr)
            crs = (np.cross(sat_tr, vel_tr) /
                   LA.norm(np.cross(sat_tr, vel_tr)))
            rad = np.cross(alo, crs)
            # compute rotation matrix to radial, along-track and cross-track 
            # coordinates 
            R = np.array([rad, alo, crs])

            delta_o = np.array([orb.dr[i], orb.dt[i], orb.dn[i]])
            delta_x = np.dot(np.transpose(R), delta_o)    
            sight   = (sat_tr - rec) / LA.norm(sat_tr - rec)
            self.corr     =  np.dot(delta_x, sight)
        
# =============================================================================
# OSR clock corrections        
# =============================================================================
class ClockCorr:
    """ Orbit correction computation.
        Input:
            - ssr clock corrections in [mm], [mm/s], [mm/s**2]
            - delta time w.r.t. the received msg of corrections
            - index of the desired satellite
        Output:
            clock correction along the line of sight in [m]
    """
    def __init__(self, clock, dt, sv):
        i = np.where(clock.gnss_id == sv)        
        if np.size(i) == 0:
            self.corr = []
        else:
            i = int(i[0])
            self.corr = (1e-3 * (clock.dc0[i] + clock.dc1[i] * dt +
                                 clock.dc2[i] * dt**2))
# =============================================================================
# OSR Code Bias    
# =============================================================================
class CodeBias:
    """Class to get code bias from decoded RTCM-SSR message
        Input:
            - RTCM SSR code bias 
            - index of the desired satellite
            - tracking mode of the desired signal
        Output:
            - code bias correction for the desired satellite and tracking mode
    """
    def __init__(self, cbias, sv, signal_ID): 
        try:
            i = np.where(cbias.gnss_id == sv)
        except AttributeError:
            self.corr = []
        if np.size(i) == 0:
            self.corr = []
        else:
            i = int(i[0])   
            if signal_ID not in cbias.name[i]:
                self.corr = []
            else:
                k = 0
                for s in cbias.name[i]:
                    if s == signal_ID:
                        self.corr = cbias.bias[i][k] 
                    k = k + 1      
# =============================================================================
# OSR Phase Bias    
# =============================================================================
class PhaseBias:
    """Class to get phase bias from decoded RTCM-SSR message
        Input:
            - RTCM SSR phase bias 
            - index of the desired satellite
            - tracking mode of the desired signal
        Output:
            - phase bias correction for the desired satellite and tracking mode
    """
    def __init__(self, pbias, sv, signal_ID):
        try:
            i = np.where(pbias.gnss_id == sv)
        except AttributeError:
            self.corr = []
            return
        if np.size(i) == 0:
            self.corr = []
        else:
            i = int(i[0])   
            k = 0
            if signal_ID not in pbias.name[i]:
                self.corr = []
            else:
                k = 0
                for s in pbias.name[i]:
                    if s == signal_ID:
                        self.corr = pbias.bias[i][k] 
                    k = k + 1         
            
# =============================================================================
#    Global Ionosphere Spherical Harmonics
# =============================================================================
class GlobalIono:
    """
        It passes the input values to the IonoComputation class for computing
        the global ionospheric influence at the user position.
    """
    def __init__(self, iono, epoch, system, ID, state, rec, fr, f_out_iono):    
        iono_influence = iono_computation.IonoComputation(epoch, state,
                                                          rec,
                                                          system, ID, fr,
                                                          iono)
        print(iono_influence, file = f_out_iono)       
        self.corr = iono_influence.stec_corr_f1
        
# =============================================================================
#                         Shapiro effect
# =============================================================================
class ShapiroEffect:
    """ Class to compute the shapiro effect.
        Input:
                - satellite coordinates at the transmission time
                - receiver coordinates
        Output:
                - shapiro effect correction [m]
        Reference:
            Teunissen, P. and Montenbruck, O. Springer Handbook of GNSS,
            Springer, 2017      
    """
    def __init__(self, sat_tr, rec):
        c = Constants().c
        mu = Constants().mu_gps
        self.corr = (2 * mu / c ** 2 *
                       np.log((np.linalg.norm(sat_tr) +
                       np.linalg.norm(rec) + 
                       np.linalg.norm(sat_tr - rec))/
                      (np.linalg.norm(sat_tr) + np.linalg.norm(rec) - 
                       np.linalg.norm(sat_tr - rec))))   

# =============================================================================
#                                   wind up correction
# =============================================================================
class WindUp:
    def __init__(self, pbias, sv, dt, state, fr, rec, lat, lon):
        """ Function to compute the wind up effect
            It needs:
                - sat state vector in ECEF
                - rec coord in ECEF 
                - ellip lat, long of the rec
                - the wavelength of the signals considered
                
        """
        try:
            i = np.where(pbias.gnss_id == sv)
        except AttributeError:
            self.corr = []
            return
        if np.size(i) == 0:
            self.corr = []
        else:
            i = int(i[0])
            sat = state[0:3]
            vel = state[3:]
        
            lam = Constants().c / fr
            diff = rec - sat 
            k = diff / LA.norm(diff)
        
            # from deg to rad for lat, lon
            lat = np.deg2rad(lat)
            lon = np.deg2rad(lon)
        
            # correction for Eart rotation
            vel[0] = vel[0] - Constants().omega_e * sat[1]
            vel[1] = vel[1] + Constants().omega_e * sat[0]
        
            # ee, en, eu unit vecotrs in ENU ref frame
            ee = np.array([-np.sin(lon)              ,
                           +np.cos(lon)              ,
                           +0                         ])
            en = np.array([-np.cos(lon) * np.sin(lat),
                           -np.sin(lon) * np.sin(lat),
                           +np.cos(lat)               ])

            # Computation of the ex, ey, ez unit vectors
            ez = -sat / LA.norm(sat)
            ey = -np.cross(sat, vel) / LA.norm(np.cross(sat, vel))
            ex = np.cross(ey, ez)
        
            # yaw angle rotation
            yaw = np.deg2rad(pbias.yaw_angle[i] + pbias.yaw_rate[i] * dt)
            R = np.array([[+np.cos(yaw),  np.sin(yaw), 0],
                           [-np.sin(yaw),  np.cos(yaw), 0],
                           [0           ,  0          , 1]])
    
            e_xyz = np.array([ex, ey, ez])
            e_Rxyz = np.dot(R, e_xyz)
            ex = e_Rxyz[0]
            ey = e_Rxyz[1]
            ez = e_Rxyz[2]
        
            # Effective dipole for the satellite
            flag = 'sat'
            D_sat = WindUp.compute_eff_dipole(k, ex , ey, flag)
        
            # Effective dipole for the receiver
            flag = 'rec'
            D_rec = WindUp.compute_eff_dipole(k, ee, en, flag)
        
            # Wind up computation
            gamma = np.dot(k, np.cross(D_sat, D_rec))
        
            omega = np.arccos(np.dot(D_sat, D_rec) /
                              (LA.norm(D_sat) * LA.norm(D_rec)))
            omega = -omega / (2 * np.pi)
        
            if gamma < 0:
                omega = -omega
            # Correction for lambda1, lambda2
            self.corr = omega * lam
        
    def compute_eff_dipole(k, ex, ey, flag):
        """ Computation of the effective dipole for the phase wind up
    
            Input:
                    - k     : dist unit vector for sat-rec in ECEF
                    - ex, ey: unit vectors in the x,y plane.
                      If the satellite is considered 
                          then x = t and y = -n directions 
                          (ref to radial-track-normal ref frame);
                      if the receiver is considered x = E and y = N
                            (North-East-Up ref frame)
                    - flag  : if 'sat' the formula
                              for the satellite is considered,
                             if 'rec' the formula
                             for the receiver is considered
            
            Output:
                    - D: effective dipole
        
                Formulas:
                    --> sat: D = ex - k*dot(k,ex) - cross(k,ey)
                    --> rec: D = ex - k*dot(k,ex) + cross(k,ey)
    
                Reference:
                    Springer Handbook for GNSS, Teunissen & Montenbruck,
                    chap.19 pag. 570
        """
    
        if flag == 'sat':
            D = ex - k * np.dot(k, ex) - np.cross(k, ey)
        elif flag == 'rec':
            D = ex - k * np.dot(k, ex) + np.cross(k, ey)
        
        return D
            
# =============================================================================
#                  satellite state vector computation    
# =============================================================================
class Orbit:
    """
        Class to compute satellite state vector at a certain epoch.
        It is defined by three methods:
            - compute_state_vector, function to compute the state vector
            - propagate_state, it propagates the initial state vector for the 
                                desired epoch, used with GLONASS satellites
            - propagate_orbit_elements, it propagates the orbt elements
                                        from ephemeris for the desired epoch
    """
    def __init__(self, gnss, receiver_xyz, ls, epoch, week):
        self.gnss = gnss
        self.receiver_xyz = receiver_xyz
        self.ls = ls
        self.epoch = epoch
        self.week = week
        self.c     = Constants().c    # speed of light [m/s]          
        self.omega_E = Constants().omega_e  # Earth rotation rate   [rad/s]
              
    def compute_state_vector(self, ephemeris, sat_clock):

        if self.gnss == 'R':
            # Info from message:
            Rday  = ephemeris.nt
            tb    = ephemeris.tb
            gamma = ephemeris.gamma
            tau   = ephemeris.tau
            dt_tau_c = ephemeris.tau_c

            # Integration step
            step = 60   # [s]

            radial = 20e6  # [m] distance first guess  
            radial_last = 0
            dt_sv = 10
            dt_sv_last = 0
            state_0 = np.zeros(6)
            t_xsv = 0
            d_xsv = 0
            td_xsv = 0
            epsilon = 1.0e-2
            state_0 = np.array([ephemeris.xn, ephemeris.yn, ephemeris.zn,
                                ephemeris.dxn, ephemeris.dyn, ephemeris.dzn])
            
            # get the luni-solar acc from ephemeris
            luni_solar = np.array([ephemeris.ddxn, ephemeris.ddyn,
                                   ephemeris.ddzn])
            dtt = radial / self.c
            # Iteration for final time of iteration for GLONASS
            while (np.abs(radial - radial_last) > 0.00001):            
                if sat_clock == 'corrected':
                    tf = self.epoch + dt_sv - radial / self.c - self.ls
                else:
                    tf = self.epoch - dtt - self.ls
    
                dt_sv_last = dt_sv
                i_day = int((tf + 10800.0 + 0.005) / Constants().day_seconds)
                t_day = tf + 10800.0 - i_day * Constants().day_seconds
            
                # With correction for Moskow time
                [iy, DOY,
                 hh, mm,
                 ss] = trafo.gpsTime2y_doy_hms(self.week, tf + 10800.0) 
            
                if np.mod(iy, 4) != 0:
                    DOY = DOY + np.mod(iy, 4) * 365 + 1
                i_day = DOY  # day in four years cycle
            
                tk = (i_day - Rday) * Constants().day_seconds + (t_day - tb)
   
                while (tk <= -Constants().day_seconds/2):
                    tk = tk + Constants().day_seconds
                while (tk > Constants().day_seconds/2):
                    tk = tk - Constants().day_seconds
                
                # calculate actual clock drift and bias
                dts    = -(tau - gamma * tk)
                if np.abs(dt_tau_c) < 1.0:    # plausibilty check for TauC
                    dts = dts -  dt_tau_c

                t_day = t_day - dts
                tk = ((i_day - Rday) * Constants().day_seconds +
                      (t_day - tb))   # with correct t_day
                while (tk <= -Constants().day_seconds/2):
                    tk = tk + Constants().day_seconds
                    t_day = t_day + Constants().day_seconds
                while (tk > Constants().day_seconds/2):
                    tk = tk - Constants().day_seconds   
                    t_day = t_day - Constants().day_seconds
                
                dt = ((i_day - d_xsv) * Constants().day_seconds +
                      (t_day - td_xsv))
                dts = -(tau - gamma * tk)

                if (np.abs(dt) <= epsilon) :
                    coord = np.array([state_0[0] + state_0[3] * dt,
                                         state_0[1] + state_0[4] * dt,
                                         state_0[2] + state_0[5] * dt])
                    vel = np.array([state_0[3], state_0[4],
                                   state_0[5]])
                    state_0 = np.array([coord[0], coord[1], coord[2],
                                        vel[0], vel[1], vel[2]])
                else:
                    if dt > 900:
                        d_xsv  = Rday
                        td_xsv = tb 
                    t0 = td_xsv + (d_xsv - i_day) *Constants().day_seconds
                    state = Orbit.propagate_state(self, t0, state_0,
                                                      luni_solar,
                                                      step, t_day) 
                    if np.size(state) > 6:
                        state = state[-1, :]   # last integration time
                    else:
                        state = state
                state = np.dot(state, 1000)  # [m]
                coord = np.array([state[0], state[1], state[2]])
                vel   = np.array([state[3], state[4], state[5]])
            
                radial_last = radial
                radial = LA.norm(coord - self.receiver_xyz)  # it has to be in meter
                dtt = (radial - radial_last) / self.c
                t_xsv = t_day
                d_xsv  = i_day
                td_xsv = t0
                dt_sv = dts  
            
            coord = Orbit.pz2wgs(self, coord)
            vel   = Orbit.pz2wgs(self, vel)
            state = np.append(coord, vel)
            
            return state 
        else:
            radial = 0             
            radial_last = 20e6     # [m] first guess about sat - rec distance 
            dt_sv = 0
            dt_sv_last = 10
            state_0 = np.zeros(6)
            t_xsv = 0
            dtt = radial_last / self.c
            # Iteration for final time of iteration 
            while (np.abs(radial -
                      radial_last) > 0.0001) | (np.abs(dt_sv -
                                                       dt_sv_last) > 0.1 *
                                                1e-7):
                if sat_clock == 'corrected':    
                    tf = self.epoch + dt_sv - radial / self.c - self.ls
                else:
                    tf = self.epoch - dtt - self.ls
                
                radial_last = radial
                dt_sv_last = dt_sv
                [state,
                 t_xsv_old,
                 dt_sv] = Orbit.propagate_orbit_elements(self, ephemeris,
                                                         tf, t_xsv, state_0)

                radial = LA.norm(np.array([state[0], state[1],
                                           state[2]]) - self.receiver_xyz)
                dtt = (radial - radial_last) / self.c
                t_xsv = t_xsv_old
                state_0 = state
    
        return state
        
    def propagate_state(self, t0, y0, parameters, step, tf):
        """
            Function to propagate the state vector of a satellite from initial
            conditions t0, y0 to the desired time tf with a time step defined
            by step. 
        """
        # differential function
        def f(t, y):
            ax_ls = parameters[0]    #
            ay_ls = parameters[1]    # --> luni-solar accelerations [m/s^2]
            az_ls = parameters[2]    #

            mu   = Constants().mu_glo
            factor = -26332671177.69
            oe_2 = 5.3174941173225e-9
            oe2  = 1.4584230e-4
              
            r = np.sqrt(y[0] ** 2 + y[1] ** 2 + y[2] ** 2)     
            v_x  = y[3]
            v_y  = y[4]
            v_z  = y[5]
      
            r2 = r  ** 2
            r3 = r  * r2
            r5 = r3 * r2

            gm3 = - mu / r3
            fr5 = factor / r5

            z2r = y[2] / r
            z2r =  z2r * z2r
            z52r = 5.0 * z2r

            fxy = (gm3 + fr5 * (1.0 - z52r) + oe_2)
                
            a_x = fxy * y[0] + oe2 * y[4] + ax_ls
            a_y = fxy * y[1] - oe2 * y[3] + ay_ls
            a_z = (gm3 + fr5 * (3.0 - z52r)) * y[2] + az_ls
    
            return [v_x, v_y, v_z, a_x, a_y, a_z] 
                    
        t  = np.linspace(t0, tf, np.abs(tf - t0) / step + 1)
        r = ode(f).set_integrator('dop853')
        r.set_initial_value(y0, t0) 

        if len(t) <= 1:
            sol = y0
        else:    
            sol = np.empty((len(t), 6))
            sol[0] = y0
            k = 1
            if tf >= t0:
                while (r.successful()) & (r.t < tf):
                    r.integrate(t[k])
                    sol[k] = r.y
                    k = k + 1
            else:
                while (r.successful()) & (r.t > tf):
                    r.integrate(t[k])
                    sol[k] = r.y
                    k = k + 1                
        return sol
    
    def propagate_orbit_elements(self, kepler, time, t_xsv, state_0):
        """ References:
            - GPS, Galileo, QZSS, Beidou ICDs
            - Springer Handbook of GNSS, Teunissen Montenbruck 2017
            - R. Marson, S. Lagrasta, F. Malvolti, T.S.V. Tiburtina:
              Fast generation of precision orbit ephemeris, Proc.
              ION ITM 2011, San Diego (ION, Virginia 2011) pp. 565–
              576
        """
        
        if ((self.gnss == 'G') | (self.gnss == 'J')):
            F  = Constants().F_gps
            mu = Constants().mu_gps
        elif ((self.gnss == 'E') | (self.gnss == 'C')):
            F  = Constants().F_gal
            mu = Constants().mu_gal
            
        # Input data from ephemeris message
        a          = kepler.root_a * kepler.root_a
        dn         = kepler.dn
        e          = kepler.ecc
        i0         = kepler.i0
        di_dt      = kepler.idot
        Omega0     = kepler.omega_0
        Omega_dot  = kepler.omega_dot
        omega      = kepler.omega
        M0         = kepler.m0
        Crc        = kepler.crc
        Crs        = kepler.crs
        Cuc        = kepler.cuc
        Cus        = kepler.cus
        Cic        = kepler.cic
        Cis        = kepler.cis
        af0        = kepler.af0
        af1        = kepler.af1
        af2        = kepler.af2        
        toe        = kepler.toe
        toc        = kepler.toc
        wn         = kepler.week                
              
        # Define tolerance for linear propagation
        epsilon = 1e-3
        # Clock corrections
        delta_clock = time  - toc                             # time
        while delta_clock <= -Constants().week_seconds/2:
            delta_clock = delta_clock + Constants().week_seconds
        
        while delta_clock >= Constants().week_seconds/2:
            delta_clock = delta_clock - Constants().week_seconds
            
        dtsdot = af1 + af2 * delta_clock                           # drift
        dts    = af0 + (af1 + af2 * delta_clock) * delta_clock     # bias  

        # Period
        tol = 10.0 * 1e-3   # [s]
        dT  = wn * Constants().week_seconds + time 
        dt  =  np.abs(time - t_xsv)
        T   = time - toe - dts

        if np.abs(T) > Constants().week_seconds/2:
            T = (np.mod(T, Constants().week_seconds/2) -
                 np.sign(T) * Constants().week_seconds/2)
        
        # Mean motion
        n = np.sqrt(mu / (a ** 3.0)) + dn
        
        # Mean anomaly
        M = M0 + n * T
        
        # Derivative Mean Anomaly
        dM = n
        
        # Eccentric anomaly : M = E - e*sin(E)
        i_max = 10
        toll  = 0.5 * 1e-11
        E0    = M
        i     = 0
        diff  = 2.0 * toll
            
        while (i < i_max) & (diff >= toll):
                i    = i + 1
                E    = M + e * np.sin(E0)
                diff = np.abs(E - E0)
                E0   = E
            
        # Correction of clock for the relativistic effect 
        dtr   = F * e * kepler.root_a * np.sin(E)
        saver = 1.0 - e * np.cos(E)
        dfr   = F * e * kepler.root_a * np.cos(E) * n / saver
        if self.gnss == 'C':
            dtr = -2 * mu ** 0.5 / (self.c ** 2) * e * kepler.root_a * np.sin(E)
        dts    = dts + dtr
        dtsdot = dtsdot + dfr

        # Derivative eccentric anomaly
        dE =  dM / (1.0 - e * np.cos(E))
        
        # True anomaly
        theta = np.arctan2((np.sqrt(1.0 - e ** 2.0) * np.sin(E)) / 
                           (1.0 - e * np.cos(E)), 
                           (np.cos(E) - e) / (1.0 - e * np.cos(E)))
        
        # Derivative true anomaly
        dtheta = (dE * np.sqrt(1.0 - e ** 2.0)) / (1.0 - e * np.cos(E))
        
        # Argument of latitude
        u_bar = omega + theta
        
        # Derivative argument of latitude
        du_bar = dtheta
        
        # Periodic corrections
        delta_r = Crs * np.sin(2.0 * u_bar) + Crc * np.cos(2.0 * u_bar)
        delta_u = Cus * np.sin(2.0 * u_bar) + Cuc * np.cos(2.0 * u_bar)
        delta_i = Cis * np.sin(2.0 * u_bar) + Cic * np.cos(2.0 * u_bar)
        
        # Deriv of corr terms for radius vector module and angular anomaly
        ddelta_r = 2 * du_bar * (Crs * np.cos(2.0 * u_bar) -
                                 Crc * np.sin(2.0 * u_bar))
        ddelta_u = 2 * du_bar * (Cus * np.cos(2.0 * u_bar) -
                                 Cuc * np.sin(2.0 * u_bar))
        ddelta_i = 2 * du_bar * (Cis * np.cos(2.0 * u_bar) -
                                 Cic * np.sin(2.0 * u_bar))
        
        # Perturbed radius, argument of latitude and inclination
        r = a * (1.0 - e * np.cos(E)) + delta_r
        u = u_bar + delta_u
        i = i0 + di_dt * T + delta_i  
        
        # Derivative of radius vector module and inclination
        dr = a * e * dE * np.sin(E) + ddelta_r
        d_i = di_dt + ddelta_i
        
        # Greenwich longitude of the ascending node 
        lambda_Om = Omega0 + (Omega_dot -
                              self.omega_E) * T - self.omega_E * toe

        # Rate of change of angular offset (derivative of lambda_Om)
        dOmega = Omega_dot - self.omega_E
        
        # Rotation matrices (left handed rotations -> clockwise of -angle)
        R3 = np.array([[np.cos(lambda_Om), -np.sin(lambda_Om), 0.0],
                       [np.sin(lambda_Om),  np.cos(lambda_Om), 0.0],
                       [0.0              ,       0.0         , 1.0]])
    
        R1 = np.array([[1.0     ,     0.0  ,   0.0     ],
                       [0.0     , np.cos(i), -np.sin(i)],
                       [0.0     , np.sin(i),  np.cos(i)]])
        
        # Satellite coordinates on Orbital Plane
        xp = r * np.cos(u)
        yp = r * np.sin(u)
       
        # Earth-fixed position   
        r_ITRF = np.dot(np.dot(R3, R1), np.array([xp, yp, 0.0]))       

        # Derivative of satellite coordinates on Orbital Plane
        dxp = dr * np.cos(u) - r * (du_bar + ddelta_u) * np.sin(u)
        dyp = dr * np.sin(u) + r * (du_bar + ddelta_u) * np.cos(u)
        
        # Rotation matrix for velocity computation
        dR1 = d_i * np.array([[0.0     ,   0.0     ,   0.0     ],
                              [0.0     , -np.sin(i), -np.cos(i)],
                              [0.0     ,  np.cos(i), -np.sin(i)]])
        
        dR3 = dOmega * np.array([[-np.sin(lambda_Om), -np.cos(lambda_Om), 0],
                                 [+np.cos(lambda_Om), -np.sin(lambda_Om), 0],
                                 [+0                ,         0         , 0]])
    
        # Velocity
        v_ITRF = (np.dot(np.dot(R3, R1), np.array([dxp, dyp, 0])) + 
                  np.dot(np.dot(dR3, R1) + np.dot(R3, dR1),
                         np.array([xp, yp, 0])))
        
        if np.abs(dT) <= tol:
                r_ITRF = r_ITRF + v_ITRF * dT
        
        # State vector
        state = np.array([r_ITRF[0], r_ITRF[1], r_ITRF[2],
                          v_ITRF[0], v_ITRF[1], v_ITRF[2] ])
        
        # Linear propagation of the orbit
        if dt < epsilon:
            state = state_0 + np.array([state_0[3] * dt, state_0[4] * dt,
                                        state_0[5] * dt, 0, 0, 0])
        
        return [state, time, dts]
    
    def pz2wgs(self, pz):
    
        R = np.array([[1                , -1.662910926205e-6, 0],
                      [1.662910926205e-6,                  1, 0],
                      [0                ,                  0, 1]])
    
        wgs = np.dot(R, pz)

        return wgs
    
# =============================================================================
# RTCM-SSR constants
# =============================================================================
class Constants:
    """ Class of constants used in the RTCM-SSR Python demo
    """        
    # Earth parameters
    re      = 6.37e6  # [m]
    WGS84_a = 6378137 # [m]
    WGS84_f = 1 / 298.257223564
    omega_e = 7.29211514670e-5 # [rad/s]
    
    # speed of light
    c       = 2.99792458e8
    
    # seconds in a day, week
    day_seconds = 86400.0     
    week_seconds = 604800.0  
        
    # gravitational constant
    mu_gps  = 398600.50e9  # [m^3/s^2]
    mu_gal  = 3.986004418e14 # [m^3/s^2]
    mu_glo  = 398600.44     # [km^3/s^2]  
        
    # relativistic clock correction parameter
    F_gps  = -4.442807633e-10
    F_gal  = -4.442807309e-10