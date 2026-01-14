import httpx
from src.shared.constants.telegram import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

class TelegramHelper:
    @staticmethod
    async def send_message(text: str) -> bool:
        """
        Gửi tin nhắn đến Telegram group đã cấu hình.
        """
        if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
            print("Telegram not configured")
            return False
            
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": text,
            "parse_mode": "HTML"
        }
        
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(url, json=payload)
                response.raise_for_status()
                return True
        except Exception as e:
            print(f"Error sending telegram message: {e}")
            return False
