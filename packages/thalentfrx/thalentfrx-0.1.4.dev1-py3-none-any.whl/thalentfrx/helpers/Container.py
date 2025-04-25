from dependency_injector import containers, providers
from fastapi import FastAPI

from ThalentFrx import ThalentFrx

class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    thalentfrx = providers.Singleton(
        ThalentFrx,
    )

