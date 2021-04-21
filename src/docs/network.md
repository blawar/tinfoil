# NUT
NUT is the simplest way to install over the network. It is a piece of software that will serve your NSP's from your PC to your switch over the network, or through USB. All NSP's must have "[titleid]" in the file name to be indexed by NUT to show up in "New Games", "New DLC", and "New Updates".

You can download NUT at https://github.com/blawar/nut/.

#HTTP / HTTPS
Tinfoil downloads the html (or json) and parses out the links. Tinfoil supports relative paths, and absolute if you want to link to a different server, or even another device such as your microSD card.

Tinfoil is known to work with Windows IIS, Apache, and Nginx. Though it should work with any HTTP server that supports ranged requests.

## Headers Sent
Tinfoil will send a few custom headers when requesting a directory only (not files):

### Theme Hash
The user's current Tinfoil theme hash is sent via "Theme: XXXXXXXXXXXXXXX".

### Host Signature
A signature of the request Url scheme and hostname is sent via "HAUTH: XXXXXXXXXXXXXX".  This value is unique to your domain, and helps prevent forged requests.  Simply verify that the client always sends the correct value.  Do not share this value.

### Host Signature
A signature of the entire request Url is sent via "UAUTH: XXXXXXXXXXXXXX".  This value is unique to your domain, and helps prevent forged requests.  Simply verify that the client always sends the correct value.  Do not share this value.

### User Fingerprint
A unique user fingerprint is sent via "UID: XXXXXXXXXXXXXX".

### User Language
Tinfoil's current language setting is set via "Language: XXXXXXXXXXXXXX".

### Tinfoil Version
The client's Tinfoil version is sent via "Version: 7.00".

## Basic Directory Serving
Just enable directory listing on your web server, and Tinfoil will automatically parse the links. Your web server will automatically generate the html!

## Authorization
## Basic Auth
Basic HTTP authentication is supported, to prevent unauthorized users from accessing your files.
## Client Certificate Auth
A custom client certificate may be specified with a custom index file.

# FTP / FTPS
Tinfoil is known to work with Windows IIS FTP server, and FileZilla. Though it works with many more servers.

# Samba / SMB
Tinfoil supports SMB / Windows File Shares.

#Google Drive
All google drive links use the gdrive: scheme within Tinfoil, however there are three different modes with different priority levels.

#1Fichier
This requires a 1Fichier account.  Generate a 1F api key in your 1F account settings, then input this API key in Tinfoil's options screen (case sensitive).

## Accessing your private 1F files
Go to file browser and add a new location: protocol is 1F, leave everything else the same.

This will only list files and directories associated with your 1F account.

## Public 1F files
Tinfoil does not currently support listing public 1F directories, however you can generate an index of 1F file links using the following format:
```
1f:file_id#name.txt
```

# Split files (JBOD)
If your filesystem / storage provider has a max file size, tinfoil supports split files using an index.
A number in the path changes the file / chunk size.  It can be changed at any time.

Example index file entry:

```
jbod:10000000/sdmc%3A%2Fbah%2Fxaa/sdmc%3A%2Fbah%2Fxab/sdmc%3A%2Fbah%2Fxac/sdmc%3A%2Fbah%2Fxad/sdmc%3A%2Fbah%2Fxae/sdmc%3A%2Fbah%2Fxaf/sdmc%3A%2Fbah%2Fxag/sdmc%3A%2Fbah%2Fxah/sdmc%3A%2Fbah%2Fxai/4036670/sdmc%3A%2Fbah%2Fxaj#filename.zip
```

## Embedding files within files with offsets (JBOD)
jbod supports offsets (in decimal) for embedding data within files (the offset is 100, the size is 1234):

```
jbod:offset/100/1234/sdmc%3A%2Ftest.file
```

## Encrypting files (JBOD)
jbod supports decrypting files.  Only AES-128-ECB is currently supported.  33333333333333333333333333333333 is the encryption key.

```
jbod:aes128/33333333333333333333333333333333/offset/0/1234/sdmc%3A%2Ftest.file
```

The first number is the size of the following chunks.  The chunk size can be changed at anytime, and is often done so for the last chunk since it is often smaller.  The chunks are urlencoded and seperated by forward slashes.

An example python script to encrypt the files is located here:

[encrypt.py](files/encrypt_nsz.py)

## URL Format
Both files and folders follow the same format.  If specifying by the google file id, use gdrive:AAAAAAAAAAAAAAAAA (notice lack of forward slash).  If specifying a path (only works with OAuth) use gdrive:/root/folder1/file.zip

## Auth
### OAuth
Google Drive OAuth has the highest priority and will always be used if setup.  OAuth is the only method to access and list private files.  You must set up google drive OAuth within NUT, and then connect Tinfoil to NUT via network or USB to transfer the OAuth token(s).

### API Key
Specifying an API key allows you to do authed requests to access private files, however listing files will not work.

### Public
This is the least reliable, however it supports listing and downloading public files.

# Dropbox
Access Token
You need an API key to use this. Go to https://www.dropbox.com/developers/apps and create a new app, and then click the "generate access token" button to generate an access token to use with Tinfoil.

Adding the location
You can edit the locations.conf file directly by adding an entry for dropbox://token:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@api.dropbox.com/ where XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX is your access token.
