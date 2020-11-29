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



def wrapKey(key, pubKey):
	cipher = PKCS1_OAEP.new(pubKey, hashAlgo = Crypto.Hash.SHA256, label=b'')
	return cipher.encrypt(key)
	
def unwrapKey(key, privateKeys):
	for privateKey in privateKeys:
		try:
			privateKey = RSA.importKey(open(privateKey).read())
			cipher = PKCS1_OAEP.new(privateKey, hashAlgo = Crypto.Hash.SHA256, label=b'')
			buf = cipher.decrypt(key)
			print(str(hx(buf)))
			return buf
		except:
			pass
	raise IOError('Failed to decrypt key, private key missing?')

aesKey = random.randint(0,0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF).to_bytes(0x10, 'big')

buf = None

def encrypt(buf, key):
	cipher = AES.new(key, AES.MODE_ECB)
	sz = len(buf)
	buf = cipher.encrypt(buf + (b'\x00' * (0x10 - (sz % 0x10))))
	return buf
	
parser = argparse.ArgumentParser()
parser.add_argument('-v', '--vm', help='vm file to include')
parser.add_argument('--zlib', action="store_true", help='use zlib commpression')
parser.add_argument('--zstd', action="store_true", help='use zstandard commpression')
parser.add_argument('-d', '--decrypt', action="store_true", help='decrypt')
parser.add_argument('-k', '--key', help='public key file to use for encryption')
parser.add_argument('-p', '--privatekeys', nargs='+', help='private keys file to use for decryption')
parser.add_argument('-i', '--input', help='input file', required=True)
parser.add_argument('-o', '--output', help='output file', required=True)

args = parser.parse_args()
	
input = b''

if args.vm and not args.decrypt:
	with open(args.vm, 'rb') as f:
		tmp = f.read()
		input += b'\x13\x37\xB0\x0B'
		input += len(tmp).to_bytes(4, 'little')
		input += tmp

with open(args.input, 'rb') as f:
	input += f.read()
	
flag = 0

if args.decrypt:
	if input[0:7] != b'TINFOIL':
		raise IOError('invalid magic')
		
	flags = input[7] & 0x0F
	
	input = input[8:]
	aesKey = unwrapKey(input[0:256], args.privatekeys)
	input = input[256:]
	
	len = int.from_bytes(input[0:8], byteorder='little')
	
	cipher = AES.new(aesKey, AES.MODE_ECB)
	input = cipher.decrypt(input[8:])
	
	if flags == 0x0E: #zlib
		input = zlib.decompress(input[0:len])
	elif flags == 0x0D: #zstd
		dctx = zstd.ZstdDecompressor()
		input = dctx.decompress(input[0:len])
	elif flags == 0x00: #plaintext
		input = input[0:len]
	else:
		raise IOError('invalid flag')
		
	with open(args.output, 'wb') as f:
		f.write(input)
else:
	if args.zlib:
		flag = 0x0E
		print('compressing with zlib')
		buf = zlib.compress(input, 9)
	elif args.zstd:
		flag = 0x0D
		print('compressing with zstandard')
		cctx = zstd.ZstdCompressor(level=22)
		buf = cctx.compress(input)
	else:
		flag = 0x00
		print('no compression used')
		buf = input
		
	sz = len(buf)

	if args.key:
		flag = flag | 0xF0
		pubKey = RSA.importKey(open(args.key).read())
		sessionKey = wrapKey(aesKey, pubKey)
		cipher = AES.new(aesKey, AES.MODE_ECB)
		buf = cipher.encrypt(buf + (b'\x00' * (0x10 - (sz % 0x10))))
	else:
		sessionKey = b'\x00' * 256
		buf = buf + (b'\x00' * (0x10 - (sz % 0x10)))

	print(aesKey)

	with open(args.output, 'wb') as f:
		f.write(b'TINFOIL')
		f.write(flag.to_bytes(1, byteorder='little'))
		f.write(sessionKey)
		f.write(sz.to_bytes(8, 'little'))
		f.write(buf)
	
print('fin')