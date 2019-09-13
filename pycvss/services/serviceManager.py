
from enum import Enum


###############################################################################
class ServiceManager:

    class ServiceType(Enum):
        MOTION_CAPTURE = 'motioncapture'
        CLASSIFICATION = 'classification'
        # TODO Add ffmpeg binding calls as services alongside
        # the current services

        def __str__(self):
            return self.value.lower()

    def __init__(self, type_: ServiceType):
        self.type = type_
        pass
