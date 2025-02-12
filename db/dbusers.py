import sqlite3
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# تطبيق nest_asyncio لتجنب مشاكل حلقة الأحداث
nest_asyncio.apply()

# إعداد قاعدة البيانات
def setup_database():
    conn = sqlite3.connect(r'C:\Users\AHMED\Desktop\btc room\db\users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER UNIQUE,
            balance INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()
    print("Database setup complete.")

# إضافة مستخدم جديد
def add_user(user_id):
    conn = sqlite3.connect(r'C:\Users\AHMED\Desktop\btc room\db\users.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id) VALUES (?)
    ''', (user_id,))
    conn.commit()
    conn.close()
    print(f"User added: {user_id}")

# الحصول على معرف المستخدم
def get_user_id(user_id):
    conn = sqlite3.connect(r'C:\Users\AHMED\Desktop\btc room\db\users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

# الأمر /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    add_user(user_id)
    await update.message.reply_text('Welcome! Your ID has been created.')

# الأمر /iid
async def iid(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    user = get_user_id(user_id)
    if user:
        await update.message.reply_text(f'Your ID: {user[0]}')  # إرسال المعرف الفعلي
    else:
        await update.message.reply_text('User not found.')

# إعداد البوت
async def main():
    setup_database()
    application = ApplicationBuilder().token("7872231654:AAEh4pdF1ulhczk9R5x_3EP41klpHrTd5_E").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("iid", iid))
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())