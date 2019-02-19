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
import rtcm_decoder
import crcmod

""" Decoding of RTCM 3 message

    Input:
    - f_in  : RTCM binary file
    - f_out : txt file of the RTCM message
    
    Output:
    - print decoded message on f_out
    
    ***************************************************************************
    Description:
    decoding the message is performed by finding the RTCM preamble in the byte 
    stream. Then the message length is decoded and the CRC sum check is
    computed (Ref. Numerical Recipes, Press, W. H. et al., 3rd edition,
    cap. 22.4).
    After verification of the CRC the complete message passes to 
    the rtcm_decoder class for decoding.
    
"""

def decode_ssr(f_in, f_out):
    with open(f_in, 'rb') as f:
        data = f.read()
    out = open(f_out, 'w')
    # Description of the preamble 
    preamble = b'\xd3'
# =============================================================================
#                        Loop over the whole message  
# =============================================================================
    i = 0
    while i <= len(data):
        if data[i:i + 1] == preamble:
            frame_header    = data[i:i + 3]
            try:
                frame_header_unpack = bitstruct.unpack('u8u6u10', frame_header)
            except:
                break
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
                dec_msg = rtcm_decoder.rtcm_decoder(msg_content, msg_len)
                # print on file decoded message
                print(dec_msg, file = out)
                i = i + msg_len + 6
            else:
                i = i + 1
                continue
        else:
            i = i + 1

    out.close()        