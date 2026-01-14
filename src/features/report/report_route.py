from fastapi import APIRouter, Request, Response, status
from fastapi.responses import JSONResponse

from src.features.report.report_schema import ReportCreateRequest
from src.features.report.report_service import ReportService

report_router = APIRouter()
_report_service = ReportService()

@report_router.post("/bottle", status_code=status.HTTP_204_NO_CONTENT)
async def report_bottle(
    request: Request,
    payload: ReportCreateRequest
) -> Response:
    auth_header = request.headers.get("Authorization")
    if not auth_header:
         return JSONResponse(status_code=401, content={"error": "auth_required"})

    success, error = await _report_service.create_report(payload, auth_header)
    
    if not success:
        status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        if error == "auth_required":
            status_code = status.HTTP_401_UNAUTHORIZED
        elif error == "bottle_not_found":
            status_code = status.HTTP_404_NOT_FOUND
        
        return JSONResponse(status_code=status_code, content={"error": error})
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
