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
import math
from numpy import linalg as LA
import rtcm_ssr2osr 

"""
    Set of classes to compute global ionospheric influence on a receiver
    location for a particular satellite and for a specific frequency. 
    
    Input:
        - epoch : epoch considered for the computation
        - state : satellite state vector
        - rec   : receiver position
        - system: GNSS system involved
        - ID    : ID of the satellite considered
        - f1    : frequency considered
        - iono  : content of ionospheric RTCM-SSR message 1264
    Output:
        - STEC value for the selected satellite and frequency for the 
          receiver location.
    ***************************************************************************
    Description:          
    the class IonoComputation compute the STEC for a particular satellite + 
    frequency for a specific receiver location. It takes in input the spherical
    harmonics coefficients of the decoded RTCM-SSR ionospheric message. 
    The satellite and receiver positions are passed to the 
    PiercePoint class which compute pierce point parameters. 
    These and the RTCM-SSR message are the input of 
    the compute_legendre_poly method, which calculates the Legendre 
    polynomial needed to compute the VTEC through the compute_vtec method. 
    Finally, the STEC is computed for the desired frequency. 
"""

class IonoComputation:
    def __init__(self, epoch, state, rec, system, ID, f1, iono): 
        
        self.epoch = epoch
        self.sat     = state[0:3]
        self.rec     = rec
        self.re      = rtcm_ssr2osr.Constants().re
        self.omega_e = rtcm_ssr2osr.Constants().omega_e     # [rad/s]
        self.system  = system
        
        self.layers = iono.n_layers
        self.stec_corr_f1 = 0
        self.strg = ''
        for l in range(self.layers):
            self.height = iono.height[l]
            self.sh_deg = iono.degree[l]
            self.sh_ord = iono.order[l]
            self.c      = iono.c[l][:]
            self.s      = iono.s[l][:]

            [lat_sph, lon_sph, height_sph,
             el, az, psi_pp, 
             lambda_pp, phi_pp,
             sf, sun_shift, lon_s,
             p_nm, p_cos, p_sin, m, n,
             vtec] = IonoComputation.compute_global_iono(self)
            stec = vtec * sf
            self.stec_corr_f1 += 40.3 * 1e16 / (f1 * f1) * stec   
                 
            self.strg += ('### SV pos/vel for SV ' + ID + ' at ' + f'{epoch}' +
                          ': ' + '{:16.4f}'.format(state[0]) + '   ' + 
                          '{:16.4f}'.format(state[1]) + '   ' + 
                          '{:16.4f}'.format(state[2]) + ' [m]' + '   ' + 
                          '{:9.4f}'.format(state[3]) + '   ' + 
                          '{:9.4f}'.format(state[4]) + '   ' +  
                          '{:9.4f}'.format(state[5]) + ' [m/s]' + '\n' +
                          'PPt at t=' +
                          f'{epoch}' + '(sun shift= ' +
                          '{:11.8f}'.format(sun_shift * 180 / np.pi) +
                          ' deg)' + ' \n' + 
                          'PPt from Ref phi_R= ' + 
                          '{:11.8f}'.format(lat_sph * 180 / np.pi) + ' lam_R=' + 
                          '{:11.8f}'.format(lon_sph * 180 / np.pi) +  
                          ' rE+hR= ' + '{:10.3f}'.format(height_sph + 6370000) + 
                          '(spherical!)' + '\n' + 
                          'PPt from Ref to SV at elev= ' +
                          '{:11.8f}'.format(el * 180 / np.pi) +  ' azim ' + 
                          '{:11.8f}'.format(az * 180 / np.pi) +
                          '(spherical!)' + '\n' +
                          'PPt psi_pp= ' +
                          '{:11.8f}'.format(psi_pp * 180 / np.pi) +
                          ' phi_pp ' + 
                          '{:11.8f}'.format(phi_pp * 180 / np.pi) +
                          ' lam_pp ' + 
                          '{:11.8f}'.format(lambda_pp * 180 / np.pi) +
                          ' lon_S ' +  
                          '{:11.8f}'.format(lon_s * 180 / np.pi) +
                          ' rE+hI: ' + 
                          '{:10.3f}'.format(self.height * 1000 + 6370000) + '\n'
                          'Pnm : ')
            # Lagrange Polynomials
            for o in range(len(p_nm)):
                m_ind = int(m[o])
                n_ind = int(n[o])
                self.strg += ('P(' + f'{n_ind}' + ',' +
                              f'{m_ind}' + ')=' +
                              '{:7.4f}'.format(p_nm[o]) + '; ')
            # Cosines
            self.strg += '\n' +  'Pcos: '
            for o in range(len(p_cos)):
                m_ind = int(m[o])
                n_ind = int(n[o])
                self.strg += ('P(' + f'{n_ind}' + ',' + 
                              f'{m_ind}' + ')=' +
                              '{:7.4f}'.format(p_cos[o]) + '; ') 
            # Sines
            self.strg += '\n' + 'Psin: '
            for o in range(len(p_sin)):
                m_ind = int(m[o])
                n_ind = int(n[o])
                self.strg += ('P(' + f'{n_ind}' + ',' + 
                              f'{m_ind}' + ')=' +
                              '{:7.4f}'.format(p_sin[o]) + '; ')
            self.strg += ('\n'+
                          'Sum VTEC=' +
                          '{:6.3f}'.format(vtec) + 
                          '[TECU]' + ',' + ' sf=' +
                          '{:6.3f}'.format(sf) +
                          ',' + 'STEC=' +
                          '{:6.3f}'.format(stec) +
                          '[TECU]' + '\n' + 
                          'SSR_VTEC: SV' + ID + 
                          ' Have SSR VTEC Iono slant influence: ' + 
                          '{:6.3f}'.format(stec) + '[TECU]' + 
                          '{:6.3f}'.format(self.stec_corr_f1) +
                          '[m-L1]' + '\n') 
            
    def __str__(self):
        return self.strg
    
    def compute_legendre_poly(self, max_val, lat_pp, lon_s):
        """ Recursive Legendre polynomials computation
        
        """
        x = np.sin(lat_pp) 
        
        # ***** Calculate Legendre polynomials with recursion algorithm ***** #
        nmax    = int(max_val + 1)
        p       = np.zeros((nmax, nmax))
        p[0][0] = 1.0

        for m in range(1, nmax, 1):
            p[m  ][m] = (2 * m - 1) * np.sqrt((1 - x * x)) * p[m - 1][m - 1]

        for m in range(1, nmax - 1, 1):
            p[m + 1][m] = (2 * x + 1) * x * p[m][m]

        for m in range(0, nmax, 1):    
            for n in range(m + 1, nmax, 1):
                p[n][m] = 1 / (n - m) * ((2 * n - 1) * x * p[n - 1][m] -
                                         (n + m - 1) * p[n - 2][m])

        # *********** Compute associated Legendre polynomials Nnm *********** #
        
        p_nm  = []
        p_cos = []
        p_sin = []
        
        m_ind = []
        n_ind = []
        
        for n in range(0, nmax, 1):
            for m in range(0, n + 1, 1):

                s2 = (((2 * n + 1) * math.factorial(n - m)) / 
                      (math.factorial(n + m)))

                if(m == 0):
                    n_nm = np.sqrt(1 * s2) * p[n][m] 
                else:
                    n_nm = np.sqrt(2 * s2) * p[n][m]
    
                p_nm = np.append(p_nm, n_nm)
            
                p_cos  = np.append(p_cos, n_nm * np.cos(m * lon_s)) 
                p_sin  = np.append(p_sin, n_nm * np.sin(m * lon_s)) 
                m_ind = np.append(m_ind, m)
                n_ind = np.append(n_ind, n)
                

                           
        return (p_nm, p_cos, p_sin, m_ind, n_ind)
         
