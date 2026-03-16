from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from bot.utils.messages import messages
from bot.database import db

router = Router()


class AdminStates(StatesGroup):
    choosing_language = State()
    in_panel = State()


class AdminFSM(StatesGroup):
    add_name = State()
    add_price = State()
    add_qty = State()
    add_city = State()
    add_district = State()
    change_balance_user_id = State()
    change_balance_amount = State()


def get_language_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="English", callback_data="admin_lang_en")]
    ])


def get_admin_panel_keyboard(lang):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=get_text("add_product_btn", lang), callback_data="admin_add_product")],
        [InlineKeyboardButton(text=get_text("view_orders_btn", lang), callback_data="admin_view_orders")],
        [InlineKeyboardButton(text=get_text("view_payments_btn", lang), callback_data="admin_view_payments")],
        [InlineKeyboardButton(text=get_text("change_balance_btn", lang), callback_data="admin_change_balance")],
        [InlineKeyboardButton(text=get_text("delete_product_btn", lang), callback_data="admin_delete_product")],
        [InlineKeyboardButton(text=get_text("back_btn", lang), callback_data="admin_back")],
        [InlineKeyboardButton(text=get_text("exit_btn", lang), callback_data="admin_exit")]
    ])


def get_text(key, lang):
    return messages.get(key, {}).get(lang, messages[key]["en"])


@router.message(Command("admin"))
async def admin_entry(message: types.Message, state: FSMContext):
    from bot.config import ADMIN_ID

    if not ADMIN_ID:
        await message.answer("ADMIN_ID is not configured")
        return

    if str(message.from_user.id) != str(ADMIN_ID):
        await message.answer("You do not have access to the admin panel.")
        return

    await state.set_state(AdminStates.choosing_language)
    await message.answer(
        messages.get("choose_language", {}).get("en", "Choose language:"),
        reply_markup=get_language_keyboard()
    )


