# FastAPI Github OIDC Middleware

FastAPI compatible middleware to authenticate Github OIDC Tokens

## Usage

### Server Side

`uv add "fastapi-github-oidc[server]"`

```python
from fastapi import Security, FastAPI
from github_oidc import GithubOIDC, GithubOIDCClaims

app = FastAPI()

@app.get("/")
async def root(claims: GithubOIDCClaims = Security(GithubOIDC())):
    return claims
```
