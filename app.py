from flask import Flask, request, jsonify, render_template
import sqlite3
import wikipedia
import os

app = Flask(__name__)

# init database
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

# homepage
@app.route("/")
def home():
    return render_template("index.html")

# AI answer system
@app.route("/api/ai", methods=["POST"])
def ai():
    question = request.json.get("message").lower()

    conn = sqlite3.connect("memory.db")
    c = conn.cursor()

    # check local memory
    c.execute("SELECT answer FROM memory WHERE question=?", (question,))
    result = c.fetchone()

    if result:
        conn.close()
        return jsonify({"answer": result[0], "source": "memory"})

    # search wikipedia
    try:
        wikipedia.set_lang("en")
        answer = wikipedia.summary(question, sentences=2)

        # save to memory
        c.execute("INSERT OR REPLACE INTO memory VALUES (?,?)", (question, answer))
        conn.commit()
        conn.close()

        return jsonify({
            "answer": answer,
            "source": "wikipedia"
        })

    except:
        conn.close()
        return jsonify({
            "answer": "Sorry vai, I couldn't find answer.",
            "source": "none"
        })

# run
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
