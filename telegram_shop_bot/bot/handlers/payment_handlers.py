from aiogram import Router, F, types
from aiogram.types import CallbackQuery, PreCheckoutQuery, Message
from bot.database import db
from bot.config import ADMIN_ID

router = Router()


@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)


@router.message(F.successful_payment)
async def process_successful_payment(message: Message):
    user = db.get_user(message.from_user.id)
    payment = message.successful_payment

    transaction_id = db.create_payment_transaction(
        user_id=message.from_user.id,
        amount=payment.total_amount,
        currency=payment.currency,
        telegram_charge_id=payment.telegram_payment_charge_id,
        provider_charge_id=payment.provider_payment_charge_id
    )

    result = db.complete_payment_transaction(
        payment.telegram_payment_charge_id,
        message.from_user.id
    )

    from bot.utils.messages import messages
    lang = user["lang"] if user else "en"

    if result["success"]:
        await message.answer(messages["payment_successful"][lang].format(
            amount=result['amount_added'],
            balance=result['new_balance'],
            transaction_id=payment.telegram_payment_charge_id
        ))

        try:
            admin_notification = (
                f"NEW PAYMENT!\n\n"
                f"From: @{message.from_user.username or 'No username'} (ID: {message.from_user.id})\n"
                f"Amount: {result['amount_added']} {payment.currency}\n"
                f"Transaction ID: {payment.telegram_payment_charge_id}\n"
                f"Provider ID: {payment.provider_payment_charge_id}\n"
                f"Date: {message.date.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            await message.bot.send_message(ADMIN_ID, admin_notification)
        except Exception as e:
            print(f"Error notifying admin: {e}")

    else:
        await message.answer(messages["payment_error"][lang])

        try:
            error_notification = (
                f"PAYMENT ERROR!\n\n"
                f"From: @{message.from_user.username or 'No username'} (ID: {message.from_user.id})\n"
                f"Amount: {payment.total_amount / 100} {payment.currency}\n"
                f"Transaction ID: {payment.telegram_payment_charge_id}\n"
                f"Error: {result.get('error', 'Unknown')}"
            )
            await message.bot.send_message(ADMIN_ID, error_notification)
        except Exception as e:
            print(f"Error notifying admin about payment error: {e}")


@router.callback_query(F.data == "user_pay_now")
async def handle_payment(callback: CallbackQuery):
    await callback.answer("Please use the top-up option in your profile.", show_alert=True)
