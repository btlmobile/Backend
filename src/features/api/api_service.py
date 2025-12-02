from __future__ import annotations

from fastapi import Header, HTTPException, status

from src.shared.helpers.tokens import TokenHelper


def get_current_user(authorization: str = Header(include_in_schema=False)) -> str:
    token_helper = TokenHelper()
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="auth_missing_token",
        )
    token = authorization.split(" ", 1)[1]
    try:
        claims = token_helper.verify(token)
        username = claims.get("sub", "")
        if not username:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="invalid_token",
            )
        return username
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
        ) from exc

