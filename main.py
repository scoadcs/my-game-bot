import telebot
from telebot import types

API_TOKEN = "8605294863:AAG8CyJbdStXHIxMDm6UE6aB6yQvVXqCNKI"
ADMIN_PASSWORD = "test233!"

bot = telebot.TeleBot(API_TOKEN)

# Глобальна база даних в пам'яті для багатьох гравців
USERS = {}
PURCHASES = {}

MANIACS = {
    "Тревис": 0,
    "Майкл": 0,
    "Паравозик мен": 160,
    "Робин": 180,
    "Варден": 200
}

SURVIVORS = {
    "Инженер": 20,
    "Статуя": "🔒 Временно недоступна",
    "Aссасин": 200,
    "Медик": 20,
    "Невидимка": 100,
    "Нубик": 0,
    "Aнгел-хранитель": 60,
    "Блокер": 120,
    "Пришелец": 120
}

def get_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("🔑 Регистрация", "🔓 Вход")
    markup.row("⚙️ Панель Админа")
    return markup

def get_main_keyboard():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.row("👤 Мой Профиль", "🎒 Владение")
    markup.row("🏪 Магазин", "🚪 Выйти")
    return markup

@bot.message_handler(commands=['start'])
def start(message):
    uid = message.from_user.id
    if uid not in USERS:
        USERS[uid] = {"pass": "", "diamonds": 0, "level": 1, "state": "", "admin": 0, "name": message.from_user.username or f"id_{uid}"}
    bot.send_message(message.chat.id, "Добро пожаловать в игру! Пройдите регистрацию или войдите.", reply_markup=get_keyboard())

@bot.message_handler(func=lambda m: "Регистрация" in m.text)
def reg(message):
    uid = message.from_user.id
    if uid not in USERS:
        USERS[uid] = {"pass": "", "diamonds": 0, "level": 1, "state": "", "admin": 0, "name": message.from_user.username or f"id_{uid}"}
    
    if USERS[uid]["pass"] != "":
        bot.send_message(message.chat.id, "Вы уже зарегистрированы! Нажмите кнопку 'Вход'.")
    else:
        USERS[uid]["state"] = "wait_pass"
        bot.send_message(message.chat.id, "Придумайте и напишите пароль для защиты вашего аккаунта:")

@bot.message_handler(func=lambda m: "Вход" in m.text)
def login(message):
    uid = message.from_user.id
    if uid in USERS and USERS[uid]["pass"] != "":
        USERS[uid]["state"] = "wait_login"
        bot.send_message(message.chat.id, "Введите ваш пароль:")
    else:
        bot.send_message(message.chat.id, "Вы еще не зарегистрированы!")

@bot.message_handler(func=lambda m: "Панель" in m.text)
def adm(message):
    uid = message.from_user.id
    if uid not in USERS:
        USERS[uid] = {"pass": "", "diamonds": 0, "level": 1, "state": "", "admin": 0, "name": message.from_user.username or f"id_{uid}"}
        
    if USERS[uid]["admin"] == 1:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.row("👥 Все участники", "⬅️ В главное меню")
        bot.send_message(message.chat.id, "Привет, Создатель!", reply_markup=markup)
    else:
        USERS[uid]["state"] = "wait_adm"
        bot.send_message(message.chat.id, "🔐 Введите секретный пароль Администратора:")

