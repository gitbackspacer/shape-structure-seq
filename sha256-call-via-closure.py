import timeit

print (timeit.repeat(
'''
import sys
import io 
from io import DEFAULT_BUFFER_SIZE

import base64
import binascii
import hashlib

def compute_hash(hashFunc):
    """ We generate sum_hexdigest  via closure """
   
    hasher = hashFunc() # free var   

    def readBuffer_hasher(input_file, buffersize = DEFAULT_BUFFER_SIZE):
        with open(input_file, 'rb') as f:
           for b in iter(lambda: f.read(buffersize), b''): # or we can use if not f.read(buffersize) break construct
               hasher.update(b)
        return hasher

    return readBuffer_hasher

###--------------------------------------##

file_path = 'test.db'

# sha256
sha256sum = compute_hash(hashlib.sha256)(file_path, buffersize = 8192)
print( binascii.hexlify(sha256sum.digest()).decode())
'''
,
repeat=3, number=1000))

## time using 1k call three repeats

## with class    [1.0990637347204182, 1.0967633780133113, 1.2028534857952224]
## with call     [1.1951834918294357, 1.1704705873799839, 1.1539998794012658]
## with closure  [1.0342765551356459, 0.988626512990237, 0.9791334253932185]
