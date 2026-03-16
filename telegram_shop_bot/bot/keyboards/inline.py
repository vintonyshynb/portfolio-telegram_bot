from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def lang_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="English", callback_data="lang_en")
            ]
        ]
    )


menus = {
    "en": [
        "Profile",
        "Top up balance",
        "Buy item",
        "Reviews",
        "Rules",
        "Partnership",
        "Chat",
        "Operator",
        "Change language"
    ]
}

callback_data_names = [
    "menu_profile", "profile_topup", "menu_buy_item", "menu_reviews", "menu_rules",
    "menu_partner", "menu_chat", "menu_operator", "menu_lang"
]

back_button_texts = {"en": "Back"}
main_button_texts = {"en": "Main menu"}


def main_menu_kb(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=menus[lang][i], callback_data=callback_data_names[i])]
            for i in range(len(menus[lang]))
        ]
    )


def get_profile_kb(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=menus[lang][1], callback_data="profile_topup")],
            [
                InlineKeyboardButton(text=back_button_texts[lang], callback_data="go_back"),
                InlineKeyboardButton(text=main_button_texts[lang], callback_data="go_main")
            ]
        ]
    )


def get_back_main_menu_kb(lang):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=back_button_texts[lang], callback_data="go_back"),
                InlineKeyboardButton(text=main_button_texts[lang], callback_data="go_main")
            ]
        ]
    )


def operator_admin_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Accept shift", callback_data="accept_shift"),
        InlineKeyboardButton(text="Mailing", callback_data="mailing"),
        InlineKeyboardButton(text="Users", callback_data="users"),
        InlineKeyboardButton(text="Transactions", callback_data="transactions")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def transaction_stats_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Last 20 deposits", callback_data="last_20_deposits"),
        InlineKeyboardButton(text="Search by amount", callback_data="search_by_amount"),
        InlineKeyboardButton(text="Bank deposits", callback_data="bank_deposits"),
        InlineKeyboardButton(text="User deposits", callback_data="user_deposits"),
        InlineKeyboardButton(text="All transactions", callback_data="all_transactions")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def all_transactions_keyboard(transaction_list):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for transaction in transaction_list:
        keyboard.add(
            InlineKeyboardButton(
                text=transaction,
                callback_data=f"transaction_{transaction}"
            )
        )
    keyboard.add(InlineKeyboardButton(text="crypto", callback_data="crypto"))
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def user_profile_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Top up balance", callback_data="topup_balance"),
        InlineKeyboardButton(text="Top up points", callback_data="topup_bonus"),
        InlineKeyboardButton(text="Purchases", callback_data="user_purchases"),
        InlineKeyboardButton(text="Give discount", callback_data="give_discount"),
        InlineKeyboardButton(text="Give treasure", callback_data="give_treasure"),
        InlineKeyboardButton(text="Give rebooking", callback_data="give_rebooking"),
        InlineKeyboardButton(text="Add label", callback_data="add_label"),
        InlineKeyboardButton(text="Ban/Unban", callback_data="ban_unban"),
        InlineKeyboardButton(text="Send message", callback_data="send_message")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def admin_panel_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Mailing", callback_data="mailing"),
        InlineKeyboardButton(text="Worker setup", callback_data="setup_workers"),
        InlineKeyboardButton(text="City setup", callback_data="setup_cities"),
        InlineKeyboardButton(text="Product setup", callback_data="setup_product"),
        InlineKeyboardButton(text="Category setup", callback_data="setup_categories"),
        InlineKeyboardButton(text="Set discount", callback_data="set_discount"),
        InlineKeyboardButton(text="Referral bonus setup", callback_data="setup_ref_bonus"),
        InlineKeyboardButton(text="Points setup", callback_data="setup_points"),
        InlineKeyboardButton(text="Payments setup", callback_data="setup_payments"),
        InlineKeyboardButton(text="Status setup", callback_data="setup_statuses"),
        InlineKeyboardButton(text="Main menu setup", callback_data="setup_main_menu"),
        InlineKeyboardButton(text="Inpost setup", callback_data="setup_inpost"),
        InlineKeyboardButton(text="Coupons", callback_data="coupons"),
        InlineKeyboardButton(text="Statistics", callback_data="statistics"),
        InlineKeyboardButton(text="Delivery setup", callback_data="setup_delivery"),
        InlineKeyboardButton(text="Language setup", callback_data="setup_languages")
    )
    return keyboard


