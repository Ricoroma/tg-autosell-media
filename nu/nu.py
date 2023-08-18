import os
import string
import time
from data.qiwi import *
from aiocryptopay import AioCryptoPay
from data.cryptopay import *
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, Message, \
    CallbackQuery, InputFile, InputMedia

from data import db
from data.config import *
from data.is_sub import IsSub
from data.loader import dp, bot
from data.keyboards import *
import requests


class States(StatesGroup):
    menu = State()
    pay = State()
    pay_sum = State()
    admin_mail = State()
    admin_mail_accept = State()
    album_name = State()
    album_preview = State()
    album_link = State()
    album_path = State()
    album_prices = State()
    album_desc = State()


# ------------------------------

def profile(user_id):
    _data = db.get_info(user_id)
    return f"""<b>Привет, {_data[2]}!</b>

👤 <b>Ваш ID:</b> {_data[1]}
📅 <b>Дата регистрации:</b> {_data[3]}
💵 <b>Баланс:</b> {_data[5]} ₽ 

<b>Зарабатывай по {db.get_settings()[5]}₽ за каждого приглашенного друга!</b>

👤 <b>Приглашено:</b> {db.get_refs(user_id)}
<b>t.me/{link}?start={user_id}</b>

<b>Администратор:</b> {admin_link} 
"""


def get_user_info(user_id):
    _data = db.get_info(user_id)
    _pre_ref = db.get_pre_ref(user_id)
    _pre_ref_str = f"""{_pre_ref} (@{db.get_info(_pre_ref)[2]})""" if int(_pre_ref) != 0 else "Нет"
    return f"""INFO *@{_data[2]}*

👤 *ID:* {_data[1]}
📅 *Дата регистрации:* {_data[3]}
💵 *Баланс:* {_data[5]}

👤 *Реферал:* {_pre_ref_str}

👤 *Приглашено:* {db.get_refs(user_id)}
"""


# ------------------------------

async def get_sub_channels():
    channels = []
    for channel_id in sub_channels:
        channel = await bot.get_chat(channel_id)
        channels.append((channel.title, channel.invite_link))
    return channels


@dp.message_handler(IsSub(), state='*')
async def send_not_sub(message: Message, state: FSMContext):
    await message.answer('Для продолжения пользования ботом вам необходимо подписаться на каналы:\n'
                         '\n\nКогда вы будете подписаны на все каналы, нажмите /start',
                         reply_markup=sub_channels_kb(await get_sub_channels()))
    data = await state.get_data()
    if not db.get_users_exist(message.from_user.id):
        if 'ref' not in data.keys():
            if message.text.startswith('/start '):
                ref = message.text.replace('/start ', '')
                await state.update_data(ref=ref)
            else:
                await state.update_data(ref='')


@dp.callback_query_handler(IsSub(), state='*')
async def send_not_sub(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Для продолжения пользования ботом вам необходимо подписаться на каналы:\n'
                              '\n\nКогда вы будете подписаны на все каналы, нажмите /start',
                              reply_markup=sub_channels_kb(await get_sub_channels()))


