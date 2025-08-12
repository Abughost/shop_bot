from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_reply_button(btns:list,size:list,repeat=False):
    buttons = ReplyKeyboardBuilder()
    buttons.add(*btns)
    if repeat:
        buttons.adjust(size[0],repeat=True)
    else:
        buttons.adjust(*size)
    return buttons.as_markup(resize_keyboard=True)