@router.callback_query(F.data.startswith("admin_lang_"))
async def set_language(call: CallbackQuery, state: FSMContext):
    lang = call.data.split("_")[-1]
    await state.update_data(admin_lang=lang)
    await state.set_state(AdminStates.in_panel)
    await call.message.edit_text(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin_back")
async def admin_back(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("admin_lang", "en")
    await call.message.edit_text(get_text("choose_language", lang), reply_markup=get_language_keyboard())
    await state.set_state(AdminStates.choosing_language)


@router.callback_query(F.data == "admin_exit")
async def admin_exit(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("admin_lang", "en")
    await state.clear()
    await call.message.edit_text(get_text("exit_panel", lang))


@router.callback_query(F.data == "admin_add_product")
async def admin_add_product(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    lang = data.get("admin_lang", "en")
    await state.set_state(AdminFSM.add_name)
    await call.message.answer(get_text("enter_product_name", lang))


@router.message(AdminFSM.add_name)
async def process_add_name(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    await state.update_data(name=message.text)
    await state.set_state(AdminFSM.add_price)
    await message.answer(get_text("enter_product_price", lang))


@router.message(AdminFSM.add_price)
async def process_add_price(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    try:
        price = float(message.text)
    except ValueError:
        await message.answer(get_text("price_must_be_number", lang))
        return
    await state.update_data(price=price)
    await state.set_state(AdminFSM.add_qty)
    await message.answer(get_text("enter_product_qty", lang))


@router.message(AdminFSM.add_qty)
async def process_add_qty(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    try:
        qty = int(message.text)
    except ValueError:
        await message.answer(get_text("qty_must_be_number", lang))
        return
    await state.update_data(qty=qty)
    await state.set_state(AdminFSM.add_city)
    await message.answer(get_text("enter_city", lang))


@router.message(AdminFSM.add_city)
async def process_add_city(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    await state.update_data(city=message.text)
    await state.set_state(AdminFSM.add_district)
    await message.answer(get_text("enter_district", lang))


@router.message(AdminFSM.add_district)
async def process_add_district(message: types.Message, state: FSMContext):
    data = await state.update_data(district=message.text)
    lang = (await state.get_data()).get("admin_lang", "en")

    db.add_item(
        name=data["name"],
        price=data["price"],
        qty=data["qty"],
        city=data["city"],
        district=data["district"]
    )

    await message.answer(get_text("product_added", lang))
    await state.set_state(AdminStates.in_panel)
    await message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin_view_orders")
async def admin_view_orders(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    orders = db.get_purchases(limit=10)
    if not orders:
        await call.message.answer(get_text("no_orders_found", lang))
    else:
        text = "\n".join([
            f"ID: {o['id']}, User: {o['user_id']}, Item: {o['item']}, Amount: {o['amount']} PLN, Date: {o['date']}"
            for o in orders
        ])
        await call.message.answer(f"{get_text('view_orders_btn', lang)}:\n{text}")
    await state.set_state(AdminStates.in_panel)
    await call.message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin_change_balance")
async def admin_change_balance(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    await state.set_state(AdminFSM.change_balance_user_id)
    await call.message.answer(get_text("enter_user_id_balance", lang))


@router.message(AdminFSM.change_balance_user_id)
async def process_user_id(message: types.Message, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    try:
        user_id = int(message.text)
    except ValueError:
        await message.answer(get_text("id_must_be_number", lang))
        return
    await state.update_data(user_id=user_id)
    await state.set_state(AdminFSM.change_balance_amount)
    await message.answer(get_text("enter_balance_amount", lang))


@router.message(AdminFSM.change_balance_amount)
async def process_balance_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    lang = data.get("admin_lang", "en")
    try:
        amount = float(message.text)
    except ValueError:
        await message.answer(get_text("amount_must_be_number", lang))
        return
    success = db.update_user_balance(data["user_id"], amount)
    if success:
        await message.answer(get_text("balance_changed", lang))
    else:
        await message.answer(get_text("user_not_found", lang))
    await state.set_state(AdminStates.in_panel)
    await message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin_delete_product")
async def admin_delete_product(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    items = db.get_items()
    if not items:
        await call.message.answer(get_text("no_items_to_delete", lang))
        await state.set_state(AdminStates.in_panel)
        await call.message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))
        return
    buttons = [
        [InlineKeyboardButton(text=f"{item['id']}: {item['name']}", callback_data=f"del_{item['id']}")]
        for item in items
    ]
    markup = InlineKeyboardMarkup(inline_keyboard=buttons)
    await call.message.answer(get_text("choose_product_to_delete", lang), reply_markup=markup)


@router.callback_query(F.data.startswith("del_"))
async def confirm_delete_item(call: CallbackQuery, state: FSMContext):
    item_id = int(call.data.split("_")[1])
    db.delete_item(item_id)
    lang = (await state.get_data()).get("admin_lang", "en")
    await call.message.answer(get_text("product_deleted", lang))
    await state.set_state(AdminStates.in_panel)
    await call.message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))


@router.callback_query(F.data == "admin_view_payments")
async def admin_view_payments(call: CallbackQuery, state: FSMContext):
    lang = (await state.get_data()).get("admin_lang", "en")
    payments = db.get_payment_transactions(limit=20)

    if not payments:
        await call.message.answer("No payment transactions.")
    else:
        text = "LAST PAYMENTS:\n\n"
        total_amount = 0

        for payment in payments:
            amount_display = payment['amount'] / 100
            total_amount += amount_display
            status_text = "COMPLETED" if payment['status'] == 'completed' else "PENDING"

            text += (f"ID: {payment['id']}\n"
                     f"User: {payment['user_id']}\n"
                     f"Amount: {amount_display} {payment['currency']}\n"
                     f"Date: {payment['created_at']}\n"
                     f"Status: {status_text}\n\n")

        text += f"TOTAL TOP UPS: {total_amount} PLN"

        if len(text) > 4000:
            chunks = [text[i:i + 4000] for i in range(0, len(text), 4000)]
            for chunk in chunks:
                await call.message.answer(chunk)
        else:
            await call.message.answer(text)

    await state.set_state(AdminStates.in_panel)
    await call.message.answer(get_text("admin_panel_title", lang), reply_markup=get_admin_panel_keyboard(lang))
