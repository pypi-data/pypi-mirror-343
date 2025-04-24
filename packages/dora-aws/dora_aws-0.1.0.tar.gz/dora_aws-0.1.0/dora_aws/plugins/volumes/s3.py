"""S3 Volume Plugin"""
from os import path
from pydantic import Field

from dora_core.plugins import Volume

class Profile(Volume):
    """S3 Volume Implementation"""
    bucket: str = Field(description="Bucket name")
    prefix: str = Field(description="Key prefix")
    format: str = Field(description="File format")
    wildcard: str = Field(description="Wildcard", default="*")

    def render(self, *args, **kwargs):
        """Implement the volume method."""
        _file = f"{self.wildcard}.{self.format}"
        if str(self.format).strip().lower() == 'iceberg':
            _file = ""
        _path = path.join(self.bucket,self.prefix,_file)
        return f"s3://{_path}"
