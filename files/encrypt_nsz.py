#/bin/python3
import sys
import os
import base64
from Crypto.Signature import PKCS1_PSS
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA 
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from binascii import hexlify as hx, unhexlify as uhx
import random
import Crypto.Hash
import zlib
import zstandard as zstd
import argparse


buf = None

def encrypt(buf, key):
	cipher = AES.new(key, AES.MODE_ECB)
	sz = len(buf)
	buf = cipher.encrypt(buf + (b'\x00' * (0x10 - (sz % 0x10))))
	return buf
	
parser = argparse.ArgumentParser()
parser.add_argument('files', nargs='*')
parser.add_argument('--aes128', help='aes 128 encryption key')

args = parser.parse_args()
	
chunkSize = 0x100000

if args.aes128:
	if len(args.aes128) != 0x20:
		raise IOError('incorrect aes128 key length')

	key = int(args.aes128, 16).to_bytes(0x10, byteorder='big')
	cipher = AES.new(key, AES.MODE_ECB)
	for file in args.files:
		with open(file, 'rb') as f:
			with open(file + '.aes', 'wb') as o:
				
				while True:
					buf = f.read(chunkSize)
					
					if not buf:
						break
						
					remain = len(buf) % 0x10
					if remain != 0:
						buf += b'\x00' * (0x10-remain)
						
					buf = cipher.encrypt(buf)
					o.write(buf)
	
print('fin')