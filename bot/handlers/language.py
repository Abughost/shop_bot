from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, Message, CallbackQuery, KeyboardButton
from aiogram.utils.i18n import I18n,lazy_gettext as __ , gettext as _

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import make_reply_button
from bot.utils.dispatcher import dp
from bot.utils.states import StepsState

@dp.callback_query(F.data == "back", StepsState.language)
async def command_start_handler(callback: CallbackQuery,state:FSMContext) -> None:

    buttons = [
        KeyboardButton(text=_("📦 Products Section")),
        KeyboardButton(text=_("📞 Connect with us")),
        KeyboardButton(text=_("🛒 Order")),
        KeyboardButton(text=_("🇺🇿/🇷🇺/🇺🇸 Choose language")),
    ]
    markup = make_reply_button(buttons,[1,1,2])

    await state.set_state(StepsState.main)
    await callback.message.delete()
    await callback.message.answer(_("Back to main section!"),reply_markup=markup)

@dp.message(F.text == __("🇺🇿/🇷🇺/🇺🇸 Choose language"))
async def language_handler(message:Message,state:FSMContext,i18n:I18n) -> None:
    buttons = [
        InlineKeyboardButton(text = "🇺🇿 Uzbek", callback_data="Uzbek"),
        InlineKeyboardButton(text = "🇷🇺 Русский", callback_data="Russian"),
        InlineKeyboardButton(text = "🇺🇸 English", callback_data="English"),
        InlineKeyboardButton(text = _("⬅️ back"), callback_data="back"),
    ]
    markup = make_inline_button(buttons,[1,2,1])
    await state.set_state(StepsState.language)
    await message.answer(_("Choose language"),reply_markup=markup)

@dp.callback_query(F.data.in_({"Uzbek","Russian","English"}))
async def language_handler(callback:CallbackQuery,state:FSMContext,i18n:I18n) -> None:
    lang = 'en'
    if callback.data == "Uzbek":
        lang = 'uz'
    elif callback.data == "Russian":
        lang = 'ru'

    i18n.current_locale = lang
    await state.update_data(locale=lang)

    buttons = [
        InlineKeyboardButton(text = "🇺🇿 Uzbek", callback_data="Uzbek"),
        InlineKeyboardButton(text = "🇷🇺 Русский", callback_data="Russian"),
        InlineKeyboardButton(text = "🇺🇸 English", callback_data="English"),
        InlineKeyboardButton(text = _("⬅️ back"), callback_data="back"),
    ]
    markup = make_inline_button(buttons,[1,2,1])
    await callback.message.delete()
    await callback.message.answer(_("Choose language"),reply_markup=markup)
