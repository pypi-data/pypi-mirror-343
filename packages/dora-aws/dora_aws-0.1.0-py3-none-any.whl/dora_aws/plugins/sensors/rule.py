"""S3 Volume Plugin"""
from pydantic import Field

from dora_core.plugins import Sensor

DOMAIN = "console.aws.amazon.com/events/home"

class Profile(Sensor):
    """Event Bridge Rule Sensor plugin Implementation"""
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
        return str(str(self.arn).split(":")[5]).split("/")[1]

    def render(self, *args, **kwargs):
        """Implement the volume method."""
        return f"https://{DOMAIN}?region={self.region}#rules/{self.resource}"
