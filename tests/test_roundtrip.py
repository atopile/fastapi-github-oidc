import httpx
import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    from fastapi import Security, FastAPI
    from github_oidc.server import GithubOIDC, GithubOIDCClaims

    app = FastAPI()

    @app.get("/")
    async def root(
        claims: GithubOIDCClaims = Security(GithubOIDC(audience="some-website.com")),
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
    from github_oidc.client import get_actions_token

    response = test_client.get(
        "/",
        headers={"Authorization": f"Bearer {get_actions_token('some-website.com')}"},
    )
    response.raise_for_status()

    assert response.status_code == 200
