"""Cerberus Schema definition and related methods."""

from dateutil import parser
from datetime import datetime

from cerberus import Validator

def _to_utc_fine(value):
    if isinstance(value, datetime):
        return value.timestamp()
    elif isinstance(value, str):
        dt = parser.parse(value)
        return dt.timestamp()
    elif isinstance(value, float):
        return value    
    raise ValueError("Unsupported date representation.")

def _to_utc(value):
    if isinstance(value, datetime):
        return int(value.timestamp())
    elif isinstance(value, str):
        dt = parser.parse(value)
        return int(dt.timestamp())
    elif isinstance(value, float):
        return int(value)
    elif isinstance(value, int):
        return value    
    raise ValueError("Unsupported date representation.")

SCHEMA = {    
    "ITU-R data set class":{
        "required": True,
        "type": "string",
        "readonly": True, 
        "default": "I/Q",
    },
    "ITU-R Recommendation":{
        "required": True,
        "type": "string",
        "readonly": True, 
        "default": "Rec. ITU-R SM.2117-0",        
    },
    "carrier_frequency":{
        "rename": "RF carrier frequency (Hz)"
    },
    "RF carrier frequency (Hz)":{
        "required": True,
        "type": "float",
        "min": 0,
        "default": 0,
    },
    "sampling_frequency":{
        "rename": "Sampling frequency (Hz)"
    },
    "Sampling frequency (Hz)":{
        "required": True,
        "type": "float",
        "forbidden": [0],
        "min": 0,
        "rename": "Sampling frequency (Hz)"
    },
    "Data set type interpretation":{
        "required": True,
        "type": "string",
        "readonly": True, 
        "default": "Integer types, used to store I/Q data, are interpreted as fix point numbers with the radix point right to the most significant bit.",    
    },
    "unit":{
        "rename": "Data set unit"
    },
    "Data set unit":{
        "required": True,
        "type": "string",        
        "default": "",
        "allowed": ["", "V", "V/m", "A/m"],        
    },
    "scaling":{    
        "rename": "Data set scaling factor"
    },
    "Data set scaling factor":{
        "required": True,
        "type": "float",        
        "default": 1,        
        "rename": "Data set scaling factor"
    },
    "device":{
        "rename": "Device"
    },
    "Device": {
        "type": "string"
    },
    "comment":{        
        "rename": "Comment"
    },
    "Comment":{
        "type": "string"        
    },
    #need to by lower than sampling_frequency
    "bandwidth":{
        "rename": "Filter bandwidth (Hz)"
    },
    "Filter bandwidth (Hz)":{
        "type": "float"
    },
    "timestamp":{
        "rename": "Timestamp coarse (s)"
    },
    "Timestamp coarse (s)":{
        "type": "integer",
        "coerce": _to_utc,
        "min": 0,
        "max": 1767150000
    },
    "timestamp_fine":{
         "rename": "Timestamp fine (ns)"
    },
    "Timestamp fine (ns)":{
        "type": "float",
        "coerce": _to_utc_fine,
        "min": 0,
        "max": 1767150000        
    },
    "latitude":{
         "rename": "Geolocation latitude (degree)"
    },
    "Geolocation latitude (degree)":{
        "type": "float",        
        "min": -180,
        "max": 180
    },
    "longitude":{
        "rename": "Geolocation longitude (degree)"
    },
    "Geolocation longitude (degree)":{
        "type": "float",        
        "min": -90,
        "max": 80
    },
    "altitude":{       
        "rename": "Geolocation altitude (m)"
    },
    "Geolocation altitude (m)":{
        "type": "float",        
        "min": -10e3
    },
    "separation":{                
        "rename": "Geolocation separation (m)"
    },
    "Geolocation separation (m)":{
        "type": "float"
    },
    "speed":{       
        "rename": "Speed over ground magnitude (m/s)"
    },
    "Speed over ground magnitude (m/s)":{
        "type": "float",        
        "min": 0
    },
    "speed_azimuth":{
        "rename": "Speed over ground azimuth (degree)"
    },
    "Speed over ground azimuth (degree)":{
        "type": "float",        
        "min": 0,
        "max": 360
    },
    "orientation_azimuth":{
        "rename": "Orientation azimuth (degree)"
    },
    "Orientation azimuth (degree)":{
        "type": "float",        
        "min": 0,
        "max": 360
    },
    "orientation_elevation":{
        "rename": "Orientation elevation (degree)"
    },
    "Orientation elevation (degree)":{
        "type": "float",        
        "min": -90,
        "max": 90
    },
    "orientation_skew":{
        "rename": "Orientation skew (degree)"
    },
    "Orientation skew (degree)":{
        "type": "float",        
        "min": -180,
        "max": 180
    },
    ######
    "magnetic_declination":{
        "rename": "Magnetic declination (degree)"
    },
    "unsynced_flag":{   
        "rename": "Unsynced timestamp flag"
    },
    "invalid_flag":{ 
        "rename": "Invalid flag"
    },
    "pllunlocked_flag":{  
        "rename": "PLL unlocked"
    },
    "agc_flag":{    
        "rename": "AGC flag"
    },
    "detected_flag":{   
        "rename": "Detected signal flag"
    },
    "spectral_inversion_flag":{        
        "rename": "Spectral inversion flag"
    },
    "overrange_flag":{    
        "rename": "Over range flag"
    },
    "lostsample_flag":{   
        "rename": "Lost sample flag"
    },
    "attenuator":{                 
        "rename": "Attenuator (dB)"
    },
    "antenna_factor":{
        "rename": "Antenna factor (1/m)"
    },
    "reference":{
        "rename": "Reference point"    
    },
    "receiver_impedance":{
        "rename": "Receiver input impedance (Ohm)"
    },
    "Magnetic declination (degree)":{
        "type": "float",        
        "min": 0,
        "max": 360,
        "dependencies": "Orientation azimuth (degree)"        
    },
    "Unsynced timestamp flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Invalid flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "PLL unlocked":{
        "type": "integer",        
        "min": 0,                       
    },
    "AGC flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Detected signal flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Spectral inversion flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Over range flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Lost sample flag":{
        "type": "integer",        
        "min": 0,                       
    },
    "Attenuator (dB)":{
        "type": "float",                          
    },
    "Antenna factor (1/m)":{
        "type": "float"        
    },
    "Reference point":{
        "type": "string",
        "allowed": ["Antenna output port", "Receiver output port"]        
    },
    "Receiver input impedance (Ohm)":{
        "type": "float"        
    }
}

ORDER = ["ITU-R data set class",
"ITU-R Recommendation",
"RF carrier frequency (Hz)",
"Sampling frequency (Hz)",
"Data set type interpretation",
"Data set unit",
"Data set scaling factor",
"Comment",
"Device",
"Filter bandwidth (Hz)",
"Timestamp coarse (s)",
"Timestamp fine (ns)",
"Geolocation latitude (degree)",
"Geolocation longitude (degree)",
"Geolocation altitude (m)",
"Geolocation separation (m)",
"Speed over ground magnitude (m/s)",
"Speed over ground azimuth (degree)",
"Orientation azimuth (degree)",
"Orientation elevation (degree)",
"Orientation skew (degree)",
"Magnetic declination (degree)",
"Unsynced timestamp flag",
"Invalid flag",
"PLL unlocked",
"AGC flag",
"Detected signal flag",
"Spectral inversion flag",
"Over range flag",
"Lost sample flag",
"Attenuator (dB)",
"Antenna factor (1/m)",
"Reference point",
"Receiver input impedance (Ohm)"]

def _user_attrs(field):
    if field.startswith("User"):
        return field
    else:
        return "User " + str(field)

validator = Validator(SCHEMA, allow_unknown={'rename_handler': _user_attrs})
