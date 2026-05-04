import google.generativeai as genai
from flask import Flask, render_template_string, request, redirect, url_for
import markdown2

genai.configure(api_key="AIzaSyDeJ3UxPCRYAcnDje4XlTaSaU_ZGjgkBbE")

app = Flask(__name__)

html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>NexBot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background: #121212;
            margin: 0;
            padding: 0;
            color: white;
        }
        .chat-container {
            width: 60%;
            margin: 40px auto;
            background: #1E1E1E;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.5);
            max-height: 80vh;
            overflow-y: auto;
        }
        h2 {
            text-align: center;
            color: #00BFFF;
        }
        .msg {
            margin: 12px 0;
            display: flex;
            flex-direction: column;
        }
        .user {
            margin-left: auto;
            background: #007BFF;
            padding: 10px 15px;
            border-radius: 15px 15px 0 15px;
            max-width: 70%;
            word-wrap: break-word;
        }
        .bot {
            margin-right: auto;
            background: #28A745;
            padding: 10px 15px;
            border-radius: 15px 15px 15px 0;
            max-width: 70%;
            word-wrap: break-word;
        }
        .typing {
            color: #aaa;
            font-style: italic;
            text-align: left;
            margin: 5px 0;
        }
        form {
            display: flex;
            justify-content: center;
            margin-top: 15px;
        }
        input[type=text] {
            flex: 1;
            padding: 12px;
            border-radius: 10px;
            border: none;
            margin-right: 10px;
        }
        input[type=submit], button {
            padding: 12px 20px;
            border-radius: 10px;
            border: none;
            background-color: #00BFFF;
            color: white;
            cursor: pointer;
            font-weight: bold;
            margin-left: 5px;
        }
        input[type=submit]:hover, button:hover {
            background-color: #009ACD;
        }
    </style>
</head>
<body>
    <div class="chat-container">
        <h2>💬 Chat with NexBot</h2>
        {% for u, b in chat %}
            <div class="msg"><div class="user">You: {{u}}</div></div>
            <div class="msg"><div class="bot">🤖 {{b | safe}}</div></div>
        {% endfor %}

        {% if typing %}
            <div class="typing">🤖 NexBot is typing...</div>
        {% endif %}

        <form method="post">
            <input type="text" name="question" placeholder="Type your message..." required autofocus>
            <input type="submit" value="Send">
        </form>

        <form method="post" action="{{ url_for('clear_chat') }}">
            <button type="submit">🗑️ Clear Chat</button>
        </form>
    </div>
</body>
</html>
"""

chat_history = []
typing_flag = False

@app.route("/", methods=["GET", "POST"])
def home():
    global chat_history, typing_flag

    if request.method == "POST":
        user_input = request.form["question"]
        typing_flag = True

        
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(user_input)

        try:
            bot_reply = response.text
        except:
            bot_reply = response.candidates[0].content.parts[0].text

        
        bot_reply_html = markdown2.markdown(bot_reply)

        chat_history.append((user_input, bot_reply_html))
        typing_flag = False

    return render_template_string(html_template, chat=chat_history, typing=typing_flag)

@app.route("/clear", methods=["POST"])
def clear_chat():
    global chat_history
    chat_history = []
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
