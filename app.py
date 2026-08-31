import subprocess
import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# Rutas del modelo compilado por setup.sh
MODEL_PATH = os.path.expanduser("~/models/llama-3.2-1b.gguf")
BINARY_PATH = os.path.abspath("./llama.cpp/build/bin/llama-cli")

# Personalidad de la IA
SYSTEM_PROMPT = "Tu nombre es Ankuna69. Eres un sistema de inteligencia artificial avanzado, directo, conciso y muy capaz que se ejecuta localmente en Termux."

# Interfaz HTML/CSS/JS integrada
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ankuna69 AI</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; display: flex; flex-direction: column; height: 100vh; }
        header { background-color: #161b22; border-bottom: 1px solid #30363d; padding: 15px; text-align: center; }
        header h1 { color: #58a6ff; font-size: 1.2rem; }
        header span { font-size: 0.8rem; color: #7d8590; }
        #chat { flex: 1; overflow-y: auto; padding: 15px; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 85%; padding: 10px 14px; border-radius: 12px; font-size: 0.95rem; line-height: 1.4; }
        .user { background-color: #1f6feb; color: #ffffff; align-self: flex-end; border-bottom-right-radius: 2px; }
        .bot { background-color: #21262d; color: #c9d1d9; align-self: flex-start; border-bottom-left-radius: 2px; border: 1px solid #30363d; }
        .input-area { background-color: #161b22; padding: 10px; border-top: 1px solid #30363d; display: flex; gap: 8px; }
        input { flex: 1; background-color: #0d1117; border: 1px solid #30363d; color: #c9d1d9; padding: 12px; border-radius: 6px; font-size: 0.95rem; outline: none; }
        input:focus { border-color: #58a6ff; }
        button { background-color: #238636; color: white; border: none; padding: 0 18px; border-radius: 6px; font-weight: bold; cursor: pointer; }
        button:disabled { background-color: #21262d; color: #484f58; }
    </style>
</head>
<body>
    <header>
        <h1>Ankuna69 System</h1>
        <span>Terminal Termux Local AI</span>
    </header>
    <div id="chat">
        <div class="msg bot"><strong>Ankuna69:</strong> Sistema en línea. ¿En qué trabajamos hoy?</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Escribe un mensaje..." onkeypress="handleKey(event)">
        <button id="sendBtn" onclick="sendMessage()">Enviar</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('userInput');
            const chat = document.getElementById('chat');
            const btn = document.getElementById('sendBtn');
            const text = input.value.trim();
            if (!text) return;

            chat.innerHTML += `<div class="msg user">${text}</div>`;
            input.value = '';
            input.disabled = true;
            btn.disabled = true;
            chat.scrollTop = chat.scrollHeight;

            const loadingId = 'load-' + Date.now();
            chat.innerHTML += `<div class="msg bot" id="${loadingId}"><strong>Ankuna69:</strong> Pensando...</div>`;
            chat.scrollTop = chat.scrollHeight;

            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ prompt: text })
                });
                const data = await res.json();
                document.getElementById(loadingId).innerHTML = `<strong>Ankuna69:</strong> ${data.response}`;
            } catch (err) {
                document.getElementById(loadingId).innerHTML = `<strong>Ankuna69:</strong> Error al procesar la solicitud.`;
            }

            input.disabled = false;
            btn.disabled = false;
            input.focus();
            chat.scrollTop = chat.scrollHeight;
        }

        function handleKey(e) {
            if (e.key === 'Enter') sendMessage();
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.json or {}
    user_prompt = data.get('prompt', '')

    if not user_prompt:
        return jsonify({'error': 'Prompt vacío'}), 400

    cmd = [
        BINARY_PATH,
        "-m", MODEL_PATH,
        "-p", f"{SYSTEM_PROMPT}\nUsuario: {user_prompt}\nAnkuna69:",
        "-n", "256",
        "--temp", "0.7",
        "--no-display-prompt"
    ]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        response_text = result.stdout.strip()
        return jsonify({'response': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    os.system("termux-wake-lock")
    app.run(host='0.0.0.0', port=5000, debug=False)

