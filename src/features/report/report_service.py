import time
from src.features.report.report_entity import ReportEntity
from src.features.report.report_schema import ReportCreateRequest
from src.shared.helpers.telegram import TelegramHelper
from src.shared.helpers.tokens import TokenHelper
from src.features.sea.bottle.bottle_entity import BottleEntity

class ReportService:
    def __init__(self):
        self._token_helper = TokenHelper()

    async def create_report(self, payload: ReportCreateRequest, authorization: str) -> tuple[bool, str | None]:
        # 1. Extract user
        reporter = self._extract_user(authorization)
        if not reporter:
            return False, "auth_required"

        # 2. Check if bottle exists
        try:
            bottle = BottleEntity.get(payload.bottle_id)
            if not bottle:
                return False, "bottle_not_found"
        except Exception:
             # Redis-om raises NotFoundError if pk not found (?) 
             # Actually .get() raises NotFoundError. Ideally handled here.
             return False, "bottle_not_found"

        # 3. Create Report
        try:
            report = ReportEntity(
                reporter=reporter,
                bottle_id=payload.bottle_id,
                reason=payload.reason,
                created_at=time.time()
            )
            report.save()
        except Exception as e:
            print(f"Error saving report: {e}")
            return False, "internal_error"

        # 4. Send Notification to Telegram
        msg = (
            f"⚠️ <b>NEW REPORT</b>\n"
            f"👤 <b>Reporter:</b> {reporter}\n"
            f"🍾 <b>Bottle ID:</b> {payload.bottle_id}\n"
            f"📝 <b>Content:</b> {bottle.content}\n"
            f"🚫 <b>Reason:</b> {payload.reason}"
        )
        await TelegramHelper.send_message(msg)

        return True, None

    def _extract_user(self, authorization: str | None) -> str:
        if not authorization or not authorization.startswith("Bearer "):
            return ""
        try:
            token = authorization.split(" ", 1)[1]
            claims = self._token_helper.verify(token)
            return claims.get("sub", "")
        except Exception:
            return ""
