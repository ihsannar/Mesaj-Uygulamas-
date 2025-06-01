from flask import Flask, render_template, request, session, redirect, url_for
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
socketio = SocketIO(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        if not username.strip():
            return render_template('index.html', error="Kullanıcı adı zorunlu.")
        session['username'] = username
        return redirect(url_for('chat'))
    return render_template('index.html')

@app.route('/chat')
def chat():
    if 'username' not in session:
        return redirect(url_for('index'))
    return render_template('chat.html', username=session['username'])

@socketio.on('send_message')
def handle_send_message(data):
    # DİKKAT: Kullanıcı adını client'tan alıyoruz!
    username = data.get('username', 'Anonim')
    msg = data['message']
    print(f"[DEBUG] GELEN MESAJ: {username}: {msg}")
    emit('receive_message', {'username': username, 'message': msg}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)

