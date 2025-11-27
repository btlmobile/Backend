from fastapi import HTTPException, status


def raise_http_error(
    error_code: str,
    status_mapping: dict[str, int],
    default_status: int = status.HTTP_400_BAD_REQUEST,
) -> None:
    status_code = status_mapping.get(error_code, default_status)
    raise HTTPException(status_code=status_code, detail=error_code)