def city_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Add city", callback_data="add_city"),
        InlineKeyboardButton(text="Add district", callback_data="add_district"),
        InlineKeyboardButton(text="Edit city name", callback_data="edit_city_name"),
        InlineKeyboardButton(text="Edit district name", callback_data="edit_district_name"),
        InlineKeyboardButton(text="Edit city photo", callback_data="edit_city_photo"),
        InlineKeyboardButton(text="Edit district photo", callback_data="edit_district_photo"),
        InlineKeyboardButton(text="Delete city photo", callback_data="delete_city_photo"),
        InlineKeyboardButton(text="Delete district photo", callback_data="delete_district_photo"),
        InlineKeyboardButton(text="Delete city", callback_data="delete_city"),
        InlineKeyboardButton(text="Delete district", callback_data="delete_district")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def product_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Add new product", callback_data="add_product"),
        InlineKeyboardButton(text="Edit product name", callback_data="edit_product_name"),
        InlineKeyboardButton(text="Edit product photo", callback_data="edit_product_photo"),
        InlineKeyboardButton(text="Delete photo", callback_data="delete_product_photo"),
        InlineKeyboardButton(text="Edit product description", callback_data="edit_product_description"),
        InlineKeyboardButton(text="Edit product price", callback_data="edit_product_price"),
        InlineKeyboardButton(text="Delete product", callback_data="delete_product")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def categories_keyboard(categories):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        keyboard.add(
            InlineKeyboardButton(
                text=category['name'],
                callback_data=f"category_{category['id']}"
            )
        )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def category_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Add category", callback_data="add_category"),
        InlineKeyboardButton(text="Categories", callback_data="categories")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def bank_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Connect proxy", callback_data="connect_proxy"),
        InlineKeyboardButton(text="IPKO bank setup", callback_data="setup_ipko"),
        InlineKeyboardButton(text="Santander bank setup", callback_data="setup_santander"),
        InlineKeyboardButton(text="Crypto setup", callback_data="setup_crypto")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def main_menu_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton(text="Set photo", callback_data="set_photo"),
        InlineKeyboardButton(text="Delete photo", callback_data="delete_photo"),
        InlineKeyboardButton(text="Set text", callback_data="set_text"),
        InlineKeyboardButton(text="Delete text", callback_data="delete_text"),
        InlineKeyboardButton(text="Add link", callback_data="add_link"),
        InlineKeyboardButton(text="Delete link", callback_data="delete_link")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def choose_action_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Start message setup", callback_data="setup_start_message"),
        InlineKeyboardButton(text="Main menu setup", callback_data="setup_main_menu")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def coupons_settings_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Active coupons", callback_data="active_coupons"),
        InlineKeyboardButton(text="Used coupons", callback_data="used_coupons"),
        InlineKeyboardButton(text="Add coupon", callback_data="add_coupon")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def statistics_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Sales", callback_data="stat_sales"),
        InlineKeyboardButton(text="Rebookings", callback_data="stat_rebookings"),
        InlineKeyboardButton(text="Treasures", callback_data="stat_treasures"),
        InlineKeyboardButton(text="Users", callback_data="stat_users"),
        InlineKeyboardButton(text="Workers", callback_data="stat_workers"),
        InlineKeyboardButton(text="Transactions", callback_data="stat_transactions")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def statistics_period_keyboard():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Today", callback_data="period_today"),
        InlineKeyboardButton(text="Yesterday", callback_data="period_yesterday"),
        InlineKeyboardButton(text="7 days", callback_data="period_7days"),
        InlineKeyboardButton(text="30 days", callback_data="period_30days"),
        InlineKeyboardButton(text="90 days", callback_data="period_90days")
    )
    keyboard.row(
        InlineKeyboardButton(text="Buyers for 14 days", callback_data="buyers_14days"),
        InlineKeyboardButton(text="Buyers for all time", callback_data="buyers_all_time")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def statistics_period_keyboard_simple():
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton(text="Today", callback_data="period_today"),
        InlineKeyboardButton(text="Yesterday", callback_data="period_yesterday"),
        InlineKeyboardButton(text="7 days", callback_data="period_7days"),
        InlineKeyboardButton(text="30 days", callback_data="period_30days"),
        InlineKeyboardButton(text="90 days", callback_data="period_90days")
    )
    keyboard.row(
        InlineKeyboardButton(text="Back", callback_data="back"),
        InlineKeyboardButton(text="Main", callback_data="main")
    )
    return keyboard


def choose_city_keyboard(cities):
    keyboard = InlineKeyboardMarkup(row_width=1)
    for city in cities:
        keyboard.add(
            InlineKeyboardButton(
                text=city['name'],
                callback_data=f"city_{city['id']}"
            )
        )
    return keyboard
