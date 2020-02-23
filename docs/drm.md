# DRM
Tinfoil supports encrypting custom index jsons, to prevent unauthorized redistribution of direct links to your private content.

## How It Works
It works by generating a random AES-128-ECB key, encrypting your content with that key, and then wrapping the key with asymetrical RSA OAEP 2048-bit and sending it to Tinfoil.

## How to Use
You can use this simple python script to encrypt your index or html files! Run encrypt.py input.json output.tfl to encrypt via command line.