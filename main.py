from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

SECRET_KEY = "6LcavvArAAAAAAOWDD_1TaBUwCfnNH3sDSR1L5cV"
# เก็บ ID ที่ผ่าน Captcha แล้วไว้ที่นี่
authorized_users = {}

@app.route('/api/activate', methods=['POST'])
def activate():
    data = request.json
    uid = str(data.get('userid'))
    token = data.get('token')
    
    verify = requests.post("https://www.google.com/recaptcha/api/siteverify", data={
        'secret': SECRET_KEY, 'response': token
    }).json()

    if verify.get('success'):
        # ลงทะเบียน ID นี้ให้ใช้งานได้ 1 ชั่วโมง (หรือจนกว่า Server จะรีสตาร์ท)
        authorized_users[uid] = True
        return jsonify({"status": "activated"})
    return jsonify({"error": "Captcha Fail"}), 400

@app.route('/api/check/<uid>')
def check(uid):
    if str(uid) in authorized_users:
        return jsonify({"access": True})
    return jsonify({"access": False}), 401

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
