import logging
import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    from fastapi import Security, FastAPI
    from github_oidc.server import GithubOIDC, GithubOIDCClaims

    app = FastAPI()
    ghoidc = GithubOIDC(audience="atopile.io")

    @app.get("/")
    async def root(
        claims: GithubOIDCClaims = Security(ghoidc),
    ):
        return claims

    return TestClient(app)


def test_invalid_auth(test_client: TestClient):
    response = test_client.get("/", headers={"Authorization": "Bearer invalid-token"})
    with pytest.raises(httpx.HTTPStatusError) as e:
        response.raise_for_status()

    assert e.value.response.status_code == 403


def test_no_auth(test_client: TestClient):
    response = test_client.get("/")
    with pytest.raises(httpx.HTTPStatusError) as e:
        response.raise_for_status()

    assert e.value.response.status_code == 403


def test_with_auth(test_client: TestClient):
    from github_oidc.client import get_actions_header
    from github_oidc.server import logger

    logger.setLevel(logging.DEBUG)

    response = test_client.get("/", headers=get_actions_header("atopile.io"))
    response.raise_for_status()

    assert response.status_code == 200