# =============================================================================
#                          VTEC computation    
# =============================================================================
    def compute_vtec(self, order, degree, c_nm, s_nm, p_cos, p_sin):
        """Computation of the VTEC
        
        """
        vtec  = 0            
        nmax    = int(degree + 1)
        i = 0
            
        for n in range(0, nmax, 1):
            mmax = int(np.min([n, order])) + 1
            for m in range(0, mmax, 1):
                tot_1 = 0
                tot_2 = 0
                if m == 0:
                    tot_1 = c_nm[m][0][n] * p_cos[i]

                else:
                    tot_2 = (c_nm[m  ][0][n  ] * p_cos[i] +
                             s_nm[m - 1][0][n - 1] *
                             p_sin[i])

                vtec = vtec + tot_1 + tot_2
                i = i + 1
            
        return vtec
 
# =============================================================================
#                        Global ionospheric corerctions
# =============================================================================    
    def compute_global_iono(self):
        """ Computation of IONO correction per satellite
            
        """
        
        c_nm = []
        s_nm = []
        c_print = np.array(self.c)
        s_print = np.array(self.s)
        order = self.sh_ord
        deg   = self.sh_deg
        nc    = len(self.c)
        ns    = len(self.s)
        h     = self.height
        index = 0
            
        for j in range(int(order) + 1):
            c_nm.append([])
            if index < nc:
                c2append = np.concatenate((np.zeros(j),
                                           c_print[index : index +
                                                   (int(deg) +
                                                    1 - j)]), axis=0)
                c_nm[j].append(c2append)
            index = index + (int(deg) + 1 - j)
                    
        index = 0        
        for j in range(int(order)):
            s_nm.append([])
            if index < ns:
                s2append = np.concatenate((np.zeros(j),
                                           s_print[index : index +
                                            (int(deg) - j)]), axis=0)
                s_nm[j].append(s2append)
            index = index + (int(deg) - j)

        # *********************************************************** #
        #                                                             #
        #                 Pierce Point computation                    #
        #                                                             #
        # *********************************************************** #
        # height needs to be in meter, but the input h is in km
        pp_comp = PiercePoint(self.sat, self.rec, h * 1000)
        # apply spin correction
        xyz_spin = pp_comp.compute_spin_corr()
        pp_comp_spin = PiercePoint(xyz_spin, self.rec,
                                   h * 1000)
        # compute spherical coordinates
        [lat_sph, lon_sph, height_sph] = pp_comp_spin.compute_xyz2sph()
        # compute az and el using spherical coordinates
        [az, el] = pp_comp_spin.compute_az_el(lat_sph, lon_sph)
        
        # compute pierce point
        [psi_pp, lambda_pp, 
         phi_pp, sf,
         sun_shift, lon_s] = pp_comp_spin.compute_pp(lat_sph, lon_sph, 
                                                     height_sph, el, az, 
                                                     self.epoch)

        # computation of the iono delay
        max_val = np.max([order, deg])
        [p_nm, p_cos, p_sin,
         m, n] = IonoComputation.compute_legendre_poly(self, max_val,
                                                       phi_pp, lon_s)
            
        vtec = IonoComputation.compute_vtec(self, order, deg, c_nm, s_nm,
                                            p_cos, p_sin)  
            
        return (lat_sph, lon_sph, height_sph, el, az, psi_pp,
                lambda_pp, phi_pp,
                sf, sun_shift, lon_s, p_nm, p_cos, p_sin, m, n, vtec)

