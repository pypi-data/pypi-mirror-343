import aiohttp
import logging
from datetime import datetime, timedelta
from enum import Enum
from typing import Tuple, Optional, Union, Dict

from .constants import CODE_ENDPOINT, AUTH_ENDPOINT, HEADERS

logger = logging.getLogger(__name__)

class AuthState(Enum):
    WAITING_USERNAME = "WAITING_USERNAME"
    WAITING_PHONE = "WAITING_PHONE"
    WAITING_CAPTCHA = "WAITING_CAPTCHA"
    WAITING_SMS_CODE = "WAITING_SMS_CODE"
    WAITING_EMAIL_CODE = "WAITING_EMAIL_CODE"
    END = "END"

class Authenticator:
    def __init__(self, identifier: str):
        self.identifier = identifier
        self.session = aiohttp.ClientSession()
        self.state = AuthState.WAITING_USERNAME.value
        self.phone_number: Optional[str] = None
        self.username: Optional[str] = None
        self.sticker: Optional[str] = None
        self.token: Optional[str] = None
        self.wbx_validation_key: Optional[str] = None
        self.email_address: Optional[str] = None
        logger.info(f"Инициализирован Authenticator для identifier={identifier}")

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        await self.session.close()
        logger.info(f"Сессия aiohttp закрыта для identifier={self.identifier}")

    async def get_code_or_captcha(self) -> Union[Tuple[Dict, str], str, None]:
        """Запрашивает код или капчу с сервера."""
        from .utils import mask_sensitive
        logger.info(f"Запрос кода или капчи для телефона={mask_sensitive(self.phone_number)}")
        payload = {"phone_number": self.phone_number, "captcha_code": ""}
        try:
            async with self.session.post(CODE_ENDPOINT, json=payload, headers=HEADERS) as response:
                logger.info(f"HTTP-запрос к {CODE_ENDPOINT}, статус: {response.status}")
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Ответ сервера: {data}")

                if data.get("result") == 4 and data.get("error") == 'waiting resend':
                    ttl = data.get("payload", {}).get("ttl", 60)
                    wait_until = datetime.now() + timedelta(seconds=ttl)
                    logger.warning(f"Слишком много запросов, ожидание до {wait_until}")
                    return f"Слишком много запросов. Попробуйте снова в {wait_until.strftime('%Y-%m-%d %H:%M:%S')}"

                if data.get("payload", {}).get("auth_method") == "sms":
                    self.sticker = data["payload"].get("sticker")
                    logger.info(f"Получен стикер: {mask_sensitive(self.sticker)}")
                    return "sms"

                if data.get("result") == 3 and "captcha" in data.get("payload", {}):
                    payload = data["payload"]
                    captcha_base64 = payload.get("captcha", "")
                    if captcha_base64:
                        logger.info("Капча получена")
                        return payload, captcha_base64
                    logger.error("Капча не предоставлена сервером")
                    return "Капча не предоставлена сервером."

                logger.error("Неизвестный ответ сервера")
                return "Неизвестный ответ сервера."
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка сети при запросе кода/капчи: {e}")
            return f"Ошибка сети: {e}"
        except ValueError as e:
            logger.error(f"Ошибка обработки ответа сервера: {e}")
            return "Ошибка обработки ответа сервера."

    async def submit_captcha(self, captcha_code: str) -> Union[Dict, str, None]:
        """Отправляет код капчи на сервер."""
        logger.info(f"Отправка кода капчи: {captcha_code}")
        payload = {"phone_number": self.phone_number, "captcha_code": captcha_code}
        try:
            async with self.session.post(CODE_ENDPOINT, json=payload, headers=HEADERS) as response:
                logger.info(f"HTTP-запрос к {CODE_ENDPOINT}, статус: {response.status}")
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Ответ сервера: {data}")

                if data.get("result") == 3 and "captcha" in data.get("payload", {}):
                    logger.warning("Неверная капча, получена новая")
                    return data["payload"]

                if "payload" in data and "sticker" in data["payload"]:
                    self.sticker = data["payload"]["sticker"]
                    logger.info(f"Получен стикер: {self.sticker}")
                    return "sms"

                logger.error("Неизвестный ответ сервера")
                return "Неизвестный ответ сервера."
        except aiohttp.ClientError as e:
            logger.error(f"Ошибка сети при отправке капчи: {e}")
            return f"Ошибка сети: {e}"
        except ValueError as e:
            logger.error(f"Ошибка обработки ответа сервера: {e}")
            return "Ошибка обработки ответа сервера."

    async def submit_code(self, code: str) -> Union[Tuple[Optional[str], Optional[str]], str, None]:
        """Отправляет SMS-код или email-код на сервер."""
        from .utils import mask_sensitive
        logger.info(f"Отправка кода: {code}")
        payload = {
            "sticker": self.sticker,
            "code": code if self.state == AuthState.WAITING_EMAIL_CODE.value else int(code)
        }
        endpoint = f"{AUTH_ENDPOINT}/tfa" if self.state == AuthState.WAITING_EMAIL_CODE.value else AUTH_ENDPOINT
        try:
            async with self.session.post(endpoint, json=payload, headers=HEADERS) as response:
                logger.info(f"HTTP-запрос к {endpoint}, статус: {response.status}")
                response.raise_for_status()
                data = await response.json()
                logger.debug(f"Ответ сервера: {data}")

                if data.get("payload", {}).get("preferred_method") == "email":
                    self.email_address = data["payload"].get("email_address")
                    new_sticker = data["payload"].get("sticker")
                    if new_sticker:
                        self.sticker = new_sticker
                        logger.info(f"Обновлен стикер для email-кода: {mask_sensitive(self.sticker)}")
                    else:
                        logger.warning("Новый стикер для email-кода не предоставлен")
                    logger.info(f"Требуется код с email: {mask_sensitive(self.email_address)}")
                    return "email"

                cookies = {key: morsel.value for key, morsel in response.cookies.items()}
                self.wbx_validation_key = cookies.get("wbx-validation-key")
                self.token = data.get("payload", {}).get("access_token")
                logger.debug(f"Куки ответа: {cookies}")

                if self.token and self.wbx_validation_key:
                    logger.info(f"Успешно получены токен и wbx-validation-key")
                    return self.token, self.wbx_validation_key
                logger.error("Не удалось получить токен или ключ")
                return "Не удалось получить токен или ключ."
        except (aiohttp.ClientError, ValueError) as e:
            logger.error(f"Ошибка при отправке кода: {e}")
            return f"Ошибка: {e}"