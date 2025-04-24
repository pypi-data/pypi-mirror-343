# -*- coding: utf-8 -*-
import json
import os
import pytest
from unittest.mock import patch, MagicMock, ANY
from path import Path

from py_pkpass.models import Barcode, BarcodeFormat, Pass, StoreCard
from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.serialization import pkcs7

cwd = Path(__file__).parent

wwdr_certificate = cwd / 'certificates' / 'wwdr_certificate.pem'
certificate = cwd / 'certificates' / 'certificate.pem'
key = cwd / 'certificates' / 'private.key'
password_file = cwd / 'certificates' / 'password.txt'

# Check if certificate files exist
CERTS_AVAILABLE = (os.path.exists(certificate) and 
                   os.path.exists(key) and 
                   os.path.exists(wwdr_certificate))

def create_shell_pass():
    """Create a basic pass for testing."""
    cardInfo = StoreCard()
    cardInfo.addPrimaryField('name', 'John Doe', 'Name')
    stdBarcode = Barcode('test barcode', BarcodeFormat.CODE128, 'alternate text')
    passfile = Pass(
        cardInfo, 
        organizationName='Org Name', 
        passTypeIdentifier='Pass Type ID', 
        teamIdentifier='Team Identifier'
    )
    passfile.barcode = stdBarcode
    passfile.serialNumber = '1234567'
    passfile.description = 'A Sample Pass'
    return passfile

@pytest.mark.skipif(not os.path.exists(cwd / 'static/white_square.png'),
                     reason="Test image file missing")
def test_create_manifest_and_signature_format():
    """Test manifest creation and signature format."""
    passfile = create_shell_pass()
    passfile.addFile('icon.png', open(cwd / 'static/white_square.png', 'rb'))
    
    # Create manifest
    manifest_json = passfile._createManifest(passfile._createPassJson())
    manifest = json.loads(manifest_json)
    
    # Check manifest structure
    assert 'pass.json' in manifest
    assert 'icon.png' in manifest
    
    # Each hash should be a 64-character SHA-256 hash
    for file_hash in manifest.values():
        assert len(file_hash) == 64
        # Try to verify it's a valid hex string
        int(file_hash, 16)

@patch('py_pkpass.models.x509.load_pem_x509_certificate')
@patch('py_pkpass.models.serialization.load_pem_private_key')
@patch('py_pkpass.models.pkcs7.PKCS7SignatureBuilder')
def test_signature_crypto_method(mock_builder, mock_load_key, mock_load_cert):
    """Test signature creation using the cryptography library."""
    # Setup mocks
    mock_cert = MagicMock()
    mock_key = MagicMock()
    mock_wwdr = MagicMock()
    mock_builder_instance = MagicMock()
    
    mock_load_cert.side_effect = [mock_cert, mock_wwdr]
    mock_load_key.return_value = mock_key
    mock_builder.return_value.set_data.return_value.add_signer.return_value.add_certificate.return_value.sign.return_value = b'mocked_signature'
    
    # Create pass and test signature creation
    passfile = create_shell_pass()
    manifest_json = passfile._createManifest(passfile._createPassJson())
    
    # Call the signature method
    with patch.object(passfile, '_readFileBytes', return_value=b'mocked_file_bytes'):
        signature = passfile._createSignatureCrypto(
            manifest_json,
            certificate,
            key,
            wwdr_certificate,
            'password123'
        )
    
    # Verify the mocks were called with expected parameters
    assert mock_load_cert.call_count == 2
    mock_load_key.assert_called_once()
    
    # Check that builder methods were called in the correct order with correct args
    mock_builder.return_value.set_data.assert_called_once_with(manifest_json.encode('UTF-8'))
    # Use ANY matcher for the SHA256 object since multiple instances will have different id
    mock_builder.return_value.set_data.return_value.add_signer.assert_called_once_with(
        mock_cert, mock_key, ANY
    )
    # Alternatively, check that it's a SHA256 instance
    args, kwargs = mock_builder.return_value.set_data.return_value.add_signer.call_args
    assert isinstance(args[2], hashes.SHA256)
    
    mock_builder.return_value.set_data.return_value.add_signer.return_value.add_certificate.assert_called_once_with(
        mock_wwdr
    )
    mock_builder.return_value.set_data.return_value.add_signer.return_value.add_certificate.return_value.sign.assert_called_once_with(
        serialization.Encoding.DER, [pkcs7.PKCS7Options.DetachedSignature]
    )
    
    # Check the signature
    assert signature == b'mocked_signature'

@pytest.mark.skipif(not os.path.exists(cwd / 'static/white_square.png'),
                     reason="Test image file missing")
def test_create_zip_structure():
    """Test the structure of the created .pkpass zip file."""
    passfile = create_shell_pass()
    passfile.addFile('icon.png', open(cwd / 'static/white_square.png', 'rb'))
    
    # Mock the signature creation
    with patch.object(passfile, '_createSignatureCrypto', return_value=b'mock_signature'):
        from io import BytesIO
        import zipfile
        
        # Create the .pkpass file in memory
        zip_buffer = BytesIO()
        passfile._createZip(
            passfile._createPassJson(),
            passfile._createManifest(passfile._createPassJson()),
            b'mock_signature',
            zip_file=zip_buffer
        )
        
        # Reset buffer position to beginning
        zip_buffer.seek(0)
        
        # Check zip file structure
        with zipfile.ZipFile(zip_buffer, 'r') as zf:
            file_list = zf.namelist()
            
            # Check required files
            assert 'signature' in file_list
            assert 'manifest.json' in file_list
            assert 'pass.json' in file_list
            assert 'icon.png' in file_list
            
            # Check file contents
            assert zf.read('signature') == b'mock_signature'
            manifest_content = zf.read('manifest.json').decode('utf-8')
            assert 'pass.json' in manifest_content
            assert 'icon.png' in manifest_content

@pytest.mark.skipif(not os.path.exists(cwd / 'static/white_square.png'),
                     reason="Test image file missing")
def test_pass_create_method():
    """Test the main create method that produces the complete .pkpass file."""
    passfile = create_shell_pass()
    passfile.addFile('icon.png', open(cwd / 'static/white_square.png', 'rb'))
    
    # Mock all the required methods
    with patch.object(passfile, '_createPassJson', return_value='{"mock":"json"}'), \
         patch.object(passfile, '_createManifest', return_value='{"mock":"manifest"}'), \
         patch.object(passfile, '_createSignatureCrypto', return_value=b'mock_signature'), \
         patch.object(passfile, '_createZip') as mock_create_zip:
        
        # Call the create method
        from io import BytesIO
        output = BytesIO()
        result = passfile.create(
            certificate,
            key,
            wwdr_certificate,
            'password123',
            zip_file=output
        )
        
        # Verify the methods were called with expected parameters
        mock_create_zip.assert_called_once_with(
            '{"mock":"json"}',
            '{"mock":"manifest"}',
            b'mock_signature',
            zip_file=output
        )
        
        # The result should be the BytesIO object
        assert result == output 