from os import getenv

from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.types import LabeledPrice, PreCheckoutQuery, KeyboardButton, MessageOrigin, CallbackQuery, Message
from sqlalchemy import update

from bot.buttons.reply import make_reply_button
from bot.handlers import session
from bot.utils.dispatcher import dp
from bot.utils.states import StepsState
from db.models import Order, OrderStatus
PAYMENT_CLICK_TOKEN = getenv("PAYMENT_CLICK_TOKEN")
@dp.callback_query(F.data == "payment")
async def invoice(callback: CallbackQuery,state:FSMContext):
    order:Order = await state.get_value('order')
    prices = []
    print(order.order_id)
    for order_item in order.order_items:
        name = order_item.products.name_en
        price = order_item.products.price
        extra_price = order_item.products.available_items[0].extra_price
        quantity = order_item.quantity
        prices.append(LabeledPrice(label=name, amount=int((price+extra_price)*12700)*quantity*100))
    await callback.message.delete()
    await callback.message.answer_invoice(title='Products', description=f"Jami {len(prices)} product order qilindi", payload=str(order.order_id),currency="UZS",prices=prices, provider_token=PAYMENT_CLICK_TOKEN)

@dp.pre_checkout_query()
async def success_handler(pre_checkout_query: PreCheckoutQuery) -> None:
    await pre_checkout_query.answer(True)

@dp.message(lambda message: bool(message.successful_payment))
async def confirm_handler(message: Message, state: FSMContext):
    if message.successful_payment:
        total_amount = message.successful_payment.total_amount//100
        order_id = int(message.successful_payment.invoice_payload)
        query = update(Order).where(Order.order_id == order_id).values(status=OrderStatus.completed ,amount = total_amount//12700)
        session.execute(query)
        session.commit()
        buttons = [
            KeyboardButton(text="📦 Products Section"),
            KeyboardButton(text="📞 Connect with us"),
            KeyboardButton(text="🛒 Order"),
            KeyboardButton(text="🇺🇿/🇷🇺/🇺🇸 Choose language"),
        ]
        markup = make_reply_button(buttons,[1,1,2])

        await state.set_state(StepsState.main)
        await message.delete()
        await message.answer(text=f"Thanks for your purchase 😊 \n{total_amount} UZS \n{order_id}",reply_markup=markup)