# =============================================================================
#                    Pierce Point computation class        
# =============================================================================
class PiercePoint:
    """ Pierce Point calculator
        including:
            - relative elev, azi computation
        Input:
            - satellite and receiver coordinates
            - ionospheric layer height
        Output:
            - pierce point parameters:
              psi_pp, lambda_pp, phi_pp, slant_factor, sun_shift, lon_s
    """
# =============================================================================
#                           Data and Initialization
# =============================================================================
    def __init__(self, sat, rec, layer_height):
        # Satellite and receiver position in ECEF + layer height
        self.sat    = sat
        self.rec    = rec 
        self.layer_h = layer_height
        # ******************************************************************* #
        #                           Ancillary data                            #
        # ******************************************************************* #
        self.re  = 6.37e6                           # [m]
        
        self.wgs84_a  = 6378137.0                   # [m]
        self.wgs84_e  = 0.0818191908426
        
        self.omega_zero_dot = 7.2921151467e-5       # earth rotation rate rad/s
        self.c              = 2.99792458e+8         # gps para 4.3

# =============================================================================
#                          Relative azimuth elevation  
# =============================================================================
    def compute_az_el(self, lat, lon):
        """ Relative azimuth and elevation computation
        
        Reference:
            "Satellite Orbits", Montenbruck & Gill, chapter 6.2 pages 211-212
        """
        R = np.array([[-np.sin(lon)               ,
                       +np.cos(lon)               ,
                       +0                          ],
                      [-np.sin(lat) * np.cos(lon),
                       -np.sin(lat) * np.sin(lon),
                       +np.cos(lat)                ],
                      [+np.cos(lat) * np.cos(lon),
                       +np.cos(lat) * np.sin(lon),
                       +np.sin(lat)                ]])

        s = np.dot(R, self.sat - self.rec)
        
        azimuth   = np.arctan2(s[0], s[1])
        elevation = np.arctan2(s[2], np.sqrt(s[0] ** 2 + s[1] ** 2))
        
        if azimuth < 0:
            azimuth   = azimuth + 2 * np.pi
        
        return np.array([azimuth, elevation])
        

