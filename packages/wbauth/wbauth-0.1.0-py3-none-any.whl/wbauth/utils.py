import base64
from io import BytesIO
from PIL import Image
from datetime import datetime, timedelta

def mask_sensitive(data: str, visible_chars: int = 4) -> str:
    """Маскирует чувствительные данные, оставляя видимыми последние visible_chars символов."""
    if len(data) <= visible_chars:
        return data
    return "*" * (len(data) - visible_chars) + data[-visible_chars:]

async def get_image_from_base64(captcha_base64: str) -> Image.Image:
    """Конвертирует base64-строку в изображение."""
    img_data = base64.b64decode(captcha_base64.split(',')[1])
    return Image.open(BytesIO(img_data))