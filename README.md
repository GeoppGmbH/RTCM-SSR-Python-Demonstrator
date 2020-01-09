# RTCM-SSR Python Demonstrator
v1.1

1. Introduction
   ============
   the RTCM-SSR Python Demonstrator is a software package
   designed to decode RTCM-SSR binary files 
   providing the RTCM-SSR message content in a
   human-readable format and to translate them into 
   Observation Space Representation (OSR),
   dealing with general GNSS-related aspects.
   
   The RTCM-SSR Python Demonstrator can perform
   the following main tasks:
   
   - decoding RTCM-SSR messages v3 and RTCM-SSR proposed messages
   - computing influence from SSR components on 
     a specific user location. 
   
   The GNSSs implemented are GPS, GLONASS, Galileo,
   Beidou, QZSS.
   The decoding involves the following messages:
    - ephemeris
    - satellite orbit and clock corrections
    - code bias
    - phase bias
    - ura
    - high rate clock
    - global ionosphere.
	
	The computed OSR components are sorted by received epoch time and
	satellite ID. Furthermore, the week of the ephemeris used
	for the computation is reported.
	The output quantities are the following:
	- elevation
	- clock correction
	- orbit correction
	- global ionosphere correction
	- Shapiro effect
	- wind up
	- phase bias
	- code bias.

2. Requirements
   ============
   the RTCM-SSR Python Demonstrator 1.0 has been developed
   and tested in Python 3+ environment on Windows.
   
   The following elements are needed in order to use the demo:

   - a computer with Windows operating system
   - a Python 3+ installation
	 (e.g. downloading Anaconda from https://www.anaconda.com/)
   - bitstruct Python module 
     (e.g. from cmd: "conda install bitstruct -c conda-forge")
   - crcmod Python module
	 (e.g. from cmd: "conda install crcmod -c conda-forge")  
   - tkinter Python module
      (e.g. from cmd: "conda install tk -c conda-forge")
   - an rtcm binary file (e.g. *.rtc).
      
3. Notes
   =====
   The results of the decoding of the input rtcm file (binary) 
   is saved in a text file named as the input file
   with ".ssr" extension.
   
   The computed influence from SSR components on user position 
   is saved in a text file named as the input file
   with ".osr" extension. Be aware that the week reported 
   in this file is the week of the used ephemeris.
   Therefore, during the crossing between one week to another,
   the epoch could refer to a different week (i.e. ephemeris week + 1). 
   Furthermore, be aware that the output is sorted per epoch 
   of the received message. 
   
   Moreover, an additional txt file is printed out 
   with ionosphere related parameters,
   e.g. pierce point parameters. It is saved in a 
   text file named as the input file with ".ion" extension.
   
   The script "start_rtcmssr_demo.py" provides a simple GUI 
   to execute the demo. The required inputs are:
   - path of the rtcm-ssr binary file
   - name of the rtcm-ssr file
   - output folder (optional)
   - ellipsoidal (WGS84) latitude, longitude, and height
     (if no input coordinates are given default values are considered:
     lat = 52.5 deg, lon = 9.5 deg, height = 100 m)
   - year and day of the year (DOY).
   
4. Additional information
   ======================
   Geo++ GmbH is the owner of the RTCM-SSR Python Demonstrator,
   developed receiving funding from the European Union's Horizon 2020
   research and innovation programme under the Marie Sklodowska-Curie
   Grant Agreement No 722023. 
   