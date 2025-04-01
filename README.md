# FastAPI Github OIDC Middleware

FastAPI compatible middleware to authenticate Github OIDC Tokens

This makes authentication via a Github Action trivial.

See: https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect

## Server Side

`uv add "fastapi-github-oidc[server]"`

```python
from fastapi import Security, FastAPI
from github_oidc.server import GithubOIDC, GithubOIDCClaims

app = FastAPI()

@app.get("/")
async def root(claims: GithubOIDCClaims = Security(GithubOIDC())):
    return claims
```

## Client Side

`uv add "fastapi-github-oidc"`

**You must also have either `httpx` or `requests` installed**

```python
from github_oidc.client import get_actions_token

token = get_actions_token(audience="atopile.io")

response = httpx.get(
    "https://atopile.io",
    headers={"Authorization": f"Bearer {token}"},
)
response.raise_for_status()
```