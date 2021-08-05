"""

- using the call method
- sentinal value check 

"""
import timeit


print (timeit.repeat(
'''
import sys
import io 
from io import DEFAULT_BUFFER_SIZE

import base64
import binascii
import hashlib

class Hash(object): 
    
   def __init__(self, shashFunc):
      self.hasher = shashFunc()  
  
   def __call__(self, input_file, buffersize = DEFAULT_BUFFER_SIZE):

       with open(input_file, 'rb') as f:
          for b in iter(lambda: f.read(buffersize), b''): # or we can use if not f.read(buffersize) break construct
                self.hasher.update(b)

       return self.hasher

 

###--------------------------------------##
file_path = 'test.db'

# sha256
sha256sum = Hash(hashlib.sha256)

sha256sumv = sha256sum(file_path, buffersize = 8192)

print( binascii.hexlify(sha256sumv.digest()).decode() )

'''
,
repeat=3, number=1000))
