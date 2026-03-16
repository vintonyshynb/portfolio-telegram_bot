from aiogram import Router, F
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(F.data == "purchase_pay")
async def handle_payment(callback: CallbackQuery):
    await callback.answer("Payment processing...")
