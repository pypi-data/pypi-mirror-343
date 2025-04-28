from ninja.security import HttpBearer


class AuthorizationTokenBase(HttpBearer):
    "DRF compatible token auth that accept both 'Token' and 'Bearer' keywords"

    openapi_bearerFormat = "Token"

    def __call__(self, request):
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Token "):
            request.headers._store["authorization"] = ("Authorization", f"Bearer {auth_header[6:]}")
        return super().__call__(request)
