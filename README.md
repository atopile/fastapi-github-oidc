# FastAPI Github OIDC Actions Middleware That Just Works™

FastAPI compatible middleware to authenticate [Github OIDC Tokens](https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect)

Want people to use your thing? Great! So we do. Make is easy!

Github OIDC is a secure authentication mechanism with near-zero configuration required for many applications.


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
from github_oidc.client import get_actions_header

response = httpx.get(
    "https://atopile.io",
    headers=get_actions_header("atopile.io"),
)
response.raise_for_status()
```

Then, in your Action:

```yaml
# ...

jobs:
  my-job:
    permissions:
      id-token: write
      contents: read

    steps:
      # ...
      - run: uv run my-script.py
```
