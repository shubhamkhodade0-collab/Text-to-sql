from dotenv import load_dotenv
import os

load_dotenv()
from flask import Flask, render_template, request, jsonify
from groq import Groq

app = Flask(__name__)

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are an expert PostgreSQL query generator.
Your job is to convert plain English text into valid PostgreSQL SQL queries.
Rules:
- Return ONLY the SQL query, nothing else
- No explanations, no markdown, no backticks
- Make the query clean and properly formatted
- Use PostgreSQL syntax strictly"""

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/convert", methods=["POST"])
def convert():
    data = request.get_json()
    user_text = data.get("text", "").strip()

    if not user_text:
        return jsonify({"error": "Please enter some text"}), 400

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_text}
            ]
        )
        sql = response.choices[0].message.content.strip()
        return jsonify({"sql": sql})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)