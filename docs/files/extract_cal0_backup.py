from Crypto.Cipher import AES
from Crypto.Util import Counter
import hashlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('input', nargs='+')
parser.add_argument('--password', '-p', default='', help='password used to encrypt the backup')
args = parser.parse_args()

iv = 0x00000000000000010000000000000000

for path in args.input:
	with open(path, 'rb') as f:
		f.seek(0x7E80)
		timestamp = f.read(8)
		original = f.read(1)
		f.read(7) # junk
		verifiedHash = f.read(0x20)
		f.seek(0x3f3c00)
		buffer = f.read(0x8000)
		
	if verifiedHash == b'\x00' * 0x10:
		print('no backup present')
		exit(-1)

	key = hashlib.sha256(args.password.encode()).digest()[0:0x10]

	ctr = Counter.new(128, initial_value=iv)
	cipher = AES.new(key, AES.MODE_CTR, counter=ctr)
	buffer = cipher.decrypt(buffer)

	hash = hashlib.sha256(buffer).digest()

	if hash != verifiedHash:
		print('hashes do not match, password could be incorrect')
		exit(-1)

	newName = '.'.join(path.split('.')[0:-1]) + '.restored.' + ('clean' if original != 0 else 'dirty') + '.bin'
	with open(newName, 'wb') as f:
		f.write(buffer)
