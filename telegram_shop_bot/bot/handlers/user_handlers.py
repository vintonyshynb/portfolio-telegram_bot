from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from bot.database import db
from bot.keyboards.inline import lang_kb, main_menu_kb, get_profile_kb, get_back_main_menu_kb
from bot.utils.messages import messages

router = Router()


class TopupState(StatesGroup):
    waiting_for_custom_amount = State()


class ReviewState(StatesGroup):
    waiting_for_review = State()


texts = {
    "en": {
        "start": "Select language",
        "lang_saved": "Language saved",
        "main_menu": "Main menu",
        "profile": {
            "username": "User",
            "id": "ID",
            "balance": "Balance",
            "discount": "Points",
            "currency": "PLN"
        },
        "not_impl": {
            "topup": "Top-up not available",
            "buy": "Buying not implemented",
            "reviews": "Reviews not available",
            "rules": "Rules not defined",
            "partner": "Partnership not available",
            "chat": "Chat not available",
            "operator": "Operator not available"
        },
        "review_prompt": "Send your review below.",
        "thank_review": "Thank you for your review!",
        "rules_text": "Rules:\n"
    }
}

REVIEW_CHAT_ID = 0


@router.message(Command("start"))
async def start_cmd(msg: types.Message):
    await msg.answer(texts["en"]["start"], reply_markup=lang_kb())


@router.callback_query(F.data.startswith("lang"))
async def lang_selected(call: types.CallbackQuery):
    lang = call.data.split("_")[1]
    user = db.get_user(call.from_user.id)
    if user:
        db.update_user_lang(call.from_user.id, lang)
    else:
        db.create_user(call.from_user.id, call.from_user.username or "NoName", lang)
    await call.message.answer(texts[lang]["lang_saved"], reply_markup=main_menu_kb(lang))
    await call.answer()


@router.callback_query(F.data == "menu_profile")
async def show_profile(call: types.CallbackQuery):
    user = db.get_user(call.from_user.id)
    lang = user["lang"]
    p = texts[lang]["profile"]
    discount = "1" if user["purchase_count"] >= 3 else "0"
    t = (f"{p['username']}: @{user['username']}\n"
         f"{p['id']}: {call.from_user.id}\n"
         f"{p['balance']}: {user['balance']} {p['currency']}\n"
         f"{p['discount']}: {discount}")
    await call.message.edit_text(t, reply_markup=get_profile_kb(lang))
    await call.answer()


@router.callback_query(F.data == "menu_reviews")
async def reviews_handler(call: types.CallbackQuery, state: FSMContext):
    lang = db.get_user(call.from_user.id)["lang"]
    await call.message.edit_text(texts[lang]["review_prompt"], reply_markup=get_back_main_menu_kb(lang))
    await state.set_state(ReviewState.waiting_for_review)
    await call.answer()


@router.message(ReviewState.waiting_for_review)
async def receive_review(msg: types.Message, state: FSMContext):
    user = db.get_user(msg.from_user.id)
    lang = user["lang"]
    await msg.bot.send_message(
        REVIEW_CHAT_ID,
        f"New review:\nFrom: @{msg.from_user.username or msg.from_user.id}\n\n{msg.text}"
    )
    await msg.answer(texts[lang]["thank_review"], reply_markup=get_back_main_menu_kb(lang))
    await state.clear()


@router.callback_query(F.data == "menu_rules")
async def rules_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    await call.message.edit_text(texts[lang]["rules_text"], reply_markup=get_back_main_menu_kb(lang))
    await call.answer()


@router.callback_query(F.data == "menu_partner")
async def partner_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    partner_texts = {
        "en": "Click the button below to start cooperation with our manager:"
    }
    url = "https://t.me/YourPartnerUsername"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Message the manager", url=url)],
            [types.InlineKeyboardButton(text="Back", callback_data="go_back")]
        ]
    )
    await call.message.edit_text(partner_texts["en"], reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data == "menu_chat")
async def chat_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    partner_texts = {
        "en": "Click the button below to chat:"
    }
    url = "https://t.me/YourPartnerUsername"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Message the chat", url=url)],
            [types.InlineKeyboardButton(text="Back", callback_data="go_back")]
        ]
    )
    await call.message.edit_text(partner_texts["en"], reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data == "menu_operator")
async def operator_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    partner_texts = {
        "en": "Click the button below to start a conversation with an operator:"
    }
    url = "https://t.me/YourPartnerUsername"
    keyboard = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text="Message the operator", url=url)],
            [types.InlineKeyboardButton(text="Back", callback_data="go_back")]
        ]
    )
    await call.message.edit_text(partner_texts["en"], reply_markup=keyboard)
    await call.answer()


@router.callback_query(F.data == "menu_lang")
async def change_lang_handler(call: types.CallbackQuery):
    await call.message.edit_text(texts["en"]["start"], reply_markup=lang_kb())
    await call.answer()


@router.callback_query(F.data == "go_back")
async def go_back_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    await call.message.edit_text(texts[lang]["main_menu"], reply_markup=main_menu_kb(lang))
    await call.answer()


@router.callback_query(F.data == "go_main")
async def go_main_handler(call: types.CallbackQuery):
    lang = db.get_user(call.from_user.id)["lang"]
    await call.message.edit_text(texts[lang]["main_menu"], reply_markup=main_menu_kb(lang))
    await call.answer()
