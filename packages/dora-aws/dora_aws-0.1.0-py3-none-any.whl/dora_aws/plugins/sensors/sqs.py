"""S3 Volume Plugin"""
from pydantic import Field

from dora_core.plugins import Sensor

class Profile(Sensor):
    """SQS Sensor plugin Implementation"""
    arn: str = Field(description="Amazon Resource Name")

    @property
    def region(self):
        """Get the region."""
        return str(self.arn).split(":")[3]

    @property
    def account(self):
        """Get the account."""
        return str(self.arn).split(":")[4]

    @property
    def resource(self):
        """Get the function name."""
        return str(self.arn).split(":")[5]

    def render(self, *args, **kwargs):
        """Implement the volume method."""
        return f"https://sqs.{self.region}.amazonaws.com/{self.account}/{self.resource}"
