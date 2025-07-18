from ...types.responses import ParametersResponse
from ...enums import Services
from ..base import BaleMethod


class GetParameters(BaleMethod):
    __service__ = Services.CONFIGS.value
    __method__ = "GetParameters"
    
    __returning__ = ParametersResponse