# Меню
@dp.message_handler(text=["💼 Профиль", "↪️ Назад"], state="*")
@dp.message_handler(commands=["start"], state="*")
async def menu(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    _user_id = message.chat.id
    _username = message.chat.username
    if not (db.get_users_exist(message.chat.id)):
        if message.text.startswith("/start ") or 'ref' in data.keys():
            if 'ref' in data.keys():
                _ref = data['ref']
            else:
                _ref = message.text.replace('/start ', '')
            if _ref.isdigit():
                if (int(message.chat.id) != int(_ref)):
                    db.add_user_to_db(message.chat.id, message.chat.username, _ref, db.get_settings()[4])
                    db.set_balance(_ref, db.get_balance(_ref) + db.get_settings()[5])
                    await bot.send_message(chat_id=admin_id,
                                           text=f"Новый пользователь: {_user_id} (@{_username})\nПригласил: {_ref}")
                    await bot.send_message(chat_id=_ref,
                                           text=f"*Кто-то перешел по твоей ссылке!*\nБаланс пополнен на {db.get_settings()[5]}",
                                           parse_mode='Markdown')
            else:
                db.add_user_to_db(message.chat.id, message.chat.username, 0, db.get_settings()[4])
                await bot.send_message(chat_id=admin_id, text=f"Новый пользователь: {_user_id} (@{_username})")
        else:
            db.add_user_to_db(message.chat.id, message.chat.username, 0, db.get_settings()[4])
            await bot.send_message(chat_id=admin_id, text=f"Новый пользователь: {_user_id} (@{_username})")
    db.update_nickname(_user_id, _username)
    await message.answer(profile(_user_id), reply_markup=main_menu(), parse_mode="HTML")
    await States.menu.set()


@dp.callback_query_handler(text='profile', state='*')
async def menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    db.update_nickname(call.from_user.id, call.from_user.username)
    await call.message.answer(profile(call.from_user.id), reply_markup=main_menu(), parse_mode="HTML")
    await call.message.delete()
    await States.menu.set()


@dp.callback_query_handler(text='refill', state='*')
@dp.message_handler(text=["💵 Пополнить баланс"], state='*')
async def menu(update: Message | CallbackQuery, state: FSMContext):
    _user_id = update.from_user.id
    _username = update.from_user.username
    if type(update) == CallbackQuery:
        await update.message.edit_text(f"💵 *Введите сумму пополнения* (целое количество рублей)", parse_mode="Markdown")
    else:
        await update.answer(f"💵 *Введите сумму пополнения* (целое количество рублей)", reply_markup=just_back(),
                            parse_mode="Markdown")
    await States.pay.set()


@dp.message_handler(state=States.pay)
async def process_refill(message: Message, state: FSMContext):
    try:
        amount = int(message.text)
    except ValueError:
        await message.answer('Вы ввели некорректную сумму. Введите целое число')
        return
    await message.answer('💳 Выберите платёжную систему', reply_markup=decide_refill())
    await state.update_data(amount_rub=amount)


@dp.callback_query_handler(text_startswith='refill:', state='*')
async def choose_refill_way(call: CallbackQuery, state: FSMContext):
    way = call.data.split(':')[1]
    data = await state.get_data()
    if way == 'cryptobot':
        amount = data['amount_rub'] * get_course('RUB', 'USD')
        await call.message.edit_text('Выберите валюту оплаты', reply_markup=payment_currency_menu())
        await state.update_data(amount=amount)
    else:
        amount = data['amount_rub']
        _code = 99 if db.get_settings()[1].isdigit() else 99999
        _random = random_order()
        can_auto_confirm = True if qiwi_token else False
        adding = '__При оплате ОБЯЗАТЕЛЬНО укажите в комментарии айди (выше)__' if not db.get_settings()[
            1].isdigit() else ''
        await call.message.edit_text(f"""
        *📈 Пополнение ID* `{_random}`
        
        Сумма - {amount} ₽

        *Для оплаты перейдите по кнопке ниже*\n\n{adding}
        """,
                                     reply_markup=inline_keyboard(amount, _random, _code, can_auto_confirm),
                                     parse_mode="Markdown")
        if not can_auto_confirm:
            await call.message.answer('После оплаты перешлите администратору сообщение выше')


@dp.callback_query_handler(text_startswith='check_qiwi', state='*')
async def check_qiwi_handler(call: CallbackQuery, state: FSMContext):
    if check_qiwi(*call.data.split(':')[1:]):
        await call.answer('✅ Пополнение успешно')
        await call.message.delete()
        amount = int(call.data.split(':')[2])
        db.set_balance(call.from_user.id, db.get_balance(call.from_user.id) + amount)
        await call.message.answer(f'Баланс пополнен на {amount} ₽', reply_markup=main_menu())
    else:
        await call.answer('❌ Пополнение не было осуществлено')
        print(call.data)


@dp.callback_query_handler(text_startswith='crypto_bot_currency', state='*')
async def crypto_bot_currency_msg(call: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    amount = data['amount']
    cryptopay = AioCryptoPay(cryptopay_token)
    invoice = await cryptopay.create_invoice(asset=call.data.split('|')[1],
                                             amount=await get_crypto_bot_sum(amount, call.data.split('|')[1]))
    await cryptopay.close()
    await call.message.edit_text(
        text=f'<b>\n\nКоличество: {data["amount_rub"]} руб\nВалюта: {call.data.split("|")[1]}\n\n'
             f'❕ Продолжите пополнеие по кнопке ниже:</b>',
        reply_markup=check_crypto(invoice.pay_url, invoice.invoice_id), parse_mode='HTML')


@dp.callback_query_handler(text='back', state='*')
async def back_to_currencies(call: CallbackQuery, state: FSMContext):
    await call.message.edit_text('Выберите валюту оплаты', reply_markup=payment_currency_menu())


@dp.callback_query_handler(text_startswith="check_crypto_bot", state='*')
async def check_crypto_bot_funds(call: types.CallbackQuery, state: FSMContext):
    try:
        if await check_crypto_bot_invoice(int(call.data.split('|')[1])):
            amount = (await state.get_data())["amount_rub"]
            await call.message.edit_text(f'✅ Баланс пополнен на {amount} руб')
            db.set_balance(call.from_user.id, db.get_balance(call.from_user.id) + amount)
            await state.finish()
        else:
            await bot.answer_callback_query(call.id, '❗ Платеж не найден', True)
    except Exception as e:
        print(e)


# ------------------------------
@dp.message_handler(text='🖼 Рандом видео', state='*')
async def user_video(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Цена видео - {db.get_settings()[2]}. У вас - {db.get_balance(message.from_user.id)}\n'
                         f'Купить случайное видео?', reply_markup=decide('video'))


@dp.message_handler(text='🖼 Рандом фото', state='*')
async def user_photo(message: Message, state: FSMContext):
    await state.finish()
    await message.answer(f'Цена фото - {db.get_settings()[3]}. У вас - {db.get_balance(message.from_user.id)}\n'
                         f'Купить случайное фото?', reply_markup=decide('photo'))


@dp.callback_query_handler(text_startswith='buy')
async def buy_random(call: CallbackQuery, state: FSMContext):
    await state.finish()
    to_buy = call.data.split(':')[1]
    price = db.get_settings()[2] if to_buy == 'video' else db.get_settings()[3]
    balance = db.get_balance(call.from_user.id)
    if price > balance:
        promo = f't.me/{link}?start={call.from_user.id}'
        await call.message.edit_text('На вашем балансе недостаточно средств. Вы можете пригласить друга по ссылке '
                                     f'<code>{promo}</code> или пополнить баланс', reply_markup=refill(promo),
                                     parse_mode='HTML')
    else:
        db.set_balance(call.from_user.id, balance - price)
        if to_buy == 'video':
            video = db.get_random_video(call.from_user.id)
            message = await bot.send_video(call.from_user.id, video[2], caption=f'Альбом - {video[3]}')
            db.add_file_id(video[0], message.video.file_id)
        else:
            photo = db.get_random_photo(call.from_user.id)
            message = await bot.send_photo(call.from_user.id, photo[2], caption=f'Альбом - {photo[3]}')
            db.add_file_id(photo[0], message.photo[-1].file_id)


@dp.message_handler(text='🗂 Альбомы', state='*')
@dp.callback_query_handler(text_startswith='show_album:', state='*')
async def show_albums(update: Message | CallbackQuery, state: FSMContext):
    data = await state.get_data()
    if 'albums' in data.keys():
        albums = data['albums']
        album = albums[int(update.data.split(':')[1]) if type(update) == CallbackQuery else 0]
    else:
        albums = db.get_all_albums()
        album = albums[0]
        await state.update_data(albums=albums)
    prewiew = db.get_file(album[2])[2]
    photo_count, video_count = db.get_photo_and_video_amount(album[1])
    text = f'{album[1]}\n\n{album[-1]}\n\nФото - {photo_count} шт., {album[4]} руб\nВидео - {video_count} шт., ' \
           f'{album[5]} руб\n\n' \
           f'💰 Цена альбома - {album[6]} руб'
    if type(update) == Message:
        await bot.send_photo(update.from_user.id, prewiew, text, reply_markup=album_priview_kb(albums, album))
    else:
        await update.message.delete()
        await bot.send_photo(update.from_user.id, prewiew, text, reply_markup=album_priview_kb(albums, album))


@dp.callback_query_handler(text_startswith='album', state='*')
async def buy_from_album(call: CallbackQuery, state: FSMContext):
    if 'albums' in await state.get_data():
        album = next(i for i in (await state.get_data())['albums'] if int(call.data.split(':')[1]) == i[0])
    else:
        album = db.get_album(call.data.split(':')[1])
    to_buy = call.data.split(':')[2]
    price = album[4] if to_buy == 'photo' else album[5] if to_buy == 'video' else album[6]
    balance = db.get_balance(call.from_user.id)
    if price > balance:
        promo = f't.me/{link}?start={call.from_user.id}'
        await call.message.answer('На вашем балансе недостаточно средств. Вы можете пригласить друга по ссылке '
                                  f'<code>{promo}</code> или пополнить баланс', reply_markup=refill(promo),
                                  parse_mode='HTML')
    else:
        if to_buy == 'video':
            while True:
                try:
                    video = db.get_video_from_album(album[1], call.from_user.id)
                    message = await bot.send_video(call.from_user.id, video[2])
                    db.add_file_id(video[0], message.video.file_id)
                    break
                except:
                    continue
        elif to_buy == 'photo':
            photo = db.get_photo_from_album(album[1], call.from_user.id)
            message = await bot.send_photo(call.from_user.id, photo[2])
            db.add_file_id(photo[0], message.photo[-1].file_id)
        else:
            await bot.send_document(call.from_user.id, album[3])
        db.set_balance(call.from_user.id, balance - price)


# ------------------------------

@dp.message_handler(commands="admin", state="*")
async def admin_menu(message: types.Message, state: FSMContext):
    if message.chat.id == admin_id:
        keyboard = InlineKeyboardMarkup()
        keyboard.add(InlineKeyboardButton(text="📬 Рассылка", callback_data=f"admin_mail"))
        _settings = db.get_settings()
        await message.answer(f"""💼 *Меню администратора*

👥 Пользователей всего: {len(db.get_all_users())}
👤 За неделю: {len(db.get_old_users(7))}
👤 За день: {len(db.get_old_users(1))}

📝 *Настройки*

Qiwi - {_settings[1]}
Цена видео - {_settings[2]}
Цена фото - {_settings[3]}
Начальный баланс - {_settings[4]}
Бонус рефки - {_settings[5]}

*/help* - Список команд админа
""", parse_mode="Markdown", reply_markup=keyboard)


@dp.message_handler(commands=['add'], state='*')
async def start_adding_album(message: Message, state: FSMContext):
    if message.chat.id != admin_id:
        return
    await state.finish()
    await message.answer('Введите название альбома')
    await States.album_name.set()


@dp.message_handler(state=States.album_name)
async def enter_alb_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await States.album_path.set()
    await message.answer('Архив')


@dp.message_handler(state=States.album_path, content_types=types.ContentType.DOCUMENT)
async def enter_link(message: Message, state: FSMContext):
    await state.update_data(arc=message.document.file_id)
    await States.album_prices.set()
    await message.answer('цены (фото пробел видео пробел альбом)')


@dp.message_handler(state=States.album_prices)
async def enter_link(message: Message, state: FSMContext):
    await state.update_data(prices=list(map(int, message.text.split())))
    await States.album_desc.set()
    await message.answer('описание')


@dp.message_handler(state=States.album_desc)
async def enter_link(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await States.album_preview.set()
    await message.answer('превью')


@dp.message_handler(state=States.album_preview, content_types=types.ContentType.PHOTO)
async def enter_prewiew(message: Message, state: FSMContext):
    await message.answer('Альбом создан')
    file_id = message.photo[-1].file_id

    data = await state.get_data()
    try:
        archieve = await bot.get_file(data['arc'])
        path = f'downloaded/{archieve.file_id}.zip'
        await bot.download_file(archieve.file_path, path)
    except:
        path = media_folder + fr'\{data["name"]}.zip'

    db.create_album(data['name'], file_id, data['arc'], path, data['prices'], data['description'])
    os.remove(path)
    await state.finish()


@dp.message_handler(commands=["qiwi", "video", "photo", "stbal", "bonus"], state="*")
async def admin_menu(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        if (message.text.count(" ") > 0):
            _data = message.text.split(" ")
            _command = _data[0][1:]
            _value = _data[1]
            if (_value.isdigit() or _command == "qiwi"):
                db.update_settings(_command, _value)
                await message.answer(f"✅ Значение {_command} изменено на {_value}", parse_mode="Markdown")
            else:
                await bot.send_message(message.chat.id, f"Неверный формат команды")
        else:
            await bot.send_message(message.chat.id, f"Неверный формат команды")


@dp.message_handler(commands=['del'], state='*')
async def albums_to_delete(message: Message, state: FSMContext):
    if message.from_user.id == admin_id:
        await state.finish()
        db.delete_album(message.text.split('-')[1].strip(' '))
        await message.answer('Альбом удалён')


@dp.message_handler(commands="help", state="*")
async def admin_help(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        await message.answer(f'''💼 *Команды админа*

*/help* - Список команд админа
*/top* - Рейтинг пользователей
*/pay 123 999* - Пополнение пользователю с ID 123 на 999
*/pay all 100* - Пополнение всем
*/info 123* - Информация о пользователе с ID 123
*/add* - добавить альбом
*/del - Название альбома* - удалить альбом
📝 *Изменение настроек*

*/video 123* - стоимость видео
*/photo 123* - стоимость фото
*/stbal 123* - начальный баланс
*/bonus 123* - бонус за приглашение
''', parse_mode="Markdown")


# ------------------------------

@dp.callback_query_handler(state=States.admin_mail_accept)
async def admin_mail(call: types.CallbackQuery, state: FSMContext):
    if (call.data == "admin_back_2"):
        for i in range(4):
            await bot.delete_message(call.from_user.id, call.message.message_id - i)
        await States.menu.set()
        await bot.send_message(call.from_user.id, "Отменено")
    elif (call.from_user.id == admin_id):
        if (call.data == "admin_mail_accept"):
            _data = await state.get_data()
            text = _data['text']
            _type = _data['type']
            photo = _data['photo']
            users = db.get_all_users()
            a = 0
            for user in users:
                try:
                    if (_type == 'text_only'):
                        await bot.send_message(user[0], text, parse_mode="HTML")
                    elif (_type == 'photo'):
                        await bot.send_photo(user[0], photo, text, parse_mode="HTML")
                    a += 1
                    time.sleep(0.1)
                except:
                    pass
            for i in range(4):
                await bot.delete_message(call.from_user.id, call.message.message_id - i)
            await States.menu.set()
            await bot.send_message(call.from_user.id, f"✅ Рассылка успешно завершена\nПолучили {a} пользователей")


@dp.callback_query_handler(state="*")
async def admin_calls(call: types.CallbackQuery, state: FSMContext):
    if (call.from_user.id == admin_id):
        if (call.data == "admin_back"):
            await bot.delete_message(call.from_user.id, call.message.message_id)
            await States.menu.set()
            await bot.send_message(call.from_user.id, "Отменено")
        elif (call.data == "admin_mail"):
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back"))
            await bot.send_message(call.from_user.id, "Введите текст рассылки: ", reply_markup=keyboard)
            await States.admin_mail.set()
        await call.answer()


@dp.message_handler(state=States.admin_mail)
async def admin_mail(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        try:
            text = message.text
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
            keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
            await state.update_data(text=text)
            await state.update_data(photo=-1)
            await States.admin_mail_accept.set()
            await bot.send_message(message.chat.id, text, parse_mode="HTML")
            await bot.send_message(message.chat.id, f"Начать рассылку для {len(db.get_all_users())} пользователей?",
                                   reply_markup=keyboard)
            await state.update_data(type='text_only')
        except:
            await bot.send_message(message.chat.id, f"❌ Неверный текст")


@dp.message_handler(content_types=types.ContentTypes.PHOTO, state=States.admin_mail)
async def admin_mail_photo(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        try:
            text = message.caption
            keyboard = InlineKeyboardMarkup()
            keyboard.add(InlineKeyboardButton(text="✅ Начать", callback_data=f"admin_mail_accept"))
            keyboard.add(InlineKeyboardButton(text="❌ Назад", callback_data=f"admin_back_2"))
            await state.update_data(text=text)
            await state.update_data(photo=message.photo[-1].file_id)
            await States.admin_mail_accept.set()
            await bot.send_photo(message.chat.id, message.photo[-1].file_id, text, parse_mode="HTML")
            await bot.send_message(message.chat.id, f"Начать рассылку для {len(db.get_all_users())} пользователей?",
                                   reply_markup=keyboard)
            await state.update_data(type='photo')
        except:
            await bot.send_message(message.chat.id, f"❌ Неверный текст")


@dp.message_handler(commands="info", state="*")
async def admin_info(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        _ID = message.text.replace("/info ", "")
        _data = db.get_info(_ID)
        if not (_ID.isdigit()):
            await bot.send_message(message.chat.id, f"Неверный формат команды")
        elif (_data == None):
            await bot.send_message(message.chat.id, f"❌ Пользователь не найден")
        else:
            await message.answer(get_user_info(_ID), reply_markup=main_menu(), parse_mode="Markdown")


@dp.message_handler(commands="top", state="*")
async def admin_top(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        _text = "<b>💵 Топ по балансу</b>"
        for i in db.get_top_balance(5):
            _text = _text + f"\n{i[5]} | {i[1]} (@{i[2]})"
        _text = _text + "\n\n"
        _text = _text + "<b>👥 Топ по рефералам</b>"
        top_refs = db.get_top_ref(5)
        if top_refs:
            for i in top_refs:
                _temp_name = db.get_info(i[2])[2]
                _text = _text + f"\n{i[0]} | {i[2]} (@{_temp_name})"
        else:
            _text = _text + f"\nНикто никого не пригласил"
        await message.answer(_text, reply_markup=main_menu(), parse_mode="HTML")


@dp.message_handler(commands="pay", state="*")
async def admin_pay(message: types.Message, state: FSMContext):
    if (message.chat.id == admin_id):
        _data = message.text.split(" ")
        if (len(_data) > 2):
            _ID = _data[1]
            _sum = _data[2]
            if (_sum.isdigit()) or _sum.replace("-", "").isdigit():
                if (_ID.isdigit()):
                    if (db.get_users_exist(_ID)):
                        db.set_balance(_ID, db.get_balance(_ID) + int(_sum))
                        _info = db.get_info(_ID)
                        await bot.send_message(message.chat.id, f"✅ Баланс {_ID} (@{_info[2]}) пополнен на {_sum}")
                        await bot.send_message(_ID, f"Ваш баланс пополнен на {_sum}")
                    else:
                        await bot.send_message(message.chat.id, f"❌ Пользователь не найден")
                elif (_ID == "all"):
                    users = db.get_all_users()
                    a = 0
                    for user in users:
                        try:
                            db.set_balance(user[0], int(db.get_balance(user[0])) + int(_sum))
                            await bot.send_message(user[0], f"Ваш баланс пополнен на {_sum}")
                            a += 1
                        except:
                            pass
                    await bot.send_message(message.chat.id, f"✅ Баланс {a} пользователей пополнен на {_sum}")
                else:
                    await bot.send_message(message.chat.id, f"Неверный формат команды")
            else:
                await bot.send_message(message.chat.id, f"Неверный формат команды")
        else:
            await bot.send_message(message.chat.id, f"Неверный формат команды")
