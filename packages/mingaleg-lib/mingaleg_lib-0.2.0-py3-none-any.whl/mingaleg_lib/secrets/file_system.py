"""
This module provides a class for accessing a secret file system.
"""

import os
import tarfile
from functools import cache
from io import BufferedReader, BytesIO
from pathlib import Path
from typing import IO, Union

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA

CWD = Path(__file__).parent


@cache
def secret_file_system(private_key: Union[str, bytes, None] = None) -> "SecretFileSystem":
    """
    Get the secret file system.
    """
    return SecretFileSystem.open(private_key)


class SecretFileSystem:
    """
    A class for accessing a secret file system.
    """

    PRIVATE_KEY_ENVIRON_NAME = "MINGALEG_SECRET_FS_PRIVATE_KEY"

    @classmethod
    def open(cls, private_key: Union[str, bytes, None] = None) -> "SecretFileSystem":
        """
        Open the secret file system.
        """
        if private_key is None:
            try:
                private_key = os.environ[cls.PRIVATE_KEY_ENVIRON_NAME]
            except KeyError as exc:
                raise SecretFileSystemException(
                    "Private key not provided: set the environment variable "
                    f"{cls.PRIVATE_KEY_ENVIRON_NAME} or pass the private key as an argument"
                ) from exc

        for encrypted_file in (CWD / "encrypted").glob("*.bin"):
            try:
                return cls(private_key=private_key, encrypted_data=encrypted_file.open("rb"))
            except InvalidPrivateKey:
                continue
        raise InvalidPrivateKey("Invalid private key")

    def __init__(self, *, private_key: Union[str, bytes], encrypted_data: BufferedReader):
        _private_key = RSA.import_key(private_key)

        enc_session_key = encrypted_data.read(_private_key.size_in_bytes())
        nonce = encrypted_data.read(16)
        tag = encrypted_data.read(16)
        ciphertext = encrypted_data.read()

        # Decrypt the session key with the private RSA key
        cipher_rsa = PKCS1_OAEP.new(_private_key)
        try:
            session_key = cipher_rsa.decrypt(enc_session_key)
        except ValueError as exc:
            raise InvalidPrivateKey(f"Invalid private key: {exc}") from exc

        # Decrypt the data with the AES session key
        cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
        data = cipher_aes.decrypt_and_verify(ciphertext, tag)

        self.tar_fs = tarfile.open(fileobj=BytesIO(data), mode="r:gz")

    def __getitem__(self, key: Union[Path, str]) -> IO[bytes]:
        obj = self.tar_fs.extractfile(str(Path("file_system", key)))
        if obj is None:
            raise FileNotFoundError(f"File {key} not found in secret_file_system")
        return obj


class SecretFileSystemException(Exception):
    """
    An exception that occurs when a secret file system is accessed.
    """


class InvalidPrivateKey(SecretFileSystemException):
    """
    An exception that occurs when an invalid private key is used to access a secret file system.
    """
