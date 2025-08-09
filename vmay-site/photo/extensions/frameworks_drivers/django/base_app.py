import os


class BaseAppConfig:
    @staticmethod
    def get_path(file):
        return os.path.join(
            os.path.dirname(os.path.abspath(file))
        )
