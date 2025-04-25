# Py-Pkpass

![Build Status](https://github.com/GlitchOo/py-pkpass/actions/workflows/ci.yml/badge.svg)

This fork is updated to use the latest version of the cryptography library, includes the NFC method, and additional tests for Python v3.8-3.12.

## Installing this fork

You can install this fork directly from GitHub or with pip:
```
pip install git+https://github.com/GlitchOo/py-pkpass.git
```

```
pip install py-pkpass
```

This Python library helps you create Apple Wallet (.pkpass) files (Apple Wallet was previously known as Passbook in iOS 6 to iOS 8).

For more information about Apple Wallet, see the:
- [Wallet Topic Page](https://developer.apple.com/wallet/)
- [Wallet Developer Guide](https://developer.apple.com/library/ios/documentation/UserExperience/Conceptual/PassKit_PG/index.html#//apple_ref/doc/uid/TP40012195)


## Getting Started

### 1) Get a Pass Type ID

* Visit the [Apple Developer Portal](https://developer.apple.com/) → Certificates, Identifiers & Profiles → Pass Type IDs → New Pass Type ID
* Select your pass type ID → Configure (Follow steps and download the generated pass.cer file)
* Use Keychain Access to export a Certificates.p12 file (you need the Apple Root Certificate installed)

### 2) Generate the certificate and key files (Note: if you are using the latest version of openssl you will need to append -legacy to each command)

```shell
# Export certificate from p12 file
openssl pkcs12 -in "Certificates.p12" -clcerts -nokeys -out certificate.pem   

# Export private key from p12 file
openssl pkcs12 -in "Certificates.p12" -nocerts -out private.key
```

You will be asked for an export password (or export phrase). In the example below, we'll use `123456` as the password.

### 3) Get the Apple WWDR Certificate

Apple Worldwide Developer Relations (WWDR) Certificate is available at [Apple's Certificate Authority](https://www.apple.com/certificateauthority/).

You can export it from Keychain Access into a .pem file (e.g., wwdr.pem).

## Usage Example

```python
#!/usr/bin/env python

from py_pkpass.models import Pass, Barcode, BarcodeFormat, StoreCard

# Create a store card pass type
cardInfo = StoreCard()
cardInfo.addPrimaryField('name', 'John Doe', 'Name')

# Pass certificate information
organizationName = 'Your organization' 
passTypeIdentifier = 'pass.com.your.organization' 
teamIdentifier = 'AGK5BZEN3E'

# Create the Pass object with the required identifiers
passfile = Pass(
    cardInfo, 
    passTypeIdentifier=passTypeIdentifier, 
    organizationName=organizationName, 
    teamIdentifier=teamIdentifier
)

# Set required pass information
passfile.serialNumber = '1234567'
passfile.description = 'Sample Pass'

# Add a barcode - all supported formats: PDF417, QR, AZTEC, CODE128
passfile.barcode = Barcode(
    message='Barcode message',
    format=BarcodeFormat.CODE128,
    altText='Alternate text'
)

# Optional: Add NFC support
nfc_message = "NFCURL:https://example.com/nfc"
encryption_key = "MIIBCgKCAQEAxDvx..."  # Your public encryption key
passfile.nfc_message = nfc_message
passfile.encryption_public_key = encryption_key
passfile.requiresAuthentication = True

# Optional: Set colors
passfile.backgroundColor = "rgb(61, 152, 60)"
passfile.foregroundColor = "rgb(255, 255, 255)"
passfile.labelColor = "rgb(255, 255, 255)"

# Optional: Prevent sharing (disables AirDrop and similar features)
passfile.sharingProhibited = True

# Including the icon and logo is necessary for the passbook to be valid
passfile.addFile('icon.png', open('images/icon.png', 'rb'))
passfile.addFile('logo.png', open('images/logo.png', 'rb'))

# Create and output the Passbook file (.pkpass)
password = '123456'
passfile.create(
    'certificate.pem',
    'private.key',
    'wwdr.pem',
    password,
    'test.pkpass'
)
```

## Testing

You can run the tests with:
```
python -m pytest -v
```

## Credits

Originally developed by [devartis](http://www.devartis.com).

## Contributors

Martin Bächtold
