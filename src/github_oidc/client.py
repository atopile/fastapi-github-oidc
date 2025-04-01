import os

try:
    import httpx as requestor
except ImportError:
    try:
        import requests as requestor
    except ImportError:
        raise ImportError(
            "Either httpx or requests must be installed to use github_oidc"
        )


def get_actions_token(audience: str) -> str:
    # Get a JWT from the Github API
    # https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect#updating-your-actions-for-oidc
    actions_token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    actions_token_url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    if not actions_token or not actions_token_url:
        raise RuntimeError(
            (
                "No actions token found in environment. Check permissions: "
                "https://docs.github.com/en/actions/security-for-github-actions/security-hardening-your-deployments/about-security-hardening-with-openid-connect#adding-permissions-settings"
            )
        )

    r = requestor.get(
        actions_token_url + f"&audience={audience}",
        headers={"Authorization": f"bearer {actions_token}"},
    )
    r.raise_for_status()

    return r.json()["value"]


if __name__ == "__main__":
    # We don't print this here to avoid exposing the token
    get_actions_token("atopile.io")
