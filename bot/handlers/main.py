from aiogram import F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import KeyboardButton, Message, CallbackQuery, InlineKeyboardButton
from aiogram.utils.i18n import lazy_gettext as __, gettext as _
from sqlalchemy import select, text
from sqlalchemy.orm import sessionmaker

from bot.buttons.inline import make_inline_button
from bot.buttons.reply import make_reply_button
from bot.utils.dispatcher import dp
from bot.utils.states import StepsState
from db.models import engine, Category, SubCategory, Product, Available, OrderItem, Order, OrderStatus

session = sessionmaker(engine)()

@dp.message(CommandStart())
async def command_start_handler(message: Message,state:FSMContext) -> None:
    buttons = [
        KeyboardButton(text=_("📦 Products Section")),
        KeyboardButton(text=_("📞 Connect with us")),
        KeyboardButton(text=_("🛒 Order")),
        KeyboardButton(text=_("🇺🇿/🇷🇺/🇺🇸 Choose language")),
    ]
    markup = make_reply_button(buttons,[1,1,2])

    await state.set_state(StepsState.main)
    await message.answer(_("Main section!"),reply_markup=markup)

@dp.callback_query(F.data == "back",StepsState.category )
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


@dp.message(F.text == __("📦 Products Section"))
async def product_handler(message: Message,state:FSMContext) -> None:

    lang = await state.get_value("locale")
    query = select(Category).order_by(getattr(Category,f"name_{lang}"))
    categories = session.execute(query).scalars().all()
    session.commit()

    buttons = [
        InlineKeyboardButton(text=f"{category.icon}{getattr(category, f"name_{lang}")}", callback_data=f"{category.category_id}" ) for category in categories
    ]
    buttons.append(InlineKeyboardButton(text=_("⬅️ back"),callback_data="back"))
    markup = make_inline_button(buttons,[2],repeat=True)
    await state.set_state(StepsState.category)

    await message.answer(f"Mahsulot turini tanlang!",reply_markup=markup)

@dp.callback_query(F.data == "back",StepsState.subcategory)
async def product_handler(callback:CallbackQuery,state:FSMContext) -> None:

    lang = await state.get_value("locale")
    query = select(Category).order_by(getattr(Category,f"name_{lang}"))
    categories = session.execute(query).scalars().all()
    session.commit()

    buttons = [
        InlineKeyboardButton(text=f"{category.icon}{getattr(category,f"name_{lang}")}", callback_data=f"{category.category_id}" ) for category in categories
    ]
    buttons.append(InlineKeyboardButton(text=_("⬅️ back"),callback_data="back"))
    markup = make_inline_button(buttons,[2],repeat=True)
    await state.set_state(StepsState.category)

    await callback.message.delete()
    await callback.message.answer(_("Choose product type!"),reply_markup=markup)


@dp.callback_query(F.data == "back",StepsState.product)
@dp.callback_query(F.data != "back",StepsState.category)
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:

    if callback.data == "back":
        category_id = await state.get_value("category_id")
    else:
        category_id = int(callback.data)
        await state.update_data(category_id=category_id)

    lang = await state.get_value("locale")
    query = select(SubCategory).where(SubCategory.category_id == category_id)
    subcats = session.execute(query).scalars().all()
    session.commit()

    buttons = [
        InlineKeyboardButton(text=f"{sub.icon} {getattr(sub,f"name_{lang}")}",callback_data=f"{sub.subcategory_id}") for sub in subcats
    ]
    buttons.append(InlineKeyboardButton(text=_("⬅️ back"),callback_data="back"))

    markup = make_inline_button(buttons,[2],repeat=True)
    await state.set_state(StepsState.subcategory)
    await callback.message.delete()
    await callback.message.answer(_("Choose type of product!"),reply_markup=markup)




@dp.callback_query(F.data == "back",StepsState.available)
@dp.callback_query(F.data != "back",StepsState.subcategory)
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:

    if callback.data == "back":
        sub_cot_id = await state.get_value("subcategory_id")
    else:
        sub_cot_id = int(callback.data)
        await state.update_data(subcategory_id= sub_cot_id)
    lang = await state.get_value("locale")
    query = select(Product).where(Product.subcategory_id == sub_cot_id)
    products = session.execute(query).scalars().all()
    session.commit()

    buttons = [
        InlineKeyboardButton(text=f"🏷️ {getattr(product,f"name_{lang}")}" , callback_data=f"{product.product_id}") for product in products
    ]
    buttons.append(InlineKeyboardButton(text=_("⬅️ back"),callback_data="back"))

    markup = make_inline_button(buttons,[2],repeat=True)
    await state.set_state(StepsState.product)
    await callback.message.delete()
    await callback.message.answer(_("Choose which brand!"),reply_markup=markup)

