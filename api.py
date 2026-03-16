from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)
DB_NAME = "finance.db"

@app.route("/api/transactions/<int:user_id>")
def get_transactions(user_id):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
        SELECT title, amount, currency, category, created_at
        FROM transactions
        WHERE user_id = ?
        ORDER BY created_at DESC
    """, (user_id,))
    rows = cur.fetchall()
    conn.close()

    categories = {}
    total = 0

    for title, amount, currency, category, created_at in rows:
        total += amount
        if category not in categories:
            categories[category] = []
        categories[category].append({
            "title": title,
            "amount": amount,
            "currency": currency,
            "date": created_at[:10]
        })

    return jsonify({
        "total": total,
        "categories": [
            {
                "name": cat,
                "total": sum(item["amount"] for item in items),
                "items": items
            }
            for cat, items in categories.items()
        ]
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
