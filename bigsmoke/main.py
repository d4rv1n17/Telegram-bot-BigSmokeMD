# imports
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import *

import logging

from data_base import SQLighter

from config import *

import markups as nav

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from text import *

from admin_id import *


# logs level
logging.basicConfig(level=logging.INFO)

# initialization of bot
proxy_url = 'http://proxy.server:3128' # it is proxy for hosting bot on pythonanywhere
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# intilialization of connection with db
db = SQLighter('db.db')

#user's language
global language
language = "RU" # default is RU - Russian language


# ---Clients' Commands--- #

#commands start
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.first_name}'.format(message.from_user) +\
    '\nВыберите язык, а затем\nнажмите кнопку "😤Модели😤"\nдля знакомства с нашим ассортиментом!', reply_markup = nav.language_menu)

    #adding user to db
    name = message.from_user.first_name
    user_id = message.from_user.id
    if(not db.user_exists(message.from_user.id)):
        # if is no user in db, we just add him
        db.add_user(user_id, name)
    else:
        # if user exists, we just pass this
        pass

    #inline button
    if language == "ROM":
        await bot.send_message(message.from_user.id, text="Alege un model⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Modele😤', callback_data=f'view ')))
    if language == "RU":
        await bot.send_message(message.from_user.id, text="Выберите модель⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Модели😤', callback_data=f'view ')))


#command for change language on RU
@dp.message_handler(commands=["🔤Язык"])
async def language_selection(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите язык!", reply_markup=nav.language_menu)


#command for change language on ROM
@dp.message_handler(commands=["🔤Limba"])
async def language_selection(message: types.Message):
    await bot.send_message(message.from_user.id, "Выберите язык!", reply_markup=nav.language_menu)


#command "😤Модели😤" on RU
@dp.message_handler(commands=["😤Модели😤"])
async def view_models(message: types.Message):
    #inline button
    if language == "ROM":
        await bot.send_message(message.from_user.id, text="Alege un model⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Modele😤', callback_data=f'view ')))
    if language == "RU":
        await bot.send_message(message.from_user.id, text="Выберите модель⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Модели😤', callback_data=f'view ')))


#command "😤Модели😤" on ROM
@dp.message_handler(commands=["😤Modele😤"])
async def view_models(message: types.Message):
    #inline button
    if language == "ROM":
        await bot.send_message(message.from_user.id, text="Alege un model⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Modele😤', callback_data=f'view ')))
    if language == "RU":
        await bot.send_message(message.from_user.id, text="Выберите модель⬇️", reply_markup=InlineKeyboardMarkup().\
        add(InlineKeyboardButton('😤Модели😤', callback_data=f'view ')))        


#first callback of inline button "😤Модели😤"
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('view '))
async def viewing_callback_run(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    all_items = db.get_all_info()
    for item in all_items:
        if item[3] == "YES":
            await bot.send_message(user_id, text="😤ELF BAR TE 5000🎄😤", reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton(f'{item[1]} {item[2]}', callback_data=f'adding {item[1]}:{item[2]}')))
        if item[3] == "NO":
            pass


#second callback of inline button "😤Модели😤"
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('adding '))
async def adding_callback_run(callback_query: types.CallbackQuery):
    data_firststep = callback_query.data.replace('adding ', '')
    data_secondstep = data_firststep.split(':')
    data1 = data_secondstep[0]
    data2 = data_secondstep[1]
    user_id = callback_query.from_user.id
    db.add_to_cart(user_id, data1, data2)
    if language == "ROM":
        await callback_query.answer(text=f'{data1} {data2} adăugat în coș!', show_alert=True)
    if language == "RU":
        await callback_query.answer(text=f'{data1} {data2} добавлен в корзину!', show_alert=True)


#callback of "del " from command "🛒Корзина"
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    data_firststep = callback_query.data.replace('del ', '')
    data_secondstep = data_firststep.split(':')
    data1 = data_secondstep[0]
    data2 = data_secondstep[1]
    user_id = callback_query.from_user.id
    db.update_cart(user_id, data1, data2)
    if language == "ROM":
        await callback_query.answer(text=f'{data1} {data2} scos din cărucior!', show_alert=True)
    if language == "RU":
        await callback_query.answer(text=f'{data1} {data2} удален из корзины!', show_alert=True)


#command to take user's phone number and continue order's confirmation
@dp.message_handler(commands=["phone"])
async def get_phone_number(message: types.Message):
    input_message = message.text[7:]
    phone_number = input_message
    if len(phone_number) == 9:
        user_id = message.from_user.id
        cart = db.get_user_cart(user_id)
        
        if language == "ROM":
            textForAdmin = f"Номер телефона: {phone_number}\nВыбранные модели: {cart}"
            textForUser = textForcommandPhoneROM
            await bot.send_message(1138527802, textForAdmin)
            await message.answer(text=textForUser)
        
        if language == "RU":   
            textForAdmin = f"Номер телефона: {phone_number}\nВыбранные модели: {cart}"
            #bot send message with user's order to admin
            await bot.send_message(1138527802, textForAdmin)
            textForUser = textForcommandPhoneRU
            await message.answer(text=textForUser)  
        
        db.del_all_user_cart(user_id)
    
    else:
        if language == "ROM":
            await message.answer("‼️Verificați dacă ați introdus corect numărul de telefon‼️")
        if language == "RU":
            await message.answer("‼️Проверьте если вы правильно ввели номер телефона‼️")



#callback of "confirm " from command "🛒Корзина"
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('confirm '))
async def confirm_callback_run(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    if language == "ROM":
        text = confirmation_text_ROM
    if language == "RU":
        text = confirmation_text_RU    
    await bot.send_message(user_id, text)


#command to view user's cart, confirm order or remove an item from cart
@dp.message_handler(commands=["🛒Корзина"])
async def view_user_cart(message: types.Message):
    user_id = message.from_user.id
    cart = db.get_user_cart(user_id)
    if len(cart) > 0:
        for row in cart:         
            #condition for language RU
            text = f"😤Модель: {row[2]}😤\n😋Вкус:{row[3]}😋"
            await bot.send_message(message.from_user.id, text)
            await bot.send_message(message.from_user.id, text='❗️Удаление товара из корзины❗️', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'❌Удалить из корзины❌', callback_data=f'del {row[2]}:{row[3]}')))
        await bot.send_message(message.from_user.id, text='❗️Потверждение заказа❗️', reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton('✅Потвердить заказ✅', callback_data='confirm ')))            

    if len(cart) <= 0:
        await bot.send_message(user_id, "❗️Корзина пуста❗️")


#callback of "confirm " from command "🛒Корзина" on ROM
@dp.message_handler(commands=["🛒Coş"])
async def view_user_cart(message: types.Message):
    user_id = message.from_user.id
    cart = db.get_user_cart(user_id)
    if len(cart) > 0:
        for row in cart:         
            #condition for language RU
            text = f"😤Model: {row[2]}😤\n😋Gust:{row[3]}😋"
            await bot.send_message(message.from_user.id, text)
            await bot.send_message(message.from_user.id, text='❗️Scoaterea unui articol din coș❗️', reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'❌Scoateți din coș❌', callback_data=f'del {row[2]}:{row[3]}')))
        await bot.send_message(message.from_user.id, text='❗️Confirmarea comenzii❗️', reply_markup=InlineKeyboardMarkup().\
            add(InlineKeyboardButton('✅Confirmă comanda✅', callback_data='confirm ')))          

    if len(cart) <= 0:
        await bot.send_message(user_id, "❗️Coșul este gol❗️")             

