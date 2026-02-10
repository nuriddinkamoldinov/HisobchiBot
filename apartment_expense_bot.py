"""
Apartment Expense Management Telegram Bot
Manages shared expenses for roommates with optimized settlements
"""

import logging
import os
from dotenv import load_dotenv
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters,
)
import sqlite3
from datetime import datetime, timedelta
from collections import defaultdict
import re

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Conversation states
(START, ENTER_NAME, CREATE_OR_JOIN, CREATE_HOME_NAME, CREATE_HOME_PASSWORD,
 CONNECT_GROUP_AFTER_CREATE, JOIN_HOME_NAME, JOIN_HOME_PASSWORD, MAIN_MENU, MANAGE_HOME,
 ENTER_EXPENSE, ENTER_REASON, ENTER_CONSUMERS, EDIT_HOME_NAME, EDIT_HOME_PASSWORD,
 DELETE_MEMBER, ASSIGN_NEW_ADMIN, CHANGE_USER_NAME) = range(18)

# Database setup
def init_db():
    """Initialize the SQLite database"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    
    # Users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY,
                  username TEXT,
                  name TEXT,
                  home_id INTEGER,
                  is_admin INTEGER DEFAULT 0)''')
    
    # Homes table
    c.execute('''CREATE TABLE IF NOT EXISTS homes
                 (home_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  home_name TEXT UNIQUE,
                  password TEXT,
                  created_at TEXT,
                  group_chat_id INTEGER,
                  message_thread_id INTEGER,
                  waiting_for_group INTEGER DEFAULT 0)''')

    # Transactions table
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                  home_id INTEGER,
                  payer_id INTEGER,
                  amount REAL,
                  reason TEXT,
                  consumers TEXT,
                  created_at TEXT,
                  week_number INTEGER)''')

    # Add group_chat_id column to existing homes table if it doesn't exist
    try:
        c.execute('ALTER TABLE homes ADD COLUMN group_chat_id INTEGER')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add message_thread_id column to existing homes table if it doesn't exist
    try:
        c.execute('ALTER TABLE homes ADD COLUMN message_thread_id INTEGER')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add waiting_for_group column to existing homes table if it doesn't exist
    try:
        c.execute('ALTER TABLE homes ADD COLUMN waiting_for_group INTEGER DEFAULT 0')
    except sqlite3.OperationalError:
        pass  # Column already exists

    # Add reason column to existing transactions table if it doesn't exist
    try:
        c.execute('ALTER TABLE transactions ADD COLUMN reason TEXT')
    except sqlite3.OperationalError:
        pass  # Column already exists
    
    conn.commit()
    conn.close()

# Database helper functions
def get_user(user_id):
    """Get user from database"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE user_id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    return user

def create_user(user_id, username, name):
    """Create new user"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('INSERT OR REPLACE INTO users (user_id, username, name) VALUES (?, ?, ?)',
              (user_id, username, name))
    conn.commit()
    conn.close()

def create_home(home_name, password, admin_id):
    """Create new home"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    try:
        c.execute('INSERT INTO homes (home_name, password, created_at) VALUES (?, ?, ?)',
                  (home_name, password, datetime.now().isoformat()))
        home_id = c.lastrowid
        c.execute('UPDATE users SET home_id = ?, is_admin = 1 WHERE user_id = ?',
                  (home_id, admin_id))
        conn.commit()
        conn.close()
        return home_id
    except sqlite3.IntegrityError:
        conn.close()
        return None

def join_home(user_id, home_name, password):
    """Join existing home"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT home_id, password FROM homes WHERE home_name = ?', (home_name,))
    result = c.fetchone()
    
    if result and result[1] == password:
        c.execute('UPDATE users SET home_id = ? WHERE user_id = ?', (result[0], user_id))
        conn.commit()
        conn.close()
        return True
    conn.close()
    return False

def get_home_members(home_id):
    """Get all members of a home"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT user_id, name, is_admin FROM users WHERE home_id = ?', (home_id,))
    members = c.fetchall()
    conn.close()
    return members

def get_group_chat_id(home_id):
    """Get group chat ID and message thread ID for a home"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('SELECT group_chat_id, message_thread_id FROM homes WHERE home_id = ?', (home_id,))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0], result[1]  # (group_chat_id, message_thread_id)
    return None, None

def set_group_chat_id(home_id, group_chat_id, message_thread_id=None):
    """Set group chat ID and message thread ID for a home"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('UPDATE homes SET group_chat_id = ?, message_thread_id = ? WHERE home_id = ?',
              (group_chat_id, message_thread_id, home_id))
    conn.commit()
    conn.close()

def add_transaction(home_id, payer_id, amount, reason, consumers):
    """Add a transaction to the database"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    week_number = datetime.now().isocalendar()[1]
    c.execute('''INSERT INTO transactions
                 (home_id, payer_id, amount, reason, consumers, created_at, week_number)
                 VALUES (?, ?, ?, ?, ?, ?, ?)''',
              (home_id, payer_id, amount, reason, ','.join(map(str, consumers)),
               datetime.now().isoformat(), week_number))
    conn.commit()
    conn.close()

def get_week_transactions(home_id, week_number=None):
    """Get all transactions for current week"""
    if week_number is None:
        week_number = datetime.now().isocalendar()[1]
    
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('''SELECT transaction_id, payer_id, amount, consumers 
                 FROM transactions 
                 WHERE home_id = ? AND week_number = ?''',
              (home_id, week_number))
    transactions = c.fetchall()
    conn.close()
    return transactions

def clear_week_transactions(home_id, week_number):
    """Clear transactions for a specific week"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('DELETE FROM transactions WHERE home_id = ? AND week_number = ?',
              (home_id, week_number))
    conn.commit()
    conn.close()

