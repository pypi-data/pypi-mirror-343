from enum import Enum


class ApiVersion(Enum):
    V1 = "v1"

    @staticmethod
    def get_default():
        return ApiVersion.V1
