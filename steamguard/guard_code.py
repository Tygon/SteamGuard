'''
Created on May 14, 2016

@author: Tygon
'''

import base64
import hashlib
import hmac

import requests

from .util import TimeAlign

def get_code(secret, code_time=None):
    """
    Gets the 2FA code for the given secret at the given time.

    :param secret: Shared secret as a string.
    :param code_time: Time of code generation. (Defaults to now).

    :returns: 2FA code as a string.
    """
    if not code_time:
        code_time = TimeAlign.get_time()

    #Decode it from base64 to bytes
    secret = base64.b64decode(secret)

    #Get current Unix time (based on seconds)
    unix_time = int(code_time/30)

    #Convert Unix time to bytes
    time_array = unix_time.to_bytes(8, byteorder='big', signed=False)

    #Generate hash using the shared secret as key and time as the message, output to bytes
    hashed_data = hmac.new(secret,msg=time_array,digestmod=hashlib.sha1).digest()

    #The decoding proccess
    b = hashed_data[19] & int('0xF',16)
    code_point = (hashed_data[b] & int('0x7F',16)) << 24 | (hashed_data[b+1] & int('0xFF',16)) << 16 | (hashed_data[b+2] & int('0xFF',16)) << 8 | (hashed_data[b+3] & int('0xFF',16))

    code_array = [1,2,3,4,5]
    steam_guard_code_translations = [50, 51, 52, 53, 54, 55, 56, 57, 66, 67, 68, 70, 71, 72, 74, 75, 77, 78, 80, 81, 82, 84, 86, 87, 88, 89]
    for i in range(0,5):
        code_array[i] = steam_guard_code_translations[int(code_point % len(steam_guard_code_translations))]
        code_point = int(code_point / len(steam_guard_code_translations))
    
    code_point = int(code_point)
    
    #Turn the integers to unicode characters
    for i,c in enumerate(code_array):
        code_array[i] = chr(c)
    
    #Concat the array to one string
    code_array = ''.join(code_array)
    return code_array
