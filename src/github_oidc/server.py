from typing import Annotated

from fastapi import HTTPException, Security
from fastapi.security import OpenIdConnect
from fastapi.security.base import SecurityBase
from fastapi.security.utils import get_authorization_scheme_param
from jwt import InvalidTokenError, PyJWKClient, decode
from pydantic import BaseModel
from starlette.status import HTTP_403_FORBIDDEN
from typing_extensions import Doc

oidc = OpenIdConnect(
    openIdConnectUrl="https://token.actions.githubusercontent.com/.well-known/openid-configuration",
)


class GithubOIDCClaims(BaseModel):
    sub: str | None = None
    aud: str | None = None
    exp: int | None = None
    iat: int | None = None
    iss: str | None = None
    jti: str | None = None
    nbf: int | None = None
    ref: str | None = None
    sha: str | None = None
    repository: str | None = None
    repository_id: int | None = None
    repository_owner: str | None = None
    repository_owner_id: int | None = None
    enterprise: str | None = None
    enterprise_id: int | None = None
    run_id: int | None = None
    run_number: int | None = None
    run_attempt: int | None = None
    actor: str | None = None
    actor_id: int | None = None
    workflow: str | None = None
    workflow_ref: str | None = None
    workflow_sha: str | None = None
    head_ref: str | None = None
    base_ref: str | None = None
    event_name: str | None = None
    ref_type: str | None = None
    ref_protected: bool | None = None
    environment: str | None = None
    environment_node_id: str | None = None
    job_workflow_ref: str | None = None
    job_workflow_sha: str | None = None
    repository_visibility: str | None = None
    runner_environment: str | None = None
    issuer_scope: str | None = None


class GithubOIDC(SecurityBase):
    """
    OpenID Connect authentication class. An instance of it would be used as a
    dependency.
    """

    def __init__(
        self,
        *,
        audience: Annotated[
            str,
            Doc(
                """
                The audience string of the token, required to decrypt it.
                """
            ),
        ],
    ):
        self.audience = audience

    async def __call__(
        self, authorization: Annotated[str, Security(oidc)]
    ) -> GithubOIDCClaims:
        scheme, token = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid authorization header"
            )

        try:
            # Extract the token from the Authorization header
            jwks_client = PyJWKClient(
                "https://token.actions.githubusercontent.com/.well-known/jwks"
            )
            signing_key = jwks_client.get_signing_key_from_jwt(token)
            claims = decode(
                token,
                signing_key,
                audience=self.audience,
                algorithms=["RS256"],
            )
            return GithubOIDCClaims(**claims)

        except InvalidTokenError as e:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Invalid token"
            ) from e

        except Exception as e:
            raise HTTPException(
                status_code=HTTP_403_FORBIDDEN, detail="Authentication failed"
            ) from e


if __name__ == "__main__":
    import uvicorn
    from fastapi import FastAPI

    app = FastAPI()

    @app.get("/")
    async def root(
        claims: GithubOIDCClaims = Security(GithubOIDC(audience="atopile.io")),
    ):
        return claims

    # This is hosted openly (0.0.0.0:8000), because it's typically exposed for debugging
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
