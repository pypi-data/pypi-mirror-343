from dependency_injector import containers, providers

from thalentfrx import ThalentFrx
from thalentfrx.configs.Environment import get_environment_variables


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    thalentfrx = providers.Singleton(
        ThalentFrx,
        env=get_environment_variables(),
    )

