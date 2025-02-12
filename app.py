from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

# مسار قاعدة البيانات
DB_PATH = r'C:\Users\AHMED\Desktop\btc room\db\users.db'

def get_user_id(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users WHERE user_id = ?', (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None

@app.route('/<int:user_id>')
def index(user_id):
    user_id_value = get_user_id(user_id)
    return render_template('home.html', user_id=user_id_value)

if __name__ == '__main__':
    app.run(debug=True)