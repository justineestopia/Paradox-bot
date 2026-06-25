from flask import Flask, render_template, request, redirect, url_for, jsonify
import database as db
import time

app = Flask(__name__)

@app.route('/')
def index():
    users = db.get_all_users()
    return render_template('index.html', users=users)

@app.route('/generate', methods=['GET', 'POST'])
def generate():
    if request.method == 'POST':
        days = int(request.form.get('days', 30))
        key = db.generate_key()
        db.create_user(f'key_{key}', key, days)
        return redirect(url_for('index'))
    return render_template('generate.html')

@app.route('/ban/<discord_id>')
def ban(discord_id):
    db.ban_user(discord_id)
    return redirect(url_for('index'))

@app.route('/unban/<discord_id>')
def unban(discord_id):
    db.unban_user(discord_id)
    return redirect(url_for('index'))

@app.route('/delete/<discord_id>')
def delete(discord_id):
    db.delete_user(discord_id)
    return redirect(url_for('index'))

@app.route('/validate', methods=['POST'])
def validate():
    data = request.get_json()
    key = data.get('key')
    hwid = data.get('hwid')
    if not key:
        return jsonify({'valid': False})
    user = db.get_user_by_key(key)
    if not user:
        return jsonify({'valid': False})
    discord_id, db_key, db_hwid, expires, _, _, banned, _ = user
    if banned or expires < int(time.time()):
        return jsonify({'valid': False})
    if not db_hwid:
        db.update_hwid(discord_id, hwid)
        db.add_execution(discord_id)
        return jsonify({'valid': True})
    if db_hwid != hwid:
        return jsonify({'valid': False})
    db.add_execution(discord_id)
    return jsonify({'valid': True})

@app.route('/paradox.lua')
def serve_loader():
    with open('loader.lua', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}

@app.route('/paradox_core.lua')
def serve_core():
    with open('paradox_obfuscated.lua', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/plain'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
