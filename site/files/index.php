<?php

$dh = opendir('.');
$buffer = '';

$publicPem = <<<EAD
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAnjCTLhNi8UHdEUlXMMI/
/LO/TsulwLwfidD3Jey3EWIfHVfms9qE1IBCLl1X0Mb8TNJxFM26sREKnn13+W2M
I8L11T8S1jse2c50Zqp5fg7/qwgM1N/tM6jTU9tmX5SKM0zbLzBhFkTjXvFy67ND
urNZLm8i/XBFKbLTNLu5wUSI6AIG0vhBzFDILhCSHucPKk+JrFNbik+qeNd9wzTT
zIhs2xcBlUzkyBQf64wgmsouZ+1qHBlHDJDoMnM/LVUSELlq/TPK3QPUspCadgTx
qbdqhXycSfshi/1VSxDWkD6Y4FUfHbRsmn1fLKa/lw0nDZQR0I2nwnrxMUSAEEaG
RQIDAQAB
-----END PUBLIC KEY-----
EAD;

$publicKey = openssl_get_publickey($publicPem);
$aesKey = openssl_random_pseudo_bytes(0x10);

while(($file = readdir($dh)) !== FALSE)
{
		if($file[0] == '.') continue;
		$buffer .= '<a href="' . urlencode($file) . '">' . htmlentities($file) . '</a><br/>';
}

if(!openssl_public_encrypt($aesKey, $sealedKey, $publicPem, OPENSSL_PKCS1_OAEP_PADDING))
{
		die('seal failed');
}

$secret = openssl_encrypt($buffer, 'aes-128-ecb', $aesKey, OPENSSL_RAW_DATA);

echo "TINFOIL\xFF";
echo $sealedKey;
echo pack('P', strlen($secret));
echo $secret;