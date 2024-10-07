from flask import Flask, request, render_template_string, jsonify
import requests
import os

app = Flask(__name__)

API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent"
API_KEY = "AIzaSyDsHdypE4NfaK7Ixo5LcbNChpzetOl85KY"  # Replace with your actual API key

def generate_response(user_input):
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input
                    }
                ]
            }
        ]
    }
    response = requests.post(f"{API_URL}?key={API_KEY}", headers=headers, json=data)
    return response.json()

# HTML template with Bootstrap 5 for professional look
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <title>Chatie ai </title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0-alpha1/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body {
            background-color: #f0f2f5;
        }
        #chatbox {
            max-width: 900px;
            margin: 50px auto;
            background-color: #fff;
            border-radius: 12px;
            padding: 30px;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.1);
        }
        .message {
            margin-bottom: 20px;
            display: flex;
            justify-content: flex-start;
        }
        .message.user {
            justify-content: flex-end;
        }
        .message p {
            max-width: 75%;
            padding: 15px;
            border-radius: 10px;
        }
        .message.user p {
            background-color: #007bff;
            color: white;
        }
        .message.ai p {
            background-color: #f1f3f5;
            color: #333;
        }
        #inputBox {
            border-radius: 12px;
            border: 1px solid #ced4da;
        }
        #sendButton {
            background-color: transparent;
            border: none;
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div id="chatbox" class="container">
        <h1 class="text-center text-primary mb-4">Chatie ai by @dev_nathani16</h1>
        <div id="messages" class="mb-4">
            <div class="message ai">
                <p>Welcome! Ask me anything.</p>
            </div>
        </div>
        <div class="input-group mb-3">
            <input type="text" id="inputBox" class="form-control" placeholder="Type a message..." aria-label="User message" onkeydown="if(event.key === 'Enter'){sendMessage()}" oninput="toggleSendButton()">
            <button id="sendButton" class="btn" onclick="sendMessage()">
                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                    <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                </svg>
            </button>
        </div>
    </div>

    <script>
        function sendMessage() {
            var inputBox = document.getElementById("inputBox");
            var message = inputBox.value;
            if (message.trim() === "") return;

            var userMessage = document.createElement("div");
            userMessage.className = "message user";
            userMessage.innerHTML = "<p>" + message + "</p>";
            document.getElementById("messages").appendChild(userMessage);

            fetch("/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ message: message })
            })
            .then(response => response.json())
            .then(data => {
                var aiMessage = document.createElement("div");
                aiMessage.className = "message ai";
                aiMessage.innerHTML = "<p>" + data.response + "</p>";
                document.getElementById("messages").appendChild(aiMessage);
            });

            inputBox.value = "";
            inputBox.focus();
            toggleSendButton(); // Update button icon after sending a message
        }

        function toggleSendButton() {
            var inputBox = document.getElementById("inputBox");
            var sendButton = document.getElementById("sendButton");
            sendButton.innerHTML = inputBox.value.trim() === ""
                ? `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send" viewBox="0 0 16 16">
                     <path d="M15.854.146a.5.5 0 0 1 .11.54l-5.819 14.547a.75.75 0 0 1-1.329.124l-3.178-4.995L.643 7.184a.75.75 0 0 1 .124-1.33L15.314.037a.5.5 0 0 1 .54.11ZM6.636 10.07l2.761 4.338L14.13 2.576zm6.787-8.201L1.591 6.602l4.339 2.76z"/>
                   </svg>`
                : `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-send-fill" viewBox="0 0 16 16">
                     <path d="M15.964.686a.5.5 0 0 0-.65-.65L.767 5.855H.766l-.452.18a.5.5 0 0 0-.082.887l.41.26.001.002 4.995 3.178 3.178 4.995.002.002.26.41a.5.5 0 0 0 .886-.083zm-1.833 1.89L6.637 10.07l-.215-.338a.5.5 0 0 0-.154-.154l-.338-.215 7.494-7.494 1.178-.471z"/>
                   </svg>`;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    response_data = generate_response(user_message)
    ai_message = response_data['candidates'][0]['content']['parts'][0]['text']
    return jsonify({"response": ai_message})

if __name__ == '__main__':
    app.run(port=5000, debug=True)
