from flask import Flask, request, jsonify
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Database Initialization
def init_db():
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS symptom_tracking (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id TEXT,
                        mood INTEGER,
                        stress INTEGER,
                        sleep INTEGER,
                        energy INTEGER,
                        date TEXT
                    )''')
    conn.commit()
    conn.close()

@app.route("/log_symptoms", methods=["POST"])
def log_symptoms():
    data = request.json
    user_id = data.get("user_id")
    mood = data.get("mood")
    stress = data.get("stress")
    sleep = data.get("sleep")
    energy = data.get("energy")
    date = datetime.now().strftime("%Y-%m-%d")

    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO symptom_tracking (user_id, mood, stress, sleep, energy, date) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, mood, stress, sleep, energy, date))
    conn.commit()
    conn.close()

    return jsonify({"message": "Symptoms logged successfully"}), 200

@app.route("/get_symptoms/<user_id>", methods=["GET"])
def get_symptoms(user_id):
    conn = sqlite3.connect("mental_health.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM symptom_tracking WHERE user_id = ?", (user_id,))
    data = cursor.fetchall()
    conn.close()

    return jsonify({"data": data}), 200

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
