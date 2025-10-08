from fastapi import Request


def get_current_username(request: Request) -> str:
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return ""
    token = auth_header.split(" ", 1)[1]
    from src.helper.jwt_helper import verify_token

    payload = verify_token(token)
    if not payload:
        return ""
    return payload.get("username", "")