@dp.callback_query(F.data == "back",StepsState.count)
@dp.callback_query(F.data != "back",StepsState.product)
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:

    if callback.data == "back":
        state_data = await state.get_data()
        product_id = state_data.get("product_id")
    else:
        product_id = int(callback.data)
        await state.update_data(product_id=product_id)
    query = select(Available).where(Available.product_id == product_id)
    availables = session.execute(query).scalars().all()
    session.commit()

    buttons = [
        InlineKeyboardButton(text=ava.size ,callback_data=f"{ava.size}_{ava.available_product_id}") for ava in availables
    ]
    buttons.append(InlineKeyboardButton(text=_("⬅️ back"),callback_data="back"))

    markup = make_inline_button(buttons,[2],repeat=True)
    await state.set_state(StepsState.available)
    await callback.message.delete()
    await callback.message.answer(_("choose appropiate size!"),reply_markup=markup)



@dp.callback_query(F.data != "back",StepsState.available)
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:
    product_id = await state.get_value("product_id")
    await state.update_data(available = callback.data.split('_')[-1])
    query = select(Product).where(Product.product_id == product_id)
    product:Product = session.execute(query).scalars().first()
    session.commit()

    quantity = 1
    await state.update_data(quantity=quantity)

    buttons = [
        InlineKeyboardButton(text="1",callback_data="number"),
        InlineKeyboardButton(text="+",callback_data=f"quantity_{quantity+1}"),
        InlineKeyboardButton(text=_("📥 Add to busket"),callback_data="add"),
        InlineKeyboardButton(text="⬅️ back",callback_data="back")
    ]

    markup = make_inline_button(buttons,[2,1,1])
    await state.set_state(StepsState.count)
    await callback.message.delete()

    available_items = product.available_items[0]

    text = f"""
    Name:  {product.name_en}
    Brand: {product.brand_name}
    size:  {callback.data.split("_")[0]}
    color: {available_items.color}
    price: {product.price + available_items.extra_price} {product.currency}
    
    """
    await state.update_data(total= product.price + available_items.extra_price)
    await state.update_data(product = product)
    await callback.message.answer_photo(photo=product.photo,caption=text,reply_markup=markup)

@dp.callback_query(F.data.startswith("quantity_"))
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:


    quantity = int(callback.data.split("_")[-1])
    await state.update_data(quantity=quantity)
    sizes = [2,1,1]
    buttons = [
        InlineKeyboardButton(text=f"{quantity}",callback_data="number"),
        InlineKeyboardButton(text="+",callback_data=f"quantity_{quantity+1}"),
        InlineKeyboardButton(text=_("📥 Add to busket"),callback_data="add"),
        InlineKeyboardButton(text="⬅️ back",callback_data="back")
    ]

    product:Product = await state.get_value("product")
    available_items = product.available_items[0]
    lang = await state.get_value("locale")

    text = _(f"""
    Name:       {getattr(product, f"name_{lang}")}
    Brand:      {product.brand_name}
    size:       {callback.data.split("_")[0]}
    color:      {available_items.color}
    price:      {(product.price + available_items.extra_price)*quantity} {product.currency}
    quantity:   {quantity}
    
    """)
    if quantity > 1:
        buttons = [InlineKeyboardButton(text="-",callback_data=f"quantity_{quantity-1}"),] + buttons
        sizes[0] += 1
    markup = make_inline_button(buttons,sizes)
    await state.set_state(StepsState.count)
    await callback.message.edit_caption(caption=text,reply_markup=markup)



@dp.callback_query(F.data == "add")
async def product_type_handler(callback: CallbackQuery,state:FSMContext) -> None:
    query = select(Order).where(Order.user_id == str(callback.from_user.id),Order.status == OrderStatus.pending)
    order:Order = session.execute(query).scalars().first()
    session.commit()
    product_id = await state.get_value("product_id")
    quantity = await state.get_value("quantity")
    total = await state.get_value("total")

    if not order:
        order = Order(user_id=str(callback.from_user.id),status=OrderStatus.pending,amount=(total*quantity))
        session.add(order)
        session.commit()
        order_id = order.order_id
    else:
        order_id = order.order_id
        order.amount += quantity*total
    orderitem = OrderItem(order_id=order_id,product_id=product_id,quantity=quantity)
    session.add(orderitem)
    session.commit()

    buttons = [
        KeyboardButton(text=_("📦 Products Section")),
        KeyboardButton(text=_("📞 Connect with us")),
        KeyboardButton(text=_("🛒 Order")),
        KeyboardButton(text=_("🇺🇿/🇷🇺/🇺🇸 Choose language")),
    ]
    markup = make_reply_button(buttons,[1,1,2])

    await state.set_state(StepsState.main)
    await callback.message.delete()
    await callback.message.answer(_("Successfully added!"),reply_markup=markup)








