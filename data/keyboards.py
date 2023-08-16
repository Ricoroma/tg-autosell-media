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
