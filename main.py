Import telebot 

From telebot import types 

 

API_TOKEN = «8605294863:AAG8CyJbdStXHIxMDm6UE6aB6yQvVXqCNKI» 

ADMIN_PASSWORD = «test233!» 

 

Telebot.apihelper.proxy = {‘https’: ‘http://proxy.server:3128’} 

Bot = telebot.TeleBot(API_TOKEN) 

 

USERS = {} 

PURCHASES = {} 

 

MANIACS = { 

    «Тревис»: 0, 

    «Майкл»: 0, 

    «Паравозик мен»: 160, 

    «Робин»: 180, 

    «Варден»: 200 

} 

 

SURVIVORS = { 

    «Инженер»: 20, 

    «Статуя»: «🔒 Временно недоступна», 

    «Aссасин»: 200, 

    «Медик»: 20, 

    «Невидимка»: 100, 

    «Нубик»: 0, 

    «Aнгел-хранитель»: 60, 

    «Блокер»: 120, 

    «Пришелец»: 120 

} 

 

Def get_keyboard(): 

    Markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 

    Markup.row(«🔑 Регистрация», «🔓 Вход») 

    Markup.row(«⚙️ Panel») 

    Return markup 

 

Def get_main_keyboard(): 

    Markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 

    Markup.row(«👤 Профиль», «🎒 Владение») 

    Markup.row(«🏪 Магазин», «🚪 Выйти») 

    Return markup 

 

@bot.message_handler(commands=[‘start’]) 

Def start(message): 

    Uid = message.from_user.id 

    If uid not in USERS: 

        USERS[uid] = {«pass»: «», «diamonds»: 0, «level»: 1, «state»: «», «admin»: 0, «name»: message.from_user.username or f»id_{uid}»} 

    Bot.send_message(message.chat.id, «Добро пожаловать в игру! Пройдите регистрацию.», reply_markup=get_keyboard()) 

 

@bot.message_handler(func=lambda m: «Регистрация» in m.text) 

Def reg(message): 

    Uid = message.from_user.id 

    If uid not in USERS: 

        USERS[uid] = {«pass»: «», «diamonds»: 0, «level»: 1, «state»: «», «admin»: 0, «name»: message.from_user.username or f»id_{uid}»} 

    If USERS[uid][«pass»] != «»: 

        Bot.send_message(message.chat.id, «Вы уже зарегистрированы!») 

    Else: 

        USERS[uid][«state»] = «wait_pass» 

        Bot.send_message(message.chat.id, «Придумайте и напишите пароль:») 

 

@bot.message_handler(func=lambda m: «Вход» in m.text) 

Def login(message): 

    Uid = message.from_user.id 

    If uid in USERS and USERS[uid][«pass»] != «»: 

        USERS[uid][«state»] = «wait_login» 

        Bot.send_message(message.chat.id, «Введите ваш пароль:») 

    Else: 

        Bot.send_message(message.chat.id, «Вы еще не зарегистрированы!») 

 

@bot.message_handler(func=lambda m: «Panel» in m.text) 

Def adm(message): 

    Uid = message.from_user.id 

    If uid not in USERS: 

        USERS[uid] = {«pass»: «», «diamonds»: 0, «level»: 1, «state»: «», «admin»: 0, «name»: message.from_user.username or f»id_{uid}»} 

    If USERS[uid][«admin»] == 1: 

        Markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 

        Markup.row(«👥 Все участники», «⬅️ В меню») 

        Bot.send_message(message.chat.id, «Привет, Создатель!», reply_markup=markup) 

    Else: 

        USERS[uid][«state»] = «wait_adm» 

        Bot.send_message(message.chat.id, «Введите пароль Администратора:») 

 

@bot.message_handler(func=lambda m: True) 

Def text(message): 

    Uid = message.from_user.id 

    If uid not in USERS: return 

    State = USERS[uid][«state»] 

     

    If state == «wait_pass»: 

        USERS[uid][«pass»] = message.text 

        USERS[uid][«state»] = «» 

        Bot.send_message(message.chat.id, «🎉 Успешно!», reply_markup=get_main_keyboard()) 

        Return 

    Elif state == «wait_login»: 

        If USERS[uid][«pass»] == message.text: 

            USERS[uid][«state»] = «» 

            Bot.send_message(message.chat.id, «✅ Вошли!», reply_markup=get_main_keyboard()) 

        Else: 

            Bot.send_message(message.chat.id, «❌ Неверный пароль!») 

        Return 

    Elif state == «wait_adm»: 

        If message.text == ADMIN_PASSWORD: 

            USERS[uid][«admin»] = 1 

            USERS[uid][«state»] = «» 

            Markup = types.ReplyKeyboardMarkup(resize_keyboard=True) 

            Markup.row(«👥 Все участники», «⬅️ В меню») 

            Bot.send_message(message.chat.id, «👨‍💻 Доступ разрешен!», reply_markup=markup) 

        Else: 

            USERS[uid][«state»] = «» 

            Bot.send_message(message.chat.id, «❌ Отклонено!», reply_markup=get_keyboard()) 

        Return 

         

    If «Профиль» in message.text: 

        Dia = USERS[uid][«diamonds»] 

        Lvl = USERS[uid][«level»] 

        Bot.send_message(message.chat.id, f»📊 Профиль:\n⭐ Уровень: {lvl}\n💎 Алмазы: {dia}») 

    Elif «Владение» in message.text: 

        Owned = PURCHASES.get(uid, []) 

        Bot.send_message(message.chat.id, f»🎒 Владение:\n» + («, «.join(owned) if owned else «Пусто.»)) 

    Elif «Магазин» in message.text: 

        Markup = types.InlineKeyboardMarkup() 

        Markup.add(types.InlineKeyboardButton(«👹 Маньяки», callback_data=»shop_man»)) 

        Markup.add(types.InlineKeyboardButton(«🏃 Выжившие», callback_data=»shop_surv»)) 

        Bot.send_message(message.chat.id, «🛍️ Выберите категорию магазина:», reply_markup=markup) 

    Elif «участники» in message.text and USERS[uid][«admin»] == 1: 

        Markup = types.InlineKeyboardMarkup() 

        Active_users = False 

        For k, v in USERS.items(): 

            If v[«admin»] == 0: 

                Active_users = True 

                Markup.add(types.InlineKeyboardButton(f»⚙️ {v[‘name’]} (Ур: {v[‘level’]} | 💎: {v[‘diamonds’]})», callback_data=f»manage_{k}»)) 

        If not active_users: 

            Bot.send_message(message.chat.id, «👥 Участников пока нет.») 

        Else: 

            Bot.send_message(message.chat.id, «👥 Выберите игрока для управления:», reply_markup=markup) 

    Elif «меню» in message.text or «Выйти» in message.text: 

        Bot.send_message(message.chat.id, «Вы вернулись.», reply_markup=get_keyboard()) 

 

@bot.callback_query_handler(func=lambda c: True) 

Def call(c): 

    Uid = c.from_user.id 

    If uid not in USERS: return 

    Owned = PURCHASES.get(uid, []) 

     

    If c.data == «shop_man»: 

        Markup = types.InlineKeyboardMarkup() 

        For k, v in MANIACS.items(): 

            If k in owned: 

                Markup.add(types.InlineKeyboardButton(f»✅ {k}», callback_data=»none»)) 

            Else: 

                Markup.add(types.InlineKeyboardButton(f»{k} — {v} 💎», callback_data=f»buy_{k}_{v}»)) 

        Bot.edit_message_text(«👹 Категория: Маньяки», c.message.chat.id, c.message.message_id, reply_markup=markup) 

    Elif c.data == «shop_surv»: 

        Markup = types.InlineKeyboardMarkup() 

        For k, v in SURVIVORS.items(): 

            If k == «Статуя»: 

                Markup.add(types.InlineKeyboardButton(f»❌ {k}», callback_data=»none»)) 

            Elif k in owned: 

                Markup.add(types.InlineKeyboardButton(f»✅ {k}», callback_data=»none»)) 

            Else: 

                Markup.add(types.InlineKeyboardButton(f»{k} — {v} 💎», callback_data=f»buy_{k}_{v}»)) 

        Bot.edit_message_text(«🏃 Категория: Выжившие», c.message.chat.id, c.message.message_id, reply_markup=markup) 

    Elif c.data.startswith(«buy_»): 

        _, name, price = c.data.split(«_») 

        Price = int(price) 

        If USERS[uid][«diamonds»] >= price: 

            USERS[uid][«diamonds»] -= price 

            If uid not in PURCHASES: PURCHASES[uid] = [] 

            PURCHASES[uid].append(name) 

            Bot.answer_callback_query(c.id, f»🎉 Куплен: {name}!», show_alert=True) 

            Bot.delete_message(c.message.chat.id, c.message.message_id) 

        Else: 

            Bot.answer_callback_query(c.id, f»❌ Нужно {price} 💎», show_alert=True) 

             

    Elif c.data.startswith(«manage_»): 

        Target_id = int(c.data.split(«_»)) 

        If target_id in USERS: 

            Name = USERS[target_id][«name»] 

            Lvl = USERS[target_id][«level»] 

            Dia = USERS[target_id][«diamonds»] 

            Markup = types.InlineKeyboardMarkup() 

            Markup.row( 

                Types.InlineKeyboardButton(«💎 +50 Алмазов», callback_data=f»give_dia_{target_id}»), 

                Types.InlineKeyboardButton(«⭐ +1 Уровень», callback_data=f»give_lvl_{target_id}») 

            ) 

            Bot.edit_message_text(f»👤 Игрок: {name}\n⭐ Уровень: {lvl}\n💎 Алмазы: {dia}», c.message.chat.id, c.message.message_id, reply_markup=markup) 

    Elif c.data.startswith(«give_dia_»): 

        Target_id = int(c.data.split(«_»)) 

        If target_id in USERS: 

            USERS[target_id][«diamonds»] += 50 

            Bot.answer_callback_query(c.id, «✅ Выдано +50 💎») 

            c.data = f»manage_{target_id}» 

            call(c) 

    elif c.data.startswith(«give_lvl_»): 

        target_id = int(c.data.split(«_»)) 

        if target_id in USERS: 

            USERS[target_id][«level»] += 1 

            Bot.answer_callback_query(c.id, «✅ Выдан +1 ⭐») 

            c.data = f»manage_{target_id}» 

            call(c) 

 

if __name__ == «__main__»: 

    print(«СТАРТ») 

    bot.infinity_polling() 

 
