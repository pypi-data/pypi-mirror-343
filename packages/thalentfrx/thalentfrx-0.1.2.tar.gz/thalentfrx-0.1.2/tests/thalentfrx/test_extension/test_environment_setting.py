import pytest
from sqlalchemy.ext.asyncio import async_sessionmaker
from thalentfrx import ThalentFrx
from thalentfrx.configs import Environment
from thalentfrx.configs import EnvironmentSettings
from thalentfrx import TestClient

env: EnvironmentSettings = Environment.get_environment_variables()
app = ThalentFrx(env=env)

def test_get_environment_value():
    pass
    # assert app.env.
    #
    # assert response.status_code == 200, response.text
    # assert response.json() == {
    #     "name": "modelA",
    #     "description": "model-a-desc",
    #     "model_b": {"username": "test-user"},
    # }
