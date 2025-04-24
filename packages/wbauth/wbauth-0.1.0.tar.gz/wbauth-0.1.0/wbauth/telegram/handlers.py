from telegram import Update, InputFile, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
import logging
from typing import Optional

from ..authenticator import Authenticator, AuthState
from ..utils import get_image_from_base64, mask_sensitive

logger = logging.getLogger(__name__)

async def cancel_button():
    """Создает кнопку отмены."""
    logger.debug("Создание кнопки отмены")
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🔙 Отмена", callback_data="cancel")]
    ])

async def send_captcha_image(update: Update, captcha_base64: str):
    """Отправляет изображение капчи пользователю."""
    logger.info(f"Отправка изображения капчи пользователю {update.effective_user.id}")
    image = await get_image_from_base64(captcha_base64)
    bio = BytesIO()
    image.save(bio, format="PNG")
    bio.seek(0)
    await update.message.reply_photo(photo=InputFile(bio, filename="captcha.png"))
    logger.info("Изображение कपчи отправлено")

async def send_error_message(update: Update, message: str):
    """Отправляет сообщение об ошибке."""
    logger.error(f"Отправка сообщения об ошибке пользователю {update.effective_user.id}: {message}")
    await update.message.reply_text(f"❌ {message}")

async def start_auth(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Начинает процесс аутентификации."""
    user_id = update.effective_user.id
    logger.info(f"Начало аутентификации для пользователя {user_id}")
    if update.callback_query:
        await update.callback_query.message.reply_text(
            "Введите название для аккаунта (любое):", reply_markup=await cancel_button()
        )
    else:
        await update.message.reply_text(
            "Введите название для аккаунта (любое):", reply_markup=await cancel_button()
        )
    context.user_data['state'] = AuthState.WAITING_USERNAME.value
    context.user_data['authenticator'] = Authenticator(str(user_id))
    logger.info(f"Состояние установлено: {AuthState.WAITING_USERNAME.value}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает сообщения пользователя в зависимости от состояния."""
    user_id = update.effective_user.id
    state = context.user_data.get('state')
    authenticator: Optional[Authenticator] = context.user_data.get('authenticator')
    text = update.message.text.strip()
    logger.info(f"Получено сообщение от пользователя {user_id} в состоянии {state}: {text}")

    if not state or not authenticator:
        logger.warning(f"Некорректное состояние или отсутствует authenticator для пользователя {user_id}")
        await update.message.reply_text("Начните процесс с команды /auth.")
        return

    if state == AuthState.WAITING_USERNAME.value:
        authenticator.username = text
        authenticator.state = AuthState.WAITING_PHONE.value
        context.user_data['state'] = AuthState.WAITING_PHONE.value
        await update.message.reply_text("Введите номер телефона:\nВ формате 79*********", reply_markup=await cancel_button())
        logger.info(f"Пользователь {user_id} ввел имя аккаунта: {text}, переход к вводу телефона")
        return

    if state == AuthState.WAITING_PHONE.value:
        logger.info(f"Пользователь {user_id} ввел телефон: {mask_sensitive(text)}")
        if text.startswith("8"):
            logger.warning(f"Пользователь {user_id} ввел номер, начинающийся с 8: {mask_sensitive(text)}")
            await update.message.reply_text(
                "❌ Номер телефона не должен начинаться с 8. Введите номер, начиная с 7 или другой корректный формат:",
                reply_markup=await cancel_button()
            )
            return
        elif text.startswith("7") and len(text) != 11:
            logger.warning(f"Пользователь {user_id} ввел номер с 7 неправильной длины: {mask_sensitive(text)}")
            await update.message.reply_text(
                "❌ Номер телефона, начинающийся с 7, должен содержать 11 цифр. Пожалуйста, проверьте номер:",
                reply_markup=await cancel_button()
            )
            return
        authenticator.phone_number = text
        result = await authenticator.get_code_or_captcha()
        if isinstance(result, str):
            if result == "sms":
                authenticator.state = AuthState.WAITING_SMS_CODE.value
                context.user_data['state'] = AuthState.WAITING_SMS_CODE.value
                await update.message.reply_text("Введите код из SMS:", reply_markup=await cancel_button())
                logger.info(f"Переход к ожиданию SMS-кода для пользователя {user_id}")
            else:
                await send_error_message(update, result)
        elif isinstance(result, tuple):
            payload, captcha_base64 = result
            authenticator.state = AuthState.WAITING_CAPTCHA.value
            context.user_data['state'] = AuthState.WAITING_CAPTCHA.value
            await send_captcha_image(update, captcha_base64)
            await update.message.reply_text("Введите код с изображения:", reply_markup=await cancel_button())
            logger.info(f"Отправлена капча пользователю {user_id}")
        return

    if state == AuthState.WAITING_CAPTCHA.value:
        logger.info(f"Пользователь {user_id} ввел код капчи: {text}")
        result = await authenticator.submit_captcha(text)
        if isinstance(result, dict):
            captcha_base64 = result.get("captcha", "")
            await send_captcha_image(update, captcha_base64)
            await update.message.reply_text("Неверная капча. Введите новый код:", reply_markup=await cancel_button())
            logger.warning(f"Неверная капча для пользователя {user_id}, отправлена новая")
        elif result == "sms":
            authenticator.state = AuthState.WAITING_SMS_CODE.value
            context.user_data['state'] = AuthState.WAITING_SMS_CODE.value
            await update.message.reply_text("Введите код из SMS:", reply_markup=await cancel_button())
            logger.info(f"Переход к ожиданию SMS-кода для пользователя {user_id}")
        else:
            await send_error_message(update, result or "Ошибка при отправке капчи.")
        return

    if state == AuthState.WAITING_SMS_CODE.value:
        logger.info(f"Пользователь {user_id} ввел SMS-код: {text}")
        result = await authenticator.submit_code(text)
        if result == "email":
            authenticator.state = AuthState.WAITING_EMAIL_CODE.value
            context.user_data['state'] = AuthState.WAITING_EMAIL_CODE.value
            await update.message.reply_text(
                f"Введите код, отправленный на email: {mask_sensitive(authenticator.email_address)}",
                reply_markup=await cancel_button()
            )
            logger.info(f"Переход к ожиданию email-кода для пользователя {user_id}")
        elif isinstance(result, tuple):
            token, wbx_key = result
            authenticator.state = AuthState.END.value
            context.user_data['state'] = AuthState.END.value
            # Здесь можно вызывать внешний callback для сохранения токена
            await update.message.reply_text("Авторизация успешна!")
            logger.info(f"Аутентификация завершена для пользователя {user_id}")
            context.user_data.clear()
        else:
            await send_error_message(update, result or "Ошибка при отправке кода.")
        return

    if state == AuthState.WAITING_EMAIL_CODE.value:
        logger.info(f"Пользователь {user_id} ввел email-код: {text}")
        result = await authenticator.submit_code(text)
        if isinstance(result, tuple):
            token, wbx_key = result
            authenticator.state = AuthState.END.value
            context.user_data['state'] = AuthState.END.value
            # Здесь можно вызывать внешний callback для сохранения токена
            await update.message.reply_text("Авторизация успешна!")
            logger.info(f"Аутентификация завершена для пользователя {user_id}")
            context.user_data.clear()
        else:
            await send_error_message(update, result or "Ошибка при отправке кода.")
        return

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Отменяет процесс аутентификации."""
    user_id = update.callback_query.from_user.id
    logger.info(f"Пользователь {user_id} отменил аутентификацию")
    context.user_data.clear()
    await update.callback_query.message.reply_text("Процесс аутентификации отменен.")
    await update.callback_query.message.delete()

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("Произошла ошибка. Попробуйте снова или используйте /cancel.")