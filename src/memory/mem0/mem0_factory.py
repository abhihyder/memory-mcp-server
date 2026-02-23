from enum import Enum
from config.app import app_config
from .mem0_base import Mem0Base

class Mem0Provider(str, Enum):
    SELF_HOSTED = "self_hosted"
    CLOUD_PLATFORM = "cloud_platform"

class Mem0Factory:
    def __init__(self):
        try:
            self.provider = Mem0Provider(app_config.MEM0_PROVIDER)
        except ValueError:
            raise ValueError(f"Invalid MEM0_PROVIDER: {app_config.MEM0_PROVIDER}. Must be one of: {[p.value for p in Mem0Provider]}")
        
    def create(self)-> Mem0Base:
        if self.provider == Mem0Provider.SELF_HOSTED:
            from .self_hosted import SelfHosted
            return SelfHosted()
        elif self.provider == Mem0Provider.CLOUD_PLATFORM:
            from .cloud_platform import CloudPlatform
            return CloudPlatform()
        else:
            raise ValueError(f"Unsupported MEM0_PROVIDER: {self.provider}")
        
mem0_factory = Mem0Factory()