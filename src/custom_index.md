A custom Tinfoil index is a special JSON file that contains a list of a files, directories, and other special parameters.  To load this index, you can either serve it over a http web server, or you can name it *.tfl and place it in any directory that Tinfoil scans.

## Basic Format

```
{
    "files": ["https://url1", "sdmc:/url2", "http://url3"],
    "directories": ["https://url1", "sdmc:/url2", "http://url3"],
    "success": "motd text here"
}
```

## Detailed Format

```
{
    "files": [
        {
            "url": "https://url1",
            "size": 1000
        },
        {
            "url": "https://url2",
            "size": 3000
        },
        {
            "url": "https://url3",
            "size": 5000
        }
    ],
    "directories": ["https://url1", "sdmc:/url2", "http://url3"],
    "success": "motd text here"
}
```

## Overriding File Names In Urls
Some urls, like gdrive, do not have the correct filename in the URL.  You can tell tinfoil to use a specified filename by using the shebang:

```
gdrive:/abc102234098#filename.nsp
```


## Message of the Day
You can specify a message to be presented to the user by setting either the "success" or "error" json key.

```
{
    "success": "hello world"
}
```

## Referrer
If serving the index over http, you may specify a referrer to prevent others from hotlinking using the "referrer" json key.
```
{
    "referrer": "http://mydomain.com/index.tfl"
}
```

## Google API Key
You may specify a google API key to be used with all gdrive:/ requests using the "googleApiKey" json key.
```
{
    "googleApiKey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

## 1Fichier API Key
You may specify a 1Fichier API key to be used with all 1f:/ requests using the "oneFichierKeys" json key.  If multiple keys are provided, Tinfoil keeps trying them until it finds one that works.
```
{
    "oneFichierKeys": ["ap1key1", "apikey2", "apikey3"]
}
```

## Custom HTTP Headers
You may specify custom HTTP headers to be sent with Tinfoil requests using the "headers" json key.
```
{
    "headers": ["My-Custom_header: hello", "My-Custom_header2: world"]
}
```

## Minimum Tinfoil Version Required
You can specify a minimum Tinfoil version to load the index using the "version" json key.
```
{
    "version": 7.00
}
```

## Client Certificate
You may specify a client certificate using "clientCertPub" and "clientCertKey" json keys.
```
{
    "clientCertPub": "-----BEGIN PUBLIC KEY----- ....",
	"clientCertKey": "-----BEGIN PRIVATE KEY----- ...."
}
```

## Theme Blacklist
You may specify a list of themes to blacklist based on their hash using the "themeBlackList" json key:

```
{
    "themeBlackList": ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]
}
```

## Theme Whitelist
You may specify a list of themes to whitelist based on their hash using the "themeWhiteList" json key:

```
{
    "themeWhiteList": ["AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA", "BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB"]
}
```

## Custom Theme Error Message

You may specify a custom theme error message using the "themeError" json key:

```
{
    "themeError": "please select an authorized theme."
}
```

## Adding User Locations

You may add a new location permenently to the user's File Browser using the "locations" json key:

```
{
    "locations": [
		"https://abc123.com/456/",
		{"url": "https://xyz.com/blah", "title": "xyz", "action"="disable"},
		{"url": "https://xyz.com/blah2", "title": "xyz2", "action"="enable"},
		{"url": "https://xyz.com/blah3", "title": "xyz3", "action"="add"}
	]
}
```

## Adding Metadata

You may add or modify title metadata using the "titledb" json key:

```
{
    "titledb": {
		"050000BADDAD0000": {
			"id": "050000BADDAD0000",
			"name": "Tinfoil",
			"version": 0,
			"region": "US",
			"releaseDate": 20180801,
			"rating": 10,
			"publisher": "N/A",
			"description": "Nintendo Switch Title Manager",
			"size": 14000000,
			"rank": 1
		}
	}
}
```

## Setting Permenent Custom Http Headers

Any file http request can contain the header "x-set-header" which will set a global http header for all subsequent file http requests.  The value should be url encoded:

```
"x-set-header: MyCustomHeader%3A%20hello%20world"
```

## Setting Temporary Custom Http Headers

Any file http request can contain the header "x-tmp-header" which will set a temporary header good only for the current request.  This only works if the headers are set and  then a 301 or 302 redirect is issued.  This is functionally a per-file-http header.  The value should be url encoded:

```
"x-tmp-header: MyCustomHeader%3A%20hello%20world"
```

