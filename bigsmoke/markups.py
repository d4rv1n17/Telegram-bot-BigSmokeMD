from aiogram.types import ReplyKeyboardMarkup, KeyboardButton



btnMAIN = KeyboardButton('⬅️Главное меню')
btnMAINROM = KeyboardButton('⬅️Meniu principal')

# --- Main RU Menu --- #
btnModels = KeyboardButton('/😤Модели😤')
btnOther = KeyboardButton('➡️ Другое')
main_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnModels, btnOther)


# --- Language Menu --- #
btnRu = KeyboardButton('🇷🇺RU')
btnRom = KeyboardButton('🇷🇴ROM')
language_menu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnRu, btnRom)


# --- Other RU Menu --- #
btnCart = KeyboardButton("/🛒Корзина")
btnLang = KeyboardButton("/🔤Язык")
btnLink = KeyboardButton('↗️Ссылки')
btnHelp = KeyboardButton('🆘Помощь')
other_menu = ReplyKeyboardMarkup(resize_keyboard = True).add(btnCart, btnLang, btnLink, btnHelp, btnMAIN)


# --- Main ROM Menu --- #
btnModelsROM = KeyboardButton('/😤Modele😤')
btnOtherROM = KeyboardButton('➡️ Alte')
main_menuROM = ReplyKeyboardMarkup(resize_keyboard = True).add(btnModelsROM, btnOtherROM)


# --- Other ROM Menu --- #
btnCartROM = KeyboardButton("/🛒Coş")
btnLangROM = KeyboardButton("/🔤Limba")
btnLinkROM = KeyboardButton('↗️Legături')
btnHelpROM = KeyboardButton('🆘Ajutor')
other_menuROM = ReplyKeyboardMarkup(resize_keyboard = True).add(btnCartROM, btnLangROM, btnLinkROM, btnHelpROM, btnMAINROM)