@bot.message_handler(func=lambda m: True)
def text(message):
    uid = message.from_user.id
    if uid not in USERS: return
    
    state = USERS[uid]["state"]
    
    if state == "wait_pass":
        USERS[uid]["pass"] = message.text
        USERS[uid]["state"] = ""
        bot.send_message(message.chat.id, "🎉 Регистрация успешна!", reply_markup=get_main_keyboard())
        return
    elif state == "wait_login":
        if USERS[uid]["pass"] == message.text:
            USERS[uid]["state"] = ""
            bot.send_message(message.chat.id, "✅ Успешный вход!", reply_markup=get_main_keyboard())
        else:
            bot.send_message(message.chat.id, "❌ Неверный пароль!")
        return
    elif state == "wait_adm":
        if message.text == ADMIN_PASSWORD:
            USERS[uid]["admin"] = 1
            USERS[uid]["state"] = ""
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.row("👥 Все участники", "⬅️ В главное меню")
            bot.send_message(message.chat.id, "👨‍💻 Доступ разрешен, Создатель!", reply_markup=markup)
        else:
            USERS[uid]["state"] = ""
            bot.send_message(message.chat.id, "❌ Доступ отклонен!", reply_markup=get_keyboard())
        return
            
    if "Профиль" in message.text:
        dia = USERS[uid]["diamonds"]
        lvl = USERS[uid]["level"]
        bot.send_message(message.chat.id, f"📊 *Ваш игровой профиль:*\n\n⭐ Уровень: {lvl}\n💎 Алмазы: {dia}", parse_mode="Markdown")
    elif "Владение" in message.text:
        owned = PURCHASES.get(uid, [])
        bot.send_message(message.chat.id, f"🎒 *Ваше владение:*\n\n" + (", ".join(owned) if owned else "У вас пока нет купленных персонажей."), parse_mode="Markdown")
    elif "Магазин" in message.text:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("👹 Маньяки", callback_data="shop_man"))
        markup.add(types.InlineKeyboardButton("🏃 Выжившие", callback_data="shop_surv"))
        bot.send_message(message.chat.id, "🛍️ Выберите категорию игрового магазина:", reply_markup=markup)
    elif "участники" in message.text and USERS[uid]["admin"] == 1:
        markup = types.InlineKeyboardMarkup()
        active_users = False
        for k, v in USERS.items():
            if v["admin"] == 0:
                active_users = True
                markup.add(types.InlineKeyboardButton(f"⚙️ {v['name']} (Ур: {v['level']} | 💎: {v['diamonds']})", callback_data=f"give_{k}"))
        if not active_users:
            bot.send_message(message.chat.id, "👥 Обычных участников в базе пока нет.")
        else:
            bot.send_message(message.chat.id, "👥 Нажмите на игрока, чтобы выдать ему +50 💎 и +1 Уровень:", reply_markup=markup)
    elif "меню" in message.text or "Выйти" in message.text:
        bot.send_message(message.chat.id, "Вы вернулись в стартовое меню.", reply_markup=get_keyboard())

@bot.callback_query_handler(func=lambda c: True)
def call(c):
    uid = c.from_user.id
    if uid not in USERS: return
    owned = PURCHASES.get(uid, [])

    if c.data == "shop_man":
        markup = types.InlineKeyboardMarkup()
        for k, v in MANIACS.items():
            if k in owned:
                markup.add(types.InlineKeyboardButton(f"✅ {k} (Куплено)", callback_data="none"))
            else:
                markup.add(types.InlineKeyboardButton(f"{k} — {v} 💎", callback_data=f"buy_{k}_{v}"))
        bot.edit_message_text("👹 Категория: Маньяки\nНажмите для покупки персонажа:", c.message.chat.id, c.message.message_id, reply_markup=markup)
    elif c.data == "shop_surv":
        markup = types.InlineKeyboardMarkup()
        for k, v in SURVIVORS.items():
            if k == "Статуя":
                markup.add(types.InlineKeyboardButton(f"❌ {k} (Недоступна)", callback_data="none"))
            elif k in owned:
                markup.add(types.InlineKeyboardButton(f"✅ {k} (Куплено)", callback_data="none"))
            else:
                markup.add(types.InlineKeyboardButton(f"{k} — {v} 💎", callback_data=f"buy_{k}_{v}"))
        bot.edit_message_text("🏃 Категория: Выжившие\nНажмите для покупки персонажа:", c.message.chat.id, c.message.message_id, reply_markup=markup)
    elif c.data.startswith("buy_"):
        _, name, price = c.data.split("_")
        price = int(price)
        if USERS[uid]["diamonds"] >= price:
            USERS[uid]["diamonds"] -= price
            if uid not in PURCHASES: PURCHASES[uid] = []
            PURCHASES[uid].append(name)
            bot.answer_callback_query(c.id, f"🎉 Персонаж {name} успешно куплен!", show_alert=True)
            bot.delete_message(c.message.chat.id, c.message.message_id)
        else:
            bot.answer_callback_query(c.id, f"❌ Недостаточно алмазов! Нужно {price} 💎", show_alert=True)
    elif c.data.startswith("give_"):
        target_id = int(c.data.split("_"))
        if target_id in USERS:
            USERS[target_id]["diamonds"] += 50
            USERS[target_id]["level"] += 1
            bot.answer_callback_query(c.id, "✅ Успешно начислено +50 💎 и +1 Уровень!")

if __name__ == "__main__":
    print("СТАРТ")
    bot.infinity_polling()
