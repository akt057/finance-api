from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

DB_PATH = "transactions.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/transactions/<int:user_id>")
def get_transactions(user_id):
    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, title, amount, currency, date
        FROM transactions
        WHERE user_id = ?
        ORDER BY date DESC
    """, (user_id,))

    rows = cursor.fetchall()

    if not rows:
        return jsonify({
            "total": 0,
            "categories": []
        })

    categories = {}
    total_sum = 0

    for row in rows:
        cat = row["category"]
        item = {
            "title": row["title"],
            "amount": row["amount"],
            "currency": row["currency"],
            "date": row["date"]
        }

        total_sum += row["amount"]

        if cat not in categories:
            categories[cat] = []

        categories[cat].append(item)

    # 🔥 ВАЖНО: возвращаем categories как МАССИВ
    categories_array = [
        {
            "name": cat,
            "total": sum(item["amount"] for item in items),
            "items": items
        }
        for cat, items in categories.items()
    ]

    return jsonify({
        "total": total_sum,
        "categories": categories_array
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
