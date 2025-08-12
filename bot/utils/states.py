from aiogram.fsm.state import StatesGroup, State


class StepsState(StatesGroup):
    main = State()
    category = State()
    subcategory = State()
    product = State()
    language = State()
    contact = State()
    share_contact = State()
    available = State()
    count = State()
    order = State()
    court = State()
    all_history = State()
    paymant = State()
