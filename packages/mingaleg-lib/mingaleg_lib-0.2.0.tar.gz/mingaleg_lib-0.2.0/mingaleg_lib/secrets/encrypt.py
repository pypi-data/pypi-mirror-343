"""
Generate a tar archive of the source directory and encrypt it with GPG.
"""

import sys
import tarfile
import tempfile
from pathlib import Path

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes

CWD = Path(__file__).parent


def encrypt_secret_file_system(source: Path, public_key_name: str) -> Path:
    """
    Generate a tar archive of the source directory and encrypt it.
    """
    with tempfile.NamedTemporaryFile() as temp_file:
        with tarfile.open(temp_file.name, mode="w:gz") as archive:
            archive.add(source, arcname="file_system", recursive=True)
        source_data = temp_file.read()

    _public_key = RSA.import_key((CWD / "public_keyring" / f"{public_key_name}.pem").read_bytes())
    session_key = get_random_bytes(16)

    cipher_rsa = PKCS1_OAEP.new(_public_key)
    enc_session_key = cipher_rsa.encrypt(session_key)

    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(source_data)

    destination = CWD / "encrypted" / f"{public_key_name}.bin"

    with open(destination, "wb") as f:
        f.write(enc_session_key)
        f.write(cipher_aes.nonce)
        f.write(tag)
        f.write(ciphertext)

    return destination


def encrypt_secret_file_system_all(source: Path) -> list[Path]:
    """
    Encrypt the secret file system for all public keys.
    """
    return [
        encrypt_secret_file_system(source, public_key.stem) for public_key in (CWD / "public_keyring").glob("*.pem")
    ]


def main(argv: list[str]):
    """
    Encrypt the secret file system.
    """
    for path in encrypt_secret_file_system_all(Path(argv[1])):
        print(path)


if __name__ == "__main__":
    main(sys.argv)
