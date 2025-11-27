from fastapi import FastAPI


def apply_security_scheme(app: FastAPI) -> None:
    if not app.openapi_schema:
        app.openapi()
    components = app.openapi_schema.setdefault("components", {})
    security_schemes = components.setdefault("securitySchemes", {})

    security_schemes["bearerAuth"] = {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
    }
    app.openapi_schema["security"] = [{"bearerAuth": []}]

