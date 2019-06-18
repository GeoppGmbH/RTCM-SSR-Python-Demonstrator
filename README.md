# RTCM-SSR-Python-Demonstrator
# v 1.0 

# 1. Introduction

   The RTCM-SSR Python Demonstrator in its current release is
   a software package designed to decode RTCM-SSR binary files 
   providing the RTCM-SSR message content in a
   human-readable format.
   It is developed in Python and it is aimed at providing a
   demo tool useful for decoding RTCM-SSR messages and 
   translating them into Observation Space Representation (OSR),
   dealing with general GNSS-related aspects.
   
   At the moment, the RTCM-SSR Python Demonstrator can perform
   the following main task:
   
   - decoding RTCM-SSR messages v3 and RTCM-SSR proposed messages.
         
   All the available GNSSs are implemented (GPS, GLONASS, Galileo,
   Beidou, QZSS).
   The decoding involves the following messages: ephemeris,
   satellite orbit and clock corrections, code bias, phase bias,
   ura, high rate clock, global ionosphere, regional ionosphere (Geo++ GmbH proposed message).

# 2. Requirements
   
   The RTCM-SSR Python Demonstrator 1.0 has been developed
   and tested in Python 3+ environment, on Windows.
   
   The following elements are needed in order to use the demo:

   - a computer with Windows operating system
   - a Python 3+ installation
   - bitstruct Python module 
   - crcmod Python module
   - a rtcm binary file (e.g. *.rtc).
      
# 3. Notes
   
   The results of the decoding of the input rtcm file (binary) 
   will be saved in the desired text file.
   The test script: "call_decode_ssr.py" is aimed at showing the use of
   the RTCM-SSR Python Demonstrator as decoder. 
   
# 4. Additional information
  
   Geo++ GmbH is the owner of the RTCM-SSR Python Demonstrator,
   developed receiving funding from the European Union's Horizon 2020
   research and innovation programme under the Marie Sklodowska-Curie
   Grant Agreement No 722023. 
   
