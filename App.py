from flask import Flask, request, jsonify, render_template_string
from groq import Groq

app = Flask(__name__)

API_KEY = "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"
client = Groq(api_key=API_KEY)

HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Sunshine Realty Assistant</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: Arial, sans-serif; background: #f0f0f0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #075e54; color: white; padding: 12px 16px; display: flex; align-items: center; gap: 12px; box-shadow: 0 2px 5px rgba(0,0,0,0.3); }
        .header-avatar { background: #128c7e; border-radius: 50%; width: 45px; height: 45px; display: flex; align-items: center; justify-content: center; font-size: 22px; }
        .header-info h2 { font-size: 17px; }
        .header-info p { font-size: 12px; opacity: 0.8; }
        .hero { background: linear-gradient(rgba(0,0,0,0.45), rgba(0,0,0,0.45)), url('https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=800') center/cover; padding: 28px 20px; color: white; text-align: center; }
        .hero h3 { font-size: 20px; margin-bottom: 6px; }
        .hero p { font-size: 13px; opacity: 0.9; margin-bottom: 16px; }
        .hero-buttons { display: flex; gap: 10px; justify-content: center; }
        .hero-btn { background: rgba(255,255,255,0.15); border: 2px solid white; color: white; padding: 8px 18px; border-radius: 20px; font-size: 13px; cursor: pointer; backdrop-filter: blur(4px); }
        .hero-btn:hover { background: white; color: #075e54; }
        .chat-box { flex: 1; overflow-y: auto; padding: 12px 16px; background: #ece5dd; }
        .message { margin: 6px 0; display: flex; flex-direction: column; }
        .message.user { align-items: flex-end; }
        .message.bot { align-items: flex-start; }
        .bubble { max-width: 78%; padding: 10px 14px; border-radius: 18px; font-size: 14px; line-height: 1.6; position: relative; box-shadow: 0 1px 2px rgba(0,0,0,0.15); }
        .user .bubble { background: #dcf8c6; border-bottom-right-radius: 4px; }
        .bot .bubble { background: white; border-bottom-left-radius: 4px; }
        .time { font-size: 10px; color: #999; margin-top: 3px; padding: 0 4px; }
        .quick-replies { display: flex; gap: 8px; flex-wrap: wrap; margin: 8px 0; }
        .quick-btn { background: white; border: 1.5px solid #075e54; color: #075e54; padding: 7px 14px; border-radius: 18px; font-size: 13px; cursor: pointer; }
        .quick-btn:hover { background: #075e54; color: white; }
        .input-area { display: flex; padding: 10px 12px; background: #f0f0f0; gap: 8px; align-items: center; border-top: 1px solid #ddd; }
        .input-area input { flex: 1; padding: 11px 16px; border: none; border-radius: 24px; background: white; font-size: 14px; outline: none; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .input-area button { background: #075e54; color: white; border: none; border-radius: 50%; width: 44px; height: 44px; font-size: 18px; cursor: pointer; box-shadow: 0 2px 5px rgba(0,0,0,0.2); }
        .footer { text-align: center; font-size: 11px; color: #aaa; padding: 6px; background: #f0f0f0; }
    </style>
</head>
<body>
    <div class="header">
        <div class="header-avatar">🏠</div>
        <div class="header-info">
            <h2>Sunshine Realty</h2>
            <p>🟢 AI Assistant • Online</p>
        </div>
    </div>

    <div class="hero">
        <h3>Find Your Dream Property</h3>
        <p>Lagos • Abuja • Port Harcourt</p>
        <div class="hero-buttons">
            <button class="hero-btn" onclick="quickSend('I want to Buy')">🏡 Buy</button>
            <button class="hero-btn" onclick="quickSend('I want to Sell')">💰 Sell</button>
            <button class="hero-btn" onclick="quickSend('I want to Rent')">🔑 Rent</button>
        </div>
    </div>

    <div class="chat-box" id="chat">
        <div class="message bot">
            <div class="bubble">Hi! 👋 Welcome to Sunshine Realty. I am your virtual assistant. How can I help you today?</div>
            <div class="time">Now</div>
        </div>
    </div>

    <div class="footer">🔒 Powered by Sunshine Realty AI</div>

    <div class="input-area">
        <input type="text" id="msg" placeholder="Type a message..." />
        <button onclick="send()">➤</button>
    </div>

    <script>
        let messages = [{role:"system", content:"You are a helpful real estate assistant for Sunshine Realty Nigeria. Help users with buying, selling and renting properties in Lagos, Abuja and Port Harcourt. Collect their name and phone number politely. Be professional, friendly and concise."}];

        function getTime() {
            return new Date().toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }

        function addMessage(text, sender) {
            const chat = document.getElementById("chat");
            const div = document.createElement("div");
            div.className = "message " + sender;
            div.innerHTML = '<div class="bubble">' + text + '</div><div class="time">' + getTime() + '</div>';
            chat.appendChild(div);
            chat.scrollTop = chat.scrollHeight;
        }

        async function send() {
            const input = document.getElementById("msg");
            const text = input.value.trim();
            if (!text) return;
            addMessage(text, "user");
            input.value = "";
            messages.push({role: "user", content: text});
            addMessage("typing...", "bot");
            const res = await fetch("/chat", {
                method: "POST",
                headers: {"Content-Type": "application/json"},
                body: JSON.stringify({messages: messages})
            });
            const data = await res.json();
            const chat = document.getElementById("chat");
            chat.removeChild(chat.lastChild);
            addMessage(data.reply, "bot");
            messages.push({role: "assistant", content: data.reply});
        }

        function quickSend(text) {
            document.getElementById("msg").value = text;
            send();
        }

        document.getElementById("msg").addEventListener("keypress", function(e) {
            if (e.key === "Enter") send();
        });
    </script>
</body>
</html>
'''

@app.route("/")
def home():
    return render_template_string(HTML)

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    messages = data["messages"]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages
    )
    reply = response.choices[0].message.content
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
