import os
import urllib.parse
import json
import pathlib
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('file', nargs='*')
parser.add_argument('-i', help='random donor file to prepend')
parser.add_argument('-o', '--output', help='output file', required=True)
parser.add_argument('--max-size', type=int, help='output file')

args = parser.parse_args()

src = urllib.parse.quote(str(args.output))

class Input:
	def __init__(self, path, offset, size):
		self.path = path
		self.offset = offset
		self.size = size

def align(f, alignment = 0x10):
	sz = f.tell()
		
	f.write(b'\x00' * (sz % alignment))
	return f.tell()

if args.i:
	with open(args.i, 'rb') as f:
		image = f.read()
else:
	image = None

inputs = []

def expandFiles(paths, maxSize = None):
	files = []
	for path in paths:
		path = pathlib.Path(path).resolve()

		if path.is_file():
			if maxSize is None or os.path.getsize(path) < maxSize:
				files.append(path)
		else:
			for f_str in os.listdir(path):
				f = pathlib.Path(f_str)
				f = path.joinpath(f)
				if maxSize is None or os.path.getsize(str(f)) < maxSize:
					files.append(str(f))
	return files
	
with open(args.output, 'wb') as o:
	if image:
		o.write(image)

	offset = align(o)
	
	for i in expandFiles(args.file, maxSize = args.max_size):
		with open(i, 'rb') as f:
			buffer = f.read()
			
			o.write(buffer)
			inputs.append(Input(i, offset, len(buffer)))
			offset = align(o)
files = []


for i in inputs:
	url = 'jbod:offset/%d/%d/%s#%s' % (i.offset, i.size, src, urllib.parse.quote(str(os.path.basename(i.path))))
	files.append({'url': url, 'size': i.size})

j = json.dumps({'files': files}, sort_keys=True, indent=4)
with open(args.output + '.json', 'w') as f:
	f.write(j)
print(j)
			