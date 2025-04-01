import logging
from github_oidc.server import GithubOIDC, GithubOIDCClaims
import github_oidc.server
import github_oidc.client
import typer
import uvicorn
from fastapi import FastAPI, Security

try:
    import httpx as requestor
except ImportError:
    import requests as requestor


app = typer.Typer()


dummy_server = FastAPI()


@dummy_server.get("/")
async def root(
    claims: GithubOIDCClaims = Security(GithubOIDC(audience="atopile.io")),
):
    return claims


@app.command()
def server():
    # Get better tracebacks from the server for debugging
    github_oidc.server.logger.setLevel(logging.DEBUG)

    # This is hosted openly (0.0.0.0:8000), because it's typically exposed for debugging
    uvicorn.run(
        "github_oidc.debug:dummy_server", host="0.0.0.0", port=8000, log_level="debug"
    )


@app.command()
def client(server: str):
    token = github_oidc.client.get_actions_token(audience="atopile.io")

    r = requestor.get(
        f"{server}/",
        headers={"Authorization": f"bearer {token}"},
    )
    r.raise_for_status()

    print("Done!")


if __name__ == "__main__":
    app()
