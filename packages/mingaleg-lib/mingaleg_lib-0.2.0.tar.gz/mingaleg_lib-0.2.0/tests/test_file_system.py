from textwrap import dedent

from mingaleg_lib.secrets.file_system import secret_file_system


def test_read_hello():
    """
    Test that the read_hello function returns the correct string.
    """
    assert secret_file_system()["hello.txt"].read().decode("utf-8") == dedent(
        """\
        Hello, hello!
        This file is supposed to be encrypted when commited to Git.
        """
    )
