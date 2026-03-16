messages = {
    "no_access": {
        "en": "You do not have access to the admin panel."
    },
    "admin_panel_title": {
        "en": "You are in the admin panel. Choose an action:"
    },
    "add_product_btn": {
        "en": "Add product"
    },
    "view_orders_btn": {
        "en": "View orders"
    },
    "change_balance_btn": {
        "en": "Change user balance"
    },
    "delete_product_btn": {
        "en": "Delete product"
    },
    "back_btn": {
        "en": "Back"
    },
    "exit_btn": {
        "en": "Exit"
    },
    "exit_panel": {
        "en": "You have exited the admin panel."
    },
    "add_product": {
        "en": "Adding a new product. Enter product name:"
    },
    "view_orders": {
        "en": "Loading orders..."
    },
    "change_balance": {
        "en": "Enter user ID to change balance:"
    },
    "delete_product": {
        "en": "Choose the product to delete:"
    },
    "enter_product_name": {
        "en": "Enter product name:"
    },
    "enter_product_price": {
        "en": "Enter product price:"
    },
    "price_must_be_number": {
        "en": "Price must be a number. Try again."
    },
    "enter_product_qty": {
        "en": "Enter product quantity:"
    },
    "qty_must_be_number": {
        "en": "Quantity must be a number. Try again."
    },
    "enter_city": {
        "en": "Enter city:"
    },
    "enter_district": {
        "en": "Enter district:"
    },
    "product_added": {
        "en": "Product added."
    },
    "no_orders_found": {
        "en": "No orders found."
    },
    "enter_user_id_balance": {
        "en": "Enter user ID to change balance:"
    },
    "id_must_be_number": {
        "en": "ID must be a number. Try again."
    },
    "enter_balance_amount": {
        "en": "Enter amount to change balance by (can be negative):"
    },
    "amount_must_be_number": {
        "en": "Amount must be a number."
    },
    "balance_changed": {
        "en": "Balance changed."
    },
    "user_not_found": {
        "en": "User not found."
    },
    "no_items_to_delete": {
        "en": "No products to delete."
    },
    "choose_product_to_delete": {
        "en": "Choose a product to delete:"
    },
    "product_deleted": {
        "en": "Product deleted."
    },
    "view_payments_btn": {
        "en": "View payments"
    },
    "payment_successful": {
        "en": "Payment successful!\n\nAdded: {amount} PLN\nNew balance: {balance} PLN\n\nTransaction ID: {transaction_id}"
    },
    "payment_error": {
        "en": "Payment processing error. Contact support."
    },
    "topup_choose_amount": {
        "en": "Choose amount to top up your balance:"
    },
    "topup_custom_amount": {
        "en": "Enter custom amount"
    },
    "custom_amount_prompt": {
        "en": "Enter amount to top up your balance (minimum 1 PLN, maximum 1000 PLN):\n\nExample: 125"
    },
    "amount_too_low": {
        "en": "Minimum amount is 1 PLN. Try again."
    },
    "amount_too_high": {
        "en": "Maximum amount is 1000 PLN. Try again."
    },
    "invalid_amount_format": {
        "en": "Invalid amount format. Enter a number (example: 25 or 25.50)"
    },
    "payments_not_configured": {
        "en": "Payments not configured. Contact administrators."
    },
    "invoice_creation_error": {
        "en": "Error creating invoice. Try again later."
    },
    "payment_info": {
        "en": "Top-up amount: {amount} PLN\n\nSecure payments via Telegram\nWe support cards\nFunds will be added to your account immediately"
    },
    "pay_button": {
        "en": "Pay {amount} PLN"
    }
}


def get_topup_amounts(lang):
    currency = {"en": "PLN"}
    topup_text = {
        "en": "Top up with"
    }

    amounts = [
        {"amount": 5000, "value": 50},
        {"amount": 10000, "value": 100},
        {"amount": 20000, "value": 200},
        {"amount": 50000, "value": 500},
        {"amount": 100000, "value": 1000}
    ]

    result = []
    for amount_data in amounts:
        result.append({
            "amount": amount_data["amount"],
            "title": f"{amount_data['value']} {currency[lang]}",
            "description": f"{topup_text[lang]} {amount_data['value']} {currency[lang]}"
        })

    return result


def format_user_profile_message(user):
    message = (f"ID: {user['id']}\n"
               f"Name: {user['name']}\n"
               f"Balance: {user['balance']}\n"
               f"Status: {user['status']}\n"
               f"Status discount: {user['status_discount']}%\n"
               f"Personal discount: {user['personal_discount']}%\n"
               f"Bonuses: {user['bonus']}\n"
               f"Rights: {user['rights']}\n"
               f"Purchases: {user['purchases']}\n"
               f"Rebookings: {user['rebookings']}\n"
               f"Total spent: {user['spent']}\n"
               f"Link: @{user['link']}\n"
               f"Registered: {user['registered']}\n\n"
               f"Account status: {user['account_status']}\n"
               f"BOT: <a href='tg://user?id={user['bot_id']}'>{user['bot_id']}</a>")
    return message


def format_ref_bonus_message(current_value):
    return (
        "Enter a number from 0 to 100 as the percentage that will be credited to the referrer when the referral tops up the balance\n"
        f"Current value {current_value}%"
    )


def format_bank_status_message(banks):
    message = ""
    for bank in banks:
        message += f"Bank - {bank['type']} {bank.get('status', '')}\n"
        message += f"login - {bank['login']}\n"
        message += f"balance - {bank['balance']} {bank['currency']}\n"
        message += f"updated - {bank['updated']}\n\n"
    return message
