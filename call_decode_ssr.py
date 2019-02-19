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

import decode_ssr

""" Test script to use the RTCM-SSR Python Demonstrator as decoder
    Input:
    - f_in : RTCM binary file (i.e. "name.rtc" or "name.bin")
    Output:
    - f_out : txt file of the RTCM message
"""
# =============================================================================
#                         Input and output file names
# =============================================================================
# Input

f_in =  'name.rtc'

# Output:
f_out = 'RTCM3_message.txt' 

# =============================================================================
#                                Call
# =============================================================================
decode_ssr.decode_ssr(f_in, f_out)
