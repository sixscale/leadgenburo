import telebot

from django.conf import settings

from .validation import BitrixDeal, Integration

bot = telebot.TeleBot(settings.TG_API_TOKEN)


def send_message_to_tg(deal_info: BitrixDeal, integration: Integration) -> None:
    message = f"""Новый лид: {deal_info.lead_name}_{deal_info.phone};\n
Имя: {deal_info.lead_name};\n
Телефон: {deal_info.phone};\n
Комментарий: {deal_info.lead_comment};\n
Доп. комментарий: {deal_info.lead_type} | {deal_info.lead_qualification};\n
Ссылка на запись: {deal_info.link_to_audio};\n
Дата лида: {deal_info.date};"""
    try:
        send_message(message, integration.tg_bot_id)
    except Exception as e:
        send_message_to_dev_chat(f"Ошибка отправки лида в телеграм: {deal_info.link_to_lead}")


def send_message_to_dev(message: str):
    send_message(
        message,
        settings.TG_DEV_ACCOUNT
    )


def send_message_to_dev_chat(message: str):
    send_message(
        message,
        settings.TG_DEV_CHAT
    )


@bot.message_handler(commands=[])
def send_message(message: str, receiver_id: str):
    bot.send_message(chat_id=receiver_id, text=message)