# ---End of Clients' Commands--- #




# ---Admins' Commands--- #

#displaying all users
@dp.message_handler(commands=["users"])
async def get_users(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        all_users = db.get_users()
        for user in all_users:
            text = f"Id: {user[0]}\nUser_id: {user[1]}\nName: {user[2]}"
            await message.answer(text)


#displaying information about admin's commands (only for admin)
@dp.message_handler(commands=["admin"])
async def admin_commands_info(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        commands_text = commands #commands is variable from text.py
        await message.answer(commands_text)


#displaying all products and their information from database
@dp.message_handler(commands=["all"])
async def displaying_all_menu(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        all_menu = db.get_all_info()
        for row in all_menu:
            text = f"Id: {row[0]}\nModel: {row[1]}\nFlavor: {row[2]}\nAvailability: {row[3]}\nPrice: {row[4]}"
            await message.answer(text) 


#removing a product from the database by its id
@dp.message_handler(commands=["remove"])
async def remove(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        id = message.text[8:]
        
        if len(id) < 0:
            remove_flag = False
            all = db.get_all_info()
            
            for product in all:
                product_id = str(product[0])
                
                if id == product_id:
                    db.remove_product(id)
                    await message.answer("Product was successfully deleted!")
                    remove_flag = True
            
            if remove_flag == False:
                await message.answer("No product with given id!")
            else:
                await message.answer("You didn't send me product's id!")    


#editing quantity of product by its id
@dp.message_handler(commands=["edit_availability"])
async def edit_quantity(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        input_message = message.text[19:].split(':')
        id = input_message[0]
        availability = input_message[1]
        
        if len(id) > 0 and len(availability) > 0: 
            db.update_availability(id, availability)
            await message.answer("Availability was successfully edited!")
        else:
            await message.answer("Error, check if you sent command correctly!")


#editing product's name
@dp.message_handler(commands=["edit_model_name"])
async def edit_name(message: types.Message):
   if message.from_user.id == admin1 or admin2 or admin3:
        input_message = message.text[17:].split(':')
        model_name = input_message[1]
        id = input_message[0]

        if len(id) > 0 and len(model_name) > 0:
            db.update_model_name(id, model_name)
            await message.answer("Product's name was successfully edited!")
        else:
            await message.answer("Error, check if you sent command correctly!")


#editing product's flavor
@dp.message_handler(commands=["edit_model_flavor"])
async def edit_name(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        input_message = message.text[19:].split(':')
        model_flavor = input_message[1]
        id = input_message[0]

        if len(id) > 0 and len(model_flavor) > 0:
            db.update_model_flavor(id, model_flavor)
            await message.answer("Product's flavor was successfully edited!")
        else:
            await message.answer("Error, check if you sent command correctly!")


#editing product's price
@dp.message_handler(commands=["edit_price"])
async def edit_price(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        input_message = message.text[12:].split(':')
        product_price = input_message[1]
        id = input_message[0]

        if len(id) > 0 and len(product_price) > 0:
            db.update_model_price(product_price, id)
            await message.answer("Product's price was successfully edited!")
        else:
            await message.answer("Error, check if you sent command correctly!")


#adding new model to database
@dp.message_handler(commands=["add"])
async def add_model(message: types.Message):
    if message.from_user.id == admin1 or admin2 or admin3:
        input_message = message.text[5:].split(':')
        model_name = input_message[0]
        model_flavor = input_message[1]
        availability = input_message[2]
        product_price =input_message[3]
        
        if len(model_name) > 0 and len(availability) > 0 and len(product_price) > 0 and len(model_flavor) > 0:
            db.add(model_name, model_flavor, availability, product_price)
            await message.answer("New product was successfully added!")
        else:
            await message.answer("Error, check if you sent command correctly!")

#send message for all users
@dp.message_handler(commands=["send"])
async def send_all(message: types.Message): 
    if message.from_user.id == admin1 or admin2 or admin3:
        text = message.text[6:]
        users = db.get_users() 
        for user in users:
            await bot.send_message(user[1], text)     
    else:
        await bot.send_message(message.from_user.id, "Error")   

# ---End of Admins' Commands--- #


#message handler
@dp.message_handler()
async def bot_message(message: types.Message):
    if message.text == '🇷🇺RU':
        global language
        language = "RU"
        await bot.send_message(message.from_user.id, "Вы выбрали 🇷🇺русский язык!", reply_markup=nav.main_menu)

    elif message.text == '🇷🇴ROM':
        language = "ROM"
        await bot.send_message(message.from_user.id, "Ai selectat limba 🇷🇴română!", reply_markup=nav.main_menuROM)

    elif message.text == '➡️ Другое':
        await bot.send_message(message.from_user.id, "➡️ Другое", reply_markup = nav.other_menu)

    elif message.text == '⬅️Главное меню':
        await bot.send_message(message.from_user.id, "⬅ Главное меню", reply_markup = nav.main_menu)

    elif message.text == '↗️Ссылки':
        text = links_text #links_text is variable from text.py
        
        await bot.send_message(message.from_user.id, text)
    
    elif message.text == '🆘Помощь':
        text = help_text #links_text is variable from text.py
        
        await bot.send_message(message.from_user.id, text)
    
    elif message.text == '⬅️Meniu principal':
        await bot.send_message(message.from_user.id, "⬅️Meniu principal", reply_markup = nav.main_menuROM)

    elif message.text == '➡️ Alte':
        await bot.send_message(message.from_user.id, "➡️ Alte", reply_markup = nav.other_menuROM) 

    elif message.text == '↗️Legături':
        text = links_textROM #links_text is variable from text.py

        await bot.send_message(message.from_user.id, text)   

    elif message.text == '🆘Ajutor':
        text = help_textROM #links_text is variable from text.py

        await bot.send_message(message.from_user.id, text)

    else:
        if language == "ROM":
            await message.reply("Echipa necunoscută!")
        if language == "RU":
            await message.reply("Неизвестная команда!")            


#start
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