def cleanup_old_transactions():
    """Delete transactions older than 2 weeks"""
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()

    # Calculate date 2 weeks ago
    two_weeks_ago = (datetime.now() - timedelta(weeks=2)).isoformat()

    # Delete old transactions
    c.execute('DELETE FROM transactions WHERE created_at < ?', (two_weeks_ago,))
    deleted_count = c.rowcount

    conn.commit()
    conn.close()

    return deleted_count

async def scheduled_cleanup(context: ContextTypes.DEFAULT_TYPE):
    """Scheduled job to cleanup old transactions"""
    deleted = cleanup_old_transactions()
    logger.info(f"2 hafta oldingi {deleted} ta harajatlar o'chirib tashlandi")

def parse_amount(text):
    """Parse amount from text, handling spaces in numbers"""
    # Remove spaces from number
    cleaned = re.sub(r'\s+', '', text.strip())
    try:
        return float(cleaned)
    except ValueError:
        return None

def calculate_settlements(transactions, members):
    """
    Calculate optimized settlements using net balance method
    Returns list of (from_user, to_user, amount) tuples
    """
    # Calculate net balance for each member
    balances = defaultdict(float)
    member_dict = {m[0]: m[1] for m in members}
    
    for trans_id, payer_id, amount, consumers_str in transactions:
        consumer_ids = [int(x) for x in consumers_str.split(',')]
        share = amount / len(consumer_ids)
        
        # Payer paid the full amount
        balances[payer_id] += amount
        
        # Each consumer owes their share
        for consumer_id in consumer_ids:
            balances[consumer_id] -= share
    
    # Separate creditors and debtors
    creditors = [(uid, bal) for uid, bal in balances.items() if bal > 0.01]
    debtors = [(uid, -bal) for uid, bal in balances.items() if bal < -0.01]
    
    # Sort by amount
    creditors.sort(key=lambda x: x[1], reverse=True)
    debtors.sort(key=lambda x: x[1], reverse=True)
    
    # Calculate settlements
    settlements = []
    i, j = 0, 0
    
    while i < len(creditors) and j < len(debtors):
        creditor_id, credit = creditors[i]
        debtor_id, debt = debtors[j]
        
        amount = min(credit, debt)
        settlements.append((debtor_id, creditor_id, amount))
        
        creditors[i] = (creditor_id, credit - amount)
        debtors[j] = (debtor_id, debt - amount)
        
        if creditors[i][1] < 0.01:
            i += 1
        if debtors[j][1] < 0.01:
            j += 1
    
    return settlements

# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start the bot and ask for user's name"""
    user = update.effective_user

    # User manual - shown to ALL users
    user_manual = (
        "Foydalanish qoidalari ‼️\n\n"
        "Botdan foydalanish uchun ismingizni kiring. Qolganlarni adashtirmaslik uchun "
        "ismingizni to'g'ri kiriting !\n\n"
        "1. Uyga qo'shiling. Agar yaratilmagan bo'lsa uy nomi va parolni yarating. "
        "Uy yaratuvchisi Admin hisoblanadi\n\n"
        "2. Uy nomi va parolni sheriklaringizga bering.\n\n"
        "3. Hamma qo'shilganiga ishonch hosil qilgandan keyin qilingan harajatlani "
        "yozishingiz mumkin.\n\n"
        "4. Qilinga harajatlarni 14 000 yoki 14000 shaklida yozishingiz mumkin\n\n"
        "5. Istalgan vaqt Admin eski ma'lumotlani o'chirib, mavjud pul o'tkazmalari "
        "haqida barcha uy a'zolariga xabar jo'natishi mumkin.\n\n"
        "6. Oddiy foydalanuvchilar har doim o'ziga tegishli pul o'tkazmalarini "
        "ko'rishlari mumkin."




    )

    await update.message.reply_text(user_manual)

    existing_user = get_user(user.id)
    if existing_user and existing_user[2] and existing_user[3]:  # Has name AND home
        await update.message.reply_text(f"Qaytganingiz bilan, {existing_user[2]}!")
        await menu(update, context)
        return ConversationHandler.END
    elif existing_user and existing_user[2] and not existing_user[3]:  # Has name but NO home
        keyboard = [['Uy yaratish', 'Uyga qo\'shilish'], ['Ismni o\'zgartirish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text(
            f"Qaytganingiz bilan, {existing_user[2]}!\n\n"
            "Siz hali hech qaysi uyga qo'shilmagansiz. Uy yaratmoqchimisiz yoki mavjud uyga qo'shilmoqchimisiz?\n"
            "Yoki ismingizni o'zgartirmoqchimisiz?",
            reply_markup=reply_markup
        )
        context.user_data['name'] = existing_user[2]
        return CREATE_OR_JOIN

    # New user
    await update.message.reply_text(
        "👋 Kvartira harajatlari botiga xush kelibsiz!\n\n"
        "Iltimos, ismingizni kiriting:"
    )
    return ENTER_NAME

async def enter_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store user's name and ask if they want to create or join home"""
    name = update.message.text.strip()
    user = update.effective_user
    
    create_user(user.id, user.username, name)
    context.user_data['name'] = name

    keyboard = [['Uy yaratish', 'Uyga qo\'shilish']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"Tanishganimdan xursandman, {name}!\n\n"
        "Yangi uy yaratmoqchimisiz yoki mavjud uyga qo'shilmoqchimisiz?",
        reply_markup=reply_markup
    )
    return CREATE_OR_JOIN

async def create_or_join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle create or join choice"""
    choice = update.message.text

    if choice == 'Uy yaratish':
        await update.message.reply_text(
            "🏠 Yangi uy yaratish\n\n"
            "Uyingiz uchun nom kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return CREATE_HOME_NAME
    elif choice == 'Uyga qo\'shilish':
        await update.message.reply_text(
            "🚪 Uyga qo'shilish\n\n"
            "Uy nomini kiriting:",
            reply_markup=ReplyKeyboardRemove()
        )
        return JOIN_HOME_NAME
    elif choice == 'Ismni o\'zgartirish':
        keyboard = [['Bekor qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "✏️ Ismni o'zgartirish\n\n"
            "Yangi ismingizni kiriting:",
            reply_markup=reply_markup
        )
        return CHANGE_USER_NAME

async def create_home_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store home name and ask for password"""
    context.user_data['home_name'] = update.message.text.strip()
    await update.message.reply_text("Uyingiz uchun parol kiriting:")
    return CREATE_HOME_PASSWORD

async def create_home_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Create the home with name and password"""
    password = update.message.text.strip()
    home_name = context.user_data['home_name']
    user = update.effective_user

    home_id = create_home(home_name, password, user.id)

    if home_id:
        # Set waiting_for_group flag in database
        conn = sqlite3.connect('apartment_bot.db')
        c = conn.cursor()
        c.execute('UPDATE homes SET waiting_for_group = 1 WHERE home_id = ?', (home_id,))
        conn.commit()
        conn.close()

        # Store info for later
        context.user_data['home_id'] = home_id
        context.user_data['home_name'] = home_name
        context.user_data['home_password'] = password

        await update.message.reply_text(
            f"✅ '{home_name}' uyi yaratildi!\n\n"
            f"📱 Endi guruh chatini ulash kerak:\n\n"
            f"1️⃣ Guruh yarating (yoki mavjud guruhdan foydalaning)\n"
            f"2️⃣ Meni guruhga qo'shing\n"
            f"3️⃣ Guruhda biror xabar yuboring (masalan: 'Test')\n\n"
            f"Guruhda xabar yuborganingizdan keyin, avtomatik ulanadi!"
            f"\n\n📋 Sheriklar uchun:\n"
            f"🏠 Uy nomi: {home_name}\n"
            f"🔑 Parol: {password}"
        )
        # Conversation ends - handle_group_message will handle the connection
        return ConversationHandler.END
    else:
        await update.message.reply_text(
            "❌ Bu nomdagi uy allaqachon mavjud. Iltimos, /start buyrug'i bilan qaytadan urinib ko'ring"
        )
        return ConversationHandler.END

async def debug_all_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Debug: Log ALL messages"""
    if update.message:
        logger.info(f"[DEBUG] Message received: chat_type={update.effective_chat.type}, user={update.effective_user.id}, text={update.message.text[:50] if update.message.text else 'no text'}")

async def handle_group_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle any message in a group - check if user is waiting to connect"""
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    # Only process if it's a group
    if chat.type not in ['group', 'supergroup']:
        return

    logger.info(f"Group message from user {user.id} in chat {chat.id}")

    # Check if this user is waiting to connect a group
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('''SELECT h.home_id, h.home_name, h.password, h.waiting_for_group
                 FROM homes h
                 JOIN users u ON h.home_id = u.home_id
                 WHERE u.user_id = ? AND u.is_admin = 1 AND h.waiting_for_group = 1''',
              (user.id,))
    result = c.fetchone()
    conn.close()

    if not result:
        logger.info(f"User {user.id} not waiting for group connection")
        return

    home_id, home_name, password, waiting = result
    logger.info(f"User {user.id} IS waiting! Connecting group {chat.id} to home {home_id}")

    # Get thread ID if in a topic
    message_thread_id = message.message_thread_id if message.is_topic_message else None

    # Connect the group
    set_group_chat_id(home_id, chat.id, message_thread_id)

    # Clear waiting flag
    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('UPDATE homes SET waiting_for_group = 0 WHERE home_id = ?', (home_id,))
    conn.commit()
    conn.close()

    # Send confirmation in group
    await update.message.reply_text(
        f"✅ Guruh '{home_name}' uyiga ulandi!\n\n"
        "Barcha harajatlar shu yerga avtomatik yuboriladi."
        + (f"\n\n📌 Mavzu: Bu mavzuga yuboriladi" if message_thread_id else "")
    )

    # Send confirmation and menu in private chat
    try:
        await context.bot.send_message(
            chat_id=user.id,
            text="✅ Guruh muvaffaqiyatli ulandi! Endi harajatlarni yozishingiz mumkin."
        )

        # Show menu in private chat
        user_data = get_user(user.id)
        is_admin = user_data[4]

        if is_admin:
            keyboard = [
                ['Uyni boshqarish'],
                ['Hisoblarni ko\'rish (Yangilash)', 'Hisoblarni ko\'rish'],
                ['Ismni o\'zgartirish', 'Uydan chiqish']
            ]
        else:
            keyboard = [
                ['Hisoblarni ko\'rish'],
                ['Ismni o\'zgartirish', 'Uydan chiqish']
            ]

        reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        role = "Administrator" if is_admin else "A'zo"

        await context.bot.send_message(
            chat_id=user.id,
            text=f"🏠 Asosiy menyu ({role})\n\nVariantni tanlang yoki harajat qo'shish uchun raqam yuboring:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Could not send private message: {e}")

    logger.info(f"Group {chat.id} successfully connected to home {home_id}")

async def connect_group_after_create(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Capture group chat ID and thread ID after home creation"""
    chat = update.effective_chat
    user = update.effective_user
    message = update.message

    logger.info(f"connect_group_after_create called by user {user.id} in chat {chat.id} (type: {chat.type})")
    logger.info(f"context.user_data: {context.user_data}")

    # Verify this is the user who created the home
    if 'home_id' not in context.user_data:
        logger.warning(f"User {user.id} has no home_id in context, ignoring")
        # Someone else sent a message, ignore it
        return CONNECT_GROUP_AFTER_CREATE

    # Check if message is from a group
    if chat.type not in ['group', 'supergroup']:
        logger.warning(f"Message not from group, chat type: {chat.type}")
        await update.message.reply_text(
            "❌ Iltimos, guruh chatida xabar yuboring!\n\n"
            "Meni guruhga qo'shib, guruhda biror xabar yuboring."
        )
        return CONNECT_GROUP_AFTER_CREATE

    # Get message thread ID (for topics/forums)
    message_thread_id = message.message_thread_id if message.is_topic_message else None
    logger.info(f"Message thread ID: {message_thread_id}")

    # Save the group chat ID and thread ID
    home_id = context.user_data['home_id']
    logger.info(f"Saving group {chat.id} to home {home_id}")
    set_group_chat_id(home_id, chat.id, message_thread_id)

    home_name = context.user_data['home_name']
    home_password = context.user_data['home_password']

    # Send confirmation in the group (same thread if topics enabled)
    logger.info(f"Sending confirmation to group {chat.id}")
    await update.message.reply_text(
        f"✅ Guruh '{home_name}' uyiga ulandi!\n\n"
        "Barcha harajatlar shu yerga avtomatik yuboriladi."
        + (f"\n\n📌 Mavzu: Bu mavzuga yuboriladi" if message_thread_id else "")
    )

    # Send setup complete message in private chat
    try:
        logger.info(f"Sending confirmation to private chat {user.id}")
        await context.bot.send_message(
            chat_id=user.id,
            text=(
                f"✅ Guruh muvaffaqiyatli ulandi!\n\n"
                f"📋 Ushbu ma'lumotlarni sheriklаringizga bering:\n"
                f"🏠 Uy nomi: {home_name}\n"
                f"🔑 Parol: {home_password}\n\n"
                f"Endi harajatlarni yozishingiz mumkin!"
            )
        )
        await menu(update, context)
        logger.info("Group connection completed successfully")
    except Exception as e:
        logger.error(f"Shaxsiy chatga xabar yuborib bo'lmadi: {e}")

    return ConversationHandler.END

async def join_home_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Store home name for joining"""
    context.user_data['join_home_name'] = update.message.text.strip()
    await update.message.reply_text("Uy parolini kiriting:")
    return JOIN_HOME_PASSWORD

async def join_home_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Join the home with credentials"""
    password = update.message.text.strip()
    home_name = context.user_data['join_home_name']
    user = update.effective_user
    
    if join_home(user.id, home_name, password):
        await update.message.reply_text(f"✅ '{home_name}' uyiga muvaffaqiyatli qo'shildingiz!")
        await menu(update, context)
    else:
        await update.message.reply_text(
            "❌ Noto'g'ri uy nomi yoki parol. Iltimos, /start buyrug'i bilan qaytadan urinib ko'ring"
        )

    return ConversationHandler.END

async def change_user_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Change user's name"""
    new_name = update.message.text.strip()

    # Check for cancel
    if new_name == 'Bekor qilish':
        user = update.effective_user
        user_data = get_user(user.id)
        if user_data[3]:  # Has a home
            await update.message.reply_text("❌ Amal bekor qilindi.")
            await menu(update, context)
        else:  # No home
            keyboard = [['Uy yaratish', 'Uyga qo\'shilish'], ['Ismni o\'zgartirish']]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
            await update.message.reply_text(
                "❌ Amal bekor qilindi.\n\n"
                "Uy yaratmoqchimisiz yoki mavjud uyga qo'shilmoqchimisiz?",
                reply_markup=reply_markup
            )
        return ConversationHandler.END

    user = update.effective_user

    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET name = ? WHERE user_id = ?', (new_name, user.id))
    conn.commit()
    conn.close()

    user_data = get_user(user.id)

    if user_data[3]:  # Has a home
        await update.message.reply_text(f"✅ Ismingiz '{new_name}' ga o'zgartirildi")
        await menu(update, context)
        return ConversationHandler.END
    else:  # No home, show create/join options
        keyboard = [['Uy yaratish', 'Uyga qo\'shilish'], ['Ismni o\'zgartirish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        await update.message.reply_text(
            f"✅ Ismingiz '{new_name}' ga o'zgartirildi\n\n"
            "Uy yaratmoqchimisiz yoki mavjud uyga qo'shilmoqchimisiz?",
            reply_markup=reply_markup
        )
        return CREATE_OR_JOIN

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show main menu based on user role"""
    user = update.effective_user
    user_data = get_user(user.id)
    
    if not user_data or not user_data[3]:  # No home
        await update.message.reply_text(
            "Siz hali hech qaysi uyga qo'shilmagansiz. Uy yaratish yoki qo'shilish uchun /start buyrug'idan foydalaning."
        )
        return

    is_admin = user_data[4]

    if is_admin:
        keyboard = [
            ['Uyni boshqarish'],
            ['Hisoblarni ko\'rish (Yangilash)', 'Hisoblarni ko\'rish'],
            ['Ismni o\'zgartirish', 'Uydan chiqish']
        ]
    else:
        keyboard = [
            ['Hisoblarni ko\'rish'],
            ['Ismni o\'zgartirish', 'Uydan chiqish']
        ]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    role = "Administrator" if is_admin else "A'zo"
    await update.message.reply_text(
        f"🏠 Asosiy menyu ({role})\n\n"
        "Variantni tanlang yoki harajat qo'shish uchun raqam yuboring:",
        reply_markup=reply_markup
    )

async def handle_menu_choice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle menu button presses"""
    choice = update.message.text
    user = update.effective_user
    user_data = get_user(user.id)
    
    if not user_data or not user_data[3]:
        await update.message.reply_text("Iltimos, avval /start buyrug'idan foydalaning.")
        return

    if choice == 'Hisoblarni ko\'rish (Yangilash)':
        await send_calculations(update, context, refresh=True)

    elif choice == 'Hisoblarni ko\'rish':
        await send_calculations(update, context, refresh=False)

    elif choice == 'Uyni boshqarish':
        if user_data[4]:  # Is admin
            keyboard = [
                ['Uy nomini o\'zgartirish', 'Parolni o\'zgartirish'],
                ['A\'zoni o\'chirish'],
                ['Menyuga qaytish']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
            await update.message.reply_text(
                "⚙️ Uyni boshqarish\n\nVariantni tanlang:",
                reply_markup=reply_markup
            )
            return MANAGE_HOME

    elif choice == 'Ismni o\'zgartirish':
        keyboard = [['Bekor qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "✏️ Ismni o'zgartirish\n\n"
            "Yangi ismingizni kiriting:",
            reply_markup=reply_markup
        )
        return CHANGE_USER_NAME

    elif choice == 'Uydan chiqish':
        await quit_home(update, context)

async def send_calculations(update: Update, context: ContextTypes.DEFAULT_TYPE, refresh=False):
    """Calculate and send settlement information"""
    user = update.effective_user
    user_data = get_user(user.id)
    home_id = user_data[3]
    week_number = datetime.now().isocalendar()[1]

    # Get transactions
    transactions = get_week_transactions(home_id, week_number)

    if not transactions:
        await update.message.reply_text("📊 Bu haftada hali hech qanday harajat qayd etilmagan.")
        return

    # Get members
    members = get_home_members(home_id)
    member_dict = {m[0]: m[1] for m in members}

    # Calculate settlements
    settlements = calculate_settlements(transactions, members)

    if refresh:
        # Refresh mode: Send to ALL members and clear transactions
        for member_id, member_name, is_admin in members:
            # Calculate what this member receives and gives
            # Skip settlements involving deleted users
            receives = [(member_dict[from_id], amount)
                       for from_id, to_id, amount in settlements
                       if to_id == member_id and from_id in member_dict]
            gives = [(member_dict[to_id], amount)
                    for from_id, to_id, amount in settlements
                    if from_id == member_id and to_id in member_dict]

            message = f"📊 {week_number}-hafta hisob-kitoblari\n"
            message += "=" * 30 + "\n\n"

            if receives:
                message += "💰 Sizga pul beradigan kishilar:\n"
                for name, amount in receives:
                    message += f"  • {name}: {amount:,.0f} so'm\n"
                message += "\n"

            if gives:
                message += "💸 Siz pul beradigan kishilar:\n"
                for name, amount in gives:
                    message += f"  • {name}: {amount:,.0f} so'm\n"
                message += "\n"

            if not receives and not gives:
                message += "✅ Sizda hech qanday qarz yo'q!\n\n"

            try:
                await context.bot.send_message(chat_id=member_id, text=message)
            except Exception as e:
                logger.error(f"Could not send message to {member_id}: {e}")

        # Clear the transactions after sending to everyone
        clear_week_transactions(home_id, week_number)
        await update.message.reply_text(
            "✅ Hisob-kitoblar barcha a'zolarga yuborildi va harajatlar tozalandi!"
        )
    else:
        # Non-refresh mode: Send ONLY to the person who requested it
        member_id = user.id
        # Skip settlements involving deleted users
        receives = [(member_dict[from_id], amount)
                   for from_id, to_id, amount in settlements
                   if to_id == member_id and from_id in member_dict]
        gives = [(member_dict[to_id], amount)
                for from_id, to_id, amount in settlements
                if from_id == member_id and to_id in member_dict]

        message = f"📊 {week_number}-hafta hisob-kitoblari (Sizning ko'rinishingiz)\n"
        message += "=" * 30 + "\n\n"

        if receives:
            message += "💰 Sizga pul beradigan kishilar:\n"
            for name, amount in receives:
                message += f"  • {name}: {amount:,.0f} so'm\n"
            message += "\n"

        if gives:
            message += "💸 Siz pul beradigan kishilar:\n"
            for name, amount in gives:
                message += f"  • {name}: {amount:,.0f} so'm\n"
            message += "\n"

        if not receives and not gives:
            message += "✅ Sizda hech qanday qarz yo'q!\n\n"

        message += "\n💡 Bu faqat sizga ko'rinadi.\n"
        message += "Harajatlar tozalanMADI."

        await update.message.reply_text(message)

async def auto_detect_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Auto-detect numbers and start expense flow"""
    user = update.effective_user
    user_data = get_user(user.id)

    # Check if user has a home
    if not user_data or not user_data[3]:
        return

    # Try to parse as amount
    amount = parse_amount(update.message.text)
    if amount is None or amount <= 0:
        return

    # Valid amount detected, start expense flow
    context.user_data['expense_amount'] = amount

    # Ask for reason
    keyboard = [['Bekor qilish']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"💰 Harajat: {amount:,.0f} so'm\n\n"
        "📝 Nima uchun sarflandi? (Mahsulotlarni kiriting)\n\n"
        "Har bir mahsulotni alohida qatorda yoki bir qatorda yozing:",
        reply_markup=reply_markup
    )

    return ENTER_REASON

async def enter_expense(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle expense amount entry"""
    amount = parse_amount(update.message.text)

    if amount is None or amount <= 0:
        await update.message.reply_text(
            "❌ Noto'g'ri miqdor. Iltimos, to'g'ri raqam kiriting:"
        )
        return ENTER_EXPENSE

    context.user_data['expense_amount'] = amount

    # Ask for reason
    keyboard = [['Bekor qilish']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    await update.message.reply_text(
        f"💰 Harajat: {amount:,.0f} so'm\n\n"
        "📝 Nima uchun sarflandi? (Mahsulotlarni kiriting)\n\n"
        "Har bir mahsulotni alohida qatorda yoki bir qatorda yozing:",
        reply_markup=reply_markup
    )

    return ENTER_REASON

async def enter_reason(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle expense reason entry"""
    # Check for cancel
    if update.message.text == 'Bekor qilish':
        await update.message.reply_text("❌ Harajat bekor qilindi.")
        await menu(update, context)
        return ConversationHandler.END

    reason = update.message.text.strip()
    context.user_data['expense_reason'] = reason

    # Get home members
    user = update.effective_user
    user_data = get_user(user.id)
    home_id = user_data[3]
    members = get_home_members(home_id)

    # Show members list
    message = "👥 Bu mahsulotni kim iste'mol qiladi?\n\n"
    message += "0. Barcha a'zolarni tanlash uchun\n"
    for idx, (member_id, name, is_admin) in enumerate(members, 1):
        message += f"{idx}. {name}\n"
    message += "\nRaqamlarni bo'sh joy bilan ajratib kiriting (masalan, '1 3 5')\nYoki hammani tanlash uchun '0' ni kiriting:"

    keyboard = [['Bekor qilish']]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

    context.user_data['members_list'] = members
    await update.message.reply_text(message, reply_markup=reply_markup)

    return ENTER_CONSUMERS

async def enter_consumers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle consumer selection"""
    # Check for cancel
    if update.message.text == 'Bekor qilish':
        await update.message.reply_text("❌ Harajat bekor qilindi.")
        await menu(update, context)
        return ConversationHandler.END

    try:
        numbers = [int(x.strip()) for x in update.message.text.split()]
        members = context.user_data['members_list']

        # Check if 0 was entered (select all)
        if 0 in numbers:
            if len(numbers) > 1:
                await update.message.reply_text(
                    "❌ '0' (barcha a'zolar) ni tanlaganda boshqa raqamlar kiritmang.\n"
                    "Hammani tanlash uchun faqat '0' kiriting yoki muayyan a'zolar raqamlarini kiriting:"
                )
                return ENTER_CONSUMERS

            # Select all members
            consumer_ids = [m[0] for m in members]
            consumer_names = [m[1] for m in members]
        else:
            # Validate numbers
            if not numbers or any(n < 1 or n > len(members) for n in numbers):
                await update.message.reply_text(
                    f"❌ Noto'g'ri tanlov. Iltimos, quyidagilardan birini kiriting:\n"
                    f"  • Barcha a'zolar uchun '0', YOKI\n"
                    f"  • 1 dan {len(members)} gacha bo'lgan raqamlar:"
                )
                return ENTER_CONSUMERS

            # Get consumer IDs
            consumer_ids = [members[n-1][0] for n in numbers]
            consumer_names = [members[n-1][1] for n in numbers]

        # Add transaction
        user = update.effective_user
        user_data = get_user(user.id)
        home_id = user_data[3]
        amount = context.user_data['expense_amount']
        reason = context.user_data.get('expense_reason', 'Sabab ko\'rsatilmagan')

        add_transaction(home_id, user.id, amount, reason, consumer_ids)

        share = amount / len(consumer_ids)

        # Send confirmation to user
        consumer_list = '\n'.join(consumer_names)
        await update.message.reply_text(
            f"✅ Harajat yozildi!\n\n"
            f"Miqdor: {amount:,.0f} so'm\n"
            f"Sabab: {reason}\n"
            f"Bo'linadi:\n\n"
            f"{consumer_list}\n\n"
            f"Har biri to'laydi: {share:,.0f} so'm"
        )

        # Send notification to group
        group_chat_id, message_thread_id = get_group_chat_id(home_id)
        if group_chat_id:
            # Check if all members are consumers
            all_members = len(consumer_ids) == len(members)

            if all_members:
                consumer_text = "Barcha uy a'zolari"
            else:
                consumer_text = '\n'.join([f"{idx}. {name}" for idx, name in enumerate(consumer_names, 1)])

            group_message = (
                f"💸 Harajat: {amount:,.0f}\n\n"
                f"📄 Sabab:\n\n"
                f"{reason}\n\n"
                f"👥 Iste'molchilar:\n\n"
                f"{consumer_text}\n\n"
                f"👤 Har biriga: {share:,.0f}"
            )

            try:
                # Send to specific topic if message_thread_id exists
                await context.bot.send_message(
                    chat_id=group_chat_id,
                    text=group_message,
                    message_thread_id=message_thread_id
                )
            except Exception as e:
                logger.error(f"Guruhga xabar yuborib bo'lmadi: {e}")

        await menu(update, context)
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text(
            "❌ Noto'g'ri format. Iltimos bo'sh joy bilan ajratib kiriting (masalan, '1 3 5')\n:"
        )
        return ENTER_CONSUMERS

async def manage_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle manage home menu"""
    choice = update.message.text

    if choice == 'Menyuga qaytish':
        await menu(update, context)
        return ConversationHandler.END

    elif choice == 'Uy nomini o\'zgartirish':
        keyboard = [['Bekor qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Yanigi uy nomini kiriting:",
            reply_markup=reply_markup
        )
        return EDIT_HOME_NAME

    elif choice == 'Parolni o\'zgartirish':
        keyboard = [['Bekor qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)
        await update.message.reply_text(
            "Yangi parolni kiriting:",
            reply_markup=reply_markup
        )
        return EDIT_HOME_PASSWORD

    elif choice == 'A\'zoni o\'chirish':
        user = update.effective_user
        user_data = get_user(user.id)
        home_id = user_data[3]
        members = get_home_members(home_id)

        # Show non-admin members
        non_admin_members = [(m[0], m[1]) for m in members if not m[2]]

        if not non_admin_members:
            await update.message.reply_text("Hech kim o'chirilmadi")
            await menu(update, context)
            return ConversationHandler.END

        message = "O'chirish uchun a'zoni tanlang\n\n"
        for idx, (member_id, name) in enumerate(non_admin_members, 1):
            message += f"{idx}. {name}\n"
        message += "\nRaqam kiriting:"

        keyboard = [['Bekor qilish']]
        reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True)

        context.user_data['delete_members_list'] = non_admin_members
        await update.message.reply_text(message, reply_markup=reply_markup)
        return DELETE_MEMBER

async def edit_home_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit home name"""
    new_name = update.message.text.strip()

    # Check for cancel
    if new_name == 'Bekor qilish':
        await update.message.reply_text("❌ Bekor qilindi.")
        await menu(update, context)
        return ConversationHandler.END

    user = update.effective_user
    user_data = get_user(user.id)
    home_id = user_data[3]

    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    try:
        c.execute('UPDATE homes SET home_name = ? WHERE home_id = ?', (new_name, home_id))
        conn.commit()
        await update.message.reply_text(f"✅ Uy nomi '{new_name}' ga o'zgartirildi")
    except sqlite3.IntegrityError:
        await update.message.reply_text("❌ Bunday uy nomi mavjud. Boshqa nom bilan urinib ko'ring")
    finally:
        conn.close()

    await menu(update, context)
    return ConversationHandler.END

async def edit_home_password(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Edit home password"""
    new_password = update.message.text.strip()

    # Check for cancel
    if new_password == 'Bekor qilish':
        await update.message.reply_text("❌ Bekor qilindi.")
        await menu(update, context)
        return ConversationHandler.END

    user = update.effective_user
    user_data = get_user(user.id)
    home_id = user_data[3]

    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('UPDATE homes SET password = ? WHERE home_id = ?', (new_password, home_id))
    conn.commit()
    conn.close()

    await update.message.reply_text(f"✅ Parol muvaffaqiyatli o'zgartirildi")
    await menu(update, context)
    return ConversationHandler.END

async def delete_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Delete a member from home"""
    # Check for cancel
    if update.message.text == 'Bekor qilish':
        await update.message.reply_text("❌ Bekor qilindi.")
        await menu(update, context)
        return ConversationHandler.END

    try:
        number = int(update.message.text.strip())
        members_list = context.user_data['delete_members_list']

        if number < 1 or number > len(members_list):
            await update.message.reply_text("❌ Noto'g'ri raqam. Qayta urining:")
            return DELETE_MEMBER

        member_id, member_name = members_list[number - 1]

        conn = sqlite3.connect('apartment_bot.db')
        c = conn.cursor()
        c.execute('UPDATE users SET home_id = NULL, is_admin = 0 WHERE user_id = ?', (member_id,))
        conn.commit()
        conn.close()

        await update.message.reply_text(f"✅ {member_name} uydan chiqarib yuborildi")

        try:
            await context.bot.send_message(
                chat_id=member_id,
                text="Siz admin tomonidan uydan chiqarib yuborildingiz"
            )
        except Exception as e:
            logger.error(f"Chiqarib yumorilgan a'zoga xabar berib bo'lmaydi: {e}")

        await menu(update, context)
        return ConversationHandler.END

    except ValueError:
        await update.message.reply_text("❌ Iltimos to'g'ri raqam kiriting:")
        return DELETE_MEMBER

async def quit_home(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Quit from home"""
    user = update.effective_user
    user_data = get_user(user.id)
    home_id = user_data[3]
    is_admin = user_data[4]

    if is_admin:
        # Check if there are other members
        members = get_home_members(home_id)
        if len(members) > 1:
            await update.message.reply_text(
                "⚠️ Admin sifatida siz faqat quyidagilani qila olasiz:\n\n"
                "1. Avval hamma a'zolarni o'chirish, yoki\n"
                "2. Yangi Admin tayyorlash\n\n"
                "Bu amalni bajarish hali mumkin emas. Iltimos, avval barcha a'zolarni o'chiring."
            )
            await menu(update, context)
            return

    conn = sqlite3.connect('apartment_bot.db')
    c = conn.cursor()
    c.execute('UPDATE users SET home_id = NULL, is_admin = 0 WHERE user_id = ?', (user.id,))
    conn.commit()
    conn.close()

    await update.message.reply_text(
        "✅ Siz uydan chiqdingiz.\n\n"
        "Yangi uyga qo'shilish yoki yaratish uchun /start buyrug'idan foydalaning.",
        reply_markup=ReplyKeyboardRemove()
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the current operation"""
    user = update.effective_user
    user_data = get_user(user.id)

    if user_data and user_data[3]:  # Has a home
        await update.message.reply_text("❌ Bekor qilindi.")
        await menu(update, context)
    else:
        await update.message.reply_text(
            "Bekor qilindi.",
            reply_markup=ReplyKeyboardRemove()
        )
    return ConversationHandler.END

def main():
    """Start the bot"""
    # Load environment variables
    load_dotenv()

    # Initialize database
    init_db()

    # Create application
    TOKEN = os.getenv('BOT_TOKEN')
    if not TOKEN:
        raise ValueError("BOT_TOKEN not found in environment variables. Please create a .env file with BOT_TOKEN=your_token")

    application = Application.builder().token(TOKEN).build()

    # Conversation handler for initial setup
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            ENTER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_name)],
            CREATE_OR_JOIN: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_or_join)],
            CREATE_HOME_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_home_name)],
            CREATE_HOME_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, create_home_password)],
            # CONNECT_GROUP_AFTER_CREATE removed - handled by handle_group_message instead
            JOIN_HOME_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, join_home_name)],
            JOIN_HOME_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, join_home_password)],
            CHANGE_USER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_user_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Auto-detect expense conversation handler (when user sends a number)
    auto_expense_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.TEXT & ~filters.COMMAND, auto_detect_expense)],
        states={
            ENTER_REASON: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_reason)],
            ENTER_CONSUMERS: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_consumers)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Manage home conversation handler
    manage_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Uyni boshqarish$'), handle_menu_choice)],
        states={
            MANAGE_HOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, manage_home)],
            EDIT_HOME_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_home_name)],
            EDIT_HOME_PASSWORD: [MessageHandler(filters.TEXT & ~filters.COMMAND, edit_home_password)],
            DELETE_MEMBER: [MessageHandler(filters.TEXT & ~filters.COMMAND, delete_member)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Change name conversation handler
    change_name_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex('^Ismni o\'zgartirish$'), handle_menu_choice)],
        states={
            CHANGE_USER_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, change_user_name)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # DEBUG: Add this first to see ALL messages
    application.add_handler(MessageHandler(filters.ALL, debug_all_messages), group=-1)

    application.add_handler(conv_handler)
    application.add_handler(manage_handler)
    application.add_handler(change_name_handler)
    application.add_handler(CommandHandler('menu', menu))
    application.add_handler(MessageHandler(
        filters.Regex(r"^(Hisoblarni ko'rish|Hisoblarni ko'rish \(Yangilash\)|Uydan chiqish)$"),
        handle_menu_choice
    ))
    # Handle group messages for connecting groups (must be before auto_expense_handler)
    application.add_handler(MessageHandler(
        filters.ChatType.GROUPS & filters.TEXT & ~filters.COMMAND,
        handle_group_message
    ))
    # Auto-detect expense handler should be last to not interfere with other handlers
    application.add_handler(auto_expense_handler)

    # Schedule daily cleanup of old transactions (runs every 24 hours)
    job_queue = application.job_queue
    job_queue.run_repeating(scheduled_cleanup, interval=timedelta(hours=24), first=10)

    # Run cleanup on startup
    cleanup_old_transactions()
    logger.info("Boshlang'ich tozalash tugatildi")

    # Start the bot
    logger.info("Bot ishga tushdi...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()