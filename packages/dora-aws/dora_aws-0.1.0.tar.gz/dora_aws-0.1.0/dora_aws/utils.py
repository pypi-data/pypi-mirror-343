"""Dora AWS Utilities."""

from typing import Tuple


def s3_bucket_key(uri: str) -> Tuple[str, str]:
    """
    Extracts the bucket name and key from an S3 URI.

    Args:
        uri (str): The S3 URI to extract the bucket name and key from.
    Returns:
        tuple: A tuple containing the bucket name and key.
    """
    _uri = uri.split("/")
    return _uri[2], "/".join(_uri[3:])
