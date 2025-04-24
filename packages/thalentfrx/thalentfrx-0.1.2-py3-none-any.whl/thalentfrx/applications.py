from fastapi import FastAPI
from thalentfrx.configs.Environment import EnvironmentSettings
from thalentfrx import __version__

class ThalentFrx(FastAPI):

    def __init__(self, env: EnvironmentSettings, *args, **kwargs):
        # Application Environment Configuration
        self.env: EnvironmentSettings = env
        if self.env.API_VERSION is not None:
            version = self.env.API_VERSION
        else:
            version = __version__
        # Instantiate FastAPI
        super().__init__(*args,
                         title = self.env.APP_NAME,
                         version = version,
                          **kwargs)


