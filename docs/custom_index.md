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
