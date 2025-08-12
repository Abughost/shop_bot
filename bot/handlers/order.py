from sqlalchemy import select, update

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import MessageOrigin, KeyboardButton, InlineKeyboardButton, CallbackQuery, LabeledPrice, \
    PreCheckoutQuery, Message
from aiogram.utils.i18n import lazy_gettext as __, gettext as _

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import make_reply_button
from bot.handlers import session
from bot.utils.dispatcher import dp
from bot.utils.states import StepsState
from db.models import Order, OrderStatus, OrderItem, Product



@dp.callback_query(F.data == "back",StepsState.order )
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



@dp.message(F.text == __("🛒 Order") ,StepsState.main)
async def command_start_handler(message: MessageOrigin,state:FSMContext) -> None:

    buttons = [
        InlineKeyboardButton(text=_("📦 All orders"),callback_data="all"),
        InlineKeyboardButton(text=_("🛒 Current orders"),callback_data="current"),
        InlineKeyboardButton(text=_("⬅️ Back"),callback_data="back")


    ]
    markup = make_inline_button(buttons,[2])

    await state.set_state(StepsState.order)
    await message.answer(_("Which one do you want to see!"),reply_markup=markup)

@dp.callback_query(F.data == "back" ,StepsState.court)
@dp.callback_query(F.data == "back" ,StepsState.all_history)
async def command_start_handler(callback:CallbackQuery,state:FSMContext) -> None:

    buttons = [
        InlineKeyboardButton(text=_("📦 All orders"),callback_data="all"),
        InlineKeyboardButton(text=_("🛒 Current orders"),callback_data="current"),
        InlineKeyboardButton(text=_("⬅️ Back"),callback_data="back")


    ]
    markup = make_inline_button(buttons,[2,1])

    await state.set_state(StepsState.order)
    await callback.message.delete()
    await callback.message.answer(_("Which one do you want to see!"),reply_markup=markup)


@dp.callback_query(F.data == "current",StepsState.order)
async def command_start_handler(callback: CallbackQuery,state:FSMContext) -> None:

    buttons = [
        InlineKeyboardButton(text=_("⬅️ Back"),callback_data="back")
    ]
    size = 1

    query = select(Order).where(Order.user_id == str(callback.from_user.id), Order.status == OrderStatus.pending)
    order = session.execute(query).scalars().first()
    session.commit()
    await state.update_data(order_id = callback.from_user.id)
    if not order:
        text = _("You don't have any order yet!")
    else:
        buttons = [InlineKeyboardButton(text=_("📦 To complete"),callback_data="payment"),] +buttons
        size += 1
        text = f"Orders:\nData: {order.created_at}"

        for i,items in enumerate(order.order_items,1):
            product:Product = items.products
            subcat = product.subcategory
            cat = subcat.category
            text1 = f"""
            \n{i}) {cat.name_en}: {subcat.name_en}\nname:  {product.name_en}\nbrand: {product.brand_name}\nprice: {product.price} {product.currency}\nquantity:{items.quantity}\n
            """
            text += text1

        text += f"Total: {order.amount} {product.currency}"

    await state.update_data(order=order)
    markup = make_inline_button(buttons,[size])
    await state.set_state(StepsState.court)
    await callback.message.delete()
    await callback.message.answer(text=text,reply_markup=markup)


@dp.callback_query(F.data == "all",StepsState.order)
async def command_start_handler(callback: CallbackQuery,state:FSMContext) -> None:

    buttons = [
        InlineKeyboardButton(text=_("⬅️ Back"),callback_data="back")
    ]
    query = select(Order).where(Order.user_id == str(callback.from_user.id), Order.status != OrderStatus.pending)
    orders = session.execute(query).scalars().all()
    session.commit()

    if not orders:
        text = _("You don't have any order yet!")
    else:
        text = ""
        total = 0
        for order in orders:
            text += f"Order:\nData: {order.created_at}"
            for i,items in enumerate(order.order_items,1):
                product:Product = items.products
                subcat = product.subcategory
                cat = subcat.category
                text1 = f"""
                \n{i}) {cat.name_en}: {subcat.name_en}\nname:  {product.name_en}\nbrand: {product.brand_name}\nprice: {product.price} {product.currency}\nquantity:{items.quantity}\n
                """
                text += text1
                total += order.amount

        text += f"Total: {total} {product.currency}"


    markup = make_inline_button(buttons,[1])
    await state.set_state(StepsState.all_history)
    await callback.message.delete()
    await callback.message.answer(text=text,reply_markup=markup)