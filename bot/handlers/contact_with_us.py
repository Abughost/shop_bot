from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, CallbackQuery, KeyboardButton, Message
from aiogram.utils.i18n import lazy_gettext as __ , gettext as _

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import make_reply_button
from bot.utils.dispatcher import dp
from bot.utils.states import StepsState


@dp.callback_query(F.data == "back",StepsState.contact )
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


@dp.message(F.text == __("📞 Connect with us"),StepsState.main)
async def command_start_handler(message: Message,state:FSMContext) -> None:

    buttons = [
        InlineKeyboardButton(text=_("📖 For Information", ),callback_data="info"),
        InlineKeyboardButton(text=_("😠 Complaint"),callback_data="negative"),
        InlineKeyboardButton(text=_("💡 Suggestions"),callback_data="positive"),
        InlineKeyboardButton(text=_("⬅️ Back"), callback_data="back"),
    ]
    markup = make_inline_button(buttons,[1],repeat=True)

    await state.set_state(StepsState.contact)
    await message.answer(_("What is the reason you want to get in touch?"),reply_markup=markup)

@dp.callback_query(F.data != "back",StepsState.contact)
async def command_start_handler(callback:CallbackQuery, state:FSMContext) -> None:

    buttons = [
        KeyboardButton(text=_("📞 Share your contact ", ),request_contact=True)
    ]
    markup = make_reply_button(buttons,[1])

    await callback.message.delete()
    await state.set_state(StepsState.share_contact)
    await callback.message.answer(_("Please leave your phone number, we will contact you ourselves."),reply_markup=markup)


@dp.message(StepsState.share_contact)
async def command_start_handler(message:Message, state:FSMContext) -> None:
    buttons = [
        KeyboardButton(text=_("📦 Products Section")),
        KeyboardButton(text=_("📞 Connect with us")),
        KeyboardButton(text=_("🛒 Order")),
        KeyboardButton(text=_("🇺🇿/🇷🇺/🇺🇸 Choose language")),
    ]
    markup = make_reply_button(buttons,[1,1,2])

    await state.set_state(StepsState.main)
    await message.answer(_("Thank! we recieve your phone number :)"),reply_markup=markup)

