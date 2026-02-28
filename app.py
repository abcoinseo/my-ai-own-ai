from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

# init db
def init_db():
    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            question TEXT PRIMARY KEY,
            answer TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

# homepage UI
@app.route("/")
def home():
    return render_template("index.html")

# ask AI
@app.route("/api/ai", methods=["POST"])
def ai():
    question = request.json.get("message").lower()

    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("SELECT answer FROM memory WHERE question=?", (question,))
    result = c.fetchone()
    conn.close()

    if result:
        return jsonify({"answer": result[0], "learned": True})
    else:
        return jsonify({
            "answer": "I don't know this yet. Please teach me below 👇",
            "learned": False
        })

# teach AI
@app.route("/api/teach", methods=["POST"])
def teach():
    question = request.json.get("question").lower()
    answer = request.json.get("answer")

    conn = sqlite3.connect("memory.db")
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO memory VALUES (?,?)", (question, answer))
    conn.commit()
    conn.close()

    return jsonify({"status": "Learned successfully ✅"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
