import typing
from data.config import *
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from data.db import *


def just_back():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('↪️ Назад'))
    return keyboard


def main_menu():
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton('🖼 Рандом видео'), KeyboardButton('🖼 Рандом фото'))
    keyboard.add(KeyboardButton('🗂 Альбомы'))
    keyboard.add(KeyboardButton('💼 Профиль'))
    keyboard.add(KeyboardButton('💵 Пополнить баланс'))
    return keyboard


def decide(type):
    markup = InlineKeyboardMarkup(row_width=2)
    kb = [
        InlineKeyboardButton('✅ Купить', callback_data=f'buy:{type}'),
        InlineKeyboardButton('❌ Отмена', callback_data=f'menu')
    ]
    return markup.add(*kb)


def refill(promo):
    return InlineKeyboardMarkup().add(InlineKeyboardButton('✅ Пополнить', callback_data='refill'))


def album_priview_kb(albums: list, current_album):
    markup = InlineKeyboardMarkup(row_width=2)
    index = albums.index(current_album)
    markup.add(InlineKeyboardButton('🖼 Рандом фото', callback_data=f'album:{current_album[0]}:photo'),
               InlineKeyboardButton('🖼 Рандом видео', callback_data=f'album:{current_album[0]}:video')).add(
        InlineKeyboardButton('🗂 Купить альбом', callback_data=f'album:{current_album[0]}:album'))
    markup.add(InlineKeyboardButton(f'{index + 1}/{len(albums)}', callback_data='None'))
    if index == 0:
        markup.add(InlineKeyboardButton('➡️', callback_data='show_album:1'))
    elif index == len(albums) - 1:
        markup.add(InlineKeyboardButton('⬅️', callback_data=f'show_album:{len(albums) - 2}'))
    else:
        markup.add(
            InlineKeyboardButton('⬅️', callback_data=f'show_album:{index - 1}'),
            InlineKeyboardButton('➡️', callback_data=f'show_album:{index + 1}'))
    return markup


def payment_currency_menu():
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='BTC', callback_data='crypto_bot_currency|BTC'),
                InlineKeyboardButton(text='ETH', callback_data='crypto_bot_currency|ETH'),
                InlineKeyboardButton(text='USDT', callback_data='crypto_bot_currency|USDT'),
            ],
            [
                InlineKeyboardButton(text='❌ Отмена', callback_data='profile'),
            ]
        ]
    )

    return markup


def check_crypto(url, invoice_id):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='💳 Пополнить', url=url),
                InlineKeyboardButton(text='🔎 Проверить платеж', callback_data=f'check_crypto_bot|{invoice_id}'),
            ],
            [
                InlineKeyboardButton(text='🔙', callback_data='back'),
            ]
        ]
    )

    return markup


def decide_refill():
    markup = InlineKeyboardMarkup(row_width=2)
    kb = [InlineKeyboardButton('🥝 Qiwi', callback_data='refill:qiwi')]
    if cryptopay_token:
        kb.append(InlineKeyboardButton('🤖 CryptoBot', callback_data='refill:cryptobot'))
    return markup.add(*kb)


def inline_keyboard(pay_sum, comment, code, can_auto_confirm):
    link = f"https://qiwi.com/payment/form/{code}?extra%5B%27account%27%5D={get_settings()[1]}&amountInteger=" \
           f"{pay_sum}&amountFraction=0&extra%5B%27comment%27%5D={comment}&currency=643&blocked%5B0%5D=sum&blocked%5B" \
           f"1%5D=comment&blocked%5B2%5D=account"
    keyboard = InlineKeyboardMarkup()
    kb = [InlineKeyboardButton(text="💵 Оплатить", url=link)]
    if can_auto_confirm:
        kb.append(InlineKeyboardButton('Проверить оплату', callback_data=f'check_qiwi:{comment}:{pay_sum}'))
    keyboard.add(*kb)
    return keyboard


def sub_channels_kb(data: typing.List[typing.Tuple[str, str]]):
    markup = InlineKeyboardMarkup(row_width=1)
    kb = []
    for title, link in data:
        kb.append(InlineKeyboardButton(title, link))
    return markup.add(*kb)
