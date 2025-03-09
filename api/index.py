from flask import Flask, request, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from pyngrok import ngrok
import os

# Access the environment variable 'MY_SECRET'
AUTH_TOKEN = os.environ.get("AUTH_TOKEN" , "default_secret")
print("My secret is:", AUTH_TOKEN)

app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/message', methods=['POST'])
def receive_message():
    data = request.get_json()
    print("Received message:", data)
    socketio.emit('new_message', data)
    return jsonify({"status": "success", "message": "Message received and broadcasted"}), 200

if __name__ == '__main__':
    # Set your ngrok auth token if needed:
    ngrok.set_auth_token(AUTH_TOKEN)
    public_url = ngrok.connect(5000)
    print("ngrok public URL:", public_url)
    socketio.run(app, host='0.0.0.0', port=5000)
