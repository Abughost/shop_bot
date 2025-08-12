from aiogram.utils.keyboard import InlineKeyboardBuilder


def make_inline_button(btns:list,size:list,repeat=False):
    buttons = InlineKeyboardBuilder()
    buttons.add(*btns)
    if repeat:
        buttons.adjust(size[0],repeat=True)
    else:
        buttons.adjust(*size)
    return buttons.as_markup()