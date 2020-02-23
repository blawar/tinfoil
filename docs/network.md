# NUT
NUT is the simplest way to install over the network. It is a piece of software that will serve your NSP's from your PC to your switch over the network, or through USB. All NSP's must have "[titleid]" in the file name to be indexed by NUT to show up in "New Games", "New DLC", and "New Updates".

You can download NUT at https://github.com/blawar/nut/.

#HTTP / HTTPS
Tinfoil downloads the html (or json), and parses out the links. Tinfoil supports relative paths, and absolute if you want to link to a different server, or even another device such as your microSD card.

Tinfoil is known to work with Windows IIS, Apache, and Nginx. Though it should work with any HTTP server that supports ranged requests.

## Headers Sent
Tinfoil will send a few custom headers when requesting a directory only (not files):

### Theme Hash
The user's current Tinfoil theme hash is sent via "Theme: XXXXXXXXXXXXXXX".

### User Fingerprint
A unique user fingerprint is sent via "UID: XXXXXXXXXXXXXX".

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

## URL Format
Both files and folders follow the same format.  If specifying by the google file id, use gdrive:AAAAAAAAAAAAAAAAA (notice lack of forward slash).  If specifying a path (only works with OAuth) use gdrive:/root/folder1/file.zip

## Auth
### OAuth
Google Drive OAuth has the highest priority, and will always be used if setup.  OAuth is the only method to access and list private files.  You must set up google drive OAuth within NUT, and then conenct Tinfoil to NUT via network or USB to transfer the OAuth token(s).

### API Key
Specifying an API key allows you to do authed requests to access private files, however listing files will not work.

### Public
This is the least reliable, however it supports listing and downloading public files.

# Dropbox
Access Token
You need an API key to ue this. Go to https://www.dropbox.com/developers/apps and create a new app, and then click the "generate access token" button to generate an access token to use with Tinfoil.

Adding the location
You can edit the locations.conf file directly by adding an entry for dropbox://token:XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX@api.dropbox.com/ where XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX is your access token.