# =============================================================================
#                     From XYZ coord to spherical lat, lon, height    
# =============================================================================
    def compute_xyz2sph(self):
        """ From coord to spherical lat, lon , height

        """
        
        height_s = LA.norm(self.rec) - self.re
        
        p = LA.norm(self.rec[0:2])
        
        lat_s = np.arctan2(self.rec[2], p)
        lon_s = np.arctan2(self.rec[1], self.rec[0])
        
        return np.array([lat_s, lon_s, height_s])

# =============================================================================
#                    From spherical lat, lon to xyz spherical 
# =============================================================================
    def compute_sph2sph_xyz(self, r, lat, lon):
        """ From spherical lat, lon to xyz spherical
        """
        x = r * np.cos(lat) * np.cos(lon)
        y = r * np.cos(lat) * np.sin(lon)
        z = r * np.sin(lat)
        return np.array([x, y, z])
    
# =============================================================================
#                           XYZ sat SPIN correction    
# =============================================================================
    def compute_spin_corr(self):
        """ Compute satellite spin
          
        """
        self.range = np.sqrt((self.sat[0] - self.rec[0]) ** 2 + 
                             (self.sat[1] - self.rec[1]) ** 2 +
                             (self.sat[2] - self.rec[2]) ** 2)
        sat_spin = np.zeros((1,3))
        sat_spin[0,0] = (self.sat[0] +
                       (self.sat[1] * self.omega_zero_dot *
                        (self.range / self.c)))
        sat_spin[0,1] = (self.sat[1] - (self.sat[0] * self.omega_zero_dot *
                                      (self.range / self.c)))
        sat_spin[0,2] = self.sat[2]
        return sat_spin[0]

# =============================================================================
#                            Pierce Point computation   
# =============================================================================
    def compute_pp(self, lat, lon, height, el, az, t):
        """ Pierce Point computation method
        """

        # ***************** Spherical Earth's central angle ***************** #
        # angle between rover position and the projection of the pierce point 
        # to the spherical Earth surface
        tmp = ((self.re + height) / 
               (self.re + self.layer_h) * np.cos(el))
       
        psi_pp = np.pi / 2 - el - np.arcsin(tmp)
        
        # ******************* Latitude and Longitude PP ********************* #
        tmp    = np.tan(psi_pp) * np.cos(az)
        ctg_lat = 1 / np.tan(lat)
        # Latitude
        phi_pp = (np.arcsin(np.sin(lat) * np.cos(psi_pp) +
                 np.cos(lat) * np.sin(psi_pp) * np.cos(az)))
        
        ang = np.arcsin(np.sin(psi_pp) * np.sin(az) / np.cos(phi_pp))
        
        # Longitude
        if(((lat >= 0) & (+tmp > ctg_lat)) |
           ((lat <  0) & (-tmp > ctg_lat))):
            
            lambda_pp = lon + np.pi - ang
        else:
            lambda_pp = lon + ang
        
        sun_shift = math.fmod((t - 50400) * np.pi / 43200, 2 * np.pi)
        
        lon_s =  math.fmod(lambda_pp + sun_shift, 2 * np.pi)
        
        slant_factor = 1.0 / np.sin(el + psi_pp)
    
        return np.array([psi_pp, lambda_pp, phi_pp, slant_factor,
                         sun_shift, lon_